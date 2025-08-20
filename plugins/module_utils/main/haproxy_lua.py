from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.validate import \
    is_unset
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.cls import BaseModule


class HaproxyLua(BaseModule):
    FIELD_ID = 'name'
    CMDS = {
        'add': 'addLua',
        'del': 'delLua',
        'set': 'setLua',
        'search': 'searchLuas',
        'detail': 'getLua',
        'toggle': 'toggleLua',
    }
    API_KEY_PATH = 'lua'
    API_MOD = 'haproxy'
    API_CONT = 'settings'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigure'
    FIELDS_CHANGE = ['description', 'enabled', 'content', 'preload', 'filename_scheme']
    FIELDS_ALL = ['name']
    FIELDS_ALL.extend(FIELDS_CHANGE)
    FIELDS_TRANSLATE = {
        'name': 'name',
        'description': 'description',
        'enabled': 'enabled',
        'content': 'content',
        'preload': 'preload',
        'filename_scheme': 'filename_scheme'
    }
    FIELDS_TYPING = {
        'bool': ['enabled']
    }
    EXIST_ATTR = 'lua'
    TIMEOUT = 60.0

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session)
        self.lua = {}

    def check(self) -> None:
        if self.p['state'] == 'present':
            if is_unset(self.p['name']):
                self.m.fail_json('You need to provide a name to create a Lua script!')
            
            if is_unset(self.p['content']):
                self.m.fail_json('You need to provide content (Lua code) to create a Lua script!')

        self._base_check()
