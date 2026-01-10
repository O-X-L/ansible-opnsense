#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (C) 2026, Wojciech Matusiak <wmatusiak@gmail.com>
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

# see: https://docs.opnsense.org/development/api/plugins/nut.html

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.handler import \
    module_dependency_error, MODULE_EXCEPTIONS

try:
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.defaults.main import \
        OPN_MOD_ARGS
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.api import single_get

except MODULE_EXCEPTIONS:
    module_dependency_error()

# DOCUMENTATION = 'https://ansible-opnsense.oxl.app/modules/nut_diagnostics.html'
# EXAMPLES = 'https://ansible-opnsense.oxl.app/modules/nut_diagnostics.html'

def run_module():
    module_args = dict(
        **OPN_MOD_ARGS,
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
    )

    res = single_get(
        module=module,
        cnf={
            'module': 'nut',
            'controller': 'diagnostics',
            'command': 'upsstatus',
        }
    )

    info = {}
    if 'response' in res:
        res = res['response'].split('\n')
        for i in res:
            if i != "":
                tmp = i.split(':', 1)
                path = tmp[0].strip().split('.')
                value = tmp[1].strip()
                t = info
                for p in path[:-1]:
                    if p not in t:
                        t[p] = {}

                    t = t[p]

                t[path[-1]] = {
                    'value': value
                }

    module.exit_json(data=info)


def main():
    run_module()


if __name__ == '__main__':
    main()
