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
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.main.haproxy_healthcheck import HaproxyHealthcheck

except MODULE_EXCEPTIONS:
    module_dependency_error()


# DOCUMENTATION = 'https://ansible-opnsense.oxl.app/modules/haproxy.html'
# EXAMPLES = 'https://ansible-opnsense.oxl.app/modules/haproxy.html'


def run_module():
    module_args = dict(
        name=dict(
            type='str', required=True,
            description='Choose a name for this health monitor.'
        ),
        description=dict(
            type='str', required=False, default=None,
            description='Choose a optional description for this health monitor.'
        ),
        type=dict(
            type='str', required=False, default='http',
            choices=['tcp', 'http', 'agent', 'ldap', 'mysql', 'pgsql', 'redis', 'smtp', 'esmtp', 'ssl'],
            description='Choose the type of the health check.'
        ),
        interval=dict(
            type='str', required=False, default='2s',
            description='Interval between health checks (e.g. 2s, 500ms). Default: 2s.'
        ),
        ssl=dict(
            type='str', required=False, default='nopref',
            choices=['nopref', 'ssl', 'sslsni', 'nossl'],
            description='Force or disable SSL for health checks.'
        ),
        ssl_sni=dict(
            type='str', required=False, default=None,
            description='SNI hostname for SSL health checks.'
        ),
        checkport=dict(
            type='int', required=False, default=None,
            description='Port for health checks (overrides server port).'
        ),
        http_method=dict(
            type='str', required=False, default='options',
            choices=['options', 'head', 'get', 'put', 'post', 'delete', 'trace'],
            description='The HTTP method for the health check.'
        ),
        http_uri=dict(
            type='str', required=False, default=None,
            description='The URI that is requested for HTTP health checks.'
        ),
        http_version=dict(
            type='str', required=False, default='http10',
            choices=['http10', 'http11', 'http2'],
            description='The HTTP version for the health check.'
        ),
        http_host=dict(
            type='str', required=False, default='localhost',
            description='Insert a Host header with this value for HTTP health checks.'
        ),
        http_expression_enabled=dict(
            type='bool', required=False, default=False,
            description='Enable HTTP expression matching.'
        ),
        http_expression=dict(
            type='str', required=False, default=None,
            choices=['status', 'rstatus', 'string', 'rstring'],
            description='Type of HTTP expression matching.'
        ),
        http_negate=dict(
            type='bool', required=False, default=False,
            description='Negate the HTTP expression result.'
        ),
        http_value=dict(
            type='str', required=False, default=None,
            description='Value to match for HTTP expression.'
        ),
        tcp_enabled=dict(
            type='bool', required=False, default=False,
            description='Enable TCP send/expect functionality.'
        ),
        tcp_send_value=dict(
            type='str', required=False, default=None,
            description='The exact string that will be sent for binary/text based health checks.'
        ),
        tcp_match_type=dict(
            type='str', required=False, default='string',
            choices=['string', 'rstring', 'binary'],
            description='Type of TCP response matching.'
        ),
        tcp_negate=dict(
            type='bool', required=False, default=False,
            description='Negate the TCP match result.'
        ),
        tcp_match_value=dict(
            type='str', required=False, default=None,
            description='Value to match in TCP response.'
        ),
        agent_port=dict(
            type='int', required=False, default=None,
            description='The TCP port for agent checks.'
        ),
        mysql_user=dict(
            type='str', required=False, default=None,
            description='A MySQL username for health checks.'
        ),
        mysql_post41=dict(
            type='bool', required=False, default=False,
            description='Use MySQL post-4.1 authentication.'
        ),
        pgsql_user=dict(
            type='str', required=False, default=None,
            description='A PostgreSQL username for health checks.'
        ),
        smtp_domain=dict(
            type='str', required=False, default=None,
            description='SMTP domain for health checks.'
        ),
        esmtp_domain=dict(
            type='str', required=False, default=None,
            description='ESMTP domain for health checks.'
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

    module_wrapper(HaproxyHealthcheck(module=module, result=result))
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
