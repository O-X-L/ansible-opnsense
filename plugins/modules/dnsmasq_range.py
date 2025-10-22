#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (C) 2025, Pascal Rath <contact+opnsense@OXL.at>
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

# see: https://docs.opnsense.org/development/api/core/dnsmasq.html

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.handler import \
    module_dependency_error, MODULE_EXCEPTIONS

try:
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.wrapper import module_wrapper
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.defaults.main import \
        OPN_MOD_ARGS, STATE_ONLY_MOD_ARG, RELOAD_MOD_ARG
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.main.dnsmasq_range import Range

except MODULE_EXCEPTIONS:
    module_dependency_error()


# DOCUMENTATION = 'https://ansible-opnsense.oxl.app/modules/dnsmasq.html'
# EXAMPLES = 'https://ansible-opnsense.oxl.app/modules/dnsmasq.html'


def run_module():
    module_args = dict(
        description=dict(
            type='str', required=True, aliases=['desc'],
            description='DHCP range description.',
        ),
        interface=dict(
            type='str', required=False, aliases=['int'],
            description='Interface to serve this range.',
        ),
        set_tag=dict(
            type='str', required=False,
            description='Tag to set for matching requests.',
        ),
        start_addr=dict(
            type='str', required=False,
            description='Start of the range, e.g. 192.168.1.100 for DHCPv4, 2000::1 for DHCPv6.',
        ),
        end_addr=dict(
            type='str', required=False,
            description='End of the range.',
        ),
        subnet_mask=dict(
            type='str', required=False,
            description='Subnet mask of the range. Leave empty to auto-calculate the subnet mask.',
        ),
        constructor=dict(
            type='str', required=False,
            description='Interface to use to calculate a DHCPv6 or RA range.',
        ),
        mode=dict(
            type='list', elements='str', required=False,
            description='Mode flags to set for this range, "static" means no addresses will be automatically assigned.',
        ),
        prefix_len=dict(
            type='int', required=False, default=64,
            description='Prefix length offered to the client.',
        ),
        lease_time=dict(
            type='int', required=False, default=86400,
            description='Defines how long the addresses (leases) given out by the server are valid.',
        ),
        domain_type=dict(
            type='str', required=False, options=['interface', 'range'], default='range',
            description='If only clients in this range, or all clients in any subnets on the selected interface match.',
        ),
        domain=dict(
            type='str', required=False,
            description='Offer this domain to DHCP clients.',
        ),
        sync=dict(
            type='bool', required=False, default=True,
            description='Ignore this range from being transfered or updated by ha sync.',
        ),
        ra_mode=dict(
            type='list', elements='str', required=False,
            options=['ra-only', 'slaac', 'ra-names', 'ra-stateless', 'ra-advrouter', 'off-link'],
            description='Control how IPv6 clients receive their addresses.',
        ),
        ra_priority=dict(
            type='str', required=False, options=['', 'high', 'low'], default='',
            description='Priority of the RA announcements.',
        ),
        ra_mtu=dict(
            type='int', required=False,
            description='MTU to send to clients via Router Advertisements.',
        ),
        ra_interval=dict(
            type='int', required=False, default=60,
            description='Time (seconds) between Router Advertisements.',
        ),
        ra_router_lifetime=dict(
            type='int', required=False, default=1200,
            description='Lifetime of the route.',
        ),
        **STATE_ONLY_MOD_ARG,
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
    )

    module_wrapper(Range(module=module, result=result))
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
