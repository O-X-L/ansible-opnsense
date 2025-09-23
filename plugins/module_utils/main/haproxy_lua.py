from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.cls import BaseModule


class HaproxyLua(BaseModule):
    CMDS = {
        'add': 'addLua',
        'del': 'delLua',
        'set': 'setLua',
        'search': 'get',
        'toggle': 'toggleLua',
    }
    API_KEY_PATH = 'haproxy.luas.lua'
    API_KEY_PATH_REQ = 'lua'
    API_MOD = 'haproxy'
    API_CONT = 'settings'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigure'

    FIELDS_TRANSLATE = {
        'enabled': 'enabled',
        'name': 'name',
        'description': 'description',
        'preload': 'preload',
        'filename_scheme': 'filename_scheme',
        'content': 'content'
    }

    FIELDS_CHANGE = list(FIELDS_TRANSLATE.keys())
    FIELDS_ALL = FIELDS_CHANGE

    FIELDS_TYPING = {
        'bool': ['enabled', 'preload'],
        'str': ['name', 'description', 'filename_scheme', 'content']
    }
    FIELD_ID = 'name'
    EXIST_ATTR = 'lua'
    TIMEOUT = 60.0

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session)
        self.lua = {}