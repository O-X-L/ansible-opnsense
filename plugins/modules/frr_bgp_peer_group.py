#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (C) 2025, Pascal Rath <contact+opnsense@OXL.at>
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

# see: https://docs.opnsense.org/development/api/plugins/quagga.html

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.handler import \
    module_dependency_error, MODULE_EXCEPTIONS

try:
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.wrapper import module_wrapper
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.defaults.main import \
        OPN_MOD_ARGS, STATE_MOD_ARG, RELOAD_MOD_ARG
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.frr_bgp_peer_group import PeerGroup

except MODULE_EXCEPTIONS:
    module_dependency_error()


# DOCUMENTATION = 'https://ansible-opnsense.oxl.app/modules/frr_bgp.html#ansibleguy-opnsense-frr-bgp-neighbor'
# EXAMPLES = 'https://ansible-opnsense.oxl.app/modules/frr_bgp.html#id2'


def run_module():
    module_args = dict(
        name=dict(
            type='str', required=True,
            description=' Name of the peer group.'
        ),
        as_mode=dict(
            type='str', required=False, aliases=['remote_as_mode'],
            choices=['', 'internal', 'external']
        ),
        as_number=dict(
            type='int', required=False, aliases=['as', 'as_nr', 'remote_as'],
        ),
        source_int=dict(
            type='str', required=False,
            aliases=['update_source', 'update_src', 'src_int'],
            description='Physical name of the IPv4 interface facing the peer',
        ),
        next_hop_self=dict(
            type='bool', required=False, default=False, aliases=['nhs'],
            description='Sets the local router as the next hop for routes advertised to the neighbor, '
                        'commonly used in Route Reflector setups.',
        ),
        send_default_route=dict(
            type='bool', required=False, default=False, aliases=['default_originate'],
            description='Enable sending of default routes to the peer group.',
        ),
        prefix_list_in=dict(
            type='str', required=False, aliases=['prefix_in', 'pre_in'],
            description='Prefix list to filter inbound prefixes from this neighbor.',
        ),
        prefix_list_out=dict(
            type='str', required=False, aliases=['prefix_out', 'pre_out'],
            description='Prefix list to filter outbound prefixes sent to this neighbor.',
        ),
        route_map_in=dict(
            type='str', required=False, aliases=['map_in', 'rm_in'],
            description='Route-map to apply to routes received from this neighbor.',
        ),
        route_map_out=dict(
            type='str', required=False, aliases=['map_out', 'rm_out'],
            description='Route-map to apply to routes advertised to this neighbor.',
        ),
        listen_ranges=dict(
            type='list', elements='str', required=False, aliases=['ranges'], default=[],
            description='One or multiple valid IP networks in CIDR notation.',
        ),
        **STATE_MOD_ARG,
        **RELOAD_MOD_ARG,
        **OPN_MOD_ARGS,
    )

    result = dict(
        changed=False,
        diff={
            'before': {},
            'after': {},
        }
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
        required_if=[
            ('state', 'present', ('as_mode', 'as_number'), True),
        ],
        mutually_exclusive=[
            ('as_mode', 'as_number'),
        ]
    )

    module_wrapper(PeerGroup(module=module, result=result))
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
