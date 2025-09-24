import pytest

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.test.mock_pytest import \
    pytest_mock_http_responses, MockAnsibleModule, MockOPNsenseModule, MOCK_RESPONSES, \
    ANSIBLE_RESULT, AnsibleError, MockAnsibleModuleWarnException, AnsibleWarning, get_ansible_module_multi_params


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
        {'multi_control': {**get_ansible_module_multi_params()['multi_control'], 'purge_filter': {'test': 1}}},
        True,
    ),
    (
        {'multi_control': {**get_ansible_module_multi_params()['multi_control'], 'purge_all': True}},
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
    am.params = {**get_ansible_module_multi_params(), **params}

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
        {'multi_control': {**get_ansible_module_multi_params()['multi_control'], 'purge_filter': {'test': 1}}},
        False,
    ),
    (
        {'multi_control': {**get_ansible_module_multi_params()['multi_control'], 'purge_all': True}},
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
    am.params = {**get_ansible_module_multi_params(), **params}

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
    am.params = get_ansible_module_multi_params()
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
    am.params = get_ansible_module_multi_params()
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
    am.params = get_ansible_module_multi_params()
    am.params['match_fields'] = match_fields

    mm = MultiModule(
        module=am,
        result=ANSIBLE_RESULT,
        entry_args={},
        kind='test',
        obj=MockOPNsenseModule,
    )
    assert mm._entry_matches(e1, e2) == result


@pytest.mark.parametrize('entry, entry_args, fail_verify, raises', [
    (
        {'name': 'test'},
        dict(
            name=dict(type='str', required=True),
            value=dict(type='str', required=False),
        ),
        False,
        None,
    ),
    (
        {'name': 'test'},
        dict(
            name=dict(type='str', required=True),
            value=dict(type='str', required=False),
        ),
        True,
        None,
    ),
    (
        {'name': 'test'},
        dict(
            name=dict(type='str', required=True),
            value=dict(type='str', required=True),
        ),
        False,
        AnsibleWarning,
    ),
    (
        {'name': 'test'},
        dict(
            name=dict(type='str', required=True),
            value=dict(type='str', required=True),
        ),
        True,
        AnsibleError,
    ),
    (
        {'name': 'test', 'value': 'any'},
        dict(
            name=dict(type='str', required=True),
            value=dict(type='str', required=True),
        ),
        True,
        None,
    ),
])
def test_multi_validate_entry(mocker, entry, entry_args, fail_verify, raises):
    pytest_mock_http_responses(
        mocker=mocker,
        responses=MOCK_RESPONSES
    )

    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.multi import build_multi_mod_args, \
        MultiModule

    am = MockAnsibleModuleWarnException()
    am.params = get_ansible_module_multi_params()
    am.params['multi_control']['fail_verify'] = fail_verify

    mm = MultiModule(
        module=am,
        result=ANSIBLE_RESULT,
        entry_args=entry_args,
        kind='test',
        obj=MockOPNsenseModule,
    )
    if raises is None:
        assert mm._validate_entry(entry) is True

    else:
        with pytest.raises(raises):
            mm._validate_entry(entry)


@pytest.mark.parametrize('match_fields, debug, mc_state, mc_enabled, mc_overrides', [
    (
        ['p1'],
        False,
        None,
        None,
        {'p2': 'b'},
    ),
])
def test_multi_build_entries(mocker, match_fields, debug, mc_state, mc_enabled, mc_overrides):
    pytest_mock_http_responses(
        mocker=mocker,
        responses=MOCK_RESPONSES
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

    if match_fields is not None:
        am.params['match_fields'] = match_fields

    am.params['debug'] = debug
    am.params['multi_control']['override'] = mc_overrides
    am.params['multi_control']['state'] = mc_state
    am.params['multi_control']['enabled'] = mc_enabled

    mm = MultiModule(
        module=am,
        result=ANSIBLE_RESULT,
        entry_args={},
        kind='test',
        obj=MockOPNsenseModule,
        validation=False,  # covered in test_multi_validate_entry
    )

    for e in mm._build_entries():
        assert e['debug'] == debug
        assert e['reload'] == False

        if match_fields is not None:
            assert e['match_fields'] == match_fields

        if mc_state is not None:
            assert e['state'] == mc_state

        if mc_enabled is not None:
            assert e['enabled'] == mc_enabled

        for k, v in mc_overrides.items():
            assert e[k] == v

        if e['p1'] == 'test3' and mc_state is None:
            assert e['state'] == 'absent'

        if e['p1'] == 'test4' and mc_state is None:
            assert e['state'] == 'present'

        if e['p1'] == 'test5' and mc_enabled is None:
            assert e['enabled'] is True

        if e['p1'] == 'test6' and mc_enabled is None:
            assert e['enabled'] is False
