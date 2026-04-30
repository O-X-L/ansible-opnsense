from ansible.module_utils.basic import AnsibleModule

from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.api import Session
from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.cls import BaseModule


class Tunable(BaseModule):
    CMDS = {
        'add': 'add_item',
        'del': 'del_item',
        'set': 'set_item',
        'search': 'search_item',
        'detail': 'get_item',
    }
    API_KEY = 'sysctl'
    API_KEY_PATH = 'sysctl'
    API_MOD = 'core'
    API_CONT = 'tunables'
    API_CONT_REL = 'tunables'
    FIELDS_CHANGE = [
        'tunable', 'description', 'value', 'default_value', 'type'
    ]
    FIELDS_ALL = FIELDS_CHANGE
    FIELDS_TRANSLATE = {
        'description': 'descr'
    }
    FIELDS_TYPING = {
        'select': ['type'],
        'int': ['value', 'default_value'],
    }
    FIELD_ID = 'tunable'
    EXIST_ATTR = 'sysctl'

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None, fail: dict = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session, f=fail)
        self.existing = {}
