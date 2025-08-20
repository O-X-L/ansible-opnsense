#!/usr/bin/python3

# Copyright: (C) 2025, MaximeWewer
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

"""Module to configure HAProxy CPUs on OPNsense"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.handler import \
    module_dependency_error, MODULE_EXCEPTIONS

try:
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.wrapper import module_wrapper
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import \
        diff_remove_empty
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.defaults.main import \
        OPN_MOD_ARGS, EN_ONLY_MOD_ARG
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.haproxy_cpu import HaproxyCpu

except MODULE_EXCEPTIONS:
    module_dependency_error()


# DOCUMENTATION = 'https://opnsense.ansibleguy.net/en/latest/modules/haproxy.html'
# EXAMPLES = 'https://opnsense.ansibleguy.net/en/latest/modules/haproxy.html'


def run_module():
    # Generate thread and CPU choices dynamically  
    thread_choices = ['all', 'odd', 'even'] + [f'x{i}' for i in range(1, 64)]
    cpu_choices = ['all', 'odd', 'even'] + [f'x{i}' for i in range(0, 64)]
    
    module_args = dict(
        name=dict(type='str', required=True),
        thread_id=dict(type='str', required=True, choices=thread_choices),
        cpu_id=dict(type='str', required=True, choices=cpu_choices),
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

    module_wrapper(HaproxyCpu(module=module, result=result))

    result['diff'] = diff_remove_empty(result['diff'])
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()