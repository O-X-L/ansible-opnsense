import pytest

from ansible_collections.oxlorg.opnsense.plugins.module_utils.test.mock_pytest import \
    pytest_mock_http_responses, MockAnsibleModule, AnsibleError
from ansible_collections.oxlorg.opnsense.plugins.module_utils.test.testdata.trust_ca_testdata import \
    Testdata_26_7_3 as CaTestdata, SECRET
from ansible_collections.oxlorg.opnsense.plugins.module_utils.test.testdata.trust_cert_testdata import \
    Testdata_26_7_3 as CertTestdata

PARAMS = dict(description='OpenVPN Server', target='cert', format='crt', password='')


def _run(params: dict, no_log: bool = False) -> dict:
    # pylint: disable=C0415
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.wrapper import module_wrapper
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.main.trust_export import Export

    module = MockAnsibleModule()
    module.params.update(params)
    module.no_log = no_log
    result = {'changed': False, 'diff': {'before': {}, 'after': {}}}
    module_wrapper(Export(module=module, result=result))
    return result


@pytest.mark.parametrize('params, no_log, expected', [
    ({}, False, '-----BEGIN CERTIFICATE-----'),
    ({'format': 'prv'}, True, SECRET),
    ({'format': 'pkcs12', 'password': 'pw'}, True, '|pw)'),
])
def test_trust_export_cert(mocker, params: dict, no_log: bool, expected: str):
    testdata = CertTestdata()
    pytest_mock_http_responses(mocker=mocker, handler=testdata)

    result = _run({**PARAMS, **params}, no_log=no_log)
    assert not result['changed']
    assert expected in result['payload']
    assert len(testdata.mutations()) == 0


def test_trust_export_ca(mocker):
    pytest_mock_http_responses(mocker=mocker, handler=CaTestdata())
    result = _run({**PARAMS, 'description': 'OpenVPN', 'target': 'ca', 'format': 'prv'}, no_log=True)
    assert SECRET in result['payload']


@pytest.mark.parametrize('params, no_log, error', [
    # private keys may only be exported by 'no_log' tasks
    ({'format': 'prv'}, False, "requires the task to set 'no_log: true'"),
    ({'format': 'pkcs12'}, False, "requires the task to set 'no_log: true'"),
    ({'target': 'ca', 'description': 'OpenVPN', 'format': 'pkcs12'}, True, 'not supported'),
    ({'description': 'does-not-exist'}, False, 'was not found'),
    # internally created certificates have no CSR
    ({'format': 'csr'}, False, 'Failed to export'),
])
def test_trust_export_fail(mocker, params: dict, no_log: bool, error: str):
    testdata = CertTestdata()
    pytest_mock_http_responses(mocker=mocker, handler=testdata if params.get('target') != 'ca' else CaTestdata())

    with pytest.raises(AnsibleError, match=error):
        _run({**PARAMS, **params}, no_log=no_log)

    assert ('generate_file', 'prv') not in testdata.calls
