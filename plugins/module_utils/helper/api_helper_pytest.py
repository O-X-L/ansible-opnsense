import pytest


def test_placeholder():
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.helper.api import \
        _load_credential_file, check_or_load_credentials, check_host, \
        get_params_path, _clean_response, debug_api, check_response, api_pretty_exception, \
        ssl_verification_lib_httpx, ssl_verification_lib_requests


def test_check_response_failure_omits_request_body():
    # a failed API call must not echo the POST body (it holds e.g. the plaintext 'password')
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.helper.api import \
        check_response

    class _Req:
        body = 'username=admin&password=SUPERSECRET'

    class _Resp:
        status_code = 400
        reason = 'Bad Request'
        url = 'https://opnsense.example/api/openvpn/instances/add'
        text = '{"result":"failed"}'

        def __init__(self):
            self.request = _Req()

        def json(self):
            return {'result': 'failed'}

    class _Module:
        params = {}

        def fail_json(self, msg):
            raise RuntimeError(msg)

    with pytest.raises(RuntimeError) as err:
        check_response(module=_Module(), cnf={}, http_client_lib='requests', response=_Resp())

    assert 'SUPERSECRET' not in str(err.value)
    assert '400' in str(err.value) and 'failed' in str(err.value)
