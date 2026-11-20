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
    ('host', 'oxl.at', True),
    ('host', '!oxl.at', False),
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
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.helper.alias import validate_values

    error_func = Mock()

    validate_values(dict(type=aliastype, content=[value]), error_func, [{'name': 'alias1'}])

    if valid:
        error_func.assert_not_called()
    else:
        error_func.assert_called_once()


def test_build_updatefreq():
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.helper.alias import build_updatefreq

    assert build_updatefreq(2.0) == 2
    assert build_updatefreq(2) == 2
    assert build_updatefreq(1.9) == 1.9
    assert build_updatefreq('1.9') == 1.9
    assert build_updatefreq('') == ''
    assert build_updatefreq(None) is None
    assert build_updatefreq('', default=True) == 7
    assert build_updatefreq(None, default=True) == 7
    assert build_updatefreq('0') == 0
    assert build_updatefreq('0.0') == 0


@pytest.mark.parametrize('value, expected', [
    ('0.00347', 0.00347),  # ~5 min
    ('0.000694', 0.000694),  # ~1 min
    ('0.04', 0.04),  # ~1 hour
    ('0.25', 0.25),  # 6 hours
    (0.25, 0.25),
    ('0.5', 0.5),
])
def test_build_updatefreq_keeps_precision(value, expected):
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.helper.alias import build_updatefreq

    assert build_updatefreq(value) == expected
    assert build_updatefreq(value, default=True) == expected


@pytest.mark.parametrize('declared, existing', [
    ('0.00347', '0.00347'),
    ('0.04', '0.04'),
    ('0.25', '0.25'),
    ('7', '7'),
    ('7', '7.0'),
    ('0.5', '0.5'),
    (5 / 1440, '0.003472'),  # computed value vs value stored with fewer digits
    ('0.003472222222222222', '0.00347222222222'),
    ('0.9999999', '1'),
])
def test_build_updatefreq_compare_stable(declared, existing):
    # desired value (alias: check / alias_multi: build + check) and existing value
    # (simplify_existing) are compared as str() - they must match
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.helper.alias import build_updatefreq

    desired_single = build_updatefreq(declared, default=True)
    desired_multi = build_updatefreq(build_updatefreq(declared), default=True)
    current = build_updatefreq(existing, default=False)

    assert str(desired_single) == str(current)
    assert str(desired_multi) == str(current)
    assert build_updatefreq(current) == current


def test_placeholder():
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.helper.alias import \
        compare_aliases, builtin_alias, filter_builtin_alias
