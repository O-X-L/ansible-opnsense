from copy import deepcopy

from ansible_collections.oxlorg.opnsense.plugins.module_utils.test.testdata.base_testdata import MockOPNsenseController

INTERFACES = {'': 'none', 'lan': 'LAN', 'wan': 'WAN', 'opt1': 'DMZ'}
AS_MODES = ['', 'internal', 'external']
FAMILIES = ['ipv4', 'ipv6']
REMOVE_PRIVATE_AS = [
    '', 'remove-private-AS', 'remove-private-AS all', 'remove-private-AS replace-AS',
    'remove-private-AS all replace-AS',
]
ALLOW_AS_IN = ['', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'origin']
ATTRIBUTE_UNCHANGED = ['', 'as-path', 'next-hop', 'med']
CAPABILITIES = ['extended-nexthop', 'dynamic', 'fqdn', 'link-local']
BESTPATH = [
    'as-path confed', 'as-path multipath-relax', 'compare-routerid', 'peer-type multipath-relax', 'aigp',
    'med missing-as-worst',
]

PEER_GROUPS = {'6adf800000000001': 'ANSIBLE_TEST_PG'}

GENERAL = {
    'enabled': '1', 'asnumber': '64496', 'distance': '', 'routerid': '10.0.0.1', 'graceful': '0',
    'networkimportcheck': '1', 'enforce_first_as': '1', 'logneighborchanges': '1', 'networks': '',
    'bestpath': '', 'maximumpaths': '', 'maximumpathsibgp': '',
}

NEIGHBOR_1 = {
    'enabled': '1', 'description': 'ANSIBLE_TEST_1_1', 'address': '10.0.0.1', 'family': 'ipv4',
    'remote_as_mode': '', 'remoteas': '64496', 'localas': '', 'password': '', 'weight': '', 'localip': '',
    'updatesource': '', 'linklocalinterface': '', 'nexthopself': '0', 'nexthopselfall': '0', 'multihop': '0',
    'rrclient': '0', 'soft_reconfiguration_inbound': '0', 'bfd': '0', 'bfd_strict': '0', 'keepalive': '60',
    'holddown': '180', 'connecttimer': '', 'defaultoriginate': '0', 'asoverride': '0', 'removeprivateas': '',
    'allowas_in': '', 'disable_connected_check': '0', 'attributeunchanged': '', 'capabilities': '',
    'linkedPrefixlistIn': '', 'linkedPrefixlistOut': '', 'linkedRoutemapIn': '', 'linkedRoutemapOut': '',
    'peergroup': '',
}


class Testdata_26_7_7(MockOPNsenseController):
    """
    Emulates the BGP part of the os-frr 2.0 API (see: OPNsense/Quagga/Api/BgpController.php, models/BGP.xml)
    as observed on 26.7:
    * 'get' returns the whole BGP model; option-fields as selection-dicts, booleans as '0'/'1'
    * 'set' writes the general settings, the neighbor commands write one neighbor each
    * the linked peer group is posted as uuid, the option-fields as the FRR command-arguments they stand for
    * a posted option that is not in the list fails validation like the real API does
    """

    def __init__(self, general: dict = None, neighbors: list = None, peer_groups: dict = None):
        super().__init__()
        self.general = deepcopy(GENERAL) if general is None else general
        self.peer_groups = PEER_GROUPS if peer_groups is None else peer_groups
        self.state = {}
        self.calls = []
        for neighbor in (neighbors if neighbors is not None else [NEIGHBOR_1]):
            self.state[self._new_uuid()] = deepcopy(neighbor)

    def commands(self) -> dict:
        return {
            'get': self._get,
            'set': self._set_general,
            'addNeighbor': self._add,
            'setNeighbor': self._set,
            'delNeighbor': self._del,
            'toggleNeighbor': self._toggle,
            'reconfigure': self._reconfigure,
        }

    def route_kwargs(self, method) -> list:
        return {
            self._get: [],
            self._set_general: ['data'],
            self._add: ['data'],
            self._set: ['uuid', 'data'],
            self._del: ['uuid'],
            self._toggle: ['uuid'],
            self._reconfigure: [],
        }[method]

    @staticmethod
    def _selection(options: (list, dict), selected: str) -> dict:
        if isinstance(options, list):
            options = {o: o for o in options}

        selected = selected.split(',')
        return {k: {'value': v, 'selected': 1 if k in selected else 0} for k, v in options.items()}

    @staticmethod
    def _validate_selection(validations: dict, field: str, options: list, value: str, multiple: bool = False):
        if multiple:
            # an empty multi-select is posted as empty string
            values = value.split(',') if value != '' else []

        else:
            values = [value]

        for v in values:
            if v not in options:
                validations[field] = 'Option not in list.'

    def _validate_general(self, general: dict) -> dict:
        validations = {}
        self._validate_selection(validations, 'bgp.bestpath', BESTPATH, general.get('bestpath', ''), multiple=True)
        for field in ['maximumpaths', 'maximumpathsibgp']:
            value = str(general.get(field, ''))
            if value != '' and not (value.isnumeric() and 1 <= int(value) <= 128):
                validations[f'bgp.{field}'] = 'The value shall be between 1 and 128 or left empty to use the default.'

        return validations

    def _validate_neighbor(self, neighbor: dict) -> dict:
        validations = {}
        self._validate_selection(validations, 'neighbor.family', FAMILIES, neighbor.get('family', ''), multiple=True)
        self._validate_selection(validations, 'neighbor.remote_as_mode', AS_MODES, neighbor.get('remote_as_mode', ''))
        self._validate_selection(
            validations, 'neighbor.removeprivateas', REMOVE_PRIVATE_AS, neighbor.get('removeprivateas', ''),
        )
        self._validate_selection(validations, 'neighbor.allowas_in', ALLOW_AS_IN, neighbor.get('allowas_in', ''))
        self._validate_selection(
            validations, 'neighbor.attributeunchanged', ATTRIBUTE_UNCHANGED, neighbor.get('attributeunchanged', ''),
        )
        self._validate_selection(
            validations, 'neighbor.capabilities', CAPABILITIES, neighbor.get('capabilities', ''), multiple=True,
        )
        self._validate_selection(
            validations, 'neighbor.peergroup', [''] + list(self.peer_groups.keys()), neighbor.get('peergroup', ''),
        )
        return validations

    def _build_general(self) -> dict:
        general = deepcopy(self.general)
        networks = general['networks'].split(',') if general['networks'] != '' else []
        general['networks'] = self._selection({n: n for n in networks}, general['networks'])
        general['bestpath'] = self._selection(BESTPATH, general['bestpath'])
        return general

    def _build_neighbor(self, neighbor: dict) -> dict:
        entry = deepcopy(neighbor)
        entry['family'] = self._selection(FAMILIES, neighbor['family'])
        entry['remote_as_mode'] = self._selection(AS_MODES, neighbor['remote_as_mode'])
        entry['updatesource'] = self._selection(INTERFACES, neighbor['updatesource'])
        entry['linklocalinterface'] = self._selection(INTERFACES, neighbor['linklocalinterface'])
        entry['removeprivateas'] = self._selection(REMOVE_PRIVATE_AS, neighbor['removeprivateas'])
        entry['allowas_in'] = self._selection(ALLOW_AS_IN, neighbor['allowas_in'])
        entry['attributeunchanged'] = self._selection(ATTRIBUTE_UNCHANGED, neighbor['attributeunchanged'])
        entry['capabilities'] = self._selection(CAPABILITIES, neighbor['capabilities'])
        entry['peergroup'] = self._selection({'': 'none', **self.peer_groups}, neighbor['peergroup'])
        for field in ['linkedPrefixlistIn', 'linkedPrefixlistOut', 'linkedRoutemapIn', 'linkedRoutemapOut']:
            entry[field] = self._selection({'': 'none'}, neighbor[field])

        return entry

    def _build_peer_groups(self) -> dict:
        return {
            uuid: {'enabled': '1', 'name': name, 'remoteas': '64498', 'remote_as_mode': self._selection(AS_MODES, '')}
            for uuid, name in self.peer_groups.items()
        }

    def _get(self) -> dict:
        self.calls.append(('get', None))
        return {'bgp': {
            **self._build_general(),
            'neighbors': {'neighbor': {uuid: self._build_neighbor(n) for uuid, n in self.state.items()}},
            'peergroups': {'peergroup': self._build_peer_groups()},
            'prefixlists': {'prefixlist': {}},
            'routemaps': {'routemap': {}},
            'aspaths': {'aspath': {}},
            'communitylists': {'communitylist': {}},
            'redistributions': {'redistribution': {}},
        }}

    def _set_general(self, data: dict) -> dict:
        self.calls.append(('set_general', deepcopy(data['bgp'])))
        validations = self._validate_general(data['bgp'])
        if len(validations) > 0:
            return {'result': 'failed', 'validations': validations}

        self.general.update({k: str(v) for k, v in data['bgp'].items()})
        return {'result': 'saved'}

    def _add(self, data: dict) -> dict:
        self.calls.append(('add', deepcopy(data['neighbor'])))
        validations = self._validate_neighbor(data['neighbor'])
        if len(validations) > 0:
            return {'result': 'failed', 'validations': validations}

        self.state[self._new_uuid()] = {k: str(v) for k, v in data['neighbor'].items()}
        return {'result': 'saved'}

    def _set(self, uuid: str, data: dict) -> dict:
        self.calls.append(('set', deepcopy(data['neighbor'])))
        if uuid not in self.state:
            return self.RES_ERROR

        validations = self._validate_neighbor(data['neighbor'])
        if len(validations) > 0:
            return {'result': 'failed', 'validations': validations}

        self.state[uuid] = {k: str(v) for k, v in data['neighbor'].items()}
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

        self.state[uuid]['enabled'] = '0' if self.state[uuid]['enabled'] == '1' else '1'
        return {'result': 'ok'}

    def _reconfigure(self) -> dict:
        self.calls.append(('reconfigure', None))
        return {'status': 'ok'}

    def mutations(self) -> list:
        return [call for call in self.calls if call[0] != 'get']

    def neighbor_by_descr(self, descr: str) -> (dict, None):
        for entry in self.state.values():
            if entry['description'] == descr:
                return entry

        return None
