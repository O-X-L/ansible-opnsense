#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (C) 2025, AnsibleGuy <guy@ansibleguy.net>
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

# see: https://docs.opnsense.org/development/api/core/interfaces.html

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.handler import \
    module_dependency_error, MODULE_EXCEPTIONS

try:
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.wrapper import module_wrapper
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.defaults.main import \
        OPN_MOD_ARGS, STATE_ONLY_MOD_ARG, RELOAD_MOD_ARG
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.interface_lagg import Lagg

except MODULE_EXCEPTIONS:
    module_dependency_error()


# DOCUMENTATION = 'https://opnsense.ansibleguy.net/modules/interface.html'
# EXAMPLES = 'https://opnsense.ansibleguy.net/modules/interface.html'


def run_module():
    module_args = dict(
        device=dict(
            type='str', required=False, aliases=['laggif'],
            description="Optional 'device' of the entry. Needs to start with 'lagg'",
        ),
        members=dict(
            type='list', elements='str', required=False, aliases=['port', 'int', 'if', 'parent'],
            description='Existing LAGG capable interface - you must provide the network '
                        "port as shown in 'Interfaces - Assignments - Network port'"
        ),
        primary_member=dict(
            type='list', elements='str', required=False,
            description='This interface will be added first in the lagg making it the primary one '
                        "- you must provide the network port as shown in 'Interfaces - Assignments - Network port'"
        ),
        proto=dict(
            type='str', required=False, aliases=['p'], default='lacp',
            choices=['none', 'lacp', 'failover', 'fec', 'loadbalance', 'roundrobin'],
            description="The protocol to use."
        ),
        lacp_fast_timeout=dict(type='bool', required=False, default=False, aliases=['fast_timeout'],
            description='Enable lacp fast-timeout on the interface.'
        ),
        use_flowid=dict(
            type='str', required=False, choices=['yes', 'no'], aliases=['flowid'],
            description='Use the RSS hash from the network card if available, otherwise a hash is locally calculated. '
                        'The default depends on the system tunable in net.link.lagg.default_use_flowid.'
        ),
        lagghash=dict(
            type='list', elements='str', required=False, aliases=['hash', 'hash_layers'],
            choices=['l2', 'l3', 'l4'],
            description='Set the packet layers to hash for aggregation protocols which load balance.'
        ),
        lacp_strict=dict(
            type='str', required=False,
            choices=['yes', 'no'],
            description='Enable lacp strict compliance on the interface. The default depends on the '
                        'system tunable in net.link.lagg.lacp.default_strict_mode.',
        ),
        mtu=dict(
            type='int', required=False,
            description='If you leave this field blank, the smallest mtu of this laggs children will be used.'
        ),
        description=dict(type='str', required=False, aliases=['desc', 'name']),
        **RELOAD_MOD_ARG,
        **STATE_ONLY_MOD_ARG,
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

    module_wrapper(Lagg(module=module, result=result))
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
