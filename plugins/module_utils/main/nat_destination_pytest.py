import pytest

from ansible_collections.oxlorg.opnsense.plugins.module_utils.test.mock_pytest import \
    pytest_mock_http_responses, MockAnsibleModule, AnsibleError
from ansible_collections.oxlorg.opnsense.plugins.module_utils.test.testdata.nat_destination_testdata import \
    Testdata_26_7_7 as DNatTestdata

# the rule seeded in the testdata, as a user would declare it
PARAMS = dict(
    description='ANSIBLE_TEST_1_1', match_fields=['description'], state='present', enabled=True, reload=True,
    sequence=1, interface=['wan'], ip_protocol='inet', protocol='TCP',
    source_invert=False, source_net='any', source_port='',
    destination_invert=False, destination_net='203.0.113.10', destination_port='443',
    target='192.168.0.10', local_port='8443', pool_opts='', nat_reflection='', associated_rule='',
    no_port_forward=False, log=True, tag='', tagged='', uuid=None,
    categories=[], sync=True,
)


def _mock(mocker, **kwargs) -> DNatTestdata:
    testdata = DNatTestdata(**kwargs)
    pytest_mock_http_responses(mocker=mocker, handler=testdata)
    return testdata


def _run(params: dict, check_mode: bool = False) -> dict:
    # pylint: disable=C0415
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.wrapper import module_wrapper
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.main.nat_destination import DNat

    module = MockAnsibleModule()
    module.params.update(params)
    module.check_mode = check_mode
    result = {'changed': False, 'diff': {'before': {}, 'after': {}}}
    module_wrapper(DNat(module=module, result=result))
    return result


def test_nat_destination_existing_rule_unchanged(mocker):
    # a rule created before 'categories' and 'sync' existed must not report a change
    testdata = _mock(mocker)
    result = _run(PARAMS)
    assert not result['changed']
    assert len(testdata.mutations()) == 0


def test_nat_destination_add_with_categories_and_no_sync(mocker):
    testdata = _mock(mocker)
    params = {**PARAMS, 'description': 'ANSIBLE_TEST_1_2', 'categories': ['VPN', 'Ops'], 'sync': False}

    result = _run(params)
    assert result['changed']
    assert [call[0] for call in testdata.mutations()] == ['add', 'apply']
    posted = testdata.mutations()[0][1]
    # names are posted to 'category' - no uuid-lookup needed on the DNat-model
    assert posted['category'] == 'Ops,VPN'
    assert str(posted['nosync']) == '1'
    assert 'categories' not in posted
    entry = testdata.rule_by_descr('ANSIBLE_TEST_1_2')
    assert entry['nosync'] == '1'
    assert [k for k, v in entry['category'].items() if v['selected'] == 1] == ['Ops', 'VPN']

    result = _run(params)
    assert not result['changed']
    assert len(testdata.mutations()) == 2


@pytest.mark.parametrize('changed', [
    {'categories': ['Ops']},
    {'sync': False},
])
def test_nat_destination_change_new_fields(mocker, changed: dict):
    testdata = _mock(mocker)
    result = _run({**PARAMS, **changed})
    assert result['changed']
    assert [call[0] for call in testdata.mutations()] == ['set', 'apply']

    result = _run({**PARAMS, **changed})
    assert not result['changed']


def test_nat_destination_clear_categories(mocker):
    testdata = _mock(mocker)
    _run({**PARAMS, 'categories': ['Ops', 'VPN']})
    assert testdata.rule_by_descr('ANSIBLE_TEST_1_1')['categories'] == '6adf800000000001,6adf800000000002'

    result = _run(PARAMS)
    assert result['changed']
    assert testdata.mutations()[-2][1]['category'] == ''
    assert testdata.rule_by_descr('ANSIBLE_TEST_1_1')['categories'] == ''


def test_nat_destination_unknown_category(mocker):
    testdata = _mock(mocker)

    with pytest.raises(AnsibleError, match=r"Unknown rule categories: \['Nope'\]"):
        _run({**PARAMS, 'categories': ['Ops', 'Nope']})

    assert len(testdata.mutations()) == 0


def test_nat_destination_no_categories_on_firewall(mocker):
    # 'category' is an empty list in the API-response if no category exists
    testdata = _mock(mocker, categories={})
    assert testdata.rule_by_descr('ANSIBLE_TEST_1_1')['category'] == []

    result = _run(PARAMS)
    assert not result['changed']

    with pytest.raises(AnsibleError, match='Unknown rule categories'):
        _run({**PARAMS, 'categories': ['Ops']})

    assert len(testdata.mutations()) == 0


def test_nat_destination_unknown_category_without_existing_rule(mocker):
    # no rule to read the option-list from - the API validation has to catch it
    testdata = _mock(mocker, rules=[])

    with pytest.raises(AnsibleError, match='rule.category'):
        _run({**PARAMS, 'categories': ['Nope']})

    assert testdata.state == {}


def test_nat_destination_check_mode(mocker):
    testdata = _mock(mocker)
    result = _run({**PARAMS, 'categories': ['Ops'], 'sync': False}, check_mode=True)
    assert result['changed']
    assert len(testdata.mutations()) == 0


def test_nat_destination_protocol_normalized(mocker):
    testdata = _mock(mocker)
    result = _run({**PARAMS, 'protocol': 'Tcp'})
    assert not result['changed']
    assert len(testdata.mutations()) == 0


def test_nat_destination_delete_and_rerun(mocker):
    testdata = _mock(mocker)
    result = _run({**PARAMS, 'state': 'absent'})
    assert result['changed']
    assert [call[0] for call in testdata.mutations()] == ['del', 'apply']
    assert testdata.state == {}

    result = _run({**PARAMS, 'state': 'absent'})
    assert not result['changed']
    assert len(testdata.mutations()) == 2


def test_nat_destination_disable_enable_uses_toggle(mocker):
    testdata = _mock(mocker)
    result = _run({**PARAMS, 'enabled': False})
    assert result['changed']
    # only the state changed - the rule is toggled, not re-sent
    assert [call[0] for call in testdata.mutations()] == ['toggle', 'apply']
    assert testdata.rule_by_descr('ANSIBLE_TEST_1_1')['disabled'] == '1'

    result = _run({**PARAMS, 'enabled': False})
    assert not result['changed']

    result = _run(PARAMS)
    assert result['changed']
    assert testdata.rule_by_descr('ANSIBLE_TEST_1_1')['disabled'] == '0'


def test_nat_destination_match_by_uuid(mocker):
    testdata = _mock(mocker)
    uuid = next(iter(testdata.state))
    result = _run({**PARAMS, 'match_fields': ['uuid'], 'uuid': uuid, 'description': 'ANSIBLE_TEST_RENAMED'})
    assert result['changed']
    assert testdata.mutations()[0][0] == 'set'
    assert len(testdata.state) == 1
    assert testdata.state[uuid]['descr'] == 'ANSIBLE_TEST_RENAMED'


def test_nat_destination_reload_false(mocker):
    testdata = _mock(mocker)
    result = _run({**PARAMS, 'target': '192.168.0.11', 'reload': False})
    assert result['changed']
    assert [call[0] for call in testdata.mutations()] == ['set']


@pytest.mark.parametrize('changed', [
    {'no_port_forward': True},
    {'associated_rule': 'pass'},
    {'nat_reflection': 'disable'},
    {'pool_opts': 'round-robin'},
    {'source_invert': True},
    {'source_net': '198.51.100.0/24'},
    {'destination_port': '8443'},
    {'local_port': '443'},
    {'protocol': 'udp'},
    {'interface': ['wan', 'lan']},
    {'log': False},
    {'sequence': 2},
    {'tag': 'dnat'},
])
def test_nat_destination_change_fields(mocker, changed: dict):
    testdata = _mock(mocker)
    result = _run({**PARAMS, **changed})
    assert result['changed']
    assert [call[0] for call in testdata.mutations()] == ['set', 'apply']

    result = _run({**PARAMS, **changed})
    assert not result['changed']
    assert len(testdata.mutations()) == 2


def test_nat_destination_missing_target(mocker):
    testdata = _mock(mocker)

    with pytest.raises(AnsibleError, match="'target'"):
        _run({**PARAMS, 'description': 'ANSIBLE_TEST_1_2', 'target': ''})

    assert len(testdata.mutations()) == 0


def test_nat_destination_list(mocker):
    # pylint: disable=C0415
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.main.nat_destination import DNat

    _mock(mocker)
    module = MockAnsibleModule()
    module.params.update(PARAMS)
    entries = DNat(module=module, result={'changed': False, 'diff': {'before': {}, 'after': {}}}).get_existing()

    assert len(entries) == 1
    entry = entries[0]
    assert entry['description'] == 'ANSIBLE_TEST_1_1'
    assert entry['enabled'] is True
    assert entry['interface'] == ['wan']
    assert entry['protocol'] == 'tcp'
    assert entry['target'] == '192.168.0.10'
    # the new fields as the 'list' module shows them: names, not uuids; a bool, not 'nosync'
    assert entry['categories'] == []
    assert entry['sync'] is True
