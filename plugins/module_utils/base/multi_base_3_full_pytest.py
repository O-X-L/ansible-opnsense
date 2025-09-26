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
    profiling=dict(type='bool'),
    match_fields=dict(type='list', elements='str'),
)
PARAM_DEFAULTS = {
    'reload': False, 'debug': False, 'profiling': False, 'match_fields': ['p1'],
}
PARAM_ENTRY_DEFAULTS = {
    'enabled': True, 'state': 'present', 'profiling': False, 'debug': False, 'p2': '', 'p3': '',
}

class MockOPNsenseModuleMulti(MockOPNsenseModule):
    FIELD_ID = 'p1'
    FIELDS_CHANGE = ['p2', 'p3', 'enabled']
    FIELDS_TYPING = {
        'bool': ['enabled'],
    }
    FIELDS_ALL = [FIELD_ID]
    FIELDS_ALL.extend(FIELDS_CHANGE)


@pytest.mark.parametrize('mc, entry_args, raises', [
    (
        {},
        BASE_PARAMS,
        None,
    ),
    (
        {},
        {**BASE_PARAMS, 'p2': {'type': 'int', 'required': True}},
        AnsibleWarning,
    ),
    (
        {'fail_verify': True},
        {**BASE_PARAMS, 'p2': {'type': 'int', 'required': True}},
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
        {**PARAM_ENTRY_DEFAULTS, 'p1': 'test1', 'p2': 'a'},
        {**PARAM_ENTRY_DEFAULTS, 'p1': 'test2'},
        {**PARAM_ENTRY_DEFAULTS, 'p1': 'test3', 'state': 'absent'},
        {**PARAM_ENTRY_DEFAULTS, 'p1': 'test4', 'state': 'present'},
        {**PARAM_ENTRY_DEFAULTS, 'p1': 'test5', 'enabled': True},
        {**PARAM_ENTRY_DEFAULTS, 'p1': 'test6', 'enabled': False},
    ]
    am.params['multi_control'] = {**am.params['multi_control'], **mc}
    am.params = {**PARAM_DEFAULTS, **am.params}

    mm = MultiModule(
        module=am,
        result=ANSIBLE_RESULT,
        entry_args=entry_args,
        kind='test',
        obj=MockOPNsenseModuleMulti,
        validation=True,
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


@pytest.mark.parametrize('mc, entry_args', [
    (
        {},
        BASE_PARAMS,
    ),
])
def test_multi_full_create(mocker, mc, entry_args):
    log_test('multi-full-create')

    testdata = GenericTestdata()
    pytest_mock_http_responses(
        mocker=mocker,
        handler=testdata,
    )

    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.multi import build_multi_mod_args, \
        MultiModule

    ### CREATE ###
    am = MockAnsibleModuleWarnException()
    am.params = get_ansible_module_multi_params()
    am.params['multi'] = [
        {**PARAM_ENTRY_DEFAULTS, 'p1': 'test1', 'p2': 'a'},
        {**PARAM_ENTRY_DEFAULTS, 'p1': 'test2'},
        {**PARAM_ENTRY_DEFAULTS, 'p1': 'test3', 'state': 'absent'},
        {**PARAM_ENTRY_DEFAULTS, 'p1': 'test4', 'state': 'present'},
        {**PARAM_ENTRY_DEFAULTS, 'p1': 'test5', 'enabled': True},
        {**PARAM_ENTRY_DEFAULTS, 'p1': 'test6', 'enabled': False},
    ]
    am.params['multi_control'] = {**am.params['multi_control'], **mc}
    am.params = {**PARAM_DEFAULTS, **am.params}

    mm = MultiModule(
        module=am,
        result=ANSIBLE_RESULT,
        entry_args=entry_args,
        kind='test',
        obj=MockOPNsenseModuleMulti,
    )

    assert mm._has_multi_crud_entries
    assert not mm._has_multi_purge_entries
    assert not mm._has_multi_purge_filters

    assert not mm._is_multi_purge()
    assert mm._is_multi_crud()

    mm.process()

    # [{'p1': 'test1', 'p2': 'a', 'p3': '', 'enabled': 1},
    #  {'p1': 'test2', 'p2': '', 'p3': '', 'enabled': 1},
    #  {'p1': 'test4', 'p2': '', 'p3': '', 'enabled': 1},
    #  {'p1': 'test5', 'p2': '', 'p3': '', 'enabled': 1},
    #  {'p1': 'test6', 'p2': '', 'p3': '', 'enabled': 0}]
    entries = list(testdata.state.values())

    assert len(entries) == 5
    for entry in entries:
        assert entry['p3'] == ''
        assert entry['p1'] != 'test3'  # absent

        if entry['p1'] == 'test1':
            assert entry['p2'] == 'a'

        else:
            assert entry['p2'] == ''

        if entry['p1'] != 'test6':
            assert entry['enabled'] == 1

        else:
            assert entry['enabled'] == 0

    ### PARTIAL UPDATE ###
    am.params = get_ansible_module_multi_params()
    am.params['multi'] = [
        {**PARAM_ENTRY_DEFAULTS, 'p1': 'test1', 'p2': 'b'},
        {**PARAM_ENTRY_DEFAULTS, 'p1': 'test3', 'state': 'absent'},
        {**PARAM_ENTRY_DEFAULTS, 'p1': 'test4', 'state': 'absent'},
        {**PARAM_ENTRY_DEFAULTS, 'p1': 'test5', 'enabled': False},
        {**PARAM_ENTRY_DEFAULTS, 'p1': 'test6', 'enabled': True},
    ]
    am.params['multi_control'] = {**am.params['multi_control'], **mc}
    am.params = {**PARAM_DEFAULTS, **am.params}

    mm = MultiModule(
        module=am,
        result=ANSIBLE_RESULT,
        entry_args=entry_args,
        kind='test',
        obj=MockOPNsenseModuleMulti,
    )
    mm.process()

    # [{'p1': 'test1', 'p2': 'b', 'p3': '', 'enabled': 1},
    #  {'p1': 'test2', 'p2': '', 'p3': '', 'enabled': 1},
    #  {'p1': 'test5', 'p2': '', 'p3': '', 'enabled': 0},
    #  {'p1': 'test6', 'p2': '', 'p3': '', 'enabled': 1}]
    entries = list(testdata.state.values())

    assert len(entries) == 4
    assert 'test2' in [e['p1'] for e in entries]  # we did not manage this entry; it should not be touched
    def check2(_entries):
        for e in _entries:
            assert e['p3'] == ''
            assert e['p1'] != 'test3'  # absent
            assert e['p1'] != 'test4'  # absent

            if e['p1'] == 'test1':
                assert e['p2'] == 'b'

            else:
                assert e['p2'] == ''

            if e['p1'] != 'test5':
                assert e['enabled'] == 1

            else:
                assert e['enabled'] == 0

    check2(entries)

    ### PURGE UNCONFIGURED ###
    am.params['multi_control']['purge_unconfigured'] = True

    mm = MultiModule(
        module=am,
        result=ANSIBLE_RESULT,
        entry_args=entry_args,
        kind='test',
        obj=MockOPNsenseModuleMulti,
    )
    mm.process()

    # [{'p1': 'test1', 'p2': 'b', 'p3': '', 'enabled': 1},
    #  {'p1': 'test5', 'p2': '', 'p3': '', 'enabled': 0},
    #  {'p1': 'test6', 'p2': '', 'p3': '', 'enabled': 1}]
    entries = list(testdata.state.values())

    assert len(entries) == 3
    assert 'test2' not in [e['p1'] for e in entries]
    check2(entries)

    ### PURGE ALL ###
    am.params['multi_control']['purge_unconfigured'] = False
    am.params['multi_control']['purge_all'] = True

    mm = MultiModule(
        module=am,
        result=ANSIBLE_RESULT,
        entry_args=entry_args,
        kind='test',
        obj=MockOPNsenseModuleMulti,
    )
    mm.process()

    assert len(testdata.state) == 0
