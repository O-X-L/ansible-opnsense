from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.cls import BaseModule
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import validate_int_fields


class General(BaseModule):
    FIELD_ID = 'name'
    CMDS = {
        'set': 'set',
        'get': 'get',
    }
    API_KEY_PATH = 'general'
    API_MOD = 'nginx'
    API_CONT = 'settings'
    FIELDS_CHANGE = [
        'enabled', 'ban_ttl',
    ]
    FIELDS_ALL = FIELDS_CHANGE
    INT_VALIDATIONS = {
        'ban_ttl': {'min': 0},
    }
    FIELDS_TYPING = {
        'bool': ['enabled'],
        'int': ['ban_ttl'],
    }

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session)

    def check(self):
        validate_int_fields(module=self.m, data=self.p, field_minmax=self.INT_VALIDATIONS)
