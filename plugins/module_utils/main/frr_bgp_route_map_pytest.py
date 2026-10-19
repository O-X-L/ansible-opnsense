import pytest


from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.module import BaseModule
from ansible_collections.oxlorg.opnsense.plugins.module_utils.main.frr_bgp_route_map import RouteMap


@pytest.fixture
def route_map(mocker):
    mocker.patch.object(BaseModule, '__init__', return_value=None)
    instance = RouteMap(module=None, result={})
    instance.r = {'diff': {'before': {}, 'after': {}}}
    instance.exists = True
    instance.existing_paths = {
        'ap1': {'description': 'AP1', 'number': '10'},
        'ap2': {'description': 'AP2', 'number': '10'},
        'ap3': {'description': 'AP3', 'number': '20'},
    }
    instance.existing_communities = {
        'cl1': {'description': 'CL1', 'number': '10'},
        'cl2': {'description': 'CL2', 'number': '10'},
    }
    instance.existing_prefixes = {
        'pl20': {'name': 'PL', 'seqnumber': '20'},
        'pl10': {'name': 'PL', 'seqnumber': '10'},
        'other': {'name': 'OTHER', 'seqnumber': '10'},
    }
    # os-frr 2.0 returns only the first entry of each group
    instance.route_map = {'as_path_list': ['ap1'], 'community_list': ['cl1'], 'prefix_list': ['pl20']}
    instance.p = {'as_path_list': ['ap1', 'ap2'], 'community_list': ['cl2'], 'prefix_list': ['pl10', 'pl20']}
    return instance


def test_same_groups_keep_existing(route_map):
    route_map._keep_unchanged_groups()

    assert route_map.p == route_map.route_map
    assert route_map.r['diff']['before'] == route_map.r['diff']['after']
    assert route_map.r['diff']['after'] == {
        'as_path_list': ['AP1'], 'community_list': ['CL1'], 'prefix_list': ['PL'],
    }


def test_other_groups_are_changed(route_map):
    route_map.p = {'as_path_list': ['ap1', 'ap3'], 'community_list': [], 'prefix_list': ['other']}
    route_map._keep_unchanged_groups()

    assert route_map.p == {'as_path_list': ['ap1', 'ap3'], 'community_list': [], 'prefix_list': ['other']}
    assert route_map.r['diff']['before']['prefix_list'] == ['PL']
    assert route_map.r['diff']['after'] == {
        'as_path_list': ['AP1', 'AP3'], 'community_list': [], 'prefix_list': ['OTHER'],
    }


def test_new_entry(route_map):
    route_map.exists = False
    route_map._keep_unchanged_groups()

    assert route_map.p['prefix_list'] == ['pl10', 'pl20']
    assert route_map.r['diff']['before'] == {}
    assert route_map.r['diff']['after']['prefix_list'] == ['PL']
