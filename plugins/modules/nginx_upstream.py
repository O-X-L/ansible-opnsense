#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (C) 2024, AnsibleGuy <guy@ansibleguy.net>
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.handler import \
    module_dependency_error, MODULE_EXCEPTIONS

try:
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.wrapper import module_wrapper
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.defaults.main import \
        OPN_MOD_ARGS, STATE_ONLY_MOD_ARG, RELOAD_MOD_ARG_DEF_FALSE
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.nginx_upstream import Upstream

except MODULE_EXCEPTIONS:
    module_dependency_error()


# DOCUMENTATION = 'https://opnsense.ansibleguy.net/modules/nginx.html'
# EXAMPLES = 'https://opnsense.ansibleguy.net/modules/nginx.html'


def run_module():
    module_args = dict(
        description=dict(type='str', required=True, aliases=['name']),
        serverentries=dict(type='list', required=True, elements='str'),
        load_balancing_algorithm=dict(
            type='str', required=False, choices=['ip_hash']
        ),
        keepalive=dict(type='int', required=False),
        keepalive_requests=dict(type='int', required=False),
        keepalive_timeout=dict(type='int', required=False),
        host_port=dict(type='int', required=False),
        x_forwarded_host_verbatim=dict(
            type='bool', required=False, default=False,
        ),
        proxy_protocol=dict(
            type='bool', required=False, default=False,
        ),
        store=dict(
            type='bool', required=False, default=False,
        ),
        tls_enable=dict(
            type='bool', required=False, default=False,
        ),
        tls_client_certificate=dict(type='str', required=False),
        tls_name_override=dict(type='str', required=False),
        tls_protocol_versions=dict(
            type='list',
            elements='str',
            required=False,
            choices=['TLSv1', 'TLSv1.1', 'TLSv1.2', 'TLSv1.3'],
        ),
        tls_session_reuse=dict(
            type='bool', required=False, default=True,
        ),
        tls_trusted_certificate=dict(
            type='list',
            elements='str',
            required=False,
        ),
        tls_verify=dict(
            type='bool', required=False, default=True,
        ),
        tls_verify_depth=dict(
            type='int', required=False, default=1,
        ),
        **RELOAD_MOD_ARG_DEF_FALSE,
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

    module_wrapper(Upstream(module=module, result=result))
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
