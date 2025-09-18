#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (C) 2025, Pascal Rath <contact+opnsense@OXL.at>
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

# see: https://docs.opnsense.org/development/api/core/firewall.html

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.handler import \
    module_dependency_error, MODULE_EXCEPTIONS

try:
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.wrapper import \
        module_wrapper, is_multi_module_call, module_multi_wrapper
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.defaults.main import \
        RELOAD_MOD_ARG_DEF_FALSE, build_multi_mod_args, OPN_MOD_ARGS, STATE_MOD_ARG
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.alias import Alias
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import ensure_list
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.alias import builtin_alias

except MODULE_EXCEPTIONS:
    module_dependency_error()


# DOCUMENTATION = 'https://ansible-opnsense.oxl.app/modules/alias.html'
# EXAMPLES = 'https://ansible-opnsense.oxl.app/modules/alias.html'


def _build_alias_args(multi: bool) -> dict:
    a = dict(
        name=dict(type='str', required=multi, aliases=['n']),
        description=dict(
            type='str', required=False, default='', aliases=['desc'],
        ),
        content=dict(
            type='list', required=False, default=[], aliases=['c', 'cont'], elements='str',
        ),
        type=dict(type='str', required=False, default='host', aliases=['t'], choices=[
            'host', 'network', 'port', 'url', 'urltable', 'geoip', 'networkgroup',
            'mac', 'dynipv6host', 'internal', 'external',
        ]),
        updatefreq_days=dict(
            type='float', default=7, required=False,
            description="Update frequency used by type 'urltable' in days - per example '0.5' for 12 hours"
        ),
        interface=dict(
            type='str', default=None, aliases=['int', 'if'], required=False,
            description=' Select the interface for the V6 dynamic IP.',
        ),
        **STATE_MOD_ARG,
    )
    if not multi:
        a = {
            **a,
            **OPN_MOD_ARGS,
        }

    return a


def _multi_callback_build(entry: dict) -> dict:
    entry['content'] = list(map(str, ensure_list(entry['content'])))
    if 'updatefreq_days' in entry:
        dec = 1
        if str(entry['updatefreq_days']).endswith('.0'):
            dec = None

        entry['updatefreq_days'] = round(entry['updatefreq_days'], dec)

    return entry


# def _multi_callback_get_existing(meta_entry: Alias) -> dict:
#     return {'aliases': meta_entry.get_existing()}


# def _multi_callback_set_existing(entry: Alias, cache: dict) -> None:
#     entry.existing_entries = cache['aliases']


def _multi_callback_update_existing(entry_cnf: dict, cache: dict) -> dict:
    cache['main'].append(entry_cnf)
    return cache


def _multi_callback_purge_exclude(entry_cnf: dict) -> bool:
    return builtin_alias(entry_cnf['name'])


def run_module():
    module_args = dict(
        **RELOAD_MOD_ARG_DEF_FALSE,  # default-true takes pretty long sometimes (urltables and so on)
        **_build_alias_args(multi=False),
        **build_multi_mod_args(
            entry=_build_alias_args(multi=True),
            aliases=['aliases']
        ),
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
        mutually_exclusive=[
            ('name', 'multi'), ('name', 'multi_purge'), ('name', 'multi_control.purge_all')
        ],
        required_one_of=[
            ('name', 'multi', 'multi_purge', 'multi_control.purge_all'),
        ],
    )

    if is_multi_module_call(module):
        module_multi_wrapper(
            module=module,
            result=result,
            obj=Alias,
            kind='alias',
            module_args=module_args,
            callback_build=_multi_callback_build,
            # callback_get_existing=_multi_callback_get_existing,
            # callback_set_existing=_multi_callback_set_existing,
            callback_update_existing=_multi_callback_update_existing,
            callback_purge_exclude=_multi_callback_purge_exclude,
        )

    else:
        module_wrapper(Alias(module=module, result=result))

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
