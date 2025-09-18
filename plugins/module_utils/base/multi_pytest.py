from ansible_collections.ansibleguy.opnsense.plugins.module_utils.test.mock_pytest import \
    pytest_mock_http_responses, MockAnsibleModule, MockOPNsenseModule, MOCK_RESPONSES, \
    ANSIBLE_RESULT


def test_build_multi_mod_args():
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.multi import build_multi_mod_args

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


def test_multi_module_base(mocker):
    pytest_mock_http_responses(
        mocker=mocker,
        responses=MOCK_RESPONSES
    )

    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.multi import build_multi_mod_args, \
        MultiModule

    am = MockAnsibleModule()
    a = {
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
    am.params = {**am.params, **a}
    res = ANSIBLE_RESULT

    mm = MultiModule(
        module=am,
        result=res,
        entry_args={},
        kind='test',
        obj=MockOPNsenseModule,
    )

    mm.process()

    assert not res['changed']
    assert len(res['diff']['before']) == 0
    assert len(res['diff']['after']) == 0


# todo: add tests for create/update/partial-deletion & purge delete/disable
