#!/usr/bin/env python3

# pylint: disable=R0915

from sys import argv
from sys import exit as sys_exit
from pathlib import Path
from os import listdir

MAX_MODULES_TO_TEST = 20  # else it will take forever :(
PREFIX_ALL = [
    'plugins/module_utils/base/'
]
PATH_ALL = [
    'plugins/module_utils/helper/api.py',
    'plugins/module_utils/helper/main.py',
    'plugins/module_utils/helper/utils.py',
    'plugins/module_utils/helper/validate.py',
    'plugins/module_utils/helper/wrapper.py',
    'plugins/module_utils/defaults/main.py',
]
PREFIX_MODULES = [
    'plugins/modules/',
    'plugins/module_utils/main/',
    'tests/',
]
PATH_MAPPING = {
    'plugins/module_utils/defaults/alias.py': ['alias', 'alias_multi'],
    'plugins/module_utils/defaults/bind_record.py': ['bind_record', 'bind_record_multi'],
    'plugins/module_utils/defaults/ipsec_auth.py': ['ipsec_auth_local', 'ipsec_auth_remote'],
    'plugins/module_utils/defaults/openvpn.py': ['openvpn_server', 'openvpn_client'],
    'plugins/module_utils/defaults/rule.py': [
        'rule', 'rule_multi', 'rule_purge', 'shaper_rule', 'nat_one_to_one', 'nat_source',
    ],
    'plugins/module_utils/helper/alias.py': ['alias', 'alias_multi', 'alias_purge'],
    'plugins/module_utils/helper/multi.py': ['rule_multi', 'alias_multi', 'bind_record_multi'],
    'plugins/module_utils/helper/purge.py': ['rule_purge', 'alias_purge'],
    'plugins/module_utils/helper/rule.py': ['rule', 'rule_multi', 'nat_source'],
    'plugins/module_utils/helper/system.py': ['system'],
    'plugins/module_utils/helper/unbound.py': [
        'unbound_general', 'unbound_acl', 'unbound_dnsbl', 'unbound_dot', 'unbound_forward', 'unbound_host',
        'unbound_host_alias',
    ],
}


def main(file_changes: (Path, str), file_out: (Path, str)):
    with open(file_changes, 'r', encoding='utf-8') as f:
        raw_changes = f.readlines()

    changes = []
    for p in raw_changes:
        p = p.strip()
        if p.endswith('.py') and (p.endswith('monit_test.py') or not p.endswith('_test.py')):
            changes.append(p)

        elif p.startswith('tests/') and p.endswith('.yml'):
            changes.append(p)

    valid_modules = []
    for f in listdir(Path(__file__).parent.parent / 'tests'):
        if not f.startswith('1_') and not f == '_tmpl' and not f == 'README.md':
            valid_modules.append(f.replace('.yml', ''))

    modules = []
    for path in changes:
        if len(modules) == valid_modules:
            break

        matched = False
        if path in PATH_ALL:
            modules = valid_modules
            break

        for prefix in PREFIX_ALL:
            if path.startswith(prefix):
                modules = valid_modules
                matched = True
                break

        if matched:
            continue

        possible_module = path.rsplit('/', 1)[1].replace('.py', '').replace('.yml', '')
        for prefix in PREFIX_MODULES:
            if path.startswith(prefix) and possible_module in valid_modules:
                modules.append(possible_module)
                matched = True
                break

        if matched:
            continue

        for match_path, match_modules in PATH_MAPPING.items():
            if path == match_path:
                modules.extend(match_modules)
                break

    modules = list(set(modules))
    print(f'MODULES THAT REQUIRE TESTING: {len(modules)}/{len(valid_modules)}')
    modules.sort()

    if len(modules) > MAX_MODULES_TO_TEST:
        print('\033[0;31m' + f'WARNING: TOO MANY MODULES TO TEST! WILL ONLY TEST {MAX_MODULES_TO_TEST}' + '\033[0m')
        modules = modules[:MAX_MODULES_TO_TEST]

    with open(file_out, 'w', encoding='utf-8') as f:
        out = '\n'.join(modules)
        if len(modules) > 0:
            out += '\n'

        f.write(out)


if __name__ == '__main__':
    if len(argv) < 3:
        print(
            "USAGE:\n"
            " 1 > File containing the list of changed files\n"
            " 2 > File to write the list of modules to\n"
        )
        sys_exit(1)

    FILE_CHANGES = Path(argv[1])
    FILE_OUT = Path(argv[2])
    if not FILE_CHANGES.is_file():
        raise FileNotFoundError(FILE_CHANGES)

    main(FILE_CHANGES, FILE_OUT)
