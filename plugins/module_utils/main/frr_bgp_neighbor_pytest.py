import pytest


from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.module import BaseModule
from ansible_collections.oxlorg.opnsense.plugins.module_utils.main.frr_bgp_neighbor import Neighbor


@pytest.fixture
def neighbor(mocker):
    mocker.patch.object(BaseModule, '__init__', return_value=None)
    instance = Neighbor(module=None, result={})
    instance.m = mocker.Mock()
    instance.m.fail_json.side_effect = AssertionError
    instance.p = {'ip': '10.0.0.1', 'family': None, 'multi_protocol': None}
    return instance


@pytest.mark.parametrize('ip, family', [
    ('10.0.0.1', ['ipv4']),
    ('fd00::1', ['ipv6']),
])
def test_family_defaults_to_ip_family(neighbor, ip, family):
    neighbor.p['ip'] = ip
    neighbor._set_family()

    assert neighbor.p['family'] == family


def test_family_is_kept(neighbor):
    neighbor.p['family'] = ['ipv6']
    neighbor._set_family()

    assert neighbor.p['family'] == ['ipv6']


@pytest.mark.parametrize('multi_protocol, family', [
    (True, ['ipv4', 'ipv6']),
    (False, ['ipv4']),
])
def test_multi_protocol(neighbor, multi_protocol, family):
    neighbor.p['multi_protocol'] = multi_protocol
    neighbor._set_family()

    assert neighbor.p['family'] == family


def test_family_and_multi_protocol_fail(neighbor):
    neighbor.p['family'] = ['ipv4']
    neighbor.p['multi_protocol'] = True

    with pytest.raises(AssertionError):
        neighbor._set_family()
