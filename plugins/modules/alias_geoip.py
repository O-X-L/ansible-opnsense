#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (C) 2026, Amir Zarinbal <zarinbal@gmail.com>
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.handler import \
    module_dependency_error, MODULE_EXCEPTIONS

try:
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.wrapper import module_wrapper
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.defaults.main import \
        OPN_MOD_ARGS, RELOAD_MOD_ARG
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.main.alias_geoip import GeoIP

except MODULE_EXCEPTIONS:
    module_dependency_error()

# DOCUMENTATION = 'https://ansible-opnsense.oxl.app/modules/alias_geoip.html'
# EXAMPLES = 'https://ansible-opnsense.oxl.app/modules/alias_geoip.html'


def run_module():
    module_args = dict(
        url=dict(
            type='str', required=True, no_log=True,
            description='Download-URL of the GeoIP database (p.e. MaxMind GeoLite2 Country CSV). '
                        'It commonly contains the credentials of the provider - so it is never shown in the '
                        'diff or result. Must use https if it carries credentials. '
                        'Set to an empty string to remove the source.',
        ),
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

    module_wrapper(GeoIP(module=module, result=result))
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
