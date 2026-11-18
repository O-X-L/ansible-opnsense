from ansible.module_utils.basic import AnsibleModule

from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.oxlorg.opnsense.plugins.module_utils.helper.validate import \
    is_unset
from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.module import BaseModule


class DNat(BaseModule):
    CMDS = {
        'add': 'add_rule',
        'del': 'del_rule',
        'set': 'set_rule',
        'search': 'get',
        'toggle': 'toggle_rule',
    }
    API_KEY_PATH = 'DNat.rule'
    API_MOD = 'firewall'
    API_CONT = 'd_nat'
    FIELDS_CHANGE = [
        'sequence', 'no_port_forward', 'interface', 'ip_protocol', 'protocol',
        'source_invert', 'source_net', 'source_port',
        'destination_invert', 'destination_net', 'destination_port',
        'target', 'local_port', 'pool_opts', 'log', 'description', 'tag', 'tagged',
        'nat_reflection', 'associated_rule', 'categories', 'sync',
    ]
    FIELDS_ALL = ['enabled']
    FIELDS_ALL.extend(FIELDS_CHANGE)
    FIELDS_BOOL_INVERT = ['enabled', 'sync']
    FIELDS_TRANSLATE = {
        'enabled': 'disabled',
        'no_port_forward': 'nordr',
        'ip_protocol': 'ipprotocol',
        'source_invert': ('source', 'not'),
        'source_net': ('source', 'network'),
        'source_port': ('source', 'port'),
        'destination_invert': ('destination', 'not'),
        'destination_net': ('destination', 'network'),
        'destination_port': ('destination', 'port'),
        'local_port': 'local-port',
        'pool_opts': 'poolopts',
        'description': 'descr',
        'nat_reflection': 'natreflection',
        'associated_rule': 'pass',
        # the DNat-model differs from the filter-models: 'category' is the field (options keyed by NAME),
        # 'categories' is a volatile mapper holding the uuids for the WebUI - we read & write 'category'
        'categories': 'category',
        'sync': 'nosync',
    }
    FIELDS_TYPING = {
        'bool': ['enabled', 'log', 'no_port_forward', 'source_invert', 'destination_invert', 'sync'],
        'list': ['interface'],
        'list_value': ['categories'],
        'select': ['ip_protocol', 'protocol', 'pool_opts', 'nat_reflection', 'associated_rule'],
        'int': ['sequence'],
    }
    INT_VALIDATIONS = {
        'sequence': {'min': 1, 'max': 999999},
    }
    EXIST_ATTR = 'rule'
    API_CMD_REL = 'apply'
    SKIP_AUTO_ENTRIES = True

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None, fail: dict = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session, f=fail)
        self.rule = {}

    def check(self) -> None:
        if self.p['state'] == 'present':
            if is_unset(self.p['target']):
                self.m.fail_json(
                    "You need to provide a 'target' to create a destination-nat rule!"
                )

        if not is_unset(self.p['protocol']):
            # OPNsense stores/returns 'protocol' lowercase (model enforces 'ChangeCase: lower') -
            # normalize here so diff-comparisons against the existing entry don't falsely report a change
            self.p['protocol'] = self.p['protocol'].lower()

        self.find(match_fields=self.p['match_fields'])

        if self.p['state'] == 'present':
            self._check_categories()

        self._base_check()

    def _get_category_selection(self) -> (dict, None):
        # every existing rule carries the full option-list of categories (keyed by name) -
        # an empty list if no category is defined on the firewall; None if no rule exists to read it from
        if not isinstance(self.existing_entries, dict):
            return None

        for entry in self.existing_entries.values():
            if not isinstance(entry, dict) or 'category' not in entry:
                continue

            if isinstance(entry['category'], dict):
                return entry['category']

            return {}

        return None

    def _check_categories(self) -> None:
        if is_unset(self.p['categories']):
            return

        selection = self._get_category_selection()
        if selection is None:
            # nothing to validate against - the API will reject unknown ones
            return

        unknown = [c for c in self.p['categories'] if c not in selection]
        if len(unknown) > 0:
            self.m.fail_json(
                f"Unknown rule categories: {unknown} | "
                f"Available: {sorted(selection.keys())}"
            )
