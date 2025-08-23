#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (C) 2025, AnsibleGuy <guy@ansibleguy.net>
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

# see: https://docs.opnsense.org/development/api/core/auth.html

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.handler import \
    module_dependency_error, MODULE_EXCEPTIONS

try:
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.wrapper import module_wrapper
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.defaults.main import \
        OPN_MOD_ARGS, STATE_ONLY_MOD_ARG
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.group import Group

except MODULE_EXCEPTIONS:
    module_dependency_error()


# DOCUMENTATION = 'https://opnsense.ansibleguy.net/modules/auth.html'
# EXAMPLES = 'https://opnsense.ansibleguy.net/modules/auth.html'


def run_module():
    module_args = dict(
        name=dict(
            type='str', required=True, aliases=['n'],
            description='Group name',
        ),
        description=dict(type='str', required=False, aliases=['desc']),
        member=dict(
            type='list', required=False, aliases=['m'], elements='str',
        ),
        privilege=dict(
            type='list', required=False, aliases=['priv', 'p'], elements='str',
        ),
        source_net=dict(
            type='list', required=False, aliases=['source', 'src', 's'], elements='str', default=[],
            description='List of networks which constraint the membership of this group to their location.',
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
    )

    module_wrapper(Group(module=module, result=result))
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
