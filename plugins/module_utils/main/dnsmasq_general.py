from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.cls import GeneralModule


class General(GeneralModule):
    CMDS = {
        'set': 'set',
        'search': 'get'
    }
    API_KEY_PATH = 'dnsmasq'
    API_MOD = 'dnsmasq'
    API_CONT = 'settings'
    API_CONT_REL = 'service'
    FIELDS_CHANGE = [
        'enabled', 'interfaces', 'regdhcp', 'regdhcpstatic', 'domain_needed', 'port', 'dnssec',
        'no_hosts', 'dhcpfirst', 'strict_order', 'strictbind', 'no_private_reverse', 'log_queries',
        'no_ident', 'regdhcpdomain', 'dns_forward_max', 'cache_size', 'local_ttl',
    ]
    FIELDS_ALL = FIELDS_CHANGE
    FIELDS_TRANSLATE = {
        'enabled': 'enable',
        'interfaces': 'interface',
    }
    FIELDS_TYPING = {
        'bool': ['enabled','regdhcp','regdhcpstatic','domain_needed', 'dnssec', 'no_hosts', 'dhcpfirst',
                 'strict_order', 'strictbind', 'no_private_reverse', 'log_queries', 'no_ident' ],
        'int': ['port', 'dns_forward_max', 'cache_size', 'local_ttl'],
        'list': ['interfaces'],
        'str': ['regdhcpdomain']
    }
    INT_VALIDATIONS = {
        'port': {'min': 0, 'max': 65535},
        'dns_forward_max': {'min': 0},
        'cache_size': {'min': 0},
        'local_ttl': {'min': 0},
    }

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        GeneralModule.__init__(self=self, m=module, r=result, s=session)
