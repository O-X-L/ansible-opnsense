from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.cls import GeneralModule


class General(GeneralModule):
    FIELD_ID = 'name'
    CMDS = {
        'set': 'set',
        'search': 'get'
    }
    API_KEY_PATH = 'dhcpv4.general'
    API_KEY_PATH_REQ = API_KEY_PATH
    API_MOD = 'kea'
    API_CONT = 'dhcpv4'
    API_CONT_REL = 'service'
    FIELDS_CHANGE = [
        'enabled', 'interfaces', 'dhcp_socket_type', 'fwrules', 'valid_lifetime'
    ]

    FIELDS_ALL = FIELDS_CHANGE
    FIELDS_TYPING = {
        'bool': ['enabled', 'fwrules',],
        'int': ['valid_lifetime'],
    }

    INT_VALIDATIONS = {
        'valid_lifetime': {'min': 0},
    }

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        GeneralModule.__init__(self=self, m=module, r=result, s=session)
