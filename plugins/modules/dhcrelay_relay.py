#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (C) 2025, Pascal Rath <contact+opnsense@OXL.at>
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

# see: https://docs.opnsense.org/development/api/core/dhcrelay.html

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.handler import \
    module_dependency_error, MODULE_EXCEPTIONS

try:
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.wrapper import module_wrapper
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.defaults.main import \
        OPN_MOD_ARGS, STATE_ONLY_MOD_ARG, RELOAD_MOD_ARG
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.main.dhcrelay_relay import DhcRelayRelay

except MODULE_EXCEPTIONS:
    module_dependency_error()


# DOCUMENTATION = 'https://ansible-opnsense.oxl.app/modules/dhcrelay_relay.html'
# EXAMPLES = 'https://ansible-opnsense.oxl.app/modules/dhcrelay_relay.html'


def run_module():
    module_args = dict(
        enabled=dict(
            type='bool', default=False,
            description='Enable or disable this relay.',
        ),
        interface=dict(
            type='str', required=True, aliases=['i', 'int'],
            description='The interface to relay DHCP requests from. '
        ),
        destination=dict(
            type='str', required=False, aliases=['dest'],
            description='The uuid of the destination server group to relay DHCP requests to.'
        ),
        agent_info=dict(
            type='bool', default=False,
            description='Add the relay agent information option.',
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
    )

    module_wrapper(DhcRelayRelay(module=module, result=result))
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
