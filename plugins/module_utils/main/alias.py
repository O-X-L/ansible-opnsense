from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.handler import \
    ModuleSoftError
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.alias import \
    validate_values, filter_builtin_alias
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import \
    get_simple_existing, simplify_translate, is_unset
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.cls import BaseModule


class Alias(BaseModule):
    FIELD_ID = 'name'
    CMDS = {
        'add': 'add_item',
        'del': 'del_item',
        'set': 'set_item',
        'search': 'get',
        'toggle': 'toggleItem',
    }
    API_KEY_PATH = 'alias.aliases.alias'
    API_MOD = 'firewall'
    API_CONT = 'alias'
    FIELDS_CHANGE = ['content', 'description']
    FIELDS_ALL = ['name', 'type', 'enabled']
    FIELDS_ALL.extend(FIELDS_CHANGE)
    FIELDS_ALL.extend(['updatefreq_days', 'interface', 'path_expression'])
    FIELDS_TRANSLATE = {
        'updatefreq_days': 'updatefreq',
    }
    FIELDS_TYPING = {
        'bool': ['enabled'],
        'select': ['type', 'interface'],
    }
    EXIST_ATTR = 'alias'
    JOIN_CHAR = '\n'
    TIMEOUT = 20.0
    MAX_ALIAS_LEN = 32

    DEFAULT_UPDATEFREQ_DAYS_URLTABLE = 7.0  # see: https://github.com/O-X-L/ansible-opnsense/pull/270

    def __init__(
            self, module: AnsibleModule, result: dict, cnf: dict = None,
            session: Session = None, fail: dict = None,
    ):
        BaseModule.__init__(self=self, m=module, r=result, s=session, f=fail)
        self.alias = {}
        self.p = self.m.params if cnf is None else cnf  # to allow override by alias_multi

    def check(self) -> None:
        if self.p['type'] == 'urltable':
            self.FIELDS_CHANGE = self.FIELDS_CHANGE + ['updatefreq_days']
            if not is_unset(self.p['updatefreq_days']):
                self.p['updatefreq_days'] = float(self.p['updatefreq_days'])

            else:
                self.p['updatefreq_days'] = self.DEFAULT_UPDATEFREQ_DAYS_URLTABLE

        if self.p['type'] == 'urljson':
            self.FIELDS_CHANGE = self.FIELDS_CHANGE + ['updatefreq_days', 'path_expression']
            if not is_unset(self.p['updatefreq_days']):
                self.p['updatefreq_days'] = float(self.p['updatefreq_days'])

        if self.p['type'] == 'dynipv6host':
            if is_unset(self.p['interface']):
                self.m.fail_json('You need to provide an interface to create a dynipv6host alias!')

            self.FIELDS_CHANGE = self.FIELDS_CHANGE + ['interface']

        if len(self.p['name']) > self.MAX_ALIAS_LEN:
            self._error(
                f"Alias name '{self.p['name']}' is invalid - "
                f"must be shorter than {self.MAX_ALIAS_LEN} characters",
            )

        self.b.find(match_fields=[self.FIELD_ID])

        if self.p['state'] == 'present':
            validate_values(error_func=self._error, cnf=self.p, existing_entries=self.existing_entries)

        self._base_check()

    def simplify_existing(self, alias: dict) -> dict:
        simple = {}

        if isinstance(alias['content'], dict):
            simple['content'] = [item for item in alias['content'].keys() if item != '']

        else:
            # if function is re-applied
            return alias

        simple = {
            **simplify_translate(
                existing=alias,
                typing=self.FIELDS_TYPING,
                translate=self.FIELDS_TRANSLATE,
            ),
            **simple,
        }

        if simple['type'] in ['urltable', 'urljson']:
            try:
                simple['updatefreq_days'] = round(float(alias['updatefreq']), 1)

            except ValueError:
                simple['updatefreq_days'] = float(0)

        return simple

    def update(self) -> None:
        # checking if alias changed
        if self.alias['type'] == self.p['type']:
            self.b.update()

        else:
            self.r['changed'] = True
            self._error(
                msg=f"Unable to update alias '{self.p[self.FIELD_ID]}' - it is not of the same type! "
                    f"You need to delete the current one first!",
                verification=False,
            )

    def delete(self) -> None:
        response = self.b.delete()

        if 'in_use' in response:
            self._error(
                msg=f"Unable to delete alias '{self.p[self.FIELD_ID]}' as it is currently referenced!",
                verification=False,
            )

    def _error(self, msg: str, verification: bool = True) -> None:
        if (verification and self.fail_verify) or (not verification and self.fail_process):
            self.m.fail_json(msg)

        else:
            self.m.warn(msg)
            raise ModuleSoftError

    def get_existing(self) -> list:
        return filter_builtin_alias(
            get_simple_existing(
                entries=self.b.search(),
                simplify_func=self.simplify_existing,
            )
        )
