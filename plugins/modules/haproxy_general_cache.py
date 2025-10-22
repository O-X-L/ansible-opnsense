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
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.main.haproxy_general_cache import HaproxyGeneralCache

except MODULE_EXCEPTIONS:
    module_dependency_error()


# DOCUMENTATION = 'https://ansible-opnsense.oxl.app/modules/haproxy.html'
# EXAMPLES = 'https://ansible-opnsense.oxl.app/modules/haproxy.html'


def run_module():
    module_args = dict(
        total_max_size=dict(
            type='int', required=False, default=4,
            description='Define the size in RAM of the cache in megabytes. This size is split in blocks of 1kB'
        ),
        max_age=dict(
            type='int', required=False, default=60,
            description='Define the maximum expiration duration. Cache-Control response headers will be respected if they are less than this value'
        ),
        max_object_size=dict(
            type='int', required=False, default=None,
            description='Define the maximum size of the objects to be cached. Must not be greater than an half of the maximum size of the cache'
        ),
        process_vary=dict(
            type='bool', required=False, default=False,
            description='Enable or disable the processing of the Vary header. When disabled, a response containing such a header will never be cached'
        ),
        max_secondary_entries=dict(
            type='int', required=False, default=10,
            description='Define the maximum number of simultaneous secondary entries with the same primary key in the cache'
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

    module_wrapper(HaproxyGeneralCache(module=module, result=result))

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
