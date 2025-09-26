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
        OPN_MOD_ARGS, RELOAD_MOD_ARG
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.haproxy_general_defaults import GeneralDefaults

except MODULE_EXCEPTIONS:
    module_dependency_error()


# DOCUMENTATION = 'https://ansible-opnsense.oxl.app/modules/haproxy.html'
# EXAMPLES = 'https://ansible-opnsense.oxl.app/modules/haproxy.html'


def run_module():
    module_args = dict(
        max_connections=dict(
            type='int', required=False, default=None,
            description='Set the maximum number of concurrent connections for public services'
        ),
        max_connections_servers=dict(
            type='int', required=False, default=None,
            description='Set the maximum number of concurrent connections for servers'
        ),
        timeout_client=dict(
            type='str', required=False, default='30s',
            description='Set the maximum inactivity time on the client side. Defaults to milliseconds'
        ),
        timeout_connect=dict(
            type='str', required=False, default='30s',
            description='Set the maximum time to wait for a connection attempt to a server to succeed'
        ),
        timeout_check=dict(
            type='str', required=False, default=None,
            description='Sets an additional read timeout for running health checks on a server'
        ),
        timeout_server=dict(
            type='str', required=False, default='30s',
            description='Set the maximum inactivity time on the server side. Defaults to milliseconds'
        ),
        retries=dict(
            type='int', required=False, default=3,
            description='Set the number of retries to perform on a server after a connection failure'
        ),
        redispatch=dict(
            type='str', required=False, default='x-1',
            choices=['x3', 'x2', 'x1', 'x0', 'x-1', 'x-2', 'x-3'],
            description='Enable or disable session redistribution in case of connection failure'
        ),
        init_addr=dict(
            type='list', elements='str', required=False, default=['last', 'libc'],
            description='Indicates in which order server addresses should be resolved upon startup'
        ),
        custom_options=dict(
            type='str', required=False, default=None,
            description='These lines will be added to the defaults settings of to the HAProxy configuration file'
        ),
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

    module_wrapper(GeneralDefaults(module=module, result=result))

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
