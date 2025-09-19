from unittest.mock import Mock
import pytest

@pytest.mark.parametrize('aliastype, value, valid', [
    ('port', '10', True),
    ('port', '999999', False),
    ('port', '!10', False),
    ('port', '20:21', True),
    ('port', '20:999999', False),
    ('port', 'alias1', True),
    ('port', 'smtp', True),
    ('port', 'notsmtp', False),
    ('host', '192.168.1.1', True),
    ('host', '192.168.1.1-192.168.1.2', True),
    ('host', '!192.168.1.1', True),
    ('host', 'ansibleguy.net', True),
    ('host', '!ansibleguy.net', False),
    ('host', 'alias1', True),
    ('network', '192.168.1.1', True),
    ('network', '!192.168.1.1', True),
    ('network', '192.168.1.0/24', True),
    ('network', '!192.168.1.0/24', True),
    ('network', '192.168.1.0/255.255.255.0', True),
    ('network', '!192.168.1.0/255.255.255.0', True),
    ('network', '192.168.2.0/0.0.0.255', True),
    ('network', '!192.168.2.0/0.0.0.255', True),
    ('network', 'alias1', True),
    ('networkgroup', 'alias1', True),
    ('networkgroup', 'noalias', False),
    ('mac', '00:11:22:33:44:55', True),
    ('mac', '00:11:22', True),
    ('mac', 'aA:bB:cC:dD:eE:fF', True),
    ('mac', '00:11:22:', False),
    ('mac', '00:11:22:3', False),
    ('mac', '00:11:22:44:55:66:77', False),
    ('asn', '0', False),
    ('asn', '10', True),
    ('asn', '4294967297', False),
])
def test_validate_values(aliastype, value, valid):
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.alias import validate_values

    error_func = Mock()

    validate_values(dict(type=aliastype, content=[value]), error_func, [{'name': 'alias1'}])

    if valid:
        error_func.assert_not_called()
    else:
        error_func.assert_called_once()


def test_build_updatefreq():
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.alias import build_updatefreq

    assert build_updatefreq(2.0) == 2
    assert build_updatefreq(2) == 2
    assert build_updatefreq(1.9) == 1.9
    assert build_updatefreq('1.9') == 1.9
    assert build_updatefreq('') == ''
    assert build_updatefreq(None) is None


def test_placeholder():
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.alias import \
        compare_aliases, builtin_alias, filter_builtin_alias
