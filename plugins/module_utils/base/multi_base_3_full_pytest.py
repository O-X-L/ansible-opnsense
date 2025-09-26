import pytest

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.test.mock_pytest import \
    pytest_mock_http_responses, MockAnsibleModuleWarnException, get_ansible_module_multi_params, ANSIBLE_RESULT, \
    MockOPNsenseModule, AnsibleWarning, AnsibleError
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.test.util_pytest import log_test
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.test.testdata.base_testdata import GenericTestdata


# todo: add tests for create/update/partial-deletion & purge delete/disable


BASE_PARAMS = dict(
    p1=dict(type='str', required=True),
    p2=dict(type='str'),
    p3=dict(type='str'),
    state=dict(type='str'),
    enabled=dict(type='bool'),
    debug=dict(type='bool'),
    reload=dict(type='bool'),
)

@pytest.mark.parametrize('mc, entry_args, raises', [
    # (
    #     {},
    #     BASE_PARAMS,
    #     None,
    # ),
    (
        {},
        {**BASE_PARAMS, 'enabled': {'type': 'bool', 'required': True}},
        AnsibleWarning,
    ),
    (
        {'fail_verify': True},
        {**BASE_PARAMS, 'enabled': {'type': 'bool', 'required': True}},
        AnsibleError,
    ),
])
def test_multi_full_create_minimal(mocker, mc, entry_args, raises):
    log_test('multi-full-create-minimal')

    pytest_mock_http_responses(
        mocker=mocker,
        handler=GenericTestdata(),
    )

    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.multi import build_multi_mod_args, \
        MultiModule

    am = MockAnsibleModuleWarnException()
    am.params = get_ansible_module_multi_params()

    am.params['multi'] = [
        {'p1': 'test1', 'p2': 'a'},
        {'p1': 'test2'},
        {'p1': 'test3', 'state': 'absent'},
        {'p1': 'test4', 'state': 'present'},
        {'p1': 'test5', 'enabled': True},
        {'p1': 'test6', 'enabled': False},
    ]
    am.params['multi_control'] = {**am.params['multi_control'], **mc}

    mm = MultiModule(
        module=am,
        result=ANSIBLE_RESULT,
        entry_args=entry_args,
        kind='test',
        obj=MockOPNsenseModule,
    )

    assert mm._has_multi_crud_entries
    assert not mm._has_multi_purge_entries
    assert not mm._has_multi_purge_filters

    assert not mm._is_multi_purge()
    assert mm._is_multi_crud()

    if raises is not None:
        with pytest.raises(raises):
            mm.process()

    else:
        mm.process()


@pytest.mark.parametrize('mc, entry_args, raises', [
    (
        {},
        {**BASE_PARAMS, 'enabled': {'type': 'bool', 'required': True}},
        AnsibleWarning,
    ),
    (
        {'fail_verify': True},
        {**BASE_PARAMS, 'enabled': {'type': 'bool', 'required': True}},
        AnsibleError,
    ),
])
def test_multi_full_create(mocker, mc, entry_args, raises):
    log_test('multi-full-create')

    pytest_mock_http_responses(
        mocker=mocker,
        handler=GenericTestdata(),
    )

    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.multi import build_multi_mod_args, \
        MultiModule

    am = MockAnsibleModuleWarnException()
    am.params = get_ansible_module_multi_params()

    am.params['multi'] = [
        {'p1': 'test1', 'p2': 'a'},
        {'p1': 'test2'},
        {'p1': 'test3', 'state': 'absent'},
        {'p1': 'test4', 'state': 'present'},
        {'p1': 'test5', 'enabled': True},
        {'p1': 'test6', 'enabled': False},
    ]
    am.params['multi_control'] = {**am.params['multi_control'], **mc}

    mm = MultiModule(
        module=am,
        result=ANSIBLE_RESULT,
        entry_args=entry_args,
        kind='test',
        obj=MockOPNsenseModule,
    )

    assert mm._has_multi_crud_entries
    assert not mm._has_multi_purge_entries
    assert not mm._has_multi_purge_filters

    assert not mm._is_multi_purge()
    assert mm._is_multi_crud()

    if raises is not None:
        with pytest.raises(raises):
            mm.process()

    else:
        mm.process()
