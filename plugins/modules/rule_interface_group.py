#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (C) 2024, AnsibleGuy <guy@ansibleguy.net>
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

# see: https://docs.opnsense.org/development/api/core/firewall.html

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.handler import \
    module_dependency_error, MODULE_EXCEPTIONS

try:
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.wrapper import module_wrapper
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.defaults.main import \
        OPN_MOD_ARGS, STATE_ONLY_MOD_ARG, RELOAD_MOD_ARG
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.rule_interface_group import Group

except MODULE_EXCEPTIONS:
    module_dependency_error()


# DOCUMENTATION = 'https://opnsense.ansibleguy.net/en/latest/modules/rule_interface_group.html'
# EXAMPLES = 'https://opnsense.ansibleguy.net/en/latest/modules/rule_interface_group.html'


def run_module():
    module_args = dict(
        name=dict(
            type='str', required=True, aliases=['ifname'],
            description='Name of the interface group. Only texts containing letters, '
                        'digits and underscores with a maximum length of 15 characters '
                        'are allowed and the name may not end with a digit.',
        ),
        members=dict(
            type='list', elements='str', required=False, aliases=['ints', 'interfaces'],
            description='Member interfaces - you must provide the network '
                        "port as shown in 'Interfaces - Assignments - Network port'"
        ),
        gui_group=dict(
            type='bool', required=False, aliases=['gui'], default=True,
            description='Grouping these members in the interfaces menu section'
        ),
        sequence=dict(
            type='int', required=False, default=0, aliases=['seq'],
            description='Priority sequence used in sorting the groups '
        ),
        description=dict(type='str', required=False, aliases=['desc']),
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

    module_wrapper(Group(module=module, result=result))
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
