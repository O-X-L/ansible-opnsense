#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (C) 2025, Pascal Rath <contact+opnsense@OXL.at>
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

# see: https://docs.opnsense.org/development/api/core/ids.html

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.handler import \
    module_dependency_error, MODULE_EXCEPTIONS

try:
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.wrapper import module_wrapper
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.defaults.main import \
        OPN_MOD_ARGS, STATE_MOD_ARG, RELOAD_MOD_ARG
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.main.ids_policy import Policy

except MODULE_EXCEPTIONS:
    module_dependency_error()


# DOCUMENTATION = 'https://ansible-opnsense.oxl.app/modules/ids.html'
# EXAMPLES = 'https://ansible-opnsense.oxl.app/modules/ids.html'


def run_module():
    module_args = dict(
        description=dict(type='str', required=True, aliases=['name', 'desc']),
        priority=dict(
            type='int', required=False, aliases=['prio'], default=0,
            description='Policies are processed on a first match basis a lower number means more important',
        ),
        rulesets=dict(
            type='list', elements='str', required=False, aliases=['rs'], default=[],
            description='Rulesets this policy applies to (all when none selected)',
        ),
        action=dict(
            type='list', elements='str', required=False, aliases=['a'],
            choices=['disable', 'alert', 'drop'],
            description='Rule configured action',
        ),
        new_action=dict(
            type='str', required=False, aliases=['na'], default='alert',
            choices=['default', 'disable', 'alert', 'drop'],
            description='Action to perform when filter policy applies',
        ),
        rules=dict(
            type='dict', required=False,
            description="Key-value pairs of policy-rules as provided by the enabled rulesets. "
                        "Values must be string or lists. Example: "
                        "'{\"rules\": {\"signature_severity\": [\"Minor\", \"Major\"], \"tag\": \"Dshield\"}}'",
        ),
        **RELOAD_MOD_ARG,
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

    module_wrapper(Policy(module=module, result=result))
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
