from time import time

TEST_FILE_CHANGES = f'/tmp/ansible-opnsense-get-changed-modules-changes-{int(time())}.txt'
TEST_FILE_MODULES = f'/tmp/ansible-opnsense-get-changed-modules-modules-{int(time())}.txt'


def _write_changes(changes: list[str]):
    with open(TEST_FILE_CHANGES, 'w', encoding='utf-8') as f:
        f.write('\n'.join(changes))


def _read_changed_modules() -> list[str]:
    with open(TEST_FILE_MODULES, 'r', encoding='utf-8') as f:
        return [m.strip() for m in f.readlines()]


def test_none():
    _write_changes([
        '.github/workflows/functional_test_pr.yml',
        'plugins/module_utils/main/test123.py',
        'scripts/get_changed_modules.py',
    ])

    from get_changed_modules import main
    main(TEST_FILE_CHANGES, TEST_FILE_MODULES)

    m = _read_changed_modules()
    assert len(m) == 0


def test_plugins_modules():
    _write_changes([
        '.github/workflows/functional_test_pr.yml',
        'plugins/modules/a-module-without-tests.py',
        'plugins/modules/alias.py',
        'plugins/module_utils/main/test123.py',
        'scripts/get_changed_modules.py',
    ])

    from get_changed_modules import main
    main(TEST_FILE_CHANGES, TEST_FILE_MODULES)

    m = _read_changed_modules()
    assert len(m) == 1
    assert m[0] == 'alias'


def test_plugins_module_utils_main():
    _write_changes([
        '.github/workflows/functional_test_pr.yml',
        'plugins/module_utils/main/alias.py',
        'plugins/module_utils/main/a-module-without-tests.py',
        'plugins/module_utils/main/test123.py',
        'scripts/get_changed_modules.py',
    ])

    from get_changed_modules import main
    main(TEST_FILE_CHANGES, TEST_FILE_MODULES)

    m = _read_changed_modules()
    assert len(m) == 1
    assert m[0] == 'alias'


def test_plugins_module_utils_base():
    _write_changes([
        '.github/workflows/functional_test_pr.yml',
        'plugins/module_utils/main/a-module-without-tests.py',
        'plugins/module_utils/base/api.py',
        'scripts/get_changed_modules.py',
    ])

    from get_changed_modules import main
    main(TEST_FILE_CHANGES, TEST_FILE_MODULES)

    m = _read_changed_modules()
    assert len(m) > 100


def test_plugins_module_utils_helper_all():
    _write_changes([
        '.github/workflows/functional_test_pr.yml',
        'plugins/module_utils/main/a-module-without-tests.py',
        'plugins/module_utils/helper/validate.py',
        'scripts/get_changed_modules.py',
    ])

    from get_changed_modules import main
    main(TEST_FILE_CHANGES, TEST_FILE_MODULES)

    m = _read_changed_modules()
    assert len(m) > 100


def test_plugins_module_utils_helper_mapping():
    _write_changes([
        '.github/workflows/functional_test_pr.yml',
        'plugins/module_utils/main/a-module-without-tests.py',
        'plugins/module_utils/helper/unbound.py',
        'scripts/get_changed_modules.py',
    ])

    from get_changed_modules import main
    main(TEST_FILE_CHANGES, TEST_FILE_MODULES)

    m = _read_changed_modules()
    assert len(m) == 7
    assert m[0].startswith('unbound_')


def test_plugins_module_utils_defaults_all():
    _write_changes([
        '.github/workflows/functional_test_pr.yml',
        'plugins/module_utils/main/a-module-without-tests.py',
        'plugins/module_utils/defaults/main.py',
        'scripts/get_changed_modules.py',
    ])

    from get_changed_modules import main
    main(TEST_FILE_CHANGES, TEST_FILE_MODULES)

    m = _read_changed_modules()
    assert len(m) > 100


def test_plugins_module_utils_defaults_mapping():
    _write_changes([
        '.github/workflows/functional_test_pr.yml',
        'plugins/module_utils/main/a-module-without-tests.py',
        'plugins/module_utils/defaults/openvpn.py',
        'scripts/get_changed_modules.py',
    ])

    from get_changed_modules import main
    main(TEST_FILE_CHANGES, TEST_FILE_MODULES)

    m = _read_changed_modules()
    assert len(m) == 2
    assert m[0].startswith('openvpn_')


def test_plugins_updated_tests():
    _write_changes([
        '.github/workflows/functional_test_pr.yml',
        'tests/openvpn_server.py',
        'tests/not-a-module.py',
        'scripts/get_changed_modules.py',
    ])

    from get_changed_modules import main
    main(TEST_FILE_CHANGES, TEST_FILE_MODULES)

    m = _read_changed_modules()
    assert len(m) == 1
    assert m[0] == 'openvpn_server'


def test_cleanup():
    from os import remove
    remove(TEST_FILE_CHANGES)
    remove(TEST_FILE_MODULES)
