import pytest
from os import environ

from ansible_collections.oxlorg.opnsense.plugins.module_utils.test.mock_pytest import \
    pytest_mock_http_responses, DUMMY_MODULE
from ansible_collections.oxlorg.opnsense.plugins.module_utils.test.util_pytest import log_test
from ansible_collections.oxlorg.opnsense.plugins.module_utils.test.testdata.base_testdata import \
    MockOPNsenseController, GenericTestdata


def test_session_creation():
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.api import Session
    s = Session(module=DUMMY_MODULE)
    s.close()


def test_session_contextmanager():
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.api import Session
    with Session(module=DUMMY_MODULE):
        pass


class Testdata(MockOPNsenseController):
    def commands(self) -> dict:
        return {
            'get': self._get,
            'set': self._set,
        }


def test_requests(mocker):
    log_test('api-requests')

    cnf = {'module': 'module', 'controller': 'controller'}

    pytest_mock_http_responses(
        mocker=mocker,
        handler=Testdata()
    )

    from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.api import Session, single_get, single_post
    with Session(module=DUMMY_MODULE) as s:
        res = s.get({**cnf, 'command': 'get'})
        assert len(res) == 0

        res = s.post({**cnf, 'command': 'set'})
        assert res == MockOPNsenseController.RES_ERROR

    assert single_get(module=DUMMY_MODULE, cnf={**cnf, 'command': 'get'}) == {}
    assert single_post(module=DUMMY_MODULE, cnf={**cnf, 'command': 'set'}) == MockOPNsenseController.RES_ERROR


def test_check_testdata(mocker):
    log_test('api-check-testdata')

    cnf = {'module': 'module', 'controller': 'controller'}

    testdata = GenericTestdata()
    pytest_mock_http_responses(
        mocker=mocker,
        handler=testdata,
    )

    from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.api import Session, single_get, single_post
    with Session(module=DUMMY_MODULE) as s:
        res_empty = {'test': {'tests': {'test': {}}}}

        # no entries exist
        res = s.get({**cnf, 'command': 'get'})
        assert res == res_empty
        assert res == testdata.pack_data({})

        res = s.post({**cnf, 'command': 'set_test'})
        assert res == MockOPNsenseController.RES_ERROR
        res = s.post({**cnf, 'command': 'set_test', 'params': '<uuid>'})
        assert res == MockOPNsenseController.RES_ERROR
        res = s.post({**cnf, 'command': 'set_test', 'params': '<uuid>', 'data': {'test': 'x'}})
        assert res == MockOPNsenseController.RES_ERROR

        res = s.post({**cnf, 'command': 'del_test'})
        assert res == MockOPNsenseController.RES_ERROR
        res = s.post({**cnf, 'command': 'del_test', 'params': '<uuid>'})
        assert res == MockOPNsenseController.RES_ERROR

        # create entry
        res = s.post({**cnf, 'command': 'add_test', 'data': {'p1': 'a'}})
        assert res == MockOPNsenseController.RES_SUCCESS

        # list should contain new entry in {'<uuid>': '<entry>'} format
        res = s.get({**cnf, 'command': 'get'})
        entries = testdata.unpack_data(res)
        assert len(entries) == 1
        entry_key = list(entries.keys())[0]

        assert res == {'test': {'tests': {'test': {
            entry_key: {'p1': 'a'},
        }}}}
        assert list(entries.values()) == [{'p1': 'a'}]

        # update entry
        res = s.post({**cnf, 'command': 'set_test'})
        assert res == MockOPNsenseController.RES_ERROR
        res = s.post({**cnf, 'command': 'set_test', 'params': '<uuid>'})
        assert res == MockOPNsenseController.RES_ERROR
        res = s.post({**cnf, 'command': 'set_test', 'params': '<uuid>', 'data': {'p1': 'x'}})
        assert res == MockOPNsenseController.RES_ERROR
        res = s.post({**cnf, 'command': 'set_test', 'params': entry_key, 'data': {'p1': 'aa'}})
        assert res == MockOPNsenseController.RES_SUCCESS

        # checking that entry was updated
        res = s.get({**cnf, 'command': 'get'})
        entries = testdata.unpack_data(res)
        assert len(entries) == 1
        assert entries[entry_key] == {'p1': 'aa'}

        # deleting entry
        res = s.post({**cnf, 'command': 'del_test'})
        assert res == MockOPNsenseController.RES_ERROR
        res = s.post({**cnf, 'command': 'del_test', 'params': '<uuid>'})
        assert res == MockOPNsenseController.RES_ERROR
        res = s.post({**cnf, 'command': 'del_test', 'params': entry_key})
        assert res == MockOPNsenseController.RES_SUCCESS

        # checking that the entry was deleted
        res = s.get({**cnf, 'command': 'get'})
        assert res == res_empty


@pytest.mark.parametrize('env_val, httpx_avail, requests_avail, expected', [
    ('', True, True, 'httpx'),
    ('', False, True, 'requests'),
    ('httpx', True, True, 'httpx'),
    ('requests', True, True, 'requests'),
    ('invalid_val', True, True, 'httpx'),
    ('requests', False, True, 'requests'),
    ('httpx', False, True, 'requests'),
    ('requests', True, False, 'httpx'),
])
def test_session_client_selection(mocker, env_val, httpx_avail, requests_avail, expected):
    """Tests the client priority fallback logic based on env vars and availability."""
    mocker.patch.dict(
        "ansible_collections.oxlorg.opnsense.plugins.module_utils.base.api.environ",
        {**environ, "HTTP_CLIENT": env_val}
    )

    # Patch the availability flags in the api module
    mocker.patch('ansible_collections.oxlorg.opnsense.plugins.module_utils.base.api.HAS_LIB_HTTPX', httpx_avail)
    mocker.patch('ansible_collections.oxlorg.opnsense.plugins.module_utils.base.api.HAS_LIB_REQUESTS', requests_avail)

    # Bypass the actual network setup steps for this unit test
    mocker.patch('ansible_collections.oxlorg.opnsense.plugins.module_utils.base.api.check_host')
    mocker.patch('ansible_collections.oxlorg.opnsense.plugins.module_utils.base.api.check_or_load_credentials',
                 return_value=('key', 'secret'))
    mocker.patch('ansible_collections.oxlorg.opnsense.plugins.module_utils.base.api.Session._start_session_lib_httpx',
                 return_value='httpx_mock')
    mocker.patch(
        'ansible_collections.oxlorg.opnsense.plugins.module_utils.base.api.Session._start_session_lib_requests',
        return_value='requests_mock')

    from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.api import Session

    session = Session(module=DUMMY_MODULE)
    assert session._http_client_lib == expected


@pytest.mark.parametrize('backend', ['httpx', 'requests'])
def test_session_request_routing(mocker, backend):
    """Tests that the correct underlying library methods are called with the proper URL formats."""
    mocker.patch.dict(
        "ansible_collections.oxlorg.opnsense.plugins.module_utils.base.api.environ",
        {**environ, "HTTP_CLIENT": backend}
    )

    mocker.patch('ansible_collections.oxlorg.opnsense.plugins.module_utils.base.api.check_host')
    mocker.patch('ansible_collections.oxlorg.opnsense.plugins.module_utils.base.api.check_or_load_credentials',
                 return_value=('key', 'secret'))
    mocker.patch('ansible_collections.oxlorg.opnsense.plugins.module_utils.base.api.debug_api')
    mocker.patch('ansible_collections.oxlorg.opnsense.plugins.module_utils.base.api.check_response',
                 return_value={'status': 'ok'})

    from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.api import Session

    session = Session(module=DUMMY_MODULE)

    # Mock the actual client instances
    mock_get = mocker.MagicMock()
    session.s.get = mock_get

    cnf = {'module': 'test_mod', 'controller': 'test_cont', 'command': 'test_cmd'}
    session.get(cnf=cnf)

    call_url = "test_mod/test_cont/test_cmd"

    assert session._http_client_lib == backend
    if backend == 'httpx':
        mock_get.assert_called_once_with(url=call_url)

    else:
        full_url = f"{session.s.base_url}/{call_url}"
        mock_get.assert_called_once_with(url=full_url, timeout=session.s.default_timeout)
