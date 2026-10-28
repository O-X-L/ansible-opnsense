from copy import deepcopy

from ansible_collections.oxlorg.opnsense.plugins.module_utils.test.testdata.base_testdata import MockOPNsenseController

CATEGORIES = {'6adf800000000001': 'Ops', '6adf800000000002': 'VPN'}

INTERFACES = {'lan': 'LAN', 'wan': 'WAN', 'opt1': 'DMZ'}
IP_PROTOCOLS = ['inet', 'inet6', 'inet46']
PROTOCOLS = ['', 'tcp', 'udp', 'tcp/udp', 'icmp']
POOL_OPTS = [
    '', 'round-robin', 'round-robin sticky-address', 'random', 'random sticky-address', 'source-hash', 'bitmask',
]
NAT_REFLECTION = ['', 'purenat', 'disable']
PASS = ['', 'pass', 'rule']

RULE_1 = {
    'sequence': '1', 'disabled': '0', 'nordr': '0', 'interface': 'wan', 'ipprotocol': 'inet', 'protocol': 'tcp',
    'source': {'not': '0', 'network': 'any', 'port': ''},
    'destination': {'not': '0', 'network': '203.0.113.10', 'port': '443'},
    'target': '192.168.0.10', 'local-port': '8443', 'poolopts': '', 'log': '1', 'descr': 'ANSIBLE_TEST_1_1',
    'tag': '', 'tagged': '', 'natreflection': '', 'pass': '', 'category': '', 'nosync': '0',
}


class Testdata_26_7_7(MockOPNsenseController):
    """
    Emulates the OPNsense destination-NAT API (see: OPNsense/Firewall/Api/DNatController.php, models/DNat.xml)
    as observed on 26.7:
    * 'get' returns the whole model; option-fields as selection-dicts, booleans as '0'/'1'
    * 'category' is a list-field whose options are keyed by the category NAME ('CategoryField') -
      an empty LIST when no category exists on the firewall
    * 'categories' is a volatile mapper holding the comma-separated category UUIDs
    * a posted unknown category fails validation like the real API does
    """

    def __init__(self, categories: dict = None, rules: list = None):
        super().__init__()
        self.categories = CATEGORIES if categories is None else categories
        self.state = {}
        self.calls = []
        for rule in (rules if rules is not None else [RULE_1]):
            self.state[self._new_uuid()] = self._build_entry(rule)

    def commands(self) -> dict:
        return {
            'get': self._get,
            'add_rule': self._add,
            'set_rule': self._set,
            'del_rule': self._del,
            'toggle_rule': self._toggle,
            'apply': self._apply,
        }

    def route_kwargs(self, method) -> list:
        return {
            self._get: [],
            self._add: ['data'],
            self._set: ['uuid', 'data'],
            self._del: ['uuid'],
            self._toggle: ['uuid'],
            self._apply: [],
        }[method]

    @staticmethod
    def _selection(options: (list, dict), selected: (str, list)) -> dict:
        if isinstance(options, list):
            options = {o: o for o in options}

        if isinstance(selected, str):
            selected = selected.split(',')

        return {k: {'value': v, 'selected': 1 if k in selected else 0} for k, v in options.items()}

    def _category_selection(self, selected: str) -> (dict, list):
        if len(self.categories) == 0:
            return []

        return self._selection({name: name for name in self.categories.values()}, selected)

    def _category_uuids(self, selected: str) -> str:
        names = selected.split(',') if selected != '' else []
        return ','.join([uuid for uuid, name in self.categories.items() if name in names])

    def _validate(self, rule: dict) -> dict:
        validations = {}
        for name in (rule.get('category', '').split(',') if rule.get('category', '') != '' else []):
            if name not in self.categories.values():
                validations['rule.category'] = 'Option not in list.'

        return validations

    def _build_entry(self, rule: dict) -> dict:
        rule = {k: (str(v) if not isinstance(v, dict) else v) for k, v in rule.items()}
        return {
            'sequence': rule['sequence'],
            'disabled': rule['disabled'],
            'nordr': rule['nordr'],
            'interface': self._selection(INTERFACES, rule['interface']),
            'ipprotocol': self._selection(IP_PROTOCOLS, rule['ipprotocol']),
            'protocol': self._selection(PROTOCOLS, rule['protocol']),
            'source': {
                'network': rule['source']['network'], 'address': rule['source']['network'],
                'port': rule['source']['port'], 'not': str(rule['source']['not']),
            },
            'destination': {
                'network': rule['destination']['network'], 'address': rule['destination']['network'],
                'port': rule['destination']['port'], 'not': str(rule['destination']['not']),
            },
            'target': rule['target'],
            'local-port': rule['local-port'],
            'poolopts': self._selection(POOL_OPTS, rule['poolopts']),
            'log': rule['log'],
            'category': self._category_selection(rule.get('category', '')),
            'categories': self._category_uuids(rule.get('category', '')),
            'descr': rule['descr'],
            'tag': rule['tag'],
            'tagged': rule['tagged'],
            'nosync': rule.get('nosync', '0'),
            'natreflection': self._selection(NAT_REFLECTION, rule['natreflection']),
            'pass': self._selection(PASS, rule['pass']),
            'audit': {},
            'associated-rule-id': '',
            'created': {},
        }

    def _get(self) -> dict:
        self.calls.append(('get', None))
        return {'DNat': {'rule': deepcopy(self.state)}}

    def _add(self, data: dict) -> dict:
        self.calls.append(('add', deepcopy(data['rule'])))
        validations = self._validate(data['rule'])
        if len(validations) > 0:
            return {'result': 'failed', 'validations': validations}

        self.state[self._new_uuid()] = self._build_entry(data['rule'])
        return {'result': 'saved'}

    def _set(self, uuid: str, data: dict) -> dict:
        self.calls.append(('set', deepcopy(data['rule'])))
        if uuid not in self.state:
            return self.RES_ERROR

        validations = self._validate(data['rule'])
        if len(validations) > 0:
            return {'result': 'failed', 'validations': validations}

        self.state[uuid] = self._build_entry(data['rule'])
        return {'result': 'saved'}

    def _del(self, uuid: str) -> dict:
        self.calls.append(('del', uuid))
        if uuid not in self.state:
            return self.RES_ERROR

        self.state.pop(uuid)
        return {'result': 'deleted'}

    def _toggle(self, uuid: str) -> dict:
        self.calls.append(('toggle', uuid))
        if uuid not in self.state:
            return self.RES_ERROR

        self.state[uuid]['disabled'] = '0' if self.state[uuid]['disabled'] == '1' else '1'
        return {'result': 'ok'}

    def _apply(self) -> dict:
        self.calls.append(('apply', None))
        return {'status': 'ok'}

    def mutations(self) -> list:
        return [call for call in self.calls if call[0] in ['add', 'set', 'del', 'toggle', 'apply']]

    def rule_by_descr(self, descr: str) -> (dict, None):
        for entry in self.state.values():
            if entry['descr'] == descr:
                return entry

        return None
