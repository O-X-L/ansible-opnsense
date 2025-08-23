from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import \
    is_unset, get_key_by_value_from_selection
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.cls import BaseModule


class Group(BaseModule):
    FIELD_ID = 'name'
    CMDS = {
        'add': 'add',
        'del': 'del',
        'set': 'set',
        'search': 'search',
        'detail': 'get',
    }
    API_KEY_PATH = 'group'
    API_MOD = 'auth'
    API_CONT = 'group'
    FIELDS_CHANGE = ['description', 'source_net']
    FIELDS_TYPING = {
        'list': ['privilege', 'member', 'source_net'],
    }
    FIELDS_TRANSLATE = {
        'privilege': 'priv',
        'source_net': 'source_networks',
    }
    FIELDS_ALL = ['name', 'privilege', 'member']
    FIELDS_ALL.extend(FIELDS_CHANGE)
    EXIST_ATTR = 'group'
    STR_VALIDATIONS = {
        'name': r'^[a-zA-Z0-9._-]{1,32}$'
    }

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session)
        self.group = {}

    def check(self) -> None:
        self._base_check()

        if not is_unset(self.p['member']) or self.p['member'] == []:
            self.FIELDS_CHANGE = self.FIELDS_CHANGE + ['member']
            self.p['member'] = [
                get_key_by_value_from_selection(self.b.raw['member'], m)
                for m in self.p['member']
            ]
        if not is_unset(self.p['privilege']) or self.p['privilege'] == []:
            self.FIELDS_CHANGE = self.FIELDS_CHANGE + ['privilege']

    def delete(self) -> None:
        if self.group['scope'] == 'system':
            self.m.fail_json(f"Not allowed to delete system group {self.group['name']}")
        self.b.delete()
