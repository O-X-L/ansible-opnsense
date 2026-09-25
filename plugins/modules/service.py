#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (C) 2025, Pascal Rath <contact+opnsense@OXL.at>
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

# module to interact with system services

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.handler import \
    module_dependency_error, MODULE_EXCEPTIONS

try:
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.defaults.main import \
        OPN_MOD_ARGS
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.api import \
        single_get, single_post

except MODULE_EXCEPTIONS:
    module_dependency_error()


# DOCUMENTATION = 'https://ansible-opnsense.oxl.app/general/service.html'
# EXAMPLES = 'https://ansible-opnsense.oxl.app/general/service.html'

# c = api-module, m = custom action-mapping, a = limited actions
SERVICES = {
    # core api
    'openssh': {'a': ['start', 'stop', 'restart', 'status']},
    'captive_portal': {'c': 'captiveportal', 'a': ['reload']},
    'cron': {'a': ['reload']},
    'ipsec_legacy': {'c': 'legacy_subsystem', 'a': ['reload'], 'm': {'reload': 'applyConfig'}},
    'ipsec': {}, 'monit': {}, 'syslog': {},
    'shaper': {
        'c': 'trafficshaper', 'a': ['reload', 'status', 'restart'],
        'm': {'restart': 'flushreload', 'status': 'statistics'}
    },
    'openvpn': {
        'c': 'openvpn', 'a': ['stop', 'status', 'start', 'reload', 'restart'],
        'm': {
            'start': 'startService', 'reload': 'reconfigure', 'restart': 'restartService',
            'status': 'searchSessions', 'stop': 'stopService',
        },
    },
    #   note: these would support more actions:
    'ids': {}, 'proxy': {}, 'unbound': {}, 'kea': {}, 'dnsmasq': {},
    # plugins
    'ftp_proxy': {'c': 'ftpproxy'},
    'iperf': {'a': ['reload', 'status', 'start', 'restart']},
    'mdns_repeater': {'c': 'mdnsrepeater', 'a': ['stop', 'status', 'start', 'restart']},
    'munin_node': {'c': 'muninnode'},
    'node_exporter': {'c': 'nodeexporter'},
    'puppet_agent': {'c': 'puppetagent'},
    'qemu_guest_agent': {'c': 'qemuguestagent'},
    'frr': {'c': 'quagga'},
    'radsec_proxy': {'c': 'radsecproxy'},
    'zabbix_agent': {'c': 'zabbixagent'},
    'zabbix_proxy': {'c': 'zabbixproxy'},
    'apcupsd': {}, 'bind': {}, 'chrony': {}, 'cicap': {}, 'collectd': {},
    'dyndns': {}, 'fetchmail': {}, 'freeradius': {}, 'haproxy': {}, 'maltrail': {},
    'netdata': {}, 'netsnmp': {}, 'nrpe': {}, 'nut': {}, 'openconnect': {}, 'proxysso': {},
    'rspamd': {}, 'shadowsocks': {}, 'softether': {}, 'sslh': {}, 'stunnel': {}, 'tayga': {},
    'telegraf': {}, 'tftp': {}, 'tinc': {}, 'wazuh_agent': {'c': 'wazuhagent'}, 'wireguard': {},
    #   note: these would support more actions:
    'acme_client': {'c': 'acmeclient'},
    'crowdsec': {'a': ['reload', 'status']},
    'dns_crypt_proxy': {'c': 'dnscryptproxy'},
    'udp_broadcast_relay': {'c': 'udpbroadcastrelay'},
    'clamav': {}, 'hwprobe': {}, 'lldpd': {}, 'nginx': {}, 'ntopng': {}, 'postfix': {}, 'redis': {},
    'relayd': {}, 'siproxd': {}, 'vnstat': {}, 'tor': {},
}

ACTION_MAPPING = {'reload': 'reconfigure'}
API_CONTROLLER = 'service'


# pylint: disable=R0915

def _openssh_status(module):
    response = single_get(module=module, cnf={
        'module': 'core', 'controller': 'service', 'command': 'search',
    })
    rows = response.get('rows', [])
    # The endpoint is paginated; never interpret a truncated result as absence.
    if int(response.get('total', len(rows))) > len(rows):
        module.fail_json('Core service list is truncated; unable to determine openssh state.')
    matches = [row for row in rows if row.get('id') == 'openssh' and row.get('name') == 'openssh']
    if len(matches) != 1:
        module.fail_json('openssh is not registered uniquely in core/service; check SSH configuration.')
    if str(matches[0].get('running')) not in ('0', '1'):
        module.fail_json('Core service API returned an invalid openssh running state.')
    return matches[0]


def _openssh(module, result):
    action = module.params['action']
    current = _openssh_status(module)
    result['data'] = current
    result['executed'] = action
    if action == 'status':
        return
    running = str(current['running']) == '1'
    if (action == 'start' and running) or (action == 'stop' and not running):
        return
    result['changed'] = True
    if module.check_mode:
        return
    response = single_post(module=module, cnf={
        'module': 'core', 'controller': 'service', 'command': action, 'params': ['openssh'],
    })
    if response.get('result') != 'ok':
        module.fail_json('Core service API did not accept the openssh action.')
    result['data'] = _openssh_status(module)
    if (str(result['data']['running']) == '1') != (action != 'stop'):
        module.fail_json('openssh did not reach the requested runtime state; inspect the service logs.')


def run_module():
    service_choices = list(SERVICES.keys())
    service_choices.sort()

    module_args = dict(
        name=dict(
            type='str', required=True, aliases=['service', 'svc', 'target', 'n'],
            choices=service_choices,
            description='What service to interact with'
        ),
        action=dict(
            type='str', required=True, aliases=['do', 'a'],
            choices=['reload', 'restart', 'start', 'status', 'stop'],
            description='What action to execute. Some services may not support all of these actions - '
                        'the module will inform you in that case'
        ),
        **OPN_MOD_ARGS,
    )

    result = dict(
        changed=False,
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
    )

    name = module.params['name']
    action = module.params['action']
    service = SERVICES[name]

    if 'a' in service and action not in service['a']:
        module.fail_json(
            f"Service '{name}' does not support the "
            f"provided action '{action}'! "
            f"Supported ones are: {service['a']}"
        )

    if name == 'openssh':
        _openssh(module, result)
        module.exit_json(**result)
        return

    # translate actions to api-commands
    # pylint: disable=R1715
    if 'm' in service and action in service['m']:
        action = service['m'][action]

    elif action in ACTION_MAPPING:
        action = ACTION_MAPPING[action]

    result['executed'] = action

    # get api-module
    if 'c' in service:
        api_module = service['c']

    else:
        api_module = name

    # pull status or execute action
    if module.params['action'] == 'status':
        info = single_get(
            module=module,
            cnf={
                'module': api_module,
                'controller': API_CONTROLLER,
                'command': action,
            }
        )

        if 'response' in info:
            info = info['response']

            if isinstance(info, str):
                info = info.strip()

        result['data'] = info

    else:
        result['changed'] = True

        if not module.check_mode:
            single_post(
                module=module,
                cnf={
                    'module': api_module,
                    'controller': API_CONTROLLER,
                    'command': action,
                }
            )

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
