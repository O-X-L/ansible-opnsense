from ansible.module_utils.basic import AnsibleModule

from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.oxlorg.opnsense.plugins.module_utils.main.ipsec_auth import \
    BaseAuth


class Auth(BaseAuth):
    CMDS = {
        'add': 'addRemote',
        'del': 'delRemote',
        'set': 'setRemote',
        'search': 'get',
        'toggle': 'toggleRemote',
    }
    API_KEY_PATH = 'swanctl.remotes.remote'

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None, fail: dict = None):
        BaseAuth.__init__(self=self, m=module, r=result, s=session, f=fail)
        self.auth = {}
