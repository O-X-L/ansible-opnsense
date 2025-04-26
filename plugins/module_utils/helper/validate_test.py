import pytest

@pytest.mark.parametrize('value, result', [
    ('00:11:22:33:44:55', True),
    ('aA:bB:cC:dD:eE:fF', True),
    ('00:11:22:33:44', False),
    ('00:11:22:33:44:55:66', False),
    ('00:11:22:33:44:5', False),
    ('00:11:22:33:44:gg', False),
    ('00:11:22:33:44:', False),
])
def test_is_valid_mac_address(value, result):
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.validate import \
        is_valid_mac_address

    assert is_valid_mac_address(value) == result

@pytest.mark.parametrize('value, result', [
    ('00:11:22:33:44:55', True),
    ('aA:bB:cC:dD:eE:fF', True),
    ('00:11:22:33:44', True),
    ('00:11:22:33', True),
    ('00:11:22', True),
    ('00:11', True),
    ('00', False),
    ('00:11:22:33:44:55:66', False),
    ('00:11:22:33:44:5', False),
    ('00:11:22:33:44:gg', False),
    ('00:11:22:33:44:', False),
])
def test_is_valid_partial_mac_address(value, result):
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.validate import \
        is_valid_partial_mac_address

    assert is_valid_partial_mac_address(value) == result

@pytest.mark.parametrize('value, result', [
    ('1.2.3.4', True),
    ('1.2.3.400', False),
    ('.2.3.4', False),
    ('1.2.a.4', False),
    ('1.2.3.0/24', False),
    ('2001:0db8:85a3:08d3:1319:8a2e:0370:7344', True),
    ('2001:0db8:85a3:08d3:1319:8a2e:0370::', True),
    ('2001:0db8:85a3::1319:8a2e:0370::', False),
])
def test_is_ip(value, result):
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.validate import \
        is_ip

    assert is_ip(value) == result

@pytest.mark.parametrize('value, result', [
    ('1.2.3.4', True),
    ('1.2.3.4/32', True),
    ('1.2.3.0/24', True),
    ('1.2.3.0/33', False),
    ('1.2.3.0/0', False),
    ('1.2.3.400', False),
    ('.2.3.4', False),
    ('1.2.a.4', False),
    ('2001:0db8:85a3:08d3:1319:8a2e:0370:7344', True),
    ('2001:0db8:85a3:08d3:1319:8a2e:0370:7344/128', True),
    ('2001:0db8:85a3:08d3:1319:8a2e:0370::', True),
    ('2001:0db8:85a3:08d3:1319:8a2e:0370::/112', True),
    ('2001:0db8:85a3:08d3:1319:8a2e:0370::/96', False),
    ('2001:0db8:85a3::1319:8a2e:0370::', False),
])
def test_is_network(value, result):
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.validate import \
        is_network

    assert is_network(value, strict=True) == result

@pytest.mark.parametrize('value, result', [
    ('0', False),
    ('10', True),
    ('65535', True),
    ('65536', False),
    ('!10', False),
    ('20:21', True),
    ('20:999999', False),
    ('smtp', True),
    ('notsmtp', False),
])
def test_is_valid_port(value, result):
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.validate import is_valid_port

    assert is_valid_port(value) == result

@pytest.mark.parametrize('value, result', [
    ('1.2.3.4-1.2.3.6', True),
    ('!1.2.3.4-1.2.3.6', False),
    ('1.2.3.4', True),
    ('1.2.3.0/24', True),
    ('1.2.3.0/255.255.255.0', True),
    ('1.2.3.0/0.0.0.255', True),
    ('!1.2.3.4', True),
    ('!1.2.3.0/24', True),
    ('!1.2.3.0/255.255.255.0', True),
    ('!1.2.3.0/0.0.0.255', True),
    ('1.2.300.4', False),
    ('1.2.3.0/33', False),
    ('2001:0db8:85a3:08d3:1319:8a2e:0370:7344', True),
    ('2001:0db8:85a3:08d3:1319:8a2e::7344', True),
    ('2001:0db8:85a3:08d3::/64', True),
    ('2001::85a3:08d3:1319::0370:7344', False),
    ('!2001:0db8:85a3:08d3:1319:8a2e:0370:7344', True),
    ('!2001::85a3:08d3:1319::0370:7344', False),
])
def test_is_valid_network(value, result):
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.validate import is_valid_network

    assert is_valid_network(value) == result

@pytest.mark.parametrize('value, result', [
    ('1.2.3.4-1.2.3.6', True),
    ('!1.2.4.5', True),
    ('1.2.4.5', True),
    ('1.2.400.5', False),
    ('ansibleguy.net', True),
    ('2001:0db8:85a3:08d3:1319:8a2e:0370:7344', True),
    ('2001::85a3:08d3:1319::0370:7344', False),
])
def test_is_valid_host(value, result):
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.validate import is_valid_host

    assert is_valid_host(value) == result
