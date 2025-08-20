from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.validate import \
    is_unset
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.cls import BaseModule


class HaproxyMapfile(BaseModule):
    FIELD_ID = 'name'
    CMDS = {
        'add': 'addMapfile',
        'del': 'delMapfile',
        'set': 'setMapfile',
        'search': 'searchMapfiles',
        'detail': 'getMapfile',
        'toggle': 'toggleMapfile',
    }
    API_KEY_PATH = 'mapfile'
    API_MOD = 'haproxy'
    API_CONT = 'settings'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigure'
    FIELDS_CHANGE = ['description', 'content']
    FIELDS_ALL = ['name']
    FIELDS_ALL.extend(FIELDS_CHANGE)
    FIELDS_TRANSLATE = {
        'description': 'description', 
        'name': 'name',
        'content': 'content'
    }
    FIELDS_TYPING = {}
    EXIST_ATTR = 'mapfile'
    TIMEOUT = 60.0

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session)
        self.mapfile = {}
        self.diff = {}

    def check(self) -> None:
        if self.p['state'] == 'present':
            if is_unset(self.p['name']):
                self.m.fail_json('You need to provide a name to create a map file!')

            if is_unset(self.p['content']):
                self.m.fail_json('You need to provide content to create a map file!')

        self._base_check()