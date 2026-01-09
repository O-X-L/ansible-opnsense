#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (C) 2026, Wojciech Matusiak <wmatusiak@gmail.com>
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

# see: https://docs.opnsense.org/development/api/plugins/nut.html

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.handler import \
    module_dependency_error, MODULE_EXCEPTIONS

try:
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.wrapper import module_wrapper
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.defaults.main import \
        OPN_MOD_ARGS, EN_ONLY_MOD_ARG, RELOAD_MOD_ARG
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.main.nut import Nut

except MODULE_EXCEPTIONS:
    module_dependency_error()


# DOCUMENTATION = 'https://ansible-opnsense.oxl.app/modules/nut.html'
# EXAMPLES = 'https://ansible-opnsense.oxl.app/modules/nut.html'

def _std_driver_args(
        driver_name: str, display_name: str,
        extra_enable_description: str = '',
        default_extra_args: dict = ['port=auto']
) -> dict:
    res = {}
    res[f"{driver_name}_enable"]=dict(
        type='bool', required=False, default=False,
        description=f'Enable the {display_name} driver. ' + extra_enable_description
    )
    res[f"{driver_name}_args"]=dict(
        type='list', elements='str', required=False,
        default=default_extra_args,
        description=f'Extra arguments for {display_name} driver, e.g. "{default_extra_args}"'
    )
    return res

def run_module():
    module_args = dict(
        mode=dict(
            type='str', required=False, default='standalone',
            choices=['standalone', 'netclient'],
            description='Service mode.'
                        'Currently only standalone and netclient are available'
        ),
        name=dict(
            type='str', required=False, default='UPSName',
            description='Name for your UPS'
        ),
        listen=dict(
            type='list', elements='str', required=False,
            default=['127.0.0.1', '::1'],
            description='Addresses this service listen on'
        ),
        admin_password=dict(
            type='str', required=False, no_log=True,
            default='Password',
            description='Password for admin user "admin"'
        ),
        monitor_password=dict(
            type='str', required=False, no_log=True,
            default='Password',
            description='Password for monitoring user "monuser"'
        ),
        **_std_driver_args('usbhid', 'USBHID'),
        **_std_driver_args('apcsmart', 'APCSMART'),
        apcupsd_enable=dict(
            type='bool', required=False, default=False,
            description='Enable the APCUPSD controlled devices driver'
        ),
        apcupsd_host=dict(
            type='str', required=False, default='localhost',
            description='Hostname or ip of the remote apcupsd server'
        ),
        apcupsd_port=dict(
            type='int', required=False, default=None,
            description='Port of the remote apcupsd server (optional)'
        ),
        **_std_driver_args('bcmxcpusb', 'PowerWare BCMXCPUSB'),
        **_std_driver_args('blazerusb', 'BlazerUSB'),
        **_std_driver_args(
            'blazerser',
            'BlazerSerial',
            extra_enable_description='Please be aware that this driver needs to run nut-tools as root.'
        ),
        netclient_enable=dict(
            type='bool', required=False, default=False,
            description='Enable the Netclient driver'
        ),
        netclient_address=dict(
            type='str', required=False, default=None,
            description='IP address of the remote NUT server'
        ),
        netclient_port=dict(
            type='int', required=False, default=3493,
            description='TCP port of the remote NUT server'
        ),
        netclient_user=dict(
            type='str', required=False, default=None,
            description='Username of the remote NUT server'
        ),
        netclient_password=dict(
            type='str', required=False, default=None, no_log=True,
            description='Password of the remote NUT server'
        ),
        **_std_driver_args('qx', 'QX'),
        **_std_driver_args('riello', 'Riello'),
        **_std_driver_args('snmp', 'SNMP', default_extra_args=['community=public']), 
        **EN_ONLY_MOD_ARG,
        **OPN_MOD_ARGS,
        **RELOAD_MOD_ARG,
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

    module_wrapper(Nut(module=module, result=result))
    module.exit_json(**result)
    

def main():
    run_module()


if __name__ == '__main__':
    main()
