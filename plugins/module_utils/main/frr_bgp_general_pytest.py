import pytest

from ansible_collections.oxlorg.opnsense.plugins.module_utils.main.frr_bgp_general import General
from ansible_collections.oxlorg.opnsense.plugins.module_utils.test.mock_pytest import \
    pytest_mock_http_responses, MockAnsibleModule, AnsibleError
from ansible_collections.oxlorg.opnsense.plugins.module_utils.test.testdata.frr_bgp_testdata import \
    Testdata_26_7_7 as BgpTestdata

# the settings seeded in the testdata, as a user would declare them
PARAMS = dict(
    as_number=64496, distance=None, id='10.0.0.1', graceful=False, networks=[], network_import_check=True,
    log_neighbor_changes=True, enforce_first_as=True, bestpath=[], maximum_paths=None, maximum_paths_ibgp=None,
    enabled=True, reload=True,
)
# the options os-frr 2.0 added to the BGP process
OPTIONS = dict(
    enforce_first_as=False, bestpath=['as-path multipath-relax', 'compare-routerid'], maximum_paths=2,
    maximum_paths_ibgp=4,
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
    module_wrapper(General(module=module, result=result))
    return result


def test_frr_bgp_general_existing_unchanged(mocker):
    testdata = _mock(mocker)
    result = _run(PARAMS)
    assert not result['changed']
    assert len(testdata.mutations()) == 0


def test_frr_bgp_general_set_options(mocker):
    testdata = _mock(mocker)
    result = _run({**PARAMS, **OPTIONS})
    assert result['changed']
    assert [call[0] for call in testdata.mutations()] == ['set_general', 'reconfigure']
    posted = testdata.mutations()[0][1]
    assert str(posted['enforce_first_as']) == '0'
    assert posted['bestpath'] == 'as-path multipath-relax,compare-routerid'
    assert str(posted['maximumpaths']) == '2'
    assert str(posted['maximumpathsibgp']) == '4'

    result = _run({**PARAMS, **OPTIONS, 'bestpath': ['compare-routerid', 'as-path multipath-relax']})
    assert not result['changed']
    assert len(testdata.mutations()) == 2


@pytest.mark.parametrize('changed', [{k: v} for k, v in OPTIONS.items()])
def test_frr_bgp_general_change_option(mocker, changed: dict):
    testdata = _mock(mocker)
    result = _run({**PARAMS, **changed})
    assert result['changed']
    assert [call[0] for call in testdata.mutations()] == ['set_general', 'reconfigure']


@pytest.mark.parametrize('field', ['maximum_paths', 'maximum_paths_ibgp'])
def test_frr_bgp_general_invalid_maximum_paths(mocker, field: str):
    testdata = _mock(mocker)
    with pytest.raises(AnsibleError, match=field):
        _run({**PARAMS, field: 200})

    assert len(testdata.mutations()) == 0


def test_frr_bgp_general_check_mode(mocker):
    testdata = _mock(mocker)
    result = _run({**PARAMS, **OPTIONS}, check_mode=True)
    assert result['changed']
    assert len(testdata.mutations()) == 0


def test_frr_bgp_general_list(mocker):
    testdata = _mock(mocker)
    _run({**PARAMS, **OPTIONS})

    module = MockAnsibleModule()
    module.params.update(PARAMS)
    general = General(module=module, result={'changed': False, 'diff': {'before': {}, 'after': {}}})
    general.search_call()
    existing = general.get_existing()
    assert existing['enforce_first_as'] is False
    assert existing['bestpath'] == ['as-path multipath-relax', 'compare-routerid']
    assert existing['maximum_paths'] == 2
    assert len(testdata.mutations()) == 2
