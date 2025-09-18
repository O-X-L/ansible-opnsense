# pylint: disable=C0415

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.test.mock_pytest import \
    pytest_mock_http_responses, DUMMY_MODULE


def test_session_creation():
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import Session
    s = Session(module=DUMMY_MODULE)
    s.close()


def test_session_contextmanager():
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import Session
    with Session(module=DUMMY_MODULE):
        pass


def test_requests(mocker):
    mod, cont, cmd = 'module', 'controller', 'command'
    cnf = {'module': mod, 'controller': cont, 'command': cmd}
    res_get, res_post = {'msg': 'OK'}, {'msg': 'Nope'}

    pytest_mock_http_responses(
        mocker=mocker,
        responses={
            f'get-{mod}/{cont}/{cmd}': res_get,
            f'post-{mod}/{cont}/{cmd}': res_post,
        }
    )

    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import Session, single_get, single_post
    with Session(module=DUMMY_MODULE) as s:
        res = s.get(cnf)
        assert res == res_get

        res = s.post(cnf)
        assert res == res_post

    assert single_get(module=DUMMY_MODULE, cnf=cnf) == res_get
    assert single_post(module=DUMMY_MODULE, cnf=cnf) == res_post
