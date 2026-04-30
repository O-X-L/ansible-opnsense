#!/usr/bin/python
# -*- coding: utf-8 -*-

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.handler import \
    module_dependency_error, MODULE_EXCEPTIONS

try:
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.wrapper import module_wrapper
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.defaults.main import \
        OPN_MOD_ARGS, STATE_ONLY_MOD_ARG, RELOAD_MOD_ARG
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.main.tunable import Tunable

except MODULE_EXCEPTIONS:
    module_dependency_error()


def run_module():
    module_args = dict(
        tunable=dict(
            type='str', required=True, description='Tunable name',
        ),
        description=dict(type='str', required=False, aliases=['descr']),
        value=dict(
            type='int', required=True, aliases=['val'],
        ),
        default_value=dict(
            type='int', required=False, aliases=['default', 'def_val'],
        ),
        type=dict(
            type='str', required=False, elements='str', choices=['', 'w', 't'], default='',
            description="Type of tunable. Can be the following values: Runtime('w'), Boot-time('t'), Environment('').",
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

    if not module.params.get('default_value'):
        module.params['default_value'] = module.params.get('value')

    module_wrapper(Tunable(module=module, result=result))
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
