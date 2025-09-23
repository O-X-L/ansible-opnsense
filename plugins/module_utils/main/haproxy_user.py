from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.cls import BaseModule


class HaproxyUser(BaseModule):
    CMDS = {
        'add': 'addUser',
        'del': 'delUser',
        'set': 'setUser',
        'search': 'get',
        'toggle': 'toggleUser',
    }
    API_KEY_PATH = 'haproxy.users.user'
    API_KEY_PATH_REQ = 'user'
    API_MOD = 'haproxy'
    API_CONT = 'settings'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigure'

    FIELDS_TRANSLATE = {
        'enabled': 'enabled',
        'name': 'name',
        'description': 'description',
        'password': 'password'
    }

    FIELDS_CHANGE = list(FIELDS_TRANSLATE.keys())
    FIELDS_ALL = FIELDS_CHANGE
    
    FIELDS_DIFF_NO_LOG = ['password']

    FIELDS_TYPING = {
        'bool': ['enabled'],
        'str': ['name', 'description', 'password']
    }
    FIELD_ID = 'name'
    EXIST_ATTR = 'user'
    TIMEOUT = 60.0

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session)
        self.user = {}