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
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.main.haproxy_server import HaproxyServer

except MODULE_EXCEPTIONS:
    module_dependency_error()


# DOCUMENTATION = 'https://ansible-opnsense.oxl.app/modules/haproxy.html'
# EXAMPLES = 'https://ansible-opnsense.oxl.app/modules/haproxy.html'


def run_module():
    module_args = dict(
        name=dict(
            type='str', required=True,
            description='Name to identify this Server.'
        ),
        description=dict(
            type='str', required=False, default=None,
            description='Description for this Server.'
        ),
        address=dict(
            type='str', required=False, default=None,
            description='Servername or IP address of the server.'
        ),
        port=dict(
            type='int', required=False, default=None,
            description='Port number of the server.'
        ),
        checkport=dict(
            type='int', required=False, default=None,
            description='Port number for health checks.'
        ),
        mode=dict(
            type='str', required=False, default='active',
            choices=['active', 'backup', 'disabled'],
            description='Set the server mode.'
        ),
        multiplexer_protocol=dict(
            type='str', required=False, default='unspecified',
            choices=['unspecified', 'fcgi', 'h2', 'h1'],
            description='Protocol for multiplexing.'
        ),
        type=dict(
            type='str', required=False, default='static',
            choices=['static', 'template', 'unix'],
            description='Server type.'
        ),
        service_name=dict(
            type='str', required=False, default=None,
            description='Service name for DNS SRV record discovery.'
        ),
        number=dict(
            type='str', required=False, default=None,
            description='Server number or range for template servers.'
        ),
        linked_resolver=dict(
            type='str', required=False, default=None,
            description='Select resolver configuration for this server.'
        ),
        resolver_opts=dict(
            type='list', elements='str', required=False, default=[],
            choices=['allow-dup-ip', 'ignore-weight', 'prevent-dup-ip'],
            description='Add resolver options.'
        ),
        resolve_prefer=dict(
            type='str', required=False, default=None,
            choices=['ipv4', 'ipv6'],
            description='Prefer IP family for DNS resolution.'
        ),
        ssl_enabled=dict(
            type='bool', required=False, default=False,
            description='Enable SSL for this server.'
        ),
        ssl_verify_cert=dict(
            type='bool', required=False, default=True,
            description='Enable SSL certificate verification.'
        ),
        ssl_ca=dict(
            type='list', elements='str', required=False, default=[],
            description='Certificate Authorities for SSL verification.'
        ),
        ssl_crl=dict(
            type='str', required=False, default=None,
            description='Certificate Revocation List for SSL verification.'
        ),
        ssl_client_certificate=dict(
            type='str', required=False, default=None,
            description='Client certificate for SSL authentication.'
        ),
        ssl_sni=dict(
            type='str', required=False, default=None,
            description='SNI hostname for SSL connections.'
        ),
        max_connections=dict(
            type='int', required=False, default=None,
            description='Maximum connections to this server.'
        ),
        weight=dict(
            type='int', required=False, default=None,
            description='Weight of the server for load balancing.'
        ),
        check_interval=dict(
            type='str', required=False, default=None,
            description='Interval between health checks.'
        ),
        check_down_interval=dict(
            type='str', required=False, default=None,
            description='Interval between health checks when server is down.'
        ),
        source=dict(
            type='str', required=False, default=None,
            description='Source address to use when connecting to this server.'
        ),
        advanced=dict(
            type='str', required=False, default=None,
            description='Advanced server options.'
        ),
        unix_socket=dict(
            type='str', required=False, default=None,
            description='Unix socket frontend for this server.'
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

    module_wrapper(HaproxyServer(module=module, result=result))
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
