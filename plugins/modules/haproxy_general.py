#!/usr/bin/python

# Copyright: (C) 2025, MaximeWewer
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

"""Module to configure HAProxy general settings on OPNsense"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.handler import \
    module_dependency_error, MODULE_EXCEPTIONS

try:
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.defaults.main import \
        OPN_MOD_ARGS, EN_ONLY_MOD_ARG
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.haproxy_general import HaproxyGeneral

except MODULE_EXCEPTIONS:
    module_dependency_error()


# DOCUMENTATION = 'https://opnsense.ansibleguy.net/en/latest/modules/haproxy.html'
# EXAMPLES = 'https://opnsense.ansibleguy.net/en/latest/modules/haproxy.html'


def run_module():
    """Initiate module execution"""
    module_args = dict(
        graceful_stop=dict(type='bool', required=False, default=False),
        hard_stop_after=dict(type='str', required=False, default='60s'),
        close_spread_time=dict(type='str', required=False),
        seamless_reload=dict(type='bool', required=False, default=False),
        show_intro=dict(type='bool', required=False, default=True),
        store_ocsp=dict(type='bool', required=False, default=False),
        tuning_max_connections=dict(type='int', required=False),
        tuning_nbthread=dict(type='int', required=False, default=1),
        tuning_resolvers_prefer=dict(
            type='str', required=False, default='ipv4',
            choices=['ipv4', 'ipv6']
        ),
        tuning_ssl_server_verify=dict(
            type='str', required=False, default='ignore',
            choices=['ignore', 'required']
        ),
        tuning_root=dict(type='bool', required=False, default=False),
        peers_enabled=dict(type='bool', required=False, default=False),
        peers_name1=dict(type='str', required=False),
        peers_listen1=dict(type='str', required=False),
        peers_port1=dict(type='int', required=False, default=1024),
        peers_name2=dict(type='str', required=False),
        peers_listen2=dict(type='str', required=False),
        peers_port2=dict(type='int', required=False, default=1024),
        # Additional tuning parameters
        tuning_max_dh_size=dict(type='int', required=False, default=2048),
        tuning_buffer_size=dict(type='int', required=False, default=16384),
        tuning_spread_checks=dict(type='int', required=False, default=2),
        tuning_bogus_proxy_enabled=dict(type='bool', required=False, default=False),
        tuning_lua_max_mem=dict(type='int', required=False, default=0),
        tuning_custom_options=dict(type='str', required=False),
        tuning_ocsp_update_enabled=dict(type='bool', required=False, default=False),
        tuning_ocsp_update_min_delay=dict(type='int', required=False, default=300),
        tuning_ocsp_update_max_delay=dict(type='int', required=False, default=3600),
        tuning_ssl_defaults_enabled=dict(type='bool', required=False, default=False),
        tuning_ssl_bind_options=dict(type='list', elements='str', required=False),
        tuning_ssl_min_version=dict(
            type='str', required=False, default='TLSv1.2',
            choices=['SSLv3', 'TLSv1.0', 'TLSv1.1', 'TLSv1.2', 'TLSv1.3']
        ),
        tuning_ssl_max_version=dict(
            type='str', required=False,
            choices=['SSLv3', 'TLSv1.0', 'TLSv1.1', 'TLSv1.2', 'TLSv1.3']
        ),
        # Defaults section parameters
        defaults_max_connections=dict(type='int', required=False),
        defaults_max_connections_servers=dict(type='int', required=False),
        defaults_timeout_client=dict(type='str', required=False, default='30s'),
        defaults_timeout_connect=dict(type='str', required=False, default='30s'),
        defaults_timeout_check=dict(type='str', required=False),
        defaults_timeout_server=dict(type='str', required=False, default='30s'),
        defaults_retries=dict(type='int', required=False, default=3),
        defaults_redispatch=dict(
            type='str', required=False, default='x-1',
            choices=['x3', 'x2', 'x1', 'x0', 'x-1', 'x-2', 'x-3']
        ),
        defaults_init_addr=dict(
            type='list', elements='str', required=False, 
            default=['last', 'libc']
        ),
        defaults_custom_options=dict(type='str', required=False),
        # Logging section parameters
        logging_host=dict(type='str', required=False, default='127.0.0.1'),
        logging_facility=dict(
            type='str', required=False, default='local0',
            choices=['alert', 'audit', 'auth2', 'auth', 'cron2', 'cron', 'daemon', 
                     'ftp', 'kern', 'local0', 'local1', 'local2', 'local3', 'local4',
                     'local5', 'local6', 'local7', 'lpr', 'mail', 'news', 'ntp',
                     'syslog', 'user', 'uucp']
        ),
        logging_level=dict(
            type='str', required=False, default='info',
            choices=['alert', 'crit', 'debug', 'emerg', 'err', 'info', 'notice', 'warning']
        ),
        logging_length=dict(type='int', required=False),
        # Stats section parameters
        stats_enabled=dict(type='bool', required=False, default=False),
        stats_port=dict(type='int', required=False, default=8822),
        stats_remote_enabled=dict(type='bool', required=False, default=False),
        stats_remote_bind=dict(type='list', elements='str', required=False),
        stats_auth_enabled=dict(type='bool', required=False, default=False),
        stats_users=dict(type='list', elements='str', required=False),
        stats_custom_options=dict(type='str', required=False),
        stats_prometheus_enabled=dict(type='bool', required=False, default=False),
        stats_prometheus_bind=dict(
            type='list', elements='str', required=False, 
            default=['*:8404']
        ),
        stats_prometheus_path=dict(type='str', required=False, default='/metrics'),
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

    # Create and run HAProxy general configuration handler
    handler = HaproxyGeneral(module=module, result=result)
    
    try:
        handler.process()
    except Exception as e:
        module.fail_json(msg=f"HAProxy general configuration failed: {str(e)}")
    
    module.exit_json(**result)


def main():
    """Module entry point"""
    run_module()


if __name__ == '__main__':
    main()