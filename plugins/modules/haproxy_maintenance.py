#!/usr/bin/python

# Copyright: (C) 2025, MaximeWewer
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

"""Module to perform HAProxy maintenance operations on OPNsense"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.handler import \
    module_dependency_error, MODULE_EXCEPTIONS

try:
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.wrapper import module_wrapper
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.defaults.main import \
        OPN_MOD_ARGS
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.haproxy_maintenance import HaproxyMaintenance

except MODULE_EXCEPTIONS:
    module_dependency_error()


# DOCUMENTATION = 'https://opnsense.ansibleguy.net/en/latest/modules/haproxy.html'
# EXAMPLES = 'https://opnsense.ansibleguy.net/en/latest/modules/haproxy.html'


def run_module():
    """Initiate module execution"""
    module_args = dict(
        action=dict(
            type='str', required=True,
            choices=[
                'cert_actions', 'cert_diff', 'cert_sync', 'cert_sync_bulk',
                'get', 'search_certificate_diff', 'search_server',
                'server_state', 'server_state_bulk', 'server_weight', 
                'server_weight_bulk', 'fetch_cron_integration', 'set'
            ]
        ),
        server=dict(type='str', required=False),
        state=dict(
            type='str', required=False,
            choices=['ready', 'drain', 'maint']
        ),
        weight=dict(type='int', required=False),
        **OPN_MOD_ARGS,
    )

    result = dict(
        changed=False,
        result={},
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
    )

    module_wrapper(HaproxyMaintenance(module=module, result=result))

    module.exit_json(**result)


def main():
    """Module entry point"""
    run_module()


if __name__ == '__main__':
    main()