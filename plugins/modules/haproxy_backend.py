#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (C) 2025, MaximeWewer
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

# see: https://docs.opnsense.org/development/api/plugins/haproxy.html

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.handler import \
    module_dependency_error, MODULE_EXCEPTIONS

try:
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.wrapper import module_wrapper
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.defaults.main import \
        OPN_MOD_ARGS, STATE_MOD_ARG, RELOAD_MOD_ARG
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.main.haproxy_backend import HaproxyBackend

except MODULE_EXCEPTIONS:
    module_dependency_error()


# DOCUMENTATION = 'https://ansible-opnsense.oxl.app/modules/haproxy.html'
# EXAMPLES = 'https://ansible-opnsense.oxl.app/modules/haproxy.html'


def run_module():
    module_args = dict(
        name=dict(
            type='str', required=True,
            description='Name to identify this Backend Pool.'
        ),
        description=dict(
            type='str', required=False,
            description='Description for this Backend Pool.'
        ),
        mode=dict(
            type='str', required=False, default='http',
            choices=['http', 'tcp'],
            description='Set the running mode or protocol of the Backend Pool.'
        ),
        algorithm=dict(
            type='str', required=False, default='source',
            choices=['source', 'roundrobin', 'static-rr', 'leastconn', 'uri', 'random'],
            description='Define the load balancing algorithm to be used in a Backend Pool.'
        ),
        random_draws=dict(
            type='int', required=False, default=2,
            description='Number of draws before selecting the least loaded server (Random algorithm).'
        ),
        proxy_protocol=dict(
            type='str', required=False, default=None,
            choices=['v1', 'v2'],
            description='Enforces use of the PROXY protocol over any connection established to the configured servers.'
        ),
        linked_servers=dict(
            type='list', elements='str', required=False, default=[],
            description='Add servers to this backend.'
        ),
        linked_fcgi=dict(
            type='str', required=False, default=None,
            description='Select the FastCGI application that should be used for all servers in this backend.'
        ),
        linked_resolver=dict(
            type='str', required=False, default=None,
            description='Select the custom resolver configuration that should be used for all servers in this backend.'
        ),
        resolver_opts=dict(
            type='list', elements='str', required=False, default=[],
            choices=['allow-dup-ip', 'ignore-weight', 'prevent-dup-ip'],
            description='Add resolver options.'
        ),
        resolve_prefer=dict(
            type='str', required=False, default=None,
            choices=['ipv4', 'ipv6'],
            description='Preferred IP family when DNS returns multiple addresses (ipv4/ipv6).'
        ),
        source=dict(
            type='str', required=False, default=None,
            description='Sets the source address which will be used when connecting to the server(s).'
        ),
        health_check_enabled=dict(
            type='bool', required=False, default=True,
            description='Enable or disable health checking.'
        ),
        health_check=dict(
            type='str', required=False, default=None,
            description='Select Health Monitor for servers in this backend.'
        ),
        health_check_log_status=dict(
            type='bool', required=False, default=False,
            description='Enable to log health check status updates.'
        ),
        check_interval=dict(
            type='str', required=False, default=None,
            description='Sets the interval for running health checks on all configured servers.'
        ),
        check_down_interval=dict(
            type='str', required=False, default=None,
            description='Health check interval when server is DOWN.'
        ),
        health_check_fall=dict(
            type='int', required=False, default=None,
            description='Consecutive failed health checks before server is marked unavailable.'
        ),
        health_check_rise=dict(
            type='int', required=False, default=None,
            description='The number of consecutive successful health checks before a server is considered as available.'
        ),
        linked_mailer=dict(
            type='str', required=False, default=None,
            description='Select an e-mail alert configuration.'
        ),
        http2_enabled=dict(
            type='bool', required=False, default=True,
            description='Enable support for end-to-end HTTP/2 communication.'
        ),
        http2_enabled_nontls=dict(
            type='bool', required=False, default=False,
            description='Enable support for HTTP/2 even if TLS is not enabled.'
        ),
        ba_advertised_protocols=dict(
            type='list', elements='str', required=False, default=['h2', 'http11'],
            choices=['h2', 'http11', 'http10'],
            description='Protocols advertised via TLS ALPN extension.'
        ),
        forwarded_header=dict(
            type='bool', required=False, default=False,
            description='Enable insertion of the RFC7239 forwarded header in requests sent to servers.'
        ),
        forwarded_header_parameters=dict(
            type='list', elements='str', required=False, default=[],
            choices=['proto', 'host', 'for', 'by'],
            description='Select which parameters to include in the forwarded header.'
        ),
        forward_for=dict(
            type='bool', required=False, default=False,
            description='Enable insertion of the X-Forwarded-For header to requests sent to servers.'
        ),
        persistence=dict(
            type='str', required=False, default=None,
            choices=['sticktable', 'cookie'],
            description='Choose how HAProxy should track user-to-server mappings.'
        ),
        persistence_cookiemode=dict(
            type='str', required=False, default='piggyback',
            choices=['piggyback', 'new'],
            description='Cookie handling mode for persistence.'
        ),
        persistence_cookiename=dict(
            type='str', required=False, default=None,
            description='Cookie name to use for persistence.'
        ),
        persistence_stripquotes=dict(
            type='bool', required=False, default=False,
            description='Enable to automatically strip quotes from the cookie value.'
        ),
        stickiness_pattern=dict(
            type='str', required=False, default=None,
            description='Choose a request pattern to associate a user to a server.'
        ),
        stickiness_data_types=dict(
            type='list', elements='str', required=False, default=None,
            description='This is used to store additional information in the stick-table.'
        ),
        stickiness_expire=dict(
            type='str', required=False, default='30m',
            description='Maximum duration of an entry in the stick-table.'
        ),
        stickiness_size=dict(
            type='str', required=False, default='50k',
            description='Maximum number of entries that can fit in the table.'
        ),
        stickiness_cookiename=dict(
            type='str', required=False, default=None,
            description='Cookie name to use for stick table.'
        ),
        stickiness_cookielength=dict(
            type='int', required=False, default=None,
            description='The maximum number of characters that will be stored in the stick table.'
        ),
        stickiness_conn_rate_period=dict(
            type='str', required=False, default='10s',
            description='Rate period for connection rate tracking in stick table.'
        ),
        stickiness_sess_rate_period=dict(
            type='str', required=False, default='10s',
            description='Rate period for session rate tracking in stick table.'
        ),
        stickiness_http_req_rate_period=dict(
            type='str', required=False, default='10s',
            description='Rate period for HTTP request rate tracking in stick table.'
        ),
        stickiness_http_err_rate_period=dict(
            type='str', required=False, default='10s',
            description='Rate period for HTTP error rate tracking in stick table.'
        ),
        stickiness_bytes_in_rate_period=dict(
            type='str', required=False, default='1m',
            description='Rate period for bytes in rate tracking in stick table.'
        ),
        stickiness_bytes_out_rate_period=dict(
            type='str', required=False, default='1m',
            description='Rate period for bytes out rate tracking in stick table.'
        ),
        basic_auth_enabled=dict(
            type='bool', required=False, default=False,
            description='Enable HTTP Basic Authentication.'
        ),
        basic_auth_users=dict(
            type='list', elements='str', required=False, default=[],
            description='Allowed users for Basic Authentication.'
        ),
        basic_auth_groups=dict(
            type='list', elements='str', required=False, default=[],
            description='Allowed groups for Basic Authentication.'
        ),
        tuning_timeout_connect=dict(
            type='str', required=False, default=None,
            description='Set the maximum time to wait for a connection attempt to a server to succeed.'
        ),
        tuning_timeout_check=dict(
            type='str', required=False, default=None,
            description='Sets an additional read timeout for running health checks on a server.'
        ),
        tuning_timeout_server=dict(
            type='str', required=False, default=None,
            description='Set the maximum inactivity time on the server side.'
        ),
        tuning_retries=dict(
            type='int', required=False, default=None,
            description='Set the number of retries to perform on a server after a connection failure.'
        ),
        custom_options=dict(
            type='str', required=False, default=None,
            description='These lines will be added to the HAProxy backend configuration.'
        ),
        tuning_defaultserver=dict(
            type='str', required=False, default=None,
            description='Default option for all server entries.'
        ),
        tuning_noport=dict(
            type='bool', required=False, default=False,
            description='Do not use port on server, use the same port as frontend receive.'
        ),
        tuning_httpreuse=dict(
            type='str', required=False, default=None,
            choices=['never', 'safe', 'aggressive', 'always'],
            description='Declare how idle HTTP connections may be shared between requests.'
        ),
        tuning_caching=dict(
            type='bool', required=False, default=False,
            description='Enable caching of responses from this backend.'
        ),
        linked_actions=dict(
            type='list', elements='str', required=False, default=[],
            description='Choose rules to be included in this Backend Pool.'
        ),
        linked_errorfiles=dict(
            type='list', elements='str', required=False, default=[],
            description='Choose error messages to be included in this Backend Pool.'
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
        required_if=[
            # When persistence is set to cookie, cookiemode is required
            ('persistence', 'cookie', ('persistence_cookiemode',)),
            # When persistence is set to sticktable, stickiness fields are required
            ('persistence', 'sticktable', ('stickiness_expire', 'stickiness_size')),
            # When using stickiness pattern, these fields are required
            ('stickiness_pattern', 'src', ('stickiness_expire', 'stickiness_size')),
            ('stickiness_pattern', 'src_ipv4', ('stickiness_expire', 'stickiness_size')),
            ('stickiness_pattern', 'src_ipv6', ('stickiness_expire', 'stickiness_size')),
            ('stickiness_pattern', 'dst', ('stickiness_expire', 'stickiness_size')),
            ('stickiness_pattern', 'dst_ipv4', ('stickiness_expire', 'stickiness_size')),
            ('stickiness_pattern', 'dst_ipv6', ('stickiness_expire', 'stickiness_size')),
        ],
    )

    module_wrapper(HaproxyBackend(module=module, result=result))
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
