import pytest

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.test.mock_pytest import \
    pytest_mock_http_responses, MockAnsibleModule, MockOPNsenseModule, MOCK_RESPONSES, \
    ANSIBLE_RESULT, AnsibleError


ANSIBLE_MODULE_MULTI_PARAMS = {
    **MockAnsibleModule.PARAMS,
    'multi': {},
    'multi_purge': {},
    'multi_control': {
        'state': None,
        'enabled': None,
        'override': {},
        'fail_verify': False,
        'fail_process': True,
        'output_info': False,
        'purge_action': 'delete',
        'purge_filter': {},
        'purge_filter_invert': False,
        'purge_filter_partial': False,
        'purge_all': False,
    },
}


def test_build_multi_mod_args():
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.multi import build_multi_mod_args
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.defaults.main import \
        OPN_MOD_ARGS

    mod_args = {
        'arg1': {'a': 'b'},
        'arg2': {'required': True},
    }
    multi_alias = 'x'
    desc = 'desc'

    a = build_multi_mod_args(
        mod_args=mod_args,
        aliases=[multi_alias],
        description=desc,
        not_required=['arg2']
    )

    assert 'multi' in a
    assert multi_alias in a['multi']['aliases']
    assert desc == a['multi']['description']

    assert 'multi_purge' in a
    assert f'{multi_alias}_purge' in a['multi_purge']['aliases']

    assert 'multi_control' in a
    assert 'options' in a['multi_control']
    mc = a['multi_control']['options']
    assert 'state' in mc
    assert 'enabled' in mc
    assert 'override' in mc
    assert 'fail_verify' in mc
    assert 'fail_process' in mc
    assert 'output_info' in mc
    assert 'purge_action' in mc
    assert 'purge_filter' in mc
    assert 'purge_filter_invert' in mc
    assert 'purge_filter_partial' in mc
    assert 'purge_all' in mc

    mo = a['multi']['options']
    for k in OPN_MOD_ARGS:
        assert k in mo


@pytest.mark.parametrize('params, result', [
    (
        {},
        False,
    ),
    (
        {'name': 'test'},
        False,
    ),
    (
        {'multi': {'test': 1}},
        False,
    ),
    (
        {'multi_purge': {'test': 1}},
        True,
    ),
    (
        {'multi_control': {**ANSIBLE_MODULE_MULTI_PARAMS['multi_control'], 'purge_filter': {'test': 1}}},
        True,
    ),
    (
        {'multi_control': {**ANSIBLE_MODULE_MULTI_PARAMS['multi_control'], 'purge_all': True}},
        True,
    ),
])
def test_multi_module_is_multi_purge(mocker, params, result):
    pytest_mock_http_responses(
        mocker=mocker,
        responses=MOCK_RESPONSES
    )

    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.multi import build_multi_mod_args, \
        MultiModule

    am = MockAnsibleModule()
    am.params = {**ANSIBLE_MODULE_MULTI_PARAMS, **params}

    mm = MultiModule(
        module=am,
        result=ANSIBLE_RESULT,
        entry_args={},
        kind='test',
        obj=MockOPNsenseModule,
    )
    assert mm._is_multi_purge() == result


@pytest.mark.parametrize('params, result', [
    (
        {},
        False,
    ),
    (
        {'name': 'test'},
        False,
    ),
    (
        {'multi': {'test': 1}},
        True,
    ),
    (
        {'multi_purge': {'test': 1}},
        False,
    ),
    (
        {'multi_control': {**ANSIBLE_MODULE_MULTI_PARAMS['multi_control'], 'purge_filter': {'test': 1}}},
        False,
    ),
    (
        {'multi_control': {**ANSIBLE_MODULE_MULTI_PARAMS['multi_control'], 'purge_all': True}},
        False,
    ),
])
def test_multi_module_is_multi_crud(mocker, params, result):
    pytest_mock_http_responses(
        mocker=mocker,
        responses=MOCK_RESPONSES
    )

    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.multi import build_multi_mod_args, \
        MultiModule

    am = MockAnsibleModule()
    am.params = {**ANSIBLE_MODULE_MULTI_PARAMS, **params}

    mm = MultiModule(
        module=am,
        result=ANSIBLE_RESULT,
        entry_args={},
        kind='test',
        obj=MockOPNsenseModule,
    )
    assert mm._is_multi_crud() == result


def test_multi_module_base(mocker):
    pytest_mock_http_responses(
        mocker=mocker,
        responses=MOCK_RESPONSES
    )

    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.multi import build_multi_mod_args, \
        MultiModule

    am = MockAnsibleModule()
    am.params = ANSIBLE_MODULE_MULTI_PARAMS.copy()
    res = ANSIBLE_RESULT
    mm = MultiModule(
        module=am,
        result=res,
        entry_args={},
        kind='test',
        obj=MockOPNsenseModule,
    )

    with pytest.raises(AnsibleError):
        # invalid multi-module parameters
        mm.process()

    # basic multi-entries
    mm.p['multi'] = [{'test': 'a'}]
    mm._init_cases()
    mm.process()
    assert mm._is_multi_crud()
    assert not mm._is_multi_purge()
    mm.p['multi'] = []

    # assert not res['changed']
    # assert len(res['diff']['before']) == 0
    # assert len(res['diff']['after']) == 0

    # purge multi-entries
    mm.p['multi_purge'] = [{'test': 'a'}]
    mm._init_cases()
    mm.process()
    assert not mm._is_multi_crud()
    assert mm._is_multi_purge()
    mm.p['multi_purge'] = []

    # purge filter without all/specific-list
    mm.p['multi_control']['purge_filter'] = {'name': 'abc'}
    mm._init_cases()
    assert not mm._is_multi_crud()
    assert mm._is_multi_purge()
    with pytest.raises(AnsibleError):
        mm.process()

    # purge filter with all
    mm.p['multi_control']['purge_all'] = True
    mm._init_cases()
    assert not mm._is_multi_crud()
    assert mm._is_multi_purge()
    mm.process()
    mm.p['multi_control']['purge_all'] = False

    # purge filter with specific-list
    mm.p['multi_purge'] = [{'test': 'a'}]
    assert not mm._is_multi_crud()
    assert mm._is_multi_purge()
    mm._init_cases()
    mm.process()
    mm.p['multi_purge'] = []

    mm.p['multi_control']['purge_filter'] = {}


@pytest.mark.parametrize('purge_filter, entry, partial, invert, result', [
    (
        {'name': 'match'},  # filter
        {'name': 'test'},  # entry
        False, False, False,
    ),
    (
        {'name': 'match'},  # filter
        {'name': 'test'},  # entry
        False, True, True,
    ),
    (
        {'name': 'match'},  # filter
        {'name': 'match'},  # entry
        False, False, True,
    ),
    (
        {'name': 'match'},  # filter
        {'name': 'match1'},  # entry
        False, False, False,
    ),
    (
        {'name': 'match'},  # filter
        {'name': 'match1'},  # entry
        True, False, True,
    ),
    (
        {'name': 'match1'},  # filter
        {'name': 'match1'},  # entry
        True, False, True,
    ),
    (
        {'name': 'match1'},  # filter
        {'name': 'match'},  # entry
        True, False, False,
    ),
    (
        {'ip_protocol': 'inet', 'action': 'block'},  # filter
        {'name': 'test', 'destination_net': '1.1.1.1', 'ip_protocol': 'inet', 'action': 'block'},  # entry
        False, False, True,
    ),
    (
        {'ip_protocol': 'inet', 'action': 'block'},  # filter
        {'name': 'test', 'destination_net': '1.1.1.1', 'ip_protocol': 'inet', 'action': 'pass'},  # entry
        False, False, False,
    ),
])
def test_multi_module_purge_filter(mocker, purge_filter, entry, partial, invert, result):
    pytest_mock_http_responses(
        mocker=mocker,
        responses=MOCK_RESPONSES
    )

    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.multi import build_multi_mod_args, \
        MultiModule

    am = MockAnsibleModule()
    am.params = ANSIBLE_MODULE_MULTI_PARAMS.copy()
    am.params['multi_control']['purge_all'] = True
    am.params['multi_control']['purge_filter_partial'] = partial
    am.params['multi_control']['purge_filter_invert'] = invert
    am.params['multi_control']['purge_filter'] = purge_filter

    mm = MultiModule(
        module=am,
        result=ANSIBLE_RESULT,
        entry_args={},
        kind='test',
        obj=MockOPNsenseModule,
    )
    assert mm._matches_purge_filter(entry) == result


@pytest.mark.parametrize('e1, e2, match_fields, result', [
    (
        {'name': 'match'},
        {'name': 'test'},
        ['name'],
        False,
    ),
    (
        {'name': 'test'},
        {'name': 'test'},
        ['name'],
        True,
    ),
    (
        {'name': 1},
        {'name': '1'},
        ['name'],
        True,
    ),
    (
        {'name': 'test', 'desc': 'abc', 'text': 'this is a day'},
        {'name': 'test', 'desc': 'no'},
        ['name', 'desc'],
        False,
    ),
    (
        {'name': 'test', 'desc': 'abc', 'text': 'this is a day'},
        {'name': 'test', 'text': 'is'},
        ['name', 'text'],
        False,
    ),
    (
        {'name': 'test', 'desc': 'abc', 'text': 'this is a day'},
        {'name': 'test', 'desc': 'abc'},
        ['name', 'desc'],
        True,
    ),
])
def test_multi_module_entry_matches(mocker, e1, e2, match_fields, result):
    pytest_mock_http_responses(
        mocker=mocker,
        responses=MOCK_RESPONSES
    )

    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.multi import build_multi_mod_args, \
        MultiModule

    am = MockAnsibleModule()
    am.params = ANSIBLE_MODULE_MULTI_PARAMS.copy()
    am.params['match_fields'] = match_fields

    mm = MultiModule(
        module=am,
        result=ANSIBLE_RESULT,
        entry_args={},
        kind='test',
        obj=MockOPNsenseModule,
    )
    assert mm._entry_matches(e1, e2) == result


# todo: add tests for create/update/partial-deletion & purge delete/disable
