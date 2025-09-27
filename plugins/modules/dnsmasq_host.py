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
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.dnsmasq_host import Host

except MODULE_EXCEPTIONS:
    module_dependency_error()


# DOCUMENTATION = 'https://ansible-opnsense.oxl.app/modules/dnsmasq.html'
# EXAMPLES = 'https://ansible-opnsense.oxl.app/modules/dnsmasq.html'


def run_module():
    module_args = dict(
        description=dict(
            type='str', required=True, aliases=['desc'],
            description='DHCP host description.',
        ),
        host=dict(
            type='str', required=False, aliases=['h'],
            description='Name of the host, without the domain part.',
        ),
        domain=dict(
            type='str', required=False, aliases=['d'],
            description='Domain of the host.',
        ),
        local=dict(
            type='bool', required=False, default=False,
            description='Set the domain as local.',
        ),
        ip=dict(
            type='list', elements='str', required=False, default=[],
            description='IP addresses of the host.',
        ),
        aliases=dict(
            type='list', elements='str', required=False, default=[],
            description='Adds additional static A, AAAA and PTR records for the given alternative names (FQDN).',
        ),
        cnames=dict(
            type='list', elements='str', required=False, default=[],
            description='Adds additional CNAME records for the given alternative names.',
        ),
        # DHCP
        client_id=dict(
            type='str', required=False,
            description='DHCP boot server address.',
        ),
        hardware_addr=dict(
            type='list', elements='str', required=False, aliases=['mac'], default=[],
            description='Hardware address of the client.',
        ),
        lease_time=dict(
            type='int', required=False,
            description='Time the lease is valid.',
        ),
        ignore=dict(
            type='bool', required=False, default=False,
            description='Ignore any DHCP packets of this host.',
        ),
        set_tag=dict(
            type='str', required=False,
            description='Tag to set for matching requests.',
        ),
        comments=dict(
            type='str', required=False,
            description='A comment for your reference (not parsed).',
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

    module_wrapper(Host(module=module, result=result))
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
