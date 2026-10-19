#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (C) 2025, Pascal Rath <contact+opnsense@OXL.at>
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

# see: https://docs.opnsense.org/development/api/plugins/firewall.html

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.handler import \
    module_dependency_error, MODULE_EXCEPTIONS

try:
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.defaults.main import OPN_MOD_ARGS

except MODULE_EXCEPTIONS:
    module_dependency_error()

# DOCUMENTATION = 'https://ansible-opnsense.oxl.app/modules/savepoint.html'
# EXAMPLES = 'https://ansible-opnsense.oxl.app/modules/savepoint.html'


def run_module():
    module_args = dict(
        action=dict(
            type='str', required=False, default='create',
            choices=['create', 'revert', 'apply', 'cancel_rollback', 'cancel'],
        ),
        revision=dict(
            type='str', required=False,
            description='Savepoint revision to apply, revert or cancel_rollback'
        ),
        controller=dict(
            type='str', required=False, default='filter', description='Target API controller',
            choices=['source_nat', 'filter', 'one_to_one']
        ),
        api_module=dict(type='str', required=False, default='firewall', choices=['firewall']),
        **OPN_MOD_ARGS
    )

    AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
    ).fail_json(
        'This module was removed as OPNsense 26.7 dropped the firewall savepoint API '
        '(savepoint, revert, cancelRollback and the rollback timer of apply) without a replacement. '
        'See: https://github.com/opnsense/core/pull/10411'
    )


def main():
    run_module()


if __name__ == '__main__':
    main()
