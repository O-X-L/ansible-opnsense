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
        OPN_MOD_ARGS, STATE_MOD_ARG, RELOAD_MOD_ARG
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.main.ipsec_manual_spd import ManualSPD

except MODULE_EXCEPTIONS:
    module_dependency_error()


# DOCUMENTATION = 'https://ansible-opnsense.oxl.app/modules/ipsec.html'
# EXAMPLES = 'https://ansible-opnsense.oxl.app/modules/ipsec.html'


def run_module():
    module_args = dict(
        name=dict(
            type='str', required=False, aliases=['description', 'desc'],
            description='Unique name to identify the entry',
        ),
        request_id=dict(
            type='int', required=False, aliases=['req_id', 'reqid'],
            description='Reqid to register this manual spd entry on.',
        ),
        connection_child=dict(
            type='str', required=False,
            description='Connection child to register this manual spd entry on.',
        ),
        source=dict(
            type='str', required=False, aliases=['s', 'src', 'source_net'],
            description='Source network, usually the networks you would like to accept using NAT.',
        ),
        destination=dict(
            type='str', required=False, aliases=['d', 'dest', 'destination_net'],
            description='Destination network, leave empty to use the networks propagated in the child sa.',
        ),
        **RELOAD_MOD_ARG,
        **STATE_MOD_ARG,
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
        required_if=[
            ('state', 'present', ('source',)),
            ('state', 'present', ('request_id', 'connection_child'), True),
        ],
        mutually_exclusive=[
            ('request_id', 'connection_child'),
        ],
    )

    module_wrapper(ManualSPD(module=module, result=result))
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
