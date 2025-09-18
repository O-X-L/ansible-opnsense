class MockHttpResponse:
    def __init__(self, res: dict):
        self._res = res
        self.status_code = 200

    def json(self) -> dict:
        return self._res


class MockHttpClient:
    def __init__(self, mock_responses: dict, base_url: str = '', **kwargs):
        self._mock_responses = mock_responses
        self.base_url = base_url
        del kwargs

    def get(self, url: str) -> MockHttpResponse:
        location = url.replace(self.base_url, '')
        return MockHttpResponse(self._mock_responses[f'get-{location}'])

    def post(self, url: str, **kwargs) -> MockHttpResponse:
        del kwargs
        location = url.replace(self.base_url, '')
        return MockHttpResponse(self._mock_responses[f'post-{location}'])

    def close(self):
        return


def pytest_mock_http_responses(mocker, responses: dict):
    """
    Mock httpx.Client to unit-test 'around' it

    :param mocker: pytest mocker instance
    :param responses: A mapping of '<get/post>-<HTTP-LOCATION>' => response dict
    :return: None
    """
    mock_resolver = mocker.patch('httpx.Client', autospec=True)
    mock_resolver.return_value = MockHttpClient(mock_responses=responses)
