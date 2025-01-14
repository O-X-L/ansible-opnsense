from re import match as regex_match
from typing import Callable
from ipaddress import ip_network, ip_address

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.defaults.main import \
    BUILTIN_ALIASES, BUILTIN_INTERFACE_ALIASES_REG
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.validate import \
    is_valid_mac_address, is_valid_url, is_valid_domain
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import \
    get_selected


def validate_values(cnf: dict, error_func: Callable, existing_entries: dict) -> None:
    v_type = cnf['type']

    if isinstance(existing_entries, dict):
        existing_entries = {
            a['name']: get_selected(a['type'])
            for a in existing_entries.values()
        }
    else:
        existing_entries = {
            a['name']: a['type']
            for a in existing_entries
        }

    for value in cnf['content']:
        error = f"Value '{value}' is invalid for type '{v_type}'!"

        if v_type == 'port':
            if value in existing_entries and existing_entries[value] == 'port':
                continue

            if str(value).find(':') != -1:
                to_check = value.split(':')

            else:
                to_check = [value]

            for _value in to_check:
                try:
                    if int(_value) < 1 or int(_value) > 65535:
                        error_func(error)

                except ValueError:
                    error_func(error)

        elif v_type == 'mac':
            # todo: support for partial mac addresses?
            if not is_valid_mac_address(value):
                error_func(error)

        elif v_type in ['url', 'urltable']:
            if not is_valid_url(value):
                error_func(error)

        elif v_type == 'network':
            if value in existing_entries and existing_entries[value] in ['network', 'host']:
                continue

            value = value[1:] if value.startswith('!') else value

            try:
                ip_network(value)

            except ValueError:
                error_func(error)

        elif v_type == 'host':
            if value in existing_entries and existing_entries[value] in ['network', 'host']:
                continue

            if is_valid_domain(value):
                continue

            for _value in value.split('-', 1):
                _value = _value[1:] if _value.startswith('!') else _value
                try:
                    ip_address(_value)

                except ValueError:
                    error_func(error)


def check_purge_filter(module: AnsibleModule, existing_rule: dict) -> bool:
    # used for 'alias_multi' and 'rule_multi'
    to_purge = True

    for filter_key, filter_value in module.params['filters'].items():
        if module.params['filter_invert']:
            # purge all except matches
            if module.params['filter_partial']:
                if str(existing_rule[filter_key]).find(filter_value) != -1:
                    to_purge = False
                    break

            else:
                if existing_rule[filter_key] == filter_value:
                    to_purge = False
                    break

        else:
            # purge only matches
            if module.params['filter_partial']:
                if str(existing_rule[filter_key]).find(filter_value) == -1:
                    to_purge = False
                    break

            else:
                if existing_rule[filter_key] != filter_value:
                    to_purge = False
                    break

    return to_purge


def compare_aliases(existing: dict, configured: dict) -> tuple:
    before = list(map(str, existing['content']))
    after = list(map(str, configured['content']))
    before.sort()
    after.sort()
    return before != after, before, after


def check_purge_configured(module: AnsibleModule, existing_alias: dict) -> bool:
    to_purge = True
    existing_name = existing_alias['name']

    for alias_name in module.params['aliases'].keys():
        if existing_name == alias_name:
            to_purge = False
            break

    return to_purge


def builtin_alias(name: str) -> bool:
    # ignore built-in aliases
    return name in BUILTIN_ALIASES or \
           regex_match(BUILTIN_INTERFACE_ALIASES_REG, name) is not None


def filter_builtin_alias(aliases: list) -> list:
    filtered = []

    for alias in aliases:
        # ignore built-in aliases
        if not builtin_alias(alias['name']):
            filtered.append(alias)

    return filtered
