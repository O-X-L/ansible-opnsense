#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (C) 2025, MaximeWewer
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

# see: https://docs.opnsense.org/development/api/plugins/haproxy.html

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.handler import \
    module_dependency_error, MODULE_EXCEPTIONS

try:
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.helper.wrapper import module_wrapper
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.defaults.main import \
        OPN_MOD_ARGS, EN_ONLY_MOD_ARG, RELOAD_MOD_ARG
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.main.haproxy_general_settings import HaproxyGeneralSettings

except MODULE_EXCEPTIONS:
    module_dependency_error()


# DOCUMENTATION = 'https://ansible-opnsense.oxl.app/modules/haproxy.html'
# EXAMPLES = 'https://ansible-opnsense.oxl.app/modules/haproxy.html'


def run_module():
    module_args = dict(
        graceful_stop=dict(
            type='bool', required=False, default=True,
            description='Enable graceful stop mode which handles existing connections before stopping'
        ),
        hard_stop_after=dict(
            type='int', required=False, default=None,
            description='Maximum time in seconds for a graceful stop, after which HAProxy terminates all connections'
        ),
        close_spread_time=dict(
            type='int', required=False, default=None,
            description='Time window in seconds to spread connection closing during graceful shutdown'
        ),
        seamless_reload=dict(
            type='bool', required=False, default=False,
            description='Handle restarts without losing connections'
        ),
        show_intro=dict(
            type='bool', required=False, default=True,
            description='Show/hide introduction pages'
        ),
        **EN_ONLY_MOD_ARG,
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
    )

    module_wrapper(HaproxyGeneralSettings(module=module, result=result))

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
