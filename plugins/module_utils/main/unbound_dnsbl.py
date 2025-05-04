from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.cls import GeneralModule


# Supported as of OPNsense 23.7
class DnsBL(GeneralModule):
    CMDS = {
        'set': 'set',
        'search': 'get',
    }
    API_KEY_PATH = 'unbound.dnsbl'
    API_KEY_PATH_REQ = API_KEY_PATH
    API_MOD = 'unbound'
    API_CONT = 'settings'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigureGeneral'
    FIELDS_CHANGE = [
        'enabled', 'safesearch', 'type', 'lists', 'whitelists', 'blocklists', 'wildcards', 'address', 'nxdomain'
    ]
    FIELDS_ALL = FIELDS_CHANGE
    FIELDS_TYPING = {
        'bool': ['enabled', 'safesearch', 'nxdomain'],
        'list': ['type', 'lists', 'whitelists', 'blocklists', 'wildcards'],
    }

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        GeneralModule.__init__(self=self, m=module, r=result, s=session)

    def check(self) -> None:
        self.settings = self._search_call()
        self._build_diff()
