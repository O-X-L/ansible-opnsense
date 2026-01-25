from ansible.module_utils.basic import AnsibleModule
from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.api import Session
from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.cls import BaseModule


class HaproxyMapfile(BaseModule):
    FIELD_ID = 'name'

    CMDS = {
        'add': 'addMapfile',
        'del': 'delMapfile',
        'set': 'setMapfile',
        'search': 'get',
        'toggle': 'toggleMapfile',
    }
    API_KEY_PATH = 'haproxy.mapfiles.mapfile'
    API_MOD = 'haproxy'
    API_CONT = 'settings'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigure'

    FIELDS_CHANGE = ['name', 'description', 'content']
    FIELDS_ALL = FIELDS_CHANGE

    EXIST_ATTR = 'haproxy_mapfile'

    FIELDS_TYPING = {}

    STR_VALIDATIONS = {
        'name': r'^[^\t^,^;^\.^\[^\]^\{^\}]{1,255}$',
        'description': r'^.{1,255}$',
    }

    TIMEOUT = 20.0

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session)
        self.haproxy_mapfile = {}