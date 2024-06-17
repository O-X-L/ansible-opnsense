#!/usr/bin/env python3

# Copyright: (C) 2023, AnsibleGuy <guy@ansibleguy.net>
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

# see: https://docs.opnsense.org/development/api/plugins/nginx.html

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.handler import \
    module_dependency_error, MODULE_EXCEPTIONS
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import diff_remove_empty
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.wrapper import module_wrapper

try:
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.defaults.main import EN_ONLY_MOD_ARG, OPN_MOD_ARGS
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.nginx_general import General


except MODULE_EXCEPTIONS:
    module_dependency_error()

# DOCUMENTATION = 'https://opnsense.ansibleguy.net/en/latest/modules/nginx.html'
# EXAMPLES = 'https://opnsense.ansibleguy.net/en/latest/modules/nginx.html'


def run_module():
    module_args = dict(
        ban_ttl=dict(type='int', required=False, default=0),
        **EN_ONLY_MOD_ARG,
        **OPN_MOD_ARGS,
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
    )

    result = dict(
        changed=False,
        diff={
            'before': {},
            'after': {},
        }
    )

    General(module=module, result=result)
    result['diff'] = diff_remove_empty(result['diff'])

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
