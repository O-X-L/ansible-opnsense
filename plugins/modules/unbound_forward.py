#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (C) 2024, AnsibleGuy <guy@ansibleguy.net>
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

# see: https://docs.opnsense.org/development/api/core/unbound.html

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.handler import \
    module_dependency_error, MODULE_EXCEPTIONS

try:
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.wrapper import module_wrapper
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.defaults.main import \
        OPN_MOD_ARGS, STATE_MOD_ARG, RELOAD_MOD_ARG
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.unbound_forward import Forward

except MODULE_EXCEPTIONS:
    module_dependency_error()


# DOCUMENTATION = 'https://opnsense.ansibleguy.net/en/latest/modules/unbound_forwarding.html'
# EXAMPLES = 'https://opnsense.ansibleguy.net/en/latest/modules/unbound_forwarding.html'


def run_module():
    module_args = dict(
        domain=dict(
            type='str', required=False, aliases=['dom', 'd'],
            description='Domain of the host. All queries for this domain will be forwarded to the nameserver '
                        'specified. Leave empty to catch all queries and forward them to the nameserver'
        ),
        target=dict(
            type='str', required=True, aliases=['tgt', 'server', 'srv'],
            description='Server to forward the dns queries to'
        ),
        port=dict(
            type='int', required=False, default=53, aliases=['p'],
            description='DNS port of the target server'
        ),
        type=dict(type='str', required=False, choices=['forward'], default='forward'),
        forward_tcp=dict(
            type='bool', required=False, default=False, aliases=['forward_tcp_upstream', 'fwd_tcp'],
            description='Upstream queries use TCP only for transport regardless of global flag tcp-upstream. '
                        'Please note this setting applies to the domain, so when multiple forwarders are '
                        'defined for the same domain, all are assumed to use tcp only.'
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
    )

    module_wrapper(Forward(module=module, result=result))
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
