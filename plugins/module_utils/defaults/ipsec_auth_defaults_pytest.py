def test_match_fields_is_exposed():
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.defaults.ipsec_auth import IPSEC_AUTH_MOD_ARGS

    assert 'match_fields' in IPSEC_AUTH_MOD_ARGS
    assert IPSEC_AUTH_MOD_ARGS['match_fields']['type'] == 'list'
    # without a default the module never matches existing entries and creates duplicates
    assert IPSEC_AUTH_MOD_ARGS['match_fields']['default'] == ['name']
