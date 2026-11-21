import pytest

from ansible_collections.oxlorg.opnsense.plugins.module_utils.test.mock_pytest import \
    pytest_mock_http_responses, MockAnsibleModule, AnsibleError
from ansible_collections.oxlorg.opnsense.plugins.module_utils.test.testdata.trust_ca_testdata import \
    Testdata_26_7_3 as CaTestdata, SECRET

PARAMS = dict(
    description='TestCA', ca='', key_type='2048', digest='sha256', lifetime=825, common_name='OPNsense Test CA',
    country='AT', state_or_province='', city='', organization='', organizational_unit='', email='', ocsp_uri='',
    match_fields=['description'], state='present',
)
PARAMS_OPENVPN = {**PARAMS, 'description': 'OpenVPN', 'common_name': 'openvpn'}


def _mock(mocker) -> CaTestdata:
    testdata = CaTestdata()
    pytest_mock_http_responses(mocker=mocker, handler=testdata)
    return testdata


def _run(params: dict, check_mode: bool = False) -> dict:
    # pylint: disable=C0415
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.wrapper import module_wrapper
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.main.trust_ca import Ca

    module = MockAnsibleModule()
    module.params.update(params)
    module.check_mode = check_mode
    result = {'changed': False, 'diff': {'before': {}, 'after': {}}}
    module_wrapper(Ca(module=module, result=result))
    assert SECRET not in str(result)
    return result


def test_trust_ca_create_and_rerun(mocker):
    testdata = _mock(mocker)
    params = {**PARAMS, 'lifetime': 36500, 'key_type': 'secp521r1'}

    result = _run(params)
    assert result['changed']
    assert len(testdata.mutations()) == 1
    request = testdata.mutations()[0][1]
    assert request['action'] == 'internal'
    assert request['descr'] == 'TestCA'
    assert request['caref'] == ''
    assert request['commonname'] == 'OPNsense Test CA'
    assert request['key_type'] == 'secp521r1'
    assert request['lifetime'] == 36500

    # the API returns the default lifetime - the actual one must be calculated from the validity-timestamps
    result = _run(params)
    assert not result['changed']
    assert len(testdata.mutations()) == 1


def test_trust_ca_check_mode(mocker):
    testdata = _mock(mocker)
    result = _run(PARAMS, check_mode=True)
    assert result['changed']
    assert len(testdata.mutations()) == 0


@pytest.mark.parametrize('changed', [
    {'key_type': '4096'},
    {'lifetime': 3650},
    {'common_name': 'other'},
    {'country': 'DE'},
    {'ca': 'OpenVPN'},
])
def test_trust_ca_immutable(mocker, changed: dict):
    testdata = _mock(mocker)
    _run(PARAMS)

    with pytest.raises(AnsibleError, match='cannot be changed without re-issuing'):
        _run({**PARAMS, **changed})

    assert len(testdata.mutations()) == 1


def test_trust_ca_rename_keeps_ca(mocker):
    testdata = _mock(mocker)
    _run(PARAMS)

    params = {**PARAMS, 'description': 'TestCA renamed', 'match_fields': ['common_name']}
    result = _run(params)
    assert result['changed']
    assert result['diff']['before']['description'] == 'TestCA'
    assert result['diff']['after']['description'] == 'TestCA renamed'

    request = testdata.mutations()[-1][1]
    assert request['action'] == 'existing'
    assert request['descr'] == 'TestCA renamed'
    assert request['crt_payload'] != ''
    assert len(testdata.regenerated) == 0

    assert not _run(params)['changed']


def test_trust_ca_intermediate(mocker):
    testdata = _mock(mocker)
    _run({**PARAMS, 'ca': 'OpenVPN'})
    assert testdata.mutations()[-1][1]['caref'] == '65f0af2ce06c7'

    # matching by reference-id
    assert not _run({**PARAMS, 'ca': '65f0af2ce06c7'})['changed']

    with pytest.raises(AnsibleError, match='was not found'):
        _run({**PARAMS, 'description': 'other', 'ca': 'does-not-exist'})


def test_trust_ca_delete(mocker):
    testdata = _mock(mocker)
    _run(PARAMS)

    result = _run({**PARAMS, 'state': 'absent'})
    assert result['changed']
    assert testdata.mutations()[-1][0] == 'del'

    assert not _run({**PARAMS, 'state': 'absent'})['changed']


def test_trust_ca_delete_in_use(mocker):
    testdata = _mock(mocker)
    with pytest.raises(AnsibleError, match='still referenced'):
        _run({**PARAMS_OPENVPN, 'state': 'absent'})

    assert len(testdata.mutations()) == 0


def test_trust_ca_ambiguous(mocker):
    testdata = _mock(mocker)
    _run(PARAMS)
    _run({**PARAMS, 'description': 'TestCA 2'})

    with pytest.raises(AnsibleError, match='Multiple existing'):
        _run({**PARAMS, 'match_fields': ['common_name']})


def test_trust_ca_existing_has_no_secrets(mocker):
    _mock(mocker)

    # pylint: disable=C0415
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.main.trust_ca import Ca

    module = MockAnsibleModule()
    module.params.update(PARAMS)
    existing = Ca(module=module, result={}).get_existing()
    assert len(existing) == 1
    assert existing[0]['description'] == 'OpenVPN'
    assert existing[0]['lifetime'] == 825
    assert existing[0]['crt_payload'].startswith('-----BEGIN CERTIFICATE-----')
    assert SECRET not in str(existing)

    # used by the 'list' module
    raw = Ca(module=module, result={}).search_call()
    assert len(raw) == 1
    assert raw[0]['descr'] == 'OpenVPN'
    assert SECRET not in str(raw)
