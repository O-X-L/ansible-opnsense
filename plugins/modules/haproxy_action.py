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
        OPN_MOD_ARGS, STATE_MOD_ARG, RELOAD_MOD_ARG
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.haproxy_action import HaproxyAction

except MODULE_EXCEPTIONS:
    module_dependency_error()


# DOCUMENTATION = 'https://ansible-opnsense.oxl.app/modules/haproxy.html'
# EXAMPLES = 'https://ansible-opnsense.oxl.app/modules/haproxy.html'


def run_module():
    module_args = dict(
        name=dict(
            type='str', required=True,
            description='Name to identify this rule'
        ),
        description=dict(
            type='str', required=False, default=None,
            description='Description for this rule'
        ),
        test_type=dict(
            type='str', required=False, default=None,
            description='Choose how to test. By using IF it tests if the condition evaluates to true'
        ),
        linked_acls=dict(
            type='list', required=False, default=None,
            description='Select one or more conditions to be used for this rule'
        ),
        operator=dict(
            type='str', required=False, default=None,
            description='Choose a logical operator'
        ),
        type=dict(
            type='str', required=False, default=None,
            description='Choose a HAProxy function that should be executed if the condition evaluates to true'
        ),
        use_backend=dict(
            type='str', required=False, default=None,
            description='HAProxy will use this backend pool if the condition evaluates to true'
        ),
        use_server=dict(
            type='str', required=False, default=None,
            description='HAProxy will use this server instead of other servers that are specified in the Backend Pool'
        ),
        custom_rule=dict(
            type='str', required=False, default=None,
            description='Custom rule (option pass-through)'
        ),
        # FastCGI fields
        fcgi_pass_header=dict(
            type='str', required=False, default=None,
            description='FastCGI pass-header'
        ),
        fcgi_set_param=dict(
            type='str', required=False, default=None,
            description='FastCGI set-param'
        ),
        # HTTP Request fields
        http_request_auth=dict(
            type='str', required=False, default=None,
            description='HTTP request auth realm'
        ),
        http_request_redirect=dict(
            type='str', required=False, default=None,
            description='HTTP request redirect location'
        ),
        http_request_lua=dict(
            type='str', required=False, default=None,
            description='HTTP request lua action'
        ),
        http_request_use_service=dict(
            type='str', required=False, default=None,
            description='HTTP request lua service'
        ),
        # HTTP Request Header Add
        http_request_add_header_name=dict(
            type='str', required=False, default=None,
            description='HTTP request header name to add'
        ),
        http_request_add_header_content=dict(
            type='str', required=False, default=None,
            description='HTTP request header content to add'
        ),
        # HTTP Request Header Set
        http_request_set_header_name=dict(
            type='str', required=False, default=None,
            description='HTTP request header name to set'
        ),
        http_request_set_header_content=dict(
            type='str', required=False, default=None,
            description='HTTP request header content to set'
        ),
        # HTTP Request Header Delete
        http_request_del_header_name=dict(
            type='str', required=False, default=None,
            description='HTTP request header name to delete'
        ),
        # HTTP Request Set Path
        http_request_set_path=dict(
            type='str', required=False, default=None,
            description='HTTP request set-path value'
        ),
        # HTTP Request Set Variable
        http_request_set_var_scope=dict(
            type='str', required=False, default=None,
            description='HTTP request set-var scope (proc/sess/txn/req/res)'
        ),
        http_request_set_var_name=dict(
            type='str', required=False, default=None,
            description='HTTP request set-var name'
        ),
        http_request_set_var_expr=dict(
            type='str', required=False, default=None,
            description='HTTP request set-var expression'
        ),
        # HTTP Response fields
        http_response_lua=dict(
            type='str', required=False, default=None,
            description='HTTP response lua script'
        ),
        http_response_set_status_code=dict(
            type='int', required=False, default=None,
            description='HTTP response status code (100-999)'
        ),
        http_response_set_status_reason=dict(
            type='str', required=False, default=None,
            description='HTTP response status reason'
        ),
        # TCP fields
        tcp_request_content_lua=dict(
            type='str', required=False, default=None,
            description='TCP request content lua script'
        ),
        tcp_request_inspect_delay=dict(
            type='str', required=False, default=None,
            description='TCP request inspect-delay'
        ),
        tcp_response_content_lua=dict(
            type='str', required=False, default=None,
            description='TCP response content lua script'
        ),
        tcp_response_inspect_delay=dict(
            type='str', required=False, default=None,
            description='TCP response inspect-delay'
        ),
        # Monitor fail
        monitor_fail_uri=dict(
            type='str', required=False, default=None,
            description='Monitor fail URI'
        ),
        # Map use backend
        map_use_backend_file=dict(
            type='str', required=False, default=None,
            description='Map file for backend selection'
        ),
        map_use_backend_default=dict(
            type='str', required=False, default=None,
            description='Default backend for map-based selection'
        ),
        **STATE_MOD_ARG,
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

    module_wrapper(HaproxyAction(module=module, result=result))

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()