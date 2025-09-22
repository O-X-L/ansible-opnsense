from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.cls import BaseModule


class Cpu(BaseModule):
    CMDS = {
        'add': 'addCpu',
        'del': 'delCpu',
        'set': 'setCpu',
        'search': 'get',
        'toggle': 'toggleCpu',
    }
    API_KEY_PATH = 'haproxy.cpus.cpu'
    API_KEY_PATH_REQ = 'cpu'
    API_MOD = 'haproxy'
    API_CONT = 'settings'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigure'

    FIELDS_TRANSLATE = {
        'enabled': 'enabled',
        'name': 'name',
        'thread_id': 'thread_id',
        'cpu_id': 'cpu_id',
    }

    FIELDS_CHANGE = list(FIELDS_TRANSLATE.keys())
    FIELDS_ALL = FIELDS_CHANGE

    FIELD_ID = 'name'
    EXIST_ATTR = 'cpu'

    FIELDS_TYPING = {
        'bool': ['enabled'],
        'str': ['thread_id'],
        'list': ['cpu_id'],
    }

    STR_VALIDATIONS = {
        'name': r'^[a-zA-Z0-9._-]{1,64}$',  # Name validation
        'thread_id': r'^(all|odd|even|x[0-9]+)$'  # Thread ID validation
    }

    TIMEOUT = 60.0

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session)
        self.cpu = {}
