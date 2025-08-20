#!/usr/bin/python

# Copyright: (C) 2025, MaximeWewer
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

"""Module to configure HAProxy frontends on OPNsense"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.handler import \
    module_dependency_error, MODULE_EXCEPTIONS

try:
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.wrapper import module_wrapper
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.defaults.main import \
        OPN_MOD_ARGS, EN_ONLY_MOD_ARG
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.haproxy_frontend import HaproxyFrontend

except MODULE_EXCEPTIONS:
    module_dependency_error()


# DOCUMENTATION = 'https://opnsense.ansibleguy.net/en/latest/modules/haproxy.html'
# EXAMPLES = 'https://opnsense.ansibleguy.net/en/latest/modules/haproxy.html'


def run_module():
    """Initiate module execution"""
    module_args = dict(
        name=dict(type='str', required=True),
        description=dict(type='str', required=False),
        bind_address=dict(type='str', required=True),
        bind_port=dict(type='int', required=True),
        ssl_enabled=dict(type='bool', required=False, default=False),
        ssl_certificates=dict(type='list', elements='str', required=False),
        default_backend=dict(type='str', required=False),
        linked_actions=dict(type='list', elements='str', required=False),
        linked_errorfiles=dict(type='list', elements='str', required=False),
        basic_auth_users=dict(type='list', elements='str', required=False),
        basic_auth_groups=dict(type='list', elements='str', required=False),
        mode=dict(
            type='str', required=False, default='http',
            choices=['http', 'tcp']
        ),
        max_connections=dict(type='int', required=False),
        log_enabled=dict(type='bool', required=False, default=False),
        advanced_options=dict(type='str', required=False),
        state=dict(type='str', default='present', choices=['present', 'absent']),
        **EN_ONLY_MOD_ARG,
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

    module_wrapper(HaproxyFrontend(module=module, result=result))

    module.exit_json(**result)


def main():
    """Module entry point"""
    run_module()


if __name__ == '__main__':
    main()