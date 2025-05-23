#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (C) 2025, AnsibleGuy <guy@ansibleguy.net>
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

# see: https://docs.opnsense.org/development/api/core/firewall.html

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.handler import \
    module_dependency_error, MODULE_EXCEPTIONS

try:
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.wrapper import module_wrapper
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.defaults.main import \
        RELOAD_MOD_ARG_DEF_FALSE, build_multi_mod_args, OPN_MOD_ARGS, STATE_MOD_ARG
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.alias import Alias
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.multi import MultiModule
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import ensure_list

except MODULE_EXCEPTIONS:
    module_dependency_error()


# DOCUMENTATION = 'https://opnsense.ansibleguy.net/modules/alias.html'
# EXAMPLES = 'https://opnsense.ansibleguy.net/modules/alias.html'


ALIAS_DEFAULTS = {
    'state': 'present',
    'enabled': True,
    'description': '',
    'type': 'host',
    'content': [],
    'debug': False,
    'updatefreq_days': 7.0,
    'interface': None
}

ALIAS_MOD_ARG_ALIASES = {
    'name': ['n'],
    'content': ['c', 'cont'],
    'type': ['t'],
    'description': ['desc'],
    'state': ['st'],
    'enabled': ['en'],
    'interface': ['int', 'if']
}


def _build_alias_args(multi: bool) -> dict:
    a = dict(
        name=dict(type='str', required=multi, aliases=ALIAS_MOD_ARG_ALIASES['name']),
        description=dict(
            type='str', required=False, default=ALIAS_DEFAULTS['description'],
            aliases=ALIAS_MOD_ARG_ALIASES['description']
        ),
        content=dict(
            type='list', required=False, default=ALIAS_DEFAULTS['content'],
            aliases=ALIAS_MOD_ARG_ALIASES['content'], elements='str',
        ),
        type=dict(type='str', required=False, choices=[
            'host', 'network', 'port', 'url', 'urltable', 'geoip', 'networkgroup',
            'mac', 'dynipv6host', 'internal', 'external',
        ], default=ALIAS_DEFAULTS['type'], aliases=ALIAS_MOD_ARG_ALIASES['type']),
        updatefreq_days=dict(
            type='float', default=ALIAS_DEFAULTS['updatefreq_days'], required=False,
            description="Update frequency used by type 'urltable' in days - "
                        "per example '0.5' for 12 hours"
        ),
        interface=dict(
            type='str', default=ALIAS_DEFAULTS['interface'],
            aliases=ALIAS_MOD_ARG_ALIASES['interface'], required=False,
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


def run_module():
    module_args = dict(
        **RELOAD_MOD_ARG_DEF_FALSE,  # default-true takes pretty long sometimes (urltables and so on)
        **_build_alias_args(multi=False),
        **build_multi_mod_args(
            entry=_build_alias_args(multi=True),
            aliases=['aliases']
        ),
        # todo: require either name or multi
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

    if len(module.params['multi']) > 0:
        mm = MultiModule(
            module=module,
            result=result,
            kind='alias',
            obj=Alias,
            entry_args=module_args['multi']['options'],
            callback_build=_multi_callback_build,
            # callback_get_existing=_multi_callback_get_existing,
            # callback_set_existing=_multi_callback_set_existing,
            callback_update_existing=_multi_callback_update_existing,
        )
        # todo: implement calling via module_wrapper
        mm.process()

    else:
        module_wrapper(Alias(module=module, result=result))

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
