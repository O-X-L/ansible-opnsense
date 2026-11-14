from ansible.module_utils.basic import AnsibleModule

from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.module import BaseModule


class Tunable(BaseModule):
    FIELD_ID = 'tunable'
    CMDS = {
        'add': 'add_item',
        'del': 'del_item',
        'set': 'set_item',
        'search': 'search_item',
        'detail': 'get_item',
    }
    API_KEY_PATH = 'sysctl'
    API_MOD = 'core'
    API_CONT = 'tunables'
    FIELDS_CHANGE = ['value', 'description']
    FIELDS_ALL = [FIELD_ID]
    FIELDS_ALL.extend(FIELDS_CHANGE)
    FIELDS_TRANSLATE = {
        'description': 'descr',
    }
    FIELDS_TYPING = {}
    EXIST_ATTR = 'entry'

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None, fail: dict = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session, f=fail)
        self.entry = {}

    def check(self) -> None:
        if self.p['state'] == 'present' and self.p['value'] is None:
            self.m.fail_json("You need to provide a 'value' to set a tunable!")

        self._base_check()

        if not self.exists:
            return

        # OPNsense lists the tunables it knows by default with an md5 key in place of a UUID;
        # they are not in the config until they are set, so there is nothing to delete
        if self.p['state'] == 'absent' and not self._is_configured():
            self.exists = False
            return

        # the API fills an empty description with the one from the system
        if self.p['description'] is None:
            self.p['description'] = self.entry.get('description', '')
            self.r['diff']['after'] = self.build_diff(data=self.p)

    def _is_configured(self) -> bool:
        return len(str(self.entry.get(self.field_pk, '')).split('-')) == 5

    def update(self) -> None:
        self._base_update(enable_switch=False)
