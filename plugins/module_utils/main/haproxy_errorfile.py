from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.cls import BaseModule


class HaproxyErrorfile(BaseModule):
    CMDS = {
        'add': 'addErrorfile',
        'del': 'delErrorfile',
        'set': 'setErrorfile',
        'search': 'get',
        'toggle': 'toggleErrorfile',
    }
    API_KEY_PATH = 'haproxy.errorfiles.errorfile'
    API_KEY_PATH_REQ = 'errorfile'
    API_MOD = 'haproxy'
    API_CONT = 'settings'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigure'

    FIELDS_TRANSLATE = {
        'name': 'name',
        'description': 'description',
        'code': 'code',
        'content': 'content'
    }

    FIELDS_CHANGE = list(FIELDS_TRANSLATE.keys())
    FIELDS_ALL = FIELDS_CHANGE

    FIELDS_TYPING = {
        'str': ['name', 'description', 'code', 'content']
    }
    FIELD_ID = 'name'
    EXIST_ATTR = 'errorfile'
    TIMEOUT = 60.0

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session)
        self.errorfile = {}