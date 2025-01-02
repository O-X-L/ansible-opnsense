from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import \
    validate_int_fields, is_unset
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.cls import BaseModule


class Certificate(BaseModule):
    FIELD_ID = 'description'
    CMDS = {
        'add': 'add',
        'del': 'del',
        'set': 'update',
        'search': 'get',
        'toggle': 'toggle',
    }
    API_KEY_PATH = 'acmeclient.certificates.certificate'
    API_MOD = 'acmeclient'
    API_CONT = 'certificates'
    API_CONT_GET = 'settings'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigure'
    FIELDS_CHANGE = ['name', 'alt_names', 'account', 'validation', 'restart_actions', 'auto_renewal', 'renew_interval', 'aliasmode']
    FIELDS_ALL = [
        'enabled', 'description', 'domainalias', 'challengealias'
    ]
    FIELDS_ALL.extend(FIELDS_CHANGE)
    FIELDS_TRANSLATE = {
        'alt_names': 'altNames',
        'validation': 'validationMethod',
        'key_ength': 'keyLength',
        'restart_actions': 'restartActions',
        'auto_renewal': 'autoRenewal',
        'renew_interval': 'renewInterval',
    }
    FIELDS_TYPING = {
        'bool': ['enabled', 'auto_renewal'],
        'list': ['alt_names', 'restart_actions'],
        'select': ['account', 'validation', 'restart_actions', 'aliasmode'],
        'int': ['renew_interval'],
    }
    INT_VALIDATIONS = {
        'renew_interval': {'min': 1, 'max': 5000},
    }
    EXIST_ATTR = 'certificate'
    SEARCH_ADDITIONAL = {
        'existing_accounts': 'acmeclient.accounts.account',
        'existing_validations': 'acmeclient.validations.validation',
        'existing_actions': 'acmeclient.actions.action',
    }

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session)
        self.certificate = {}
        self.existing_accounts = {}
        self.existing_validations = {}
        self.existing_actions = {}

    def check(self) -> None:
        if self.p['state'] == 'present':
            if is_unset(self.p['name']):
                self.m.fail_json('You need to provide a name to create/update certificates!')

            validate_int_fields(module=self.m, data=self.p, field_minmax=self.INT_VALIDATIONS)

            if self.p['aliasmode'] == 'domain':
                self.FIELDS_CHANGE = self.FIELDS_CHANGE + ['domainalias']
            elif self.p['aliasmode'] == 'challenge':
                self.FIELDS_CHANGE = self.FIELDS_CHANGE + ['challengealias']

        self._base_check()

        if self.p['state'] == 'present':
            if is_unset(self.p['account']):
                self.m.fail_json(f"You need to provide an account to create/update certificates!")
            else:
                for key, values in self.existing_accounts.items():
                    if values['name'] == self.p['account']:
                        self.p['account'] = key
                        break
                else:
                    self.m.fail_json(f"Account {self.p['account']} does not exist! {self.existing_accounts}")

            if is_unset(self.p['validation']):
                self.m.fail_json(f"You need to provide the validation to create/update certificates!")
            else:
                for key, values in self.existing_validations.items():
                    if values['name'] == self.p['validation']:
                        self.p['validation'] = key
                        break
                else:
                    self.m.fail_json(f"Validation {self.p['validation']} does not exist!")

            if not is_unset(self.p['restart_actions']):
                mapping = {
                    values['name']: key
                    for key, values in self.existing_actions.items()
                }

                missing = [
                    action
                    for action in self.p['restart_actions']
                    if action not in mapping
                ]
                if any(missing):
                    self.m.fail_json(f"Actions {missing.join(',')} do not exist!")

                self.p['restart_actions'] = [
                    mapping[action]
                    for action in self.p['restart_actions']
                ]

    def create(self) -> None:
        cont_get, mod_get = self.API_CONT, self.API_MOD
        self.call_cnf['controller'] = cont_get
        self.call_cnf['module'] = mod_get
        self.b.create()

    def update(self) -> None:
        cont_get, mod_get = self.API_CONT, self.API_MOD
        self.call_cnf['controller'] = cont_get
        self.call_cnf['module'] = mod_get
        self.b.update()

    def delete(self) -> None:
        cont_get, mod_get = self.API_CONT, self.API_MOD
        self.call_cnf['controller'] = cont_get
        self.call_cnf['module'] = mod_get
        self.b.delete()
