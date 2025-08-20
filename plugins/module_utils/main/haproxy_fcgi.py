from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.validate import \
    is_unset
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.cls import BaseModule


class HaproxyFcgi(BaseModule):
    FIELD_ID = 'name'
    CMDS = {
        'add': 'addFcgi',
        'del': 'delFcgi',
        'set': 'setFcgi',
        'search': 'searchFcgis',
        'detail': 'getFcgi',
        'toggle': 'toggleFcgi',
    }
    API_KEY_PATH = 'fcgi'
    API_MOD = 'haproxy'
    API_CONT = 'settings'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigure'
    FIELDS_CHANGE = ['description', 'docroot', 'index']
    FIELDS_ALL = ['name']
    FIELDS_ALL.extend(FIELDS_CHANGE)
    FIELDS_TRANSLATE = {
        'name': 'name',
        'description': 'description',
        'docroot': 'docroot',
        'index': 'index'
    }
    FIELDS_TYPING = {}
    EXIST_ATTR = 'fcgi'
    TIMEOUT = 60.0

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session)
        self.fcgi = {}

    def check(self) -> None:
        if self.p['state'] == 'present':
            if is_unset(self.p['name']):
                self.m.fail_json('You need to provide a name to create an FCGI app!')

        self._base_check()
