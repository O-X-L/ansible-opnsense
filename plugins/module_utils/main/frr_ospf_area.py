from ansible.module_utils.basic import AnsibleModule

from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.oxlorg.opnsense.plugins.module_utils.helper.main import is_unset
from ansible_collections.oxlorg.opnsense.plugins.module_utils.helper.validate import is_ip4
from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.module import BaseModule


class Area(BaseModule):
    FIELD_ID = 'area'
    CMDS = {
        'add': 'addArea',
        'del': 'delArea',
        'set': 'setArea',
        'search': 'get',
        'toggle': 'toggleArea',
    }
    API_KEY_PATH = 'ospf.areas.area'
    API_MOD = 'quagga'
    API_CONT = 'ospfsettings'
    API_CONT_REL = 'service'
    FIELDS_CHANGE = ['type', 'ranges', 'prefix_list_in', 'prefix_list_out']
    FIELDS_ALL = [FIELD_ID, 'enabled']
    FIELDS_ALL.extend(FIELDS_CHANGE)
    FIELDS_TRANSLATE = {
        'area': 'id',
        'prefix_list_in': 'linkedPrefixlistIn',
        'prefix_list_out': 'linkedPrefixlistOut',
    }
    FIELDS_TYPING = {
        'bool': ['enabled'],
        'list': ['ranges'],
        'select': ['type', 'prefix_list_in', 'prefix_list_out'],
    }
    FIELDS_VALUE_MAPPING = {
        'type': {'normal': ''},
    }
    EXIST_ATTR = 'area'
    SEARCH_ADDITIONAL = {
        'existing_prefixes': 'ospf.prefixlists.prefixlist',
    }
    LINK_FIELDS = ['prefix_list_in', 'prefix_list_out']

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None, fail: dict = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session, f=fail)
        self.area = {}
        self.existing_prefixes = None

    def check(self) -> None:
        if not is_ip4(self.p['area']):
            self.m.fail_json(
                f"The provided area '{self.p['area']}' is invalid! "
                'It must be in dotted format like 0.0.0.1'
            )

        self._base_check()

        if self.p['state'] == 'present':
            for field in self.LINK_FIELDS:
                self._find_prefix_list(field)

        for state in ['before', 'after']:
            diff = self.r['diff'].get(state, {})
            for field in self.LINK_FIELDS:
                if field in diff:
                    diff[field] = self._prefix_list_name(diff[field])

    def _prefixes(self) -> dict:
        if isinstance(self.existing_prefixes, dict):
            return self.existing_prefixes

        return {}

    def _prefix_list_name(self, uuid: str) -> str:
        if uuid in self._prefixes():
            return self._prefixes()[uuid]['name']

        return uuid

    def _find_prefix_list(self, field: str) -> None:
        # since os-frr 2.0 (OPNsense 26.7) prefix-lists are linked as groups of all entries sharing a name
        #   the API shows one entry-uuid per group, so we keep the linked one if it is part of the group
        if is_unset(self.p[field]):
            self.p[field] = ''
            return

        uuids = [uuid for uuid, entry in self._prefixes().items() if entry['name'] == self.p[field]]
        if len(uuids) == 0:
            self.m.fail_json(f"Provided {field} '{self.p[field]}' was not found!")

        current = self.area.get(field) if self.exists else None
        self.p[field] = current if current in uuids else uuids[0]

    def get_existing(self) -> list:
        existing = []

        for entry in self._base_get_existing():
            for field in self.LINK_FIELDS:
                entry[field] = self._prefix_list_name(entry[field])

            existing.append(entry)

        return existing
