def test_build_multi_mod_args():
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.multi import build_multi_mod_args
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.defaults.main import \
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
