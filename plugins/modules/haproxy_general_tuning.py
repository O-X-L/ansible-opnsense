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
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.haproxy_general_tuning import GeneralTuning

except MODULE_EXCEPTIONS:
    module_dependency_error()


# DOCUMENTATION = 'https://ansible-opnsense.oxl.app/modules/haproxy.html'
# EXAMPLES = 'https://ansible-opnsense.oxl.app/modules/haproxy.html'


def run_module():
    module_args = dict(
        root=dict(
            type='bool', required=False, default=False,
            description='Enable or disable HAProxy running as user root. Enabling this option is strongly discouraged'
        ),
        max_connections=dict(
            type='int', required=False, default=None,
            description='Sets the maximum number of concurrent connections per HAProxy process'
        ),
        nbthread=dict(
            type='int', required=False, default=1,
            description='Number of threads to create for each HAProxy process'
        ),
        resolvers_prefer=dict(
            type='str', required=False, default='ipv4',
            choices=['ipv4', 'ipv6'],
            description='Choose which IP family is preferred when resolving DNS names'
        ),
        ssl_server_verify=dict(
            type='str', required=False, default='ignore',
            choices=['ignore', 'required', 'none'],
            description='Enforces behavior for SSL verify on servers, ignoring per-server settings'
        ),
        max_dh_size=dict(
            type='int', required=False, default=2048,
            description='Sets the maximum size of Diffie-Hellman parameters for ephemeral/temporary key exchange'
        ),
        buffer_size=dict(
            type='int', required=False, default=16384,
            description='Change the buffer size in bytes, affecting session coexistence and memory usage'
        ),
        spread_checks=dict(
            type='int', required=False, default=2,
            description='Add randomness in the check interval between 0 and +/- 50%'
        ),
        bogus_proxy_enabled=dict(
            type='bool', required=False, default=False,
            description='Disables support for HAProxy PROXY protocol in bogus header'
        ),
        lua_max_mem=dict(
            type='int', required=False, default=0,
            description='Sets maximum RAM in megabytes per process usable by Lua'
        ),
        custom_options=dict(
            type='str', required=False, default=None,
            description='Custom HAProxy options to add to global section'
        ),
        ocsp_update_enabled=dict(
            type='bool', required=False, default=False,
            description='Enable automatic OCSP response updates at least once an hour'
        ),
        ocsp_update_min_delay=dict(
            type='int', required=False, default=300,
            description='Minimum delay in seconds between two OCSP updates'
        ),
        ocsp_update_max_delay=dict(
            type='int', required=False, default=3600,
            description='Maximum delay in seconds between two OCSP updates'
        ),
        ssl_defaults_enabled=dict(
            type='bool', required=False, default=False,
            description='Enable global SSL default values with configurable version and cipher options'
        ),
        ssl_bind_options=dict(
            type='list', elements='str', required=False, default=['prefer-client-ciphers'],
            description='SSL/TLS binding options'
        ),
        ssl_min_version=dict(
            type='str', required=False, default='TLSv1.2',
            choices=['SSLv3', 'TLSv1.0', 'TLSv1.1', 'TLSv1.2', 'TLSv1.3'],
            description='Minimum SSL/TLS version'
        ),
        ssl_max_version=dict(
            type='str', required=False, default=None,
            choices=['SSLv3', 'TLSv1.0', 'TLSv1.1', 'TLSv1.2', 'TLSv1.3'],
            description='Maximum SSL/TLS version'
        ),
        ssl_cipher_list=dict(
            type='str', required=False, default=None,
            description='SSL cipher list for TLSv1.2 and below'
        ),
        ssl_cipher_suites=dict(
            type='str', required=False, default=None,
            description='SSL cipher suites for TLSv1.3'
        ),
        h2_initial_window_size=dict(
            type='int', required=False, default=None,
            description='HTTP/2 initial window size'
        ),
        h2_initial_window_size_outgoing=dict(
            type='int', required=False, default=None,
            description='HTTP/2 initial window size for outgoing connections'
        ),
        h2_initial_window_size_incoming=dict(
            type='int', required=False, default=None,
            description='HTTP/2 initial window size for incoming connections'
        ),
        h2_max_concurrent_streams=dict(
            type='int', required=False, default=None,
            description='HTTP/2 maximum concurrent streams'
        ),
        h2_max_concurrent_streams_outgoing=dict(
            type='int', required=False, default=None,
            description='HTTP/2 maximum concurrent streams for outgoing connections'
        ),
        h2_max_concurrent_streams_incoming=dict(
            type='int', required=False, default=None,
            description='HTTP/2 maximum concurrent streams for incoming connections'
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

    module_wrapper(GeneralTuning(module=module, result=result))

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()