import pytest
from datetime import timedelta


def test_placeholder():
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.helper.api import \
        _load_credential_file, check_or_load_credentials, check_host, \
        get_params_path, debug_api, check_response, api_pretty_exception, \
        ssl_verification_lib_httpx, ssl_verification_lib_requests


class MockRequestLibHttpx:
    body = 'username=admin&password=SUPERSECRET'
    url = 'https://opnsense.example/api/openvpn/instances/add'
    method = 'POST'


class MockResponseLibHttpx:
    status_code = 400

    @staticmethod
    def json():
        return {'result': 'failed'}

    @property
    def __dict__(self) -> dict:
        return {
            'status_code': self.status_code,
            'reason': 'Bad Request',
            'text': '{"result":"failed"}',
            '_request': MockRequestLibHttpx(),
        }


class MockRequestLibRequests:
    body = 'username=admin&password=SUPERSECRET'
    method = 'POST'

    @property
    def __dict__(self) -> dict:
        return {
            'method': self.method,
            'body': 'username=admin&password=SUPERSECRET',
        }


class MockResponseLibRequests:
    status_code = 400

    @staticmethod
    def json():
        return {'result': 'failed'}

    @property
    def __dict__(self) -> dict:
        return {
            'status_code': self.status_code,
            'reason': 'Bad Request',
            'text': '{"result":"failed"}',
            'url': 'https://opnsense.example/api/openvpn/instances/add',
            'request': MockRequestLibRequests(),
        }


@pytest.mark.parametrize('response, expected', [
    (
        {
            'status_code': 200, 'headers': {'server': 'OPNsense'},
            '_request': MockRequestLibHttpx(),
            'next_request': None, 'extensions': {'http_version': b'HTTP/1.1'}, 'history': [], 'is_closed': True,
            'is_stream_consumed': True, 'default_encoding': 'utf-8', 'stream': 'whatever', '_num_bytes_downloaded': 75,
            '_decoder': 'whatever', '_elapsed': timedelta(microseconds=41331),
            '_content': b'{"result":"failed","validations":{"rule.interface":"A value is required."}}',
        },
        {
            'status_code': 200,
            'url': MockRequestLibHttpx.url,
            'method': 'POST',
            'http_client': 'httpx',
            'body': b'{"result":"failed","validations":{"rule.interface":"A value is required."}}',
            'elapsed_ms': 41331,
            'bytes_downloaded': 75,
        }
    ),
])
def test_sanitize_response_for_logging_lib_httpx(response: dict, expected: dict):
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.helper.api import \
        _sanitize_response_for_logging_lib_httpx

    result = _sanitize_response_for_logging_lib_httpx(response)
    assert len(result) == len(expected)
    for key, value in expected.items():
        assert result[key] == value


@pytest.mark.parametrize('response, expected', [
    (
        {
            '_content': b'{"result":"failed","validations":{"rule.interface":"A value is required."}}',
             '_content_consumed': True, '_next': None, 'status_code': 200, 'headers': {'server': 'OPNsense'},
             'raw': 'whatever', 'encoding': 'UTF-8', 'history': [], 'reason': 'OK',
             'url': MockRequestLibHttpx.url,
             'cookies': 'whatever', 'elapsed': timedelta(microseconds=41041),
             'request': MockRequestLibRequests(), 'connection': 'whatever'
        },
        {
            'status_code': 200,
            'url': MockRequestLibHttpx.url,
            'method': 'POST',
            'elapsed_ms': 41041,
            'http_client': 'requests',
            'reason': 'OK',
            'body': b'{"result":"failed","validations":{"rule.interface":"A value is required."}}',
        }
    ),
])
def test_sanitize_response_for_logging_lib_requests(response: dict, expected: dict):
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.helper.api import \
        _sanitize_response_for_logging_lib_requests

    result = _sanitize_response_for_logging_lib_requests(response)
    assert len(result) == len(expected)
    for key, value in expected.items():
        assert result[key] == value


@pytest.mark.parametrize('http_client', ['httpx', 'requests'])
def test_check_response_failure_omits_request_body(http_client: str):
    # a failed API call must not echo the POST body (it holds e.g. the plaintext 'password')
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.helper.api import \
        check_response

    if http_client == 'httpx':
        response = MockResponseLibHttpx()

    else:
        response = MockResponseLibRequests()

    class _Module:
        params = {}

        def fail_json(self, msg):
            raise RuntimeError(msg)

    with pytest.raises(RuntimeError) as err:
        check_response(module=_Module(), cnf={}, http_client_lib=http_client, response=response)

    assert 'SUPERSECRET' not in str(err.value)
    assert '400' in str(err.value) and 'failed' in str(err.value)
