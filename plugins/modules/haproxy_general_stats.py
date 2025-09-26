#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (C) 2025, AnsibleGuy <guy@ansibleguy.net>
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

# see: https://docs.opnsense.org/development/api/plugins/haproxy.html

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.handler import \
    module_dependency_error, MODULE_EXCEPTIONS

try:
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.wrapper import module_wrapper
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.defaults.main import \
        OPN_MOD_ARGS, EN_ONLY_MOD_ARG, RELOAD_MOD_ARG
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.haproxy_general_stats import GeneralStats

except MODULE_EXCEPTIONS:
    module_dependency_error()


# DOCUMENTATION = 'https://ansible-opnsense.oxl.app/modules/haproxy.html'
# EXAMPLES = 'https://ansible-opnsense.oxl.app/modules/haproxy.html'


def run_module():
    module_args = dict(
        port=dict(
            type='int', required=False, default=8822,
            description='Choose a TCP port to be used for the local statistics page. The default value is 8822'
        ),
        remote_enabled=dict(
            type='bool', required=False, default=False,
            description='Enable remote access to HAProxy statistics page. This may be a security risk if authentication is not enabled'
        ),
        remote_bind=dict(
            type='list', elements='str', required=False, default=[],
            description='Configure listen addresses for the statistics page to enable remote access'
        ),
        auth_enabled=dict(
            type='bool', required=False, default=False,
            description='Enable authentication'
        ),
        users=dict(
            type='list', elements='str', required=False, default=[],
            description='Allowed users in format user:password'
        ),
        allowed_users=dict(
            type='list', elements='str', required=False, default=[],
            description='List of user names that are allowed to access the statistics page. User names will be automatically resolved to UUIDs'
        ),
        allowed_groups=dict(
            type='list', elements='str', required=False, default=[],
            description='List of group names that are allowed to access the statistics page. Group names will be automatically resolved to UUIDs'
        ),
        custom_options=dict(
            type='str', required=False, default=None,
            description='These lines will be added to the statistics settings of the HAProxy configuration file'
        ),
        prometheus_enabled=dict(
            type='bool', required=False, default=False,
            description='Enable HAProxy Prometheus exporter'
        ),
        prometheus_bind=dict(
            type='list', elements='str', required=False, default=['*:8404'],
            description='Configure listen addresses for the prometheus exporter'
        ),
        prometheus_path=dict(
            type='str', required=False, default='/metrics',
            description='The path where the Prometheus exporter can be accessed'
        ),
        **EN_ONLY_MOD_ARG,
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

    module_wrapper(GeneralStats(module=module, result=result))

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
