#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (C) 2025, Pascal Rath <contact+opnsense@OXL.at>
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

# see: https://docs.opnsense.org/development/api/plugins/quagga.html

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.handler import \
    module_dependency_error, MODULE_EXCEPTIONS

try:
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.defaults.main import \
        OPN_MOD_ARGS, STATE_MOD_ARG, RELOAD_MOD_ARG

except MODULE_EXCEPTIONS:
    module_dependency_error()


# DOCUMENTATION = 'https://ansible-opnsense.oxl.app/modules/frr_ospf.html'
# EXAMPLES = 'https://ansible-opnsense.oxl.app/modules/frr_ospf.html'


def run_module():
    module_args = dict(
        ip=dict(type='str', required=True, aliases=['nw_address', 'network_address', 'address']),
        mask=dict(type='int', required=True, aliases=['nw_mask', 'network_mask']),
        area=dict(
            type='str', required=False,
            description='Area in dotted-quad format (A.B.C.D) like 0.0.0.0, not in decimal format (0). '
                        'Only use Area in Interface tab or in Network tab once'
        ),
        area_range=dict(
            type='str', required=False,
            description='Here you can summarize a network for this area like fe80:1234::/56'
        ),
        prefix_list_in=dict(
            type='str', required=False, aliases=['prefix_in', 'pre_in']
        ),
        prefix_list_out=dict(
            type='str', required=False, aliases=['prefix_out', 'pre_out']
        ),
        match_fields=dict(
            type='list', required=False, elements='str',
            description='Fields that are used to match configured network with the running config - '
                        "if any of those fields are changed, the module will think it's a new entry",
            choices=['ip', 'mask', 'area', 'area_range'],
            default=['ip', 'mask'],
        ),
        **STATE_MOD_ARG,
        **RELOAD_MOD_ARG,
        **OPN_MOD_ARGS,
    )

    AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
    ).fail_json(
        'This module was removed as OPNsense 26.7 (os-frr 2.0) dropped OSPFv3 networks, '
        'FRR does not support assigning IPv6 prefixes to OSPFv3 areas with a router-level network command. '
        "Assign the area to the interface instead (module 'frr_ospf3_interface'). "
        'See: https://github.com/opnsense/plugins/pull/5751'
    )


def main():
    run_module()


if __name__ == '__main__':
    main()
