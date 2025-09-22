from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.cls import BaseModule


class HaproxyGroup(BaseModule):
    CMDS = {
        'add': 'addGroup',
        'del': 'delGroup',
        'set': 'setGroup',
        'search': 'get',
        'toggle': 'toggleGroup',
    }
    API_KEY_PATH = 'haproxy.groups.group'
    API_KEY_PATH_REQ = 'group'
    API_MOD = 'haproxy'
    API_CONT = 'settings'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigure'

    FIELDS_TRANSLATE = {
        'enabled': 'enabled',
        'name': 'name',
        'description': 'description',
        'members': 'members',
        'add_userlist': 'add_userlist'
    }

    FIELDS_CHANGE = list(FIELDS_TRANSLATE.keys())
    FIELDS_ALL = FIELDS_CHANGE

    FIELDS_TYPING = {
        'bool': ['enabled', 'add_userlist'],
        'str': ['name', 'description'],
        'list': ['members']
    }
    FIELD_ID = 'name'
    EXIST_ATTR = 'group'
    TIMEOUT = 60.0

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session)
        self.group = {}