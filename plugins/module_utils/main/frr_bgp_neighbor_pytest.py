import pytest


from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.module import BaseModule
from ansible_collections.oxlorg.opnsense.plugins.module_utils.main.frr_bgp_neighbor import Neighbor
from ansible_collections.oxlorg.opnsense.plugins.module_utils.test.mock_pytest import \
    pytest_mock_http_responses, MockAnsibleModule, AnsibleError
from ansible_collections.oxlorg.opnsense.plugins.module_utils.test.testdata.frr_bgp_testdata import \
    Testdata_26_7_7 as BgpTestdata, PEER_GROUPS

# the neighbor seeded in the testdata, as a user would declare it
PARAMS = dict(
    description='ANSIBLE_TEST_1_1', match_fields=['description'], state='present', enabled=True, reload=True,
    ip='10.0.0.1', as_number=64496, local_as=None, remote_as_mode=None, password=None, weight=None,
    local_ip=None, source_int=None, ipv6_link_local_int=None, next_hop_self=False, next_hop_self_all=False,
    multi_hop=False, family=None, multi_protocol=None, rrclient=False, soft_reconfiguration_inbound=False,
    bfd=False, bfd_strict=False, send_default_route=False, as_override=False, remove_private_as='',
    allow_as_in='', disable_connected_check=False, attribute_unchanged='', capabilities=[], keepalive=60,
    hold_down=180, connect_timer=None, prefix_list_in=None, prefix_list_out=None, route_map_in=None,
    route_map_out=None, peer_group=None,
)
# the options os-frr 2.0 added to a neighbor
OPTIONS = dict(
    local_as=64499, soft_reconfiguration_inbound=True, bfd=True, bfd_strict=True, remove_private_as='replace_all',
    allow_as_in='3', attribute_unchanged='next-hop', capabilities=['extended-nexthop', 'fqdn'],
    peer_group='ANSIBLE_TEST_PG',
)


def _mock(mocker, **kwargs) -> BgpTestdata:
    testdata = BgpTestdata(**kwargs)
    pytest_mock_http_responses(mocker=mocker, handler=testdata)
    return testdata


def _run(params: dict, check_mode: bool = False) -> dict:
    # pylint: disable=C0415
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.wrapper import module_wrapper

    module = MockAnsibleModule()
    module.params.update(params)
    module.check_mode = check_mode
    result = {'changed': False, 'diff': {'before': {}, 'after': {}}}
    module_wrapper(Neighbor(module=module, result=result))
    return result


def test_frr_bgp_neighbor_existing_unchanged(mocker):
    # a neighbor as 26.7 returns it - with all the fields the module did not know - reads back as unchanged
    testdata = _mock(mocker)
    result = _run(PARAMS)
    assert not result['changed']
    assert len(testdata.mutations()) == 0


def test_frr_bgp_neighbor_add_with_options(mocker):
    testdata = _mock(mocker)
    params = {**PARAMS, **OPTIONS, 'description': 'ANSIBLE_TEST_1_2', 'ip': '10.0.2.1'}

    result = _run(params)
    assert result['changed']
    assert [call[0] for call in testdata.mutations()] == ['add', 'reconfigure']
    posted = testdata.mutations()[0][1]
    assert str(posted['localas']) == '64499'
    assert str(posted['soft_reconfiguration_inbound']) == '1'
    assert str(posted['bfd_strict']) == '1'
    # the API stores the FRR command-argument, the module shows the option-name
    assert posted['removeprivateas'] == 'remove-private-AS all replace-AS'
    assert str(posted['allowas_in']) == '3'
    assert posted['attributeunchanged'] == 'next-hop'
    assert posted['capabilities'] == 'extended-nexthop,fqdn'
    # the peer group is linked by its uuid, resolved from the name
    assert posted['peergroup'] == list(PEER_GROUPS.keys())[0]

    result = _run({**params, 'capabilities': ['fqdn', 'extended-nexthop']})
    assert not result['changed']
    assert len(testdata.mutations()) == 2


@pytest.mark.parametrize('changed', [{k: v} if k != 'bfd_strict' else {'bfd': True, k: v} for k, v in OPTIONS.items()])
def test_frr_bgp_neighbor_change_option(mocker, changed: dict):
    testdata = _mock(mocker)
    result = _run({**PARAMS, **changed})
    assert result['changed']
    assert [call[0] for call in testdata.mutations()] == ['set', 'reconfigure']


def test_frr_bgp_neighbor_unknown_peer_group(mocker):
    testdata = _mock(mocker)
    with pytest.raises(AnsibleError, match='peer-group'):
        _run({**PARAMS, 'peer_group': 'DOES-NOT-EXIST'})

    assert len(testdata.mutations()) == 0


def test_frr_bgp_neighbor_bfd_strict_without_bfd(mocker):
    testdata = _mock(mocker)
    with pytest.raises(AnsibleError, match='bfd_strict'):
        _run({**PARAMS, 'bfd_strict': True})

    assert len(testdata.calls) == 0


def test_frr_bgp_neighbor_check_mode(mocker):
    testdata = _mock(mocker)
    result = _run({**PARAMS, **OPTIONS}, check_mode=True)
    assert result['changed']
    assert len(testdata.mutations()) == 0


def test_frr_bgp_neighbor_list(mocker):
    testdata = _mock(mocker)
    _run({**PARAMS, **OPTIONS})

    module = MockAnsibleModule()
    module.params.update(PARAMS)
    existing = Neighbor(module=module, result={'changed': False, 'diff': {'before': {}, 'after': {}}}).get_existing()
    assert len(existing) == 1
    assert existing[0]['peer_group'] == 'ANSIBLE_TEST_PG'
    assert existing[0]['remove_private_as'] == 'replace_all'
    assert existing[0]['capabilities'] == ['extended-nexthop', 'fqdn']
    assert existing[0]['soft_reconfiguration_inbound'] is True
    assert len(testdata.mutations()) == 2


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
