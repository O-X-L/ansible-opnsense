from ansible_collections.ansibleguy.opnsense.plugins.module_utils.test.mock_pytest import \
    MockAnsibleModule


def test_is_multi_module_call():
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.wrapper import is_multi_module_call

    am = MockAnsibleModule()
    am.params['multi'] = {}
    am.params['multi_purge'] = {}
    am.params['multi_control'] = {
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
    }

    assert not is_multi_module_call(am)

    # multi CRUD
    am.params['multi'] = {'dummy': 'yes'}
    assert is_multi_module_call(am)
    am.params['multi'] = {}

    # multi PURGE
    am.params['multi_purge'] = {'dummy': 'yes'}
    assert is_multi_module_call(am)
    am.params['multi_purge'] = {}

    # multi purge ALL
    am.params['multi_control']['purge_all'] = True
    assert is_multi_module_call(am)
    am.params['multi_control']['purge_all'] = False

    # multi purge filter (w/o all or entries - will result in validation-error later on)
    am.params['multi_control']['purge_filter'] = {'dummy': 'yes'}
    assert is_multi_module_call(am)

    # multi purge filter (with entries)
    am.params['multi_purge'] = {'dummy': 'yes'}
    assert is_multi_module_call(am)
    am.params['multi_purge'] = {}

    # multi purge filter (with entries)
    am.params['multi_control']['purge_all'] = True
    assert is_multi_module_call(am)
    am.params['multi_control']['purge_all'] = False

    am.params['multi_control']['purge_filter'] = {}
