from copy import deepcopy
import importlib

import pytest

from ansible_collections.oxlorg.opnsense.plugins.module_utils.test.mock_pytest import (
    MockAnsibleModule, AnsibleError,
)

PREFIX = 'ansible_collections.oxlorg.opnsense.plugins'
UUID = '11111111-1111-4111-8111-111111111111'


def selections(values, selected=()):
    return {value: {'value': value, 'selected': int(value in selected)} for value in values}


def group(name='WAN_FAILOVER', tier_1=('WAN_A',), tier_2=()):
    return dict(
        name=name, descr='', trigger=selections(['down', 'downloss'], ['down']),
        poolopts=selections(['', 'round-robin'], ['']),
        item=selections(['WAN_A', 'WAN_B'], tier_1),
        item2=selections(['WAN_A', 'WAN_B'], tier_2),
        item3=selections(['WAN_A', 'WAN_B']),
        item4=selections(['WAN_A', 'WAN_B']),
        item5=selections(['WAN_A', 'WAN_B']),
    )


class GatewayAPI:
    def __init__(self, entries=None):
        self.entries = deepcopy(entries or {})
        self.calls = []
        self.ignore_update = False
        self.in_use = False

    def get(self, cnf):
        self.calls.append(('GET', deepcopy(cnf)))
        assert cnf['module'] == 'routing'
        assert cnf['controller'] == 'group_settings'
        assert cnf['command'] == 'get'
        params = cnf.get('params')
        return {'gateway_group': deepcopy(self.entries[params[0]] if params else group(tier_1=()))}

    def post(self, cnf, **kwargs):
        self.calls.append(('POST', deepcopy(cnf)))
        action = cnf['command']
        if action == 'search':
            return {'rows': [dict(uuid=uuid, name=data['name']) for uuid, data in self.entries.items()],
                    'total': len(self.entries)}
        if action == 'reconfigure':
            return {'status': 'ok'}
        if action == 'del':
            if self.in_use:
                return {'result': 'failed', 'in_use': True}
            self.entries.pop(cnf['params'][0])
            return {'result': 'deleted'}
        assert action in ('add', 'set')
        uuid = UUID if action == 'add' else cnf['params'][0]
        entry = deepcopy(self.entries.get(uuid, group(tier_1=())))
        if not self.ignore_update:
            for key, value in cnf['data']['gateway_group'].items():
                if isinstance(entry[key], dict):
                    values = value.split(',') if key.startswith('item') else [value]
                    for choice, info in entry[key].items():
                        info['selected'] = int(choice in values)
                else:
                    entry[key] = value
            self.entries[uuid] = entry
        return {'result': 'saved', 'uuid': uuid}

    def close(self):
        pass

    @property
    def mutations(self):
        return [cnf for method, cnf in self.calls
                if method == 'POST' and cnf['command'] != 'search']


def run(api, check=False, **params):
    module_file = importlib.import_module(PREFIX + '.modules.gateway_group')
    impl = importlib.import_module(PREFIX + '.module_utils.main.gateway_group')
    module = MockAnsibleModule()
    module.params.update({key: value.get('default') for key, value in module_file.ARGUMENT_SPEC.items()
                          if key not in module.params})
    module.params.update(name='WAN_FAILOVER', **params)
    module.check_mode = check
    result = {'changed': False, 'diff': {'before': {}, 'after': {}}}
    instance = impl.GatewayGroup(module, result, session=api)
    instance.check()
    instance.process()
    if result['changed'] and module.params['reload']:
        instance.reload()
    return result


def test_create_tiers_and_reload():
    api = GatewayAPI()
    result = run(api, tier_1=['WAN_A'], tier_2=['WAN_B'], reload=True)
    assert result['changed']
    payload = api.mutations[0]['data']['gateway_group']
    assert payload['item'] == 'WAN_A'
    assert payload['item2'] == 'WAN_B'
    assert api.mutations[-1]['command'] == 'reconfigure'


def test_repeat_preserves_omitted_fields_and_does_not_reload():
    api = GatewayAPI({UUID: group(tier_2=['WAN_B'])})
    assert not run(api, tier_1=['WAN_A'], reload=True)['changed']
    assert not api.mutations


def test_update_selected_tier():
    api = GatewayAPI({UUID: group()})
    assert run(api, tier_2=['WAN_B'])['changed']
    assert api.mutations[0]['data']['gateway_group']['item'] == 'WAN_A'


@pytest.mark.parametrize('existing', [False, True])
def test_check_mode_does_not_mutate(existing):
    api = GatewayAPI({UUID: group()} if existing else {})
    assert run(api, check=True, tier_1=['WAN_B'], reload=True)['changed']
    assert not api.mutations


def test_ambiguous_name_fails_without_mutation():
    api = GatewayAPI({UUID: group(), 'other': group()})
    with pytest.raises(AnsibleError, match='[Aa]mbiguous'):
        run(api)
    assert not api.mutations


def test_explicit_uuid_must_exist():
    api = GatewayAPI()
    with pytest.raises(AnsibleError, match='UUID'):
        run(api, uuid=UUID, tier_1=['WAN_A'])
    assert not api.mutations


def test_uuid_selects_existing():
    api = GatewayAPI({UUID: group()})
    assert not run(api, uuid=UUID)['changed']


def test_unknown_gateway_fails_before_mutation():
    api = GatewayAPI()
    with pytest.raises(AnsibleError, match='gateway'):
        run(api, tier_1=['MISSING'])
    assert not api.mutations


def test_duplicate_gateway_across_tiers_fails():
    api = GatewayAPI()
    with pytest.raises(AnsibleError, match='tier'):
        run(api, tier_1=['WAN_A'], tier_2=['WAN_A'])
    assert not api.mutations


def test_empty_group_fails():
    api = GatewayAPI()
    with pytest.raises(AnsibleError, match='tier'):
        run(api)
    assert not api.mutations


def test_tier_one_clear_is_rejected_before_write():
    api = GatewayAPI({UUID: group()})
    with pytest.raises(AnsibleError, match='tier_1'):
        run(api, tier_1=[], tier_2=['WAN_B'])
    assert not api.mutations


def test_silent_api_failure_is_detected():
    api = GatewayAPI({UUID: group()})
    api.ignore_update = True
    with pytest.raises(AnsibleError, match='verif'):
        run(api, tier_2=['WAN_B'])


def test_explicit_delete_and_repeat():
    api = GatewayAPI({UUID: group()})
    assert run(api, state='absent')['changed']
    api.calls.clear()
    assert not run(api, state='absent')['changed']
    assert not api.mutations


def test_in_use_delete_fails():
    api = GatewayAPI({UUID: group()})
    api.in_use = True
    with pytest.raises(AnsibleError, match='in use'):
        run(api, state='absent')


def test_all_module_defaults_keep_existing_groups():
    from pathlib import Path
    import yaml
    root = Path(__file__).resolve().parents[3]
    metadata = yaml.safe_load((root / 'meta/runtime.yml').read_text())
    groups = metadata['action_groups']['all'][0]['metadata']['extend_group']
    assert 'oxlorg.opnsense.system' in groups
    assert 'oxlorg.opnsense.nut_diagnostics' in groups
    assert 'oxlorg.opnsense.gateway_group' in metadata['action_groups']['route']
