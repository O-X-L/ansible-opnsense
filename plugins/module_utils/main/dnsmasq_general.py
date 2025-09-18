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
        'no_ident', 'regdhcpdomain' ]
    FIELDS_ALL = FIELDS_CHANGE
    FIELDS_TRANSLATE = {
        'enabled': 'enable',
        'interfaces': 'interface',
    }
    FIELDS_TYPING = {
        'bool': ['enabled','regdhcp','regdhcpstatic','domain_needed', 'dnssec', 'no_hosts', 'dhcpfirst',
                 'strict_order', 'strictbind', 'no_private_reverse', 'log_queries', 'no_ident' ],
        'int': ['port'],
        'list': ['interfaces'],
        'str': ['regdhcpdomain']
    }

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        GeneralModule.__init__(self=self, m=module, r=result, s=session)
