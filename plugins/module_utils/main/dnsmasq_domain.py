from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.cls import BaseModule


class Domain(BaseModule):
    FIELD_ID = 'domain'
    CMDS = {
        'add': 'add_domain',
        'del': 'del_domain',
        'set': 'set_domain',
        'search': 'get',
    }
    API_KEY_PATH = 'dnsmasq.domainoverrides'
    API_KEY_PATH_REQ = 'domainoverride'
    API_MOD = 'dnsmasq'
    API_CONT = 'settings'
    FIELDS_CHANGE = ['sequence', 'ipset', 'src_ip', 'port', 'ip', 'description']
    FIELDS_TRANSLATE = {
        'description': 'descr',
        'src_ip': 'srcip',
    }
    FIELDS_TYPING = {
        'select': ['ipset'],
        'int': ['sequence', 'port'],
    }
    FIELDS_ALL = [FIELD_ID]
    FIELDS_ALL.extend(FIELDS_CHANGE)
    EXIST_ATTR = 'domain'
    INT_VALIDATIONS = {
        'sequence': {'min': 1, 'max': 99999},
    }

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session)
        self.domain = {}
