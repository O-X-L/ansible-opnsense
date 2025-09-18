#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (C) 2025, Pascal Rath <contact+opnsense@OXL.at>
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

# see: https://docs.opnsense.org/development/api/plugins/firewall.html

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.handler import \
    module_dependency_error, MODULE_EXCEPTIONS

try:
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.utils import profiler
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.rule_purge import process
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import diff_remove_empty
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.defaults.legacy_multi import \
        PURGE_MOD_ARGS, INFO_MOD_ARG
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.defaults.main import \
        OPN_MOD_ARGS
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.defaults.rule import \
        RULE_MATCH_FIELDS_ARG, RULE_MOD_ARG_KEY_FIELD

except MODULE_EXCEPTIONS:
    module_dependency_error()


# DOCUMENTATION = 'https://ansible-opnsense.oxl.app/modules/rule_multi.html'
# EXAMPLES = 'https://ansible-opnsense.oxl.app/modules/rule_multi.html'


def run_module():
    module_args = dict(
        rules=dict(
            type='dict', required=False, default={},
            description='Configured rules - compared against existing ones'
        ),
        fail_all=dict(
            type='bool', required=False, default=False, aliases=['fail'],
            description='Fail module if single rule fails to be purged.'
        ),
        **PURGE_MOD_ARGS,
        **INFO_MOD_ARG,
        **RULE_MOD_ARG_KEY_FIELD,
        **RULE_MATCH_FIELDS_ARG,
        **OPN_MOD_ARGS,
    )

    AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
    ).fail_json('This module was deprecated in favor of: https://ansible-opnsense.oxl.app/modules/1_multi.html')


def main():
    run_module()


if __name__ == '__main__':
    main()
