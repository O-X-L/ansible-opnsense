#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (C) 2026, Pablo1
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

# see: https://docs.opnsense.org/development/api/core/core.html

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.handler import \
    module_dependency_error, MODULE_EXCEPTIONS

try:
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.wrapper import module_wrapper
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.main.tunable import Tunable
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.defaults.main import \
        OPN_MOD_ARGS, STATE_ONLY_MOD_ARG, RELOAD_MOD_ARG_DEF_FALSE

except MODULE_EXCEPTIONS:
    module_dependency_error()


# DOCUMENTATION = 'https://ansible-opnsense.oxl.app/modules/tunable.html'
# EXAMPLES = 'https://ansible-opnsense.oxl.app/modules/tunable.html'


def run_module():
    module_args = dict(
        tunable=dict(
            type='str', required=True, aliases=['name', 'sysctl'],
            description='Name of the tunable, for example net.inet.ip.redirect. Used to match the entry.'
        ),
        value=dict(
            type='str', required=False,
            description='Value of the tunable. An empty string sets it back to the system default.'
        ),
        description=dict(
            type='str', required=False, aliases=['desc', 'descr'],
            description='Description of the tunable. If unset, the existing one is kept.'
        ),
        **RELOAD_MOD_ARG_DEF_FALSE,
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

    module_wrapper(Tunable(module=module, result=result))
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
