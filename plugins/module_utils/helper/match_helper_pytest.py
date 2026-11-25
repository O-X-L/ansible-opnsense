
def test_sanitize_module_args():
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.helper.match import _sanitize_module_args


def test_get_matching():
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.helper.match import get_matching


def test_get_multiple_matching():
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.helper.match import get_multiple_matching


def test_get_matching_existing_entry_without_match_field():
    """An existing entry that lacks a match field (e.g. a dynamic gateway without address)
    must not crash the matching - it simply does not match."""
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.helper.match import get_matching
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.test.mock_pytest import MockAnsibleModule

    module = MockAnsibleModule()
    module.params['debug'] = False
    existing = [
        {'uuid': 'dyn', 'name': 'WAN_DHCP6', 'interface': 'opt1'},  # API omits 'gateway'
        {'uuid': 'gw1', 'name': 'GW_EXAMPLE', 'gateway': '192.0.2.10', 'interface': 'opt2'},
    ]
    found = get_matching(
        module=module, existing_items=existing, compare_item={'name': 'GW_EXAMPLE', 'gateway': '192.0.2.10'},
        match_fields=['name', 'gateway'],
    )
    assert found is not None and found['uuid'] == 'gw1'

    none = get_matching(
        module=module, existing_items=existing[:1], compare_item={'name': 'WAN_DHCP6', 'gateway': '2001:db8::1'},
        match_fields=['name', 'gateway'],
    )
    assert none is None
