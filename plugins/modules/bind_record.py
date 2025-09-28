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
        module_wrapper, is_multi_module_call, module_multi_wrapper
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.multi import \
        build_multi_mod_args, MultiModuleCallbacks
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.defaults.main import \
        OPN_MOD_ARGS, STATE_MOD_ARG, RELOAD_MOD_ARG
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
    entry_args = dict(
        domain=dict(type='str', required=True, aliases=['domain_name']),
        name=dict(type='str', required=True, aliases=['record']),
        type=dict(
            type='str', required=False, default='A',
            choices=[
                'A', 'AAAA', 'CAA', 'CNAME', 'DNSKEY', 'DS', 'MX', 'NS', 'PTR',
                'RRSIG', 'SRV', 'TLSA', 'TXT',
            ]
        ),
        value=dict(type='str', required=False),
        round_robin=dict(
            type='bool', required=False, default=False,
            description='If multiple records with the same domain/name/type combination exist - '
                        "the module will only execute 'state=absent' if set to 'false'. "
                        "To create multiple ones set this to 'true'. "
                        "Records will only be created, NOT UPDATED! (no matching is done)"
        ),
        match_fields=dict(
            type='list', required=False, elements='str',
            description='Fields that are used to match configured records with the running config - '
                        "if any of those fields are changed, the module will think it's a new entry",
            choices=['name', 'domain', 'type', 'value'],
            default=['name', 'domain', 'type'],
        ),
        **STATE_MOD_ARG,
    )
    entry_multi_args = build_multi_mod_args(
        mod_args=entry_args,
        aliases=['records'],
        not_required=['domain', 'name'],
    )

    module_args = dict(
        **entry_args,
        **entry_multi_args,
        **RELOAD_MOD_ARG,
        **OPN_MOD_ARGS,
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
        mutually_exclusive=[
            ('name', 'multi'), ('name', 'multi_purge'), ('name', 'multi_control.purge_all')
        ],
        required_one_of=[
            ('name', 'multi', 'multi_purge', 'multi_control.purge_all'),
        ],
    )

    result = dict(
        changed=False,
        diff={
            'before': {},
            'after': {},
        }
    )

    if is_multi_module_call(module):
        module_multi_wrapper(
            module=module,
            result=result,
            obj=Record,
            kind='record',
            entry_args=entry_multi_args,
            callbacks=MultiCallbacks(),
        )

    else:
        module_wrapper(Record(module=module, result=result))

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
