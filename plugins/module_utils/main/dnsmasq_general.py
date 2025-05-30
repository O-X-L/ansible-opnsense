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
    #API_KEY_PATH_REQ = API_KEY_PATH
    API_MOD = 'dnsmasq'
    API_CONT = 'settings'
    API_CONT_REL = 'service'
    FIELDS_CHANGE = [
        'enabled', 'interfaces', 'regdhcp', 'regdhcpstatic', 'domain_needed', 'dns_port', 'dnssec',
        'no_hosts', 'dhcpfirst', 'strict_order', 'strictbind', 'no_private_reverse', 'log_queries',
        'no_ident', 'regdhcpdomain' ]
    FIELDS_ALL = FIELDS_CHANGE
    FIELDS_TRANSLATE = {
        'enabled': 'enable',
        'interfaces': 'interface',
    }
    FIELDS_TYPING = {
        'bool': ['enabled','regdhcp','regdhcpstatic','domain_needed', 'dnssec', 'no_hosts', 'dhcpfirst',
                 'strict_order', 'strictbind', 'no_private_reverse', 'log_queries', 'no_ident' ],
        'int': ['dns_port'],
        'list': ['interfaces'],
        'str': ['regdhcpdomain']
    }
#    INT_VALIDATIONS = {
#        'lifetime': {'min': 0},
#    }

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        GeneralModule.__init__(self=self, m=module, r=result, s=session)
