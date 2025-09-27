#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (C) 2025, AnsibleGuy <guy@ansibleguy.net>
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

# see: https://docs.opnsense.org/development/api/core/dnsmasq.html

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.handler import \
    module_dependency_error, MODULE_EXCEPTIONS

try:
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.wrapper import module_wrapper
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.defaults.main import \
        OPN_MOD_ARGS, STATE_ONLY_MOD_ARG
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.dnsmasq_domain import Domain

except MODULE_EXCEPTIONS:
    module_dependency_error()


# DOCUMENTATION = 'https://ansible-opnsense.oxl.app/modules/dnsmasq.html'
# EXAMPLES = 'https://ansible-opnsense.oxl.app/modules/dnsmasq.html'


def run_module():
    module_args = dict(
        domain=dict(
            type='str', required=True, aliases=['name'],
            description='Domain to override.',
        ),
        sequence=dict(
            type='int', required=False, default=1, aliases=['seq'],
            description='Sort with a sequence number.'
        ),
        ip=dict(
            type='str', required=False,
            description='Source IP address for queries to the DNS server for the override domain.',
        ),
        port=dict(
            type='int', required=False,
            description='Specify a non standard port number.',
        ),
        src_ip=dict(
            type='str', required=False,
            description='Source IP address for queries to the DNS server for the override domain.',
        ),
        ipset=dict(
            type='str', required=False,
            description='When a client resolves the domain, the resolved IP addresses will be added to the alias.',
        ),
        description=dict(
            type='str', required=False,
            description='Description here for your reference.',
        ),
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

    module_wrapper(Domain(module=module, result=result))
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
