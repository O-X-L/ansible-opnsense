import re

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.oxlorg.opnsense.plugins.module_utils.helper.validate import \
    is_unset
from ansible_collections.oxlorg.opnsense.plugins.module_utils.helper.rule import \
    validate_values
from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.cls import BaseModule

_UUID_RE = re.compile(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$', re.IGNORECASE)


class DNat(BaseModule):
    CMDS = {
        'add': 'add_rule',
        'del': 'del_rule',
        'set': 'set_rule',
        'search': 'search_rule',
        'detail': 'get_rule',
        'toggle': 'toggle_rule',
    }
    API_KEY_PATH = 'rule'
    API_MOD = 'firewall'
    API_CONT = 'd_nat'
    FIELDS_CHANGE = [
        'sequence', 'no_rdr', 'interface', 'target', 'target_port', 'description',
        'ip_protocol', 'protocol', 'source_invert', 'source_net', 'source_port',
        'destination_invert', 'destination_net', 'destination_port', 'log',
        'nat_reflection', 'filter_rule',
    ]
    FIELDS_ALL = ['enabled']
    FIELDS_ALL.extend(FIELDS_CHANGE)
    FIELDS_TRANSLATE = {
        'enabled': 'disabled',
        'description': 'descr',
        'ip_protocol': 'ipprotocol',
        'source_invert': ('source', 'not'),
        'source_net': ('source', 'network'),
        'source_port': ('source', 'port'),
        'destination_invert': ('destination', 'not'),
        'destination_net': ('destination', 'network'),
        'destination_port': ('destination', 'port'),
        'target_port': 'local-port',
        'nat_reflection': 'natreflection',
        'no_rdr': 'nordr',
        'filter_rule': 'pass',
    }
    FIELDS_BOOL_INVERT = ['enabled']
    FIELDS_TYPING = {
        'bool': ['enabled', 'log', 'source_invert', 'destination_invert', 'no_rdr'],
        'list': [],
        'select': ['interface', 'ip_protocol', 'protocol', 'nat_reflection', 'filter_rule'],
        'int': [],
    }
    FIELDS_VALUE_MAPPING = {
        # For the OPNsense API, '' means 'any', so mapping it
        'protocol': {'any': ''},
    }
    INT_VALIDATIONS = {
        'sequence': {'min': 1, 'max': 99999},
    }
    EXIST_ATTR = 'rule'
    API_CMD_REL = 'apply'

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None, fail: dict = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session, f=fail)
        self.rule = {}

    def _filter_search_entry(self, entry: dict) -> bool:
        # OPNsense search_rule returns system entries (e.g. 'lockout_2') with non-UUID identifiers.
        # When it tries to issue a get_rule request with these 'non-UUID' identifiers (e.g.: get_rule/lockout_2),
        # the API won't return the system entry but the default response for non-existent IDs -- an empty list.
        # This breaks the code, so skip these entries.
        return bool(_UUID_RE.match(entry.get('uuid', '')))

    def check(self) -> None:
        if self.p['state'] == 'present':
            if is_unset(self.p['target']):
                self.m.fail_json(
                    "You need to provide a 'target' to create a destination-nat rule!"
                )

        if self.p['protocol'] not in [None, '', 'any']:
            self.p['protocol'] = self.p['protocol'].lower()

        self._build_log_name()
        self.b.find(match_fields=self.p['match_fields'])

        if self.p['state'] == 'present':
            validate_values(module=self.m, cnf=self.p, error_func=self.m.fail_json, kind='nat')

        self._base_check()

    def _build_log_name(self) -> str:
        if self.p['description'] not in [None, '']:
            log_name = self.p['description']

        else:
            log_name = 'FROM '

            if self.p['source_invert']:
                log_name += 'NOT '

            log_name += f"{self.p['source_net']} <= PROTO {self.p['protocol']} => "

            if self.p['destination_invert']:
                log_name += 'NOT '

            log_name += f"{self.p['destination_net']}:{self.p['destination_port']} "
            log_name += f" =DNAT=> {self.p['target']}:{self.p['target_port']}"

        return log_name
