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
        OPN_MOD_ARGS, STATE_MOD_ARG
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.user import User

except MODULE_EXCEPTIONS:
    module_dependency_error()


# DOCUMENTATION = 'https://opnsense.ansibleguy.net/modules/auth.html'
# EXAMPLES = 'https://opnsense.ansibleguy.net/modules/auth.html'


def run_module():
    module_args = dict(
        name=dict(
            type='str', required=True, aliases=['n'],
            description='User name',
        ),
        expires=dict(
            type='str', required=False,
            description='Expiration date',
        ),
        authorized_keys=dict(
            type='str', required=False,
            description='SSH authorized keys',
        ),
        shell=dict(
            type='str', required=False, choises=['/bin/csh', '/bin/sh', '/bin/tcsh'],
            description='Login shell',
        ),
        password=dict(type='str', required=False, no_log=True),
        update_password=dict(
            type='str', required=False, choices=['always', 'on_create'], default='always',
            description='Update the password `always` or only `on_create`.',
        ),
        scrambled_password=dict(
            type='bool', required=False,
            description='Generate a scrambled password to prevent local database logins for this user',
        ),
        landing_page=dict(
            type='str', required=False,
            description='Preferred landing page after login or authentication failure',
        ),
        comment=dict(
            type='str', required=False,
            description='User comment, for your own information only',
        ),
        email=dict(
            type='str', required=False,
            description='Users e-mail address, for your own information only',
        ),
        language=dict(type='str', required=False),
        description=dict(
            type='str', required=False, aliases=['desc', 'full_name'],
            description='Full name of the user'
        ),
        membership=dict(
            type='list', required=False, aliases=['group', 'm', 'g'], elements='str',
        ),
        privilege=dict(
            type='list', required=False, aliases=['priv', 'p'], elements='str',
        ),
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

    module_wrapper(User(module=module, result=result))
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
