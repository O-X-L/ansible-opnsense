#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (C) 2025, Pascal Rath <contact+opnsense@OXL.at>
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

# see: https://docs.opnsense.org/development/api/core/firewall.html

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.handler import \
    module_dependency_error, MODULE_EXCEPTIONS

try:
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.wrapper import \
        module_wrapper
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.defaults.main import \
        RELOAD_MOD_ARG_DEF_FALSE, OPN_MOD_ARGS
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.defaults.alias import \
        ALIAS_MOD_ARGS
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.main.alias import Alias

except MODULE_EXCEPTIONS:
    module_dependency_error()


# DOCUMENTATION = 'https://ansible-opnsense.oxl.app/modules/alias.html'
# EXAMPLES = 'https://ansible-opnsense.oxl.app/modules/alias.html'


def run_module():
    module_args = dict(
        **ALIAS_MOD_ARGS,
        **OPN_MOD_ARGS,
        **RELOAD_MOD_ARG_DEF_FALSE,  # default-true takes pretty long sometimes (urltables and so on)
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
        mutually_exclusive=[
            ('name', 'multi'), ('name', 'multi_purge'), ('name', 'multi_control.purge_all')
        ],
        required_one_of=[
            ('name', 'multi', 'multi_purge', 'multi_control.purge_all'),
        ],
    )

    result = dict(
        changed=False,
        diff={
            'before': {},
            'after': {},
        }
    )

    module_wrapper(Alias(module=module, result=result))
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
