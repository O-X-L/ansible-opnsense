#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (C) 2025, Pascal Rath <contact+opnsense@OXL.at>
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.handler import \
    module_dependency_error, MODULE_EXCEPTIONS

try:
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.wrapper import module_wrapper
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.defaults.main import \
        OPN_MOD_ARGS, EN_ONLY_MOD_ARG, RELOAD_MOD_ARG
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.main.hasync_general import General

except MODULE_EXCEPTIONS:
    module_dependency_error()

# DOCUMENTATION = 'https://ansible-opnsense.oxl.app/modules/hasync.html'
# EXAMPLES = 'https://ansible-opnsense.oxl.app/modules/hasync.html'


def run_module():
    module_args = dict(
        preempt=dict(
            type='bool', required=False, default=True,
            description='When this device is configured as CARP master it will try to switch to master when powering '
                        ' up, this option will keep this one slave if there already is a master on the network.',
        ),
        disconnect_ppps=dict(
            type='bool', required=False, default=False,
            description='When this device is configured as CARP backup it will disconnect all PPP type interfaces '
                        'and try to reconnect them when becoming master again.',
        ),
        pfsync_interface=dict(
            type='str', required=False, aliases=['interface', 'i', 'int'],
            description='Enable state insertion, update, and deletion messages between firewalls by utilizing the '
                        'selected interface for communication. Best choose a dedicated interface for this type of '
                        'communication to prevent manipulation of states causing security issues.',
        ),
        pfsync_peer_ip=dict(
            type='str', required=False, aliases=['peer'],
            description='Force pfsync to synchronize its state table to this IP address.',
        ),
        pfsync_version=dict(
            type='str', required=False, choices=['1301', '1400'], default='1400',
            description='Newer versions of OPNsense offer additional attributes in the state synchronization, '
                        'for compatibility reasons you can optionally choose an older version here. Always make sure '
                        'both nodes use the same version to avoid inconsistent state tables.',
        ),
        synchronize_to_ip=dict(
            type='str', required=False,
            description='IP address of the firewall to which the selected configuration sections should be '
            'synchronized. This should be empty on the backup machine. When an IP address is offered, '
            'both web GUI configurations should be equal (port and protocol).',
        ),
        verify_peer=dict(
            type='bool', required=False, default=False,
            description='In most cases the target host will be a directly attached neighbor in which case TLS '
                        'verification can be ignored.',
        ),
        username=dict(
            type='str', required=False,
            description='Web GUI username of the system entered for synchronizing your configuration.',
        ),
        password=dict(
            type='str', required=False, no_log=True,
            description='Web GUI password of the system entered for synchronizing your configuration.',
        ),
        update_password=dict(
            type='str', required=False, choices=['always', 'on_create'], default='always',
            description='Update the password `always` or only `on_create`.',
        ),
        syncitems=dict(
            type='list', required=False, default=[], elements='str',
            description='Services that should be send to the other host.',
        ),
        **RELOAD_MOD_ARG,
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

    module_wrapper(General(module=module, result=result))
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
