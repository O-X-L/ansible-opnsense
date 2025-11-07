#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (C) 2025, Pascal Rath <contact+opnsense@OXL.at>
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

# see: https://docs.opnsense.org/development/api/plugins/bind.html

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.handler import \
    module_dependency_error, MODULE_EXCEPTIONS

try:
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.wrapper import \
        module_multi_wrapper
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.multi import \
        build_multi_mod_args, MultiModuleCallbacks
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.defaults.main import \
        OPN_MOD_ARGS, RELOAD_MOD_ARG
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.defaults.bind import \
        BIND_REC_MOD_ARGS, BIND_REC_MATCH_FIELDS
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.main.bind_record import \
        Record

except MODULE_EXCEPTIONS:
    module_dependency_error()


# DOCUMENTATION = 'https://ansible-opnsense.oxl.app/modules/bind.html'
# EXAMPLES = 'https://ansible-opnsense.oxl.app/modules/bind.html'


class MultiCallbacks(MultiModuleCallbacks):
    @staticmethod
    def get_existing(meta_entry: Record) -> dict:
        meta_entry.search_call_domains()
        return {
            'main': meta_entry.get_existing(),
            'domains': meta_entry.existing_domains,
        }

    @staticmethod
    def set_existing(entry: Record, cache: dict):
        entry.existing_entries = cache['main']
        entry.existing_domains = cache['domains']


def run_module():
    entry_multi_args = build_multi_mod_args(
        mod_args=BIND_REC_MOD_ARGS,
        aliases=['records'],
        not_required=['domain'],  # overrides could be used to define the domain
    )

    module_args = dict(
        **entry_multi_args,
        **RELOAD_MOD_ARG,
        **OPN_MOD_ARGS,
        **BIND_REC_MATCH_FIELDS,
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
        required_one_of=[
            ('multi', 'multi_purge', 'multi_control.purge_all'),
        ],
    )

    result = dict(
        changed=False,
        diff={
            'before': {},
            'after': {},
        }
    )

    module_multi_wrapper(
        module=module,
        result=result,
        obj=Record,
        kind='record',
        entry_args=entry_multi_args,
        callbacks=MultiCallbacks(),
    )
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
