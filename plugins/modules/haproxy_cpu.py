#!/usr/bin/python
# -*- coding: utf-8 -*-


# Copyright: (C) 2025, MaximeWewer
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

# see: https://docs.opnsense.org/development/api/plugins/haproxy.html

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.handler import \
    module_dependency_error, MODULE_EXCEPTIONS

try:
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.wrapper import module_wrapper
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.defaults.main import \
        OPN_MOD_ARGS, STATE_MOD_ARG, RELOAD_MOD_ARG
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.main.haproxy_cpu import HaproxyCpu

except MODULE_EXCEPTIONS:
    module_dependency_error()


# DOCUMENTATION = 'https://ansible-opnsense.oxl.app/modules/haproxy.html'
# EXAMPLES = 'https://ansible-opnsense.oxl.app/modules/haproxy.html'


def run_module():
    module_args = dict(
        name=dict(
            type='str', required=True,
            description='Choose a name for this CPU affinity rule'
        ),
        thread_id=dict(
            type='str', required=False, default=None,
            choices=['all', 'odd', 'even'] + [f'x{i}' for i in range(64)],
            description='Thread ID that should bind to a specific CPU set'
        ),
        cpu_id=dict(
            type='list', elements='str', required=False, default=None,
            choices=['all', 'odd', 'even'] + [f'x{i}' for i in range(64)],
            description='Bind the process/thread ID to this CPU'
        ),
        **STATE_MOD_ARG,
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
        required_if=[
            ('state', 'present', ('thread_id', 'cpu_id')),
        ],
    )

    module_wrapper(HaproxyCpu(module=module, result=result))

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
