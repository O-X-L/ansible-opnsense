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
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.haproxy_general_peers import GeneralPeers

except MODULE_EXCEPTIONS:
    module_dependency_error()


# DOCUMENTATION = 'https://ansible-opnsense.oxl.app/modules/haproxy.html'
# EXAMPLES = 'https://ansible-opnsense.oxl.app/modules/haproxy.html'


def run_module():
    module_args = dict(
        name1=dict(
            type='str', required=False, default=None,
            description='The name of the peer. Usually the fully qualified domain name. If name matches system hostname, peer is automatically configured as local'
        ),
        listen1=dict(
            type='str', required=False, default=None,
            description='The listen address of the local peer or the address of the remote peer'
        ),
        port1=dict(
            type='int', required=False, default=1024,
            description='The TCP port that should be used for connections to this peer. It must not be used by any other service'
        ),
        name2=dict(
            type='str', required=False, default=None,
            description='The name of the peer. Usually the fully qualified domain name. If name matches system hostname, peer is automatically configured as local'
        ),
        listen2=dict(
            type='str', required=False, default=None,
            description='The listen address of the local peer or the address of the remote peer'
        ),
        port2=dict(
            type='int', required=False, default=1024,
            description='The TCP port that should be used for connections to this peer. It must not be used by any other service'
        ),
        **EN_ONLY_MOD_ARG,
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

    module_wrapper(GeneralPeers(module=module, result=result))

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
