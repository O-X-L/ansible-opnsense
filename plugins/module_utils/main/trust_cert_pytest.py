import pytest

from ansible_collections.oxlorg.opnsense.plugins.module_utils.test.mock_pytest import \
    pytest_mock_http_responses, MockAnsibleModule, AnsibleError
from ansible_collections.oxlorg.opnsense.plugins.module_utils.test.testdata.trust_cert_testdata import \
    Testdata_26_7_3 as CertTestdata
from ansible_collections.oxlorg.opnsense.plugins.module_utils.test.testdata.trust_ca_testdata import SECRET

PARAMS = dict(
    description='Test Cert 1', ca='TestCA', cert_type='server', key_type='secp384r1', digest='sha256',
    lifetime=397, common_name='', country='AT', state_or_province='Styria', city='Graz',
    organization='OXL IT Services', organizational_unit='', email='it-infra@oxl.at', ocsp_uri='',
    san_dns=['test1.template.oxl.app', 'test2.template.oxl.app'], san_ip=['192.168.1.1', '192.168.2.1'],
    san_email=[], san_uri=[], match_fields=['description'], state='present',
)
PARAMS_OPENVPN = {
    **PARAMS, 'description': 'OpenVPN Server', 'ca': 'OpenVPN', 'key_type': '2048', 'common_name': 'OpenVPN Server',
    'state_or_province': '', 'city': '', 'organization': '', 'email': '', 'san_dns': [],
    'san_ip': ['2001:db8::1', '192.168.1.1'],
}


def _mock(mocker) -> CertTestdata:
    testdata = CertTestdata()
    pytest_mock_http_responses(mocker=mocker, handler=testdata)
    return testdata


def _run(params: dict, check_mode: bool = False) -> dict:
    # pylint: disable=C0415
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.wrapper import module_wrapper
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.main.trust_cert import Cert

    module = MockAnsibleModule()
    module.params.update(params)
    module.check_mode = check_mode
    result = {'changed': False, 'diff': {'before': {}, 'after': {}}}
    module_wrapper(Cert(module=module, result=result))
    assert SECRET not in str(result)
    return result


def test_trust_cert_create_and_rerun(mocker):
    testdata = _mock(mocker)

    result = _run(PARAMS)
    assert result['changed']
    assert len(testdata.mutations()) == 1
    request = testdata.mutations()[0][1]
    assert request['action'] == 'internal'
    assert request['private_key_location'] == 'firewall'
    assert request['caref'] == '6adf83700f877'
    assert request['cert_type'] == 'server_cert'
    assert request['altnames_dns'] == 'test1.template.oxl.app\ntest2.template.oxl.app'
    assert request['altnames_ip'] == '192.168.1.1\n192.168.2.1'
    assert request['commonname'] == ''

    result = _run(PARAMS)
    assert not result['changed']
    assert len(testdata.mutations()) == 1


def test_trust_cert_existing_ipv6_san(mocker):
    testdata = _mock(mocker)
    assert not _run(PARAMS_OPENVPN)['changed']
    assert len(testdata.mutations()) == 0


def test_trust_cert_check_mode(mocker):
    testdata = _mock(mocker)
    assert _run(PARAMS, check_mode=True)['changed']
    assert len(testdata.mutations()) == 0


@pytest.mark.parametrize('changed', [
    {'san_dns': ['test1.template.oxl.app']},
    {'san_ip': ['192.168.1.1']},
    {'cert_type': 'client'},
    {'ca': 'OpenVPN'},
    {'lifetime': 30},
    {'city': 'Vienna'},
])
def test_trust_cert_immutable(mocker, changed: dict):
    testdata = _mock(mocker)
    _run(PARAMS)

    with pytest.raises(AnsibleError, match='cannot be changed without re-issuing'):
        _run({**PARAMS, **changed})

    assert len(testdata.mutations()) == 1
    assert len(testdata.regenerated) == 0


def test_trust_cert_rename_does_not_reissue(mocker):
    testdata = _mock(mocker)
    params = {**PARAMS_OPENVPN, 'description': 'OpenVPN Server renamed', 'match_fields': ['common_name']}

    result = _run(params)
    assert result['changed']
    request = testdata.mutations()[-1][1]
    assert request['action'] == 'manual'
    assert request['descr'] == 'OpenVPN Server renamed'
    assert 'prv_payload' not in request
    assert len(testdata.regenerated) == 0

    assert not _run(params)['changed']


@pytest.mark.parametrize('san', [
    {'san_dns': ['a.example.com,b.example.com']},
    {'san_dns': ['']},
    {'san_ip': ['not-an-ip']},
])
def test_trust_cert_invalid_san(mocker, san: dict):
    testdata = _mock(mocker)
    with pytest.raises(AnsibleError):
        _run({**PARAMS, **san})

    assert len(testdata.mutations()) == 0


def test_trust_cert_self_signed(mocker):
    testdata = _mock(mocker)
    _run({**PARAMS, 'ca': ''})
    assert testdata.mutations()[-1][1]['caref'] == ''


def test_trust_cert_delete(mocker):
    testdata = _mock(mocker)
    result = _run({**PARAMS_OPENVPN, 'state': 'absent'})
    assert result['changed']
    assert testdata.mutations()[-1][0] == 'del'
    assert not _run({**PARAMS_OPENVPN, 'state': 'absent'})['changed']
