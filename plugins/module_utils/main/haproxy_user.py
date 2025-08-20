from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.validate import \
    is_unset
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.cls import BaseModule


class HaproxyUser(BaseModule):
    FIELD_ID = 'name'
    CMDS = {
        'add': 'addUser',
        'del': 'delUser',
        'set': 'setUser',
        'search': 'searchUsers',
        'detail': 'getUser',
        'toggle': 'toggleUser',
    }
    API_KEY_PATH = 'user'
    API_MOD = 'haproxy'
    API_CONT = 'settings'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigure'
    FIELDS_CHANGE = ['enabled', 'description', 'password']
    FIELDS_ALL = ['name']
    FIELDS_ALL.extend(FIELDS_CHANGE)
    FIELDS_TRANSLATE = {
        'enabled': 'enabled',
        'description': 'description', 
        'name': 'name',
        'password': 'password'
    }
    FIELDS_TYPING = {
        'bool': ['enabled']
    }
    EXIST_ATTR = 'user'
    TIMEOUT = 60.0

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session)
        self.user = {}
        self.diff = {}

    def check(self) -> None:
        if self.p['state'] == 'present':
            if is_unset(self.p['name']):
                self.m.fail_json('You need to provide a name to create a user!')

            if is_unset(self.p['password']):
                self.m.fail_json('You need to provide a password to create a user!')

        self._base_check()