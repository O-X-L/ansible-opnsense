#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (C) 2025, Pascal Rath <contact+opnsense@OXL.at>
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

# see: https://docs.opnsense.org/development/api/core/kea.html

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.handler import \
    module_dependency_error, MODULE_EXCEPTIONS

try:
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.wrapper import module_wrapper
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.defaults.main import \
        OPN_MOD_ARGS, STATE_MOD_ARG, RELOAD_MOD_ARG
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.main.dhcp_reservation_v4 import ReservationV4

except MODULE_EXCEPTIONS:
    module_dependency_error()


# DOCUMENTATION = 'https://ansible-opnsense.oxl.app/modules/dhcp.html'
# EXAMPLES = 'https://ansible-opnsense.oxl.app/modules/dhcp.html'


def run_module():
    module_args = dict(
        ip=dict(
            type='str', required=True, aliases=['ip_address'],
            description='IP address to offer to the client',
        ),
        mac=dict(
            type='str', required=False, aliases=['mac_address'],
            description='MAC/Ether address of the client in question',
        ),
        subnet=dict(
            type='str', required=False,
            description='Subnet this reservation belongs to',
        ),
        hostname=dict(
            type='str', required=False,
            description='Offer a hostname to the client',
        ),
        description=dict(type='str', required=False, aliases=['desc']),
        ipv=dict(type='int', required=False, default=4, choices=[4, 6], aliases=['ip_version']),
        **RELOAD_MOD_ARG,
        **STATE_MOD_ARG,
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
    )

    if module.params['ipv'] == 6:
        module.fail_json('DHCPv6 is not yet supported!')

    module_wrapper(ReservationV4(module=module, result=result))
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
