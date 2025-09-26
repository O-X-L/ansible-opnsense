from ansible_collections.ansibleguy.opnsense.plugins.module_utils.test.util_pytest import log_test
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.test.testdata.base_testdata import \
    MockOPNsenseController


class MockHttpResponse:
    def __init__(self, res: dict):
        self._res = res
        self.status_code = 200

    def json(self) -> dict:
        return self._res


class MockHttpClient:
    def __init__(self, mock_handler: MockOPNsenseController, base_url: str = '', **kwargs):
        self._mock_handler: MockOPNsenseController = mock_handler
        self.base_url = base_url
        del kwargs

    def _process(self, method: str, url: str, data: dict = None) -> MockHttpResponse:
        log_test(f'{method} | {url}')
        location = url.replace(self.base_url, '')
        parts = location.split('/')
        commands = self._mock_handler.commands()
        if len(parts) < 3:
            return MockHttpResponse(MockOPNsenseController.RES_ERROR)

        cmd = parts[2]

        if cmd not in commands:
            return MockHttpResponse(MockOPNsenseController.RES_ERROR)

        cmd = commands[cmd]
        route_kwargs = self._mock_handler.route_kwargs(cmd)

        if 'uuid' in route_kwargs and len(parts) < 4:
            return MockHttpResponse(MockOPNsenseController.RES_ERROR)

        if 'uuid' in route_kwargs and 'data' in route_kwargs:
            res = cmd(uuid=parts[3], data=data)

        elif 'uuid' in route_kwargs:
            res = cmd(uuid=parts[3])

        elif 'data' in route_kwargs:
            res = cmd(data=data)

        else:
            res = cmd()

        return MockHttpResponse(res)

    def get(self, url: str) -> MockHttpResponse:
        return self._process('get', url)

    def post(self, url: str, json: dict = None, **kwargs) -> MockHttpResponse:
        del kwargs
        return self._process('post', url, data=json)

    def close(self):
        return


def pytest_mock_http_responses(mocker, handler: MockOPNsenseController):
    """
    Mock httpx.Client to unit-test 'around' it

    :param mocker: pytest mocker instance
    :param handler: A MockOPNsenseController instance that handles the HTTP-response logic
    :return: None
    """
    mock_resolver = mocker.patch('httpx.Client', autospec=True)
    mock_resolver.return_value = MockHttpClient(mock_handler=handler)
