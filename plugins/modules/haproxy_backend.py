#!/usr/bin/python

# Copyright: (C) 2025, MaximeWewer
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

"""Module to configure HAProxy backends on OPNsense"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.handler import \
    module_dependency_error, MODULE_EXCEPTIONS

try:
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.wrapper import module_wrapper
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.defaults.main import \
        OPN_MOD_ARGS, EN_ONLY_MOD_ARG
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.haproxy_backend import HaproxyBackend

except MODULE_EXCEPTIONS:
    module_dependency_error()


# DOCUMENTATION = 'https://opnsense.ansibleguy.net/en/latest/modules/haproxy.html'
# EXAMPLES = 'https://opnsense.ansibleguy.net/en/latest/modules/haproxy.html'


def run_module():
    """Initiate module execution"""
    module_args = dict(
        name=dict(type='str', required=True),
        description=dict(type='str', required=False),
        mode=dict(
            type='str', required=False, default='http',
            choices=['http', 'tcp']
        ),
        algorithm=dict(
            type='str', required=False, default='roundrobin',
            choices=['roundrobin', 'static-rr', 'leastconn', 'first', 'source', 'uri', 'random', 'rdp-cookie']
        ),
        source=dict(type='str', required=False),
        health_check_enabled=dict(type='bool', required=False, default=False),
        health_check=dict(type='str', required=False),
        health_check_interval=dict(type='str', required=False, default='2s'),
        health_check_timeout=dict(type='str', required=False, default='2s'),
        health_check_retries=dict(type='int', required=False, default=3),
        linked_servers=dict(type='list', elements='str', required=False),
        linked_actions=dict(type='list', elements='str', required=False),
        linked_errorfiles=dict(type='list', elements='str', required=False),
        basic_auth_users=dict(type='list', elements='str', required=False),
        basic_auth_groups=dict(type='list', elements='str', required=False),
        linked_resolver=dict(type='str', required=False),
        http_reuse=dict(
            type='str', required=False, default='never',
            choices=['never', 'safe', 'aggressive', 'always']
        ),
        state=dict(type='str', default='present', choices=['present', 'absent']),
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

    module_wrapper(HaproxyBackend(module=module, result=result))

    module.exit_json(**result)


def main():
    """Module entry point"""
    run_module()


if __name__ == '__main__':
    main()