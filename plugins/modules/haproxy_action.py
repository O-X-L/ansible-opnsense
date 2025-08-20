#!/usr/bin/python

# Copyright: (C) 2025, MaximeWewer
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

"""Module to configure HAProxy actions on OPNsense"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.handler import \
    module_dependency_error, MODULE_EXCEPTIONS

try:
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.wrapper import module_wrapper
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.defaults.main import \
        OPN_MOD_ARGS, EN_ONLY_MOD_ARG
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.haproxy_action import HaproxyAction

except MODULE_EXCEPTIONS:
    module_dependency_error()


# DOCUMENTATION = 'https://opnsense.ansibleguy.net/en/latest/modules/haproxy.html'
# EXAMPLES = 'https://opnsense.ansibleguy.net/en/latest/modules/haproxy.html'


def run_module():
    """Initiate module execution"""
    module_args = dict(
        name=dict(type='str', required=True),
        description=dict(type='str', required=False),
        test_type=dict(
            type='str', required=False, default='if',
            choices=['if', 'unless']
        ),
        linked_acls=dict(type='list', elements='str', required=False),
        operator=dict(
            type='str', required=False, default='and',
            choices=['and', 'or']
        ),
        action_type=dict(
            type='str', required=True,
            choices=[
                'use_backend', 'use_server', 'map_use_backend',
                'http-request_allow', 'http-request_deny', 'http-request_auth',
                'http-request_redirect', 'http-request_lua', 'http-request_set-header',
                'http-request_del-header', 'http-request_replace-header',
                'http-response_allow', 'http-response_deny', 'http-response_set-header',
                'http-response_del-header', 'http-response_replace-header',
                'tcp-request_accept', 'tcp-request_reject', 'tcp-request_content_accept',
                'tcp-request_content_reject', 'tcp-request_connection_accept',
                'tcp-request_connection_reject',
                'tcp-response_accept', 'tcp-response_reject', 'tcp-response_content_accept',
                'tcp-response_content_reject',
                'fcgi_app', 'fcgi_docroot', 'fcgi_index',
                'monitor_fail', 'custom'
            ]
        ),
        use_backend=dict(type='str', required=False),
        use_server=dict(type='list', elements='str', required=False),
        http_request_auth=dict(type='str', required=False),
        http_request_redirect=dict(type='str', required=False),
        http_request_lua=dict(type='str', required=False),
        custom_lua=dict(type='str', required=False),
        map_use_backend_file=dict(type='str', required=False),
        map_use_backend_default=dict(type='str', required=False),
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

    module_wrapper(HaproxyAction(module, result))

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()