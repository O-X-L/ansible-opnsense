#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (C) 2025, Pascal Rath <contact+opnsense@OXL.at>
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

# see: https://docs.opnsense.org/development/api/plugins/firewall.html

from ansible.module_utils.basic import AnsibleModule


from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.handler import \
    module_dependency_error, MODULE_EXCEPTIONS

try:
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.wrapper import \
        module_wrapper, is_multi_module_call, module_multi_wrapper
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.multi import \
        build_multi_mod_args
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.defaults.main import \
        RELOAD_MOD_ARG_DEF_FALSE, OPN_MOD_ARGS, STATE_MOD_ARG
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.defaults.rule import RULE_MOD_ARGS
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.rule import Rule

except MODULE_EXCEPTIONS:
    module_dependency_error()


# DOCUMENTATION = 'https://ansible-opnsense.oxl.app/modules/rule.html'
# EXAMPLES = 'https://ansible-opnsense.oxl.app/modules/rule.html'


def run_module():
    module_args = dict(
        **RULE_MOD_ARGS,
        **build_multi_mod_args(
           mod_args=RULE_MOD_ARGS,
           aliases=['rules']
        ),
    )

    result = dict(
        changed=False,
        diff={
            'before': {},
            'after': {},
        },
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
    )

    if is_multi_module_call(module):
        module_multi_wrapper(
            module=module,
            result=result,
            obj=Rule,
            kind='rule',
            module_args=module_args,
        )

    else:
        module_wrapper(Rule(module=module, result=result))

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
