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
        OPN_MOD_ARGS, STATE_ONLY_MOD_ARG
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.main.dnsmasq_option import Option

except MODULE_EXCEPTIONS:
    module_dependency_error()


# DOCUMENTATION = 'https://ansible-opnsense.oxl.app/modules/dnsmasq.html'
# EXAMPLES = 'https://ansible-opnsense.oxl.app/modules/dnsmasq.html'


def run_module():
    module_args = dict(
        description=dict(
            type='str', required=True, aliases=['desc'],
            description='DHCP option description.',
        ),
        type=dict(
            type='str', required=False, options=['set', 'match'], default='set',
            description='"Set" to send it to a client in a DHCP offer or '
                        '"Match" to dynamically tag clients that send it in the initial DHCP request.',
        ),
        option=dict(
            type='int', required=False,
            description='DHCPv4 option to offer to the client.',
        ),
        option6=dict(
            type='int', required=False,
            description='DHCPv6 option to offer to the client.',
        ),
        interface=dict(
            type='str', required=False, aliases=['int'],
            description='Interface this options is set for.',
        ),
        tag=dict(
            type='list', elements='str', required=False, default=[], aliases=['t'],
            description='DHCP option is only sent when all the tags do match.',
        ),
        set_tag=dict(
            type='str', required=False,
            description='Tag to set for matching requests.',
        ),
        value=dict(
            type='str', required=False,
            description='Value (or values) to send to the client. '
                        'When using "Match", leave empty to match on the option only.',
        ),
        force=dict(
            type='bool', required=False, default=False,
            description='Always send the option, also when the client does not ask for it.',
        ),
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
            ('state', 'present', ('option', 'option6'), True),
        ]
    )

    module_wrapper(Option(module=module, result=result))
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
