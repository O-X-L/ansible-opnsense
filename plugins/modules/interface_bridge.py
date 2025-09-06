#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (C) 2024, AnsibleGuy <guy@ansibleguy.net>
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.handler import \
    module_dependency_error, MODULE_EXCEPTIONS

try:
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.wrapper import module_wrapper
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.defaults.main import \
        OPN_MOD_ARGS, STATE_ONLY_MOD_ARG, RELOAD_MOD_ARG
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.interface_bridge import Bridge

except MODULE_EXCEPTIONS:
    module_dependency_error()


# DOCUMENTATION = 'https://ansible-opnsense.oxl.app/modules/interface.html'
# EXAMPLES = 'https://ansible-opnsense.oxl.app/modules/interface.html'


def run_module():
    module_args = dict(
        description=dict(
            type='str', required=True, aliases=['desc'],
            description='The unique description used to match the configured entries to the existing ones.',
        ),
        members=dict(
            type='list', elements='str', required=False, aliases=['ports', 'ints'],
            description='Interfaces participating in the bridge. - you must provide the network '
                        "port as shown in 'Interfaces - Assignments - Network port'",
        ),
        link_local=dict(
            type='bool', required=False, default=False,
            description='Enable link-local addresses on the interface.',
        ),
        stp=dict(
            type='bool', required=False, default=False,
            description='Enable spanning tree options for this bridge.',
        ),
        stp_proto=dict(
            type='str', required=False, aliases=['desc'], default='rstp', choices=['rstp', 'stp'],
            description='Protocol used for spanning tree.',
        ),
        stp_interfaces=dict(
            type='list', elements='str', required=False, default=[], aliases=['stp_ports', 'stp_ints'],
            description='Interfaces to enable Spanning Tree Protocol on.',
        ),
        stp_max_age=dict(
            type='int', required=False,
            description='Time that a Spanning Tree Protocol configuration is valid.',
        ),
        stp_fwdelay=dict(
            type='int', required=False,
            description='Time that must pass before an interface begins forwarding packets.',
        ),
        stp_hold=dict(
            type='int', required=False,
            description='Tansmit hold count for Spanning Tree.',
        ),
        cache_size=dict(
            type='int', required=False,
            description='Size of the bridge address cache.',
        ),
        cache_timeout=dict(
            type='int', required=False,
            description='Timeout of address cache entries.',
        ),
        span_interfaces=dict(
            type='list', elements='str', required=False, default=[], aliases=['span_ports', 'span_ints'],
            description='Interfaces to add as span ports.',
        ),
        edge_interfaces=dict(
            type='list', elements='str', required=False, default=[], aliases=['edge_ports', 'edge_ints'],
            description='Interfaces to set as edge ports.',
        ),
        auto_edge_interfaces=dict(
            type='list', elements='str', required=False, default=[], aliases=['auto_edge_ports', 'auto_edge_ints'],
            description='Allow selected interfaces to automatically detect edge status.',
        ),
        ptp_interfaces=dict(
            type='list', elements='str', required=False, default=[], aliases=['ptp_ports', 'ptp_ints'],
            description='Interfaces to set as point-to-point link.',
        ),
        auto_ptp_interfaces=dict(
            type='list', elements='str', required=False, default=[], aliases=['edge_ports', 'edge_ints'],
            description='Automatically detect the point-to-point status on selected interfaces.',
        ),
        static_interfaces=dict(
            type='list', elements='str', required=False, default=[],
            aliases=['static_ports', 'static_ints', 'sticky_interfaces', 'sticky_ports', 'sticky_ints'],
            description='Mark interfaces as a "sticky" interface.',
        ),
        private_interfaces=dict(
            type='list', elements='str', required=False, default=[], aliases=['private_ports', 'eprivate_ints'],
            description='Mark interfaces as a "private" interface.',
        ),
        **RELOAD_MOD_ARG,
        **STATE_ONLY_MOD_ARG,
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
            ('state', 'present', ('members',)),
        ],
    )

    module_wrapper(Bridge(module=module, result=result))
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
