from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.cls import BaseModule


class Account(BaseModule):
    FIELD_ID = 'name'
    CMDS = {
        'add': 'add',
        'del': 'del',
        'set': 'update',
        'search': 'get',
        'toggle': 'toggle',
    }
    API_KEY_PATH = 'acmeclient.accounts.account'
    API_MOD = 'acmeclient'
    API_CONT = 'accounts'
    API_CONT_GET = 'settings'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigure'
    FIELDS_CHANGE = ['description', 'custom_ca', 'eab_kid', 'eab_hmac']
    FIELDS_ALL = [
        'enabled', 'name', 'email', 'ca',
    ]
    FIELDS_ALL.extend(FIELDS_CHANGE)
    FIELDS_TYPING = {
        'bool': ['enabled'],
        'list': [],
        'select': ['ca'],
        'int': [],
    }
    EXIST_ATTR = 'account'

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session)
        self.account = {}

    def check(self) -> None:
        self._base_check()

    def process(self) -> None:
        self.b.process()

        if self.p['state'] == 'present' and self.p['register']:
            self.register()

    def register(self) -> None:
        if self.account.get('statusCode', 100) == 200:
            return

        self.r['changed'] = True
        if not self.m.check_mode:
            cont_get, mod_get = self.API_CONT, self.API_MOD
            self.call_cnf['controller'] = cont_get
            self.call_cnf['module'] = mod_get
            self.s.post(cnf={
                **self.call_cnf,
                'command': 'register',
            })

    def reload(self) -> dict:
        # no reload required
        pass

    def _search_call(self) -> list:
        result = self.b.search()

        # Reset controller and module
        cont_get, mod_get = self.API_CONT, self.API_MOD
        self.call_cnf['controller'] = cont_get
        self.call_cnf['module'] = mod_get

        return result
