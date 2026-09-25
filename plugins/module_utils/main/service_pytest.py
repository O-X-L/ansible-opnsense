from copy import deepcopy
import pytest

from ansible_collections.oxlorg.opnsense.plugins.modules import service
from ansible_collections.oxlorg.opnsense.plugins.module_utils.test.mock_pytest import (
    MockAnsibleModule, AnsibleError,
)


class Finished(Exception):
    pass


def run_service(monkeypatch, action, running=True, check=False, available=True):
    module = MockAnsibleModule()
    module.params.update(name='openssh', action=action)
    module.check_mode = check
    result = {}
    calls = []
    state = {'running': running}

    def finish(**values):
        result.update(values)
        raise Finished()

    def get(module, cnf):
        calls.append(('GET', deepcopy(cnf)))
        assert cnf == {'module': 'core', 'controller': 'service', 'command': 'search'}
        return {'rows': [{'name': 'openssh', 'id': 'openssh', 'running': int(state['running'])}]
                if available else [], 'total': int(available)}

    def post(module, cnf):
        calls.append(('POST', deepcopy(cnf)))
        assert cnf['module'] == 'core'
        assert cnf['params'] == ['openssh']
        state['running'] = cnf['command'] != 'stop'
        return {'result': 'ok'}

    module.exit_json = finish
    monkeypatch.setattr(service, 'AnsibleModule', lambda **kwargs: module)
    monkeypatch.setattr(service, 'single_get', get)
    monkeypatch.setattr(service, 'single_post', post)
    with pytest.raises(Finished):
        service.run_module()
    return result, calls


def test_openssh_supported():
    assert 'openssh' in service.SERVICES


def test_openssh_status(monkeypatch):
    result, calls = run_service(monkeypatch, 'status')
    assert not result['changed']
    assert result['data']['running'] == 1
    assert all(method == 'GET' for method, _ in calls)


@pytest.mark.parametrize('action,running', [('stop', True), ('start', False), ('restart', True)])
def test_openssh_action_routes_and_verifies(monkeypatch, action, running):
    result, calls = run_service(monkeypatch, action, running=running)
    assert result['changed']
    assert [cnf['command'] for method, cnf in calls if method == 'POST'] == [action]
    assert calls[-1][0] == 'GET'


@pytest.mark.parametrize('action,running', [('stop', False), ('start', True)])
def test_openssh_start_stop_noop(monkeypatch, action, running):
    result, calls = run_service(monkeypatch, action, running=running)
    assert not result['changed']
    assert not [method for method, _ in calls if method == 'POST']


def test_openssh_check_mode(monkeypatch):
    result, calls = run_service(monkeypatch, 'stop', check=True)
    assert result['changed']
    assert not [method for method, _ in calls if method == 'POST']


def test_openssh_missing_service_fails(monkeypatch):
    with pytest.raises(AnsibleError, match='not registered'):
        run_service(monkeypatch, 'stop', available=False)


def test_openssh_reload_rejected(monkeypatch):
    with pytest.raises(AnsibleError, match='does not support'):
        run_service(monkeypatch, 'reload')
