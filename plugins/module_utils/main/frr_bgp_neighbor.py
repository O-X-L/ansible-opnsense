from ansible.module_utils.basic import AnsibleModule

from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.oxlorg.opnsense.plugins.module_utils.helper.validate import \
    is_ip, is_ip6, is_unset
from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.module import BaseModule


class Neighbor(BaseModule):
    CMDS = {
        'add': 'addNeighbor',
        'del': 'delNeighbor',
        'set': 'setNeighbor',
        'search': 'get',
        'toggle': 'toggleNeighbor',
    }
    API_KEY_PATH = 'bgp.neighbors.neighbor'
    API_MOD = 'quagga'
    API_CONT = 'bgp'
    API_CONT_REL = 'service'
    FIELDS_CHANGE = [
        'ip', 'as_number', 'local_as', 'family', 'password', 'weight', 'local_ip', 'source_int',
        'ipv6_link_local_int', 'next_hop_self', 'next_hop_self_all',
        'multi_hop', 'rrclient', 'soft_reconfiguration_inbound', 'bfd', 'bfd_strict',
        'send_default_route', 'as_override', 'remove_private_as', 'allow_as_in',
        'disable_connected_check', 'attribute_unchanged', 'capabilities', 'keepalive', 'hold_down',
        'connect_timer', 'description', 'prefix_list_in', 'prefix_list_out',
        'route_map_in', 'route_map_out', 'remote_as_mode', 'peer_group',
    ]
    FIELDS_DIFF_NO_LOG = ['password']
    FIELDS_ALL = ['enabled']
    FIELDS_ALL.extend(FIELDS_CHANGE)
    FIELDS_TRANSLATE = {
        'as_number': 'remoteas',
        'local_as': 'localas',
        'ip': 'address',
        'local_ip': 'localip',
        'source_int': 'updatesource',
        'ipv6_link_local_int': 'linklocalinterface',
        'next_hop_self': 'nexthopself',
        'next_hop_self_all': 'nexthopselfall',
        'multi_hop': 'multihop',
        'hold_down': 'holddown',
        'connect_timer': 'connecttimer',
        'send_default_route': 'defaultoriginate',
        'as_override': 'asoverride',
        'remove_private_as': 'removeprivateas',
        'allow_as_in': 'allowas_in',
        'attribute_unchanged': 'attributeunchanged',
        'prefix_list_in': 'linkedPrefixlistIn',
        'prefix_list_out': 'linkedPrefixlistOut',
        'route_map_in': 'linkedRoutemapIn',
        'route_map_out': 'linkedRoutemapOut',
        'peer_group': 'peergroup',
    }
    FIELDS_TYPING = {
        'bool': [
            'next_hop_self', 'next_hop_self_all', 'multi_hop', 'enabled',
            'rrclient', 'soft_reconfiguration_inbound', 'bfd', 'bfd_strict', 'send_default_route',
            'as_override', 'disable_connected_check',
        ],
        'select': [
            'source_int', 'ipv6_link_local_int', 'prefix_list_in', 'prefix_list_out',
            'route_map_in', 'route_map_out', 'remote_as_mode', 'remove_private_as', 'allow_as_in',
            'attribute_unchanged', 'peer_group',
        ],
        'list': ['family', 'capabilities'],
    }
    FIELDS_VALUE_MAPPING = {
        # the API stores the FRR command-arguments; keyed by the option-names of the model
        'remove_private_as': {
            'remove_private': 'remove-private-AS',
            'remove_all': 'remove-private-AS all',
            'replace_private': 'remove-private-AS replace-AS',
            'replace_all': 'remove-private-AS all replace-AS',
        },
    }
    INT_VALIDATIONS = {
        'as_number': {'min': 1, 'max': 4294967295},
        'local_as': {'min': 1, 'max': 4294967295},
        'weight': {'min': 0, 'max': 65535},
        'keepalive': {'min': 1, 'max': 1000},
        'hold_down': {'min': 3, 'max': 3000},
        'connect_timer': {'min': 1, 'max': 65000},
    }
    EXIST_ATTR = 'neighbor'
    SEARCH_ADDITIONAL = {
        'existing_prefixes': 'bgp.prefixlists.prefixlist',
        'existing_maps': 'bgp.routemaps.routemap',
        'existing_peer_groups': 'bgp.peergroups.peergroup',
    }

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None, fail: dict = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session, f=fail)
        self.neighbor = {}
        self.existing_prefixes = None
        self.existing_maps = None
        self.existing_peer_groups = None

    def check(self) -> None:
        if self.p['state'] == 'present':
            if is_unset(self.p['ip']):
                self.m.fail_json('To create a BGP neighbor you need to provide its peer-ip!')

            if not is_ip(self.p['ip']):
                self.m.fail_json(f"Provided peer IP '{self.p['ip']}' is not a valid IP-Address!")

            if not is_unset(self.p['local_ip']) and not is_ip(self.p['local_ip']):
                self.m.fail_json(f"Provided source IP '{self.p['local_ip']}' is not a valid IP-Address!")

            if self.p['bfd_strict'] and not self.p['bfd']:
                self.m.fail_json("The option 'bfd_strict' requires 'bfd' to be enabled!")

            self._set_family()

        self._base_check()
        self._find_links()

    def _set_family(self) -> None:
        # os-frr 2.0 replaced the 'multiprotocol' toggle with the 'family' multi-select
        if self.p['multi_protocol'] is not None:
            if not is_unset(self.p['family']):
                self.m.fail_json("The options 'family' and 'multi_protocol' are mutually exclusive!")

            if self.p['multi_protocol']:
                self.p['family'] = ['ipv4', 'ipv6']

        if is_unset(self.p['family']):
            # same default as the os-frr migration of existing neighbors
            self.p['family'] = ['ipv6'] if is_ip6(self.p['ip']) else ['ipv4']

    def _find_links(self) -> None:
        links = {
            'prefix-list-in': {
                'found': False,
                'existing': self.existing_prefixes,
                'match_fields': {'name': 'prefix_list_in'}
            },
            'prefix-list-out': {
                'found': False,
                'existing': self.existing_prefixes,
                'match_fields': {'name': 'prefix_list_out'}
            },
            'route-map-in': {
                'found': False,
                'existing': self.existing_maps,
                'match_fields': {'name': 'route_map_in'}
            },
            'route-map-out': {
                'found': False,
                'existing': self.existing_maps,
                'match_fields': {'name': 'route_map_out'}
            },
            'peer-group': {
                'found': False,
                'existing': self.existing_peer_groups,
                'match_fields': {'name': 'peer_group'}
            },
        }

        for key, values in links.items():
            value_name = values['match_fields']['name']
            provided = not is_unset(self.p[value_name])
            seq_uuid_mapping = {}

            if not provided:
                continue

            if len(values['existing']) > 0:
                for uuid, entry in values['existing'].items():
                    matching = []

                    for api_field, ans_field in values['match_fields'].items():
                        if not is_unset(self.p[ans_field]):
                            matching.append(str(entry[api_field]) == str(self.p[ans_field]))

                    if all(matching):
                        self.p[value_name] = uuid
                        values['found'] = True

                        if 'seqnumber' in entry:
                            seq_uuid_mapping[int(entry['seqnumber'])] = uuid

            if not values['found']:
                self.m.fail_json(
                    f"Provided {key} '{value_name}' was not found!"
                )

            if len(seq_uuid_mapping) > 0:
                # only the lowest prefix-list uuid is linkable - all others are just extensions of the first one
                self.p[value_name] = seq_uuid_mapping[min(seq_uuid_mapping.keys())]

    def get_existing(self) -> list:
        existing = []

        for entry in self._base_get_existing():
            if entry['prefix_list_in'] not in [None, ''] and \
                    entry['prefix_list_in'] in self.existing_prefixes:
                entry['prefix_list_in'] = self.existing_prefixes[entry['prefix_list_in']]['name']

            if entry['prefix_list_out'] not in [None, ''] and \
                    entry['prefix_list_out'] in self.existing_prefixes:
                entry['prefix_list_out'] = self.existing_prefixes[entry['prefix_list_out']]['name']

            if entry['route_map_in'] not in [None, ''] and \
                    entry['route_map_in'] in self.existing_maps:
                entry['route_map_in'] = self.existing_maps[entry['route_map_in']]['name']

            if entry['route_map_out'] not in [None, ''] and \
                    entry['route_map_out'] in self.existing_maps:
                entry['route_map_out'] = self.existing_maps[entry['route_map_out']]['name']

            if entry['peer_group'] not in [None, ''] and \
                    entry['peer_group'] in self.existing_peer_groups:
                entry['peer_group'] = self.existing_peer_groups[entry['peer_group']]['name']

            existing.append(entry)

        return existing
