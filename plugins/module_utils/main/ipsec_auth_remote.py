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

    FIELDS_AUTH_REMOTE = ['ca_certificates', 'eap_radius_groups']

    FIELDS_CHANGE = list(BaseAuth.FIELDS_CHANGE)
    FIELDS_CHANGE.extend(FIELDS_AUTH_REMOTE)
    FIELDS_ALL = list(BaseAuth.FIELDS_ALL)
    FIELDS_ALL.extend(FIELDS_AUTH_REMOTE)
    FIELDS_TRANSLATE = dict(BaseAuth.FIELDS_TRANSLATE)
    FIELDS_TRANSLATE['ca_certificates'] = 'cacerts'
    FIELDS_TRANSLATE['eap_radius_groups'] = 'groups'
    FIELDS_TYPING = {}
    for _k, _v in BaseAuth.FIELDS_TYPING.items():
        if isinstance(_v, list):
            FIELDS_TYPING[_k] = list(_v)
        else:
            FIELDS_TYPING[_k] = _v
    FIELDS_TYPING['list'].extend(FIELDS_AUTH_REMOTE)

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None, fail: dict = None):
        BaseAuth.__init__(self=self, m=module, r=result, s=session, f=fail)
        self.auth = {}
