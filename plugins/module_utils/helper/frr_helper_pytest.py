from unittest.mock import MagicMock

import pytest

AREAS = {
    'uuid-backbone': {'id': '0.0.0.0', 'enabled': '1'},
    'uuid-area1': {'id': '0.0.0.1', 'enabled': '1'},
}


def _instance(area: (str, None), state: str = 'present', areas: (dict, list) = None) -> MagicMock:
    instance = MagicMock()
    instance.p = {'area': area, 'state': state}
    instance.existing_areas = AREAS if areas is None else areas
    instance.r = {'diff': {'before': {}, 'after': {}}}
    instance.m.fail_json.side_effect = SystemExit
    return instance


@pytest.mark.parametrize('area, uuid', [
    ('0.0.0.0', 'uuid-backbone'),
    ('0.0.0.1', 'uuid-area1'),
    (None, ''),
    ('', ''),
])
def test_find_ospf_area(area: (str, None), uuid: str):
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.helper.frr import \
        find_ospf_area

    instance = _instance(area)
    find_ospf_area(instance)
    assert instance.p['area'] == uuid
    instance.m.fail_json.assert_not_called()


@pytest.mark.parametrize('areas', [AREAS, [], None])
def test_find_ospf_area_missing(areas: (dict, list, None)):
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.helper.frr import \
        find_ospf_area

    instance = _instance('0.0.0.99', areas=areas)
    if areas is None:
        instance.existing_areas = None

    with pytest.raises(SystemExit):
        find_ospf_area(instance)

    absent = _instance('0.0.0.99', state='absent', areas=areas)
    find_ospf_area(absent)
    assert absent.p['area'] == '0.0.0.99'
    absent.m.fail_json.assert_not_called()


def test_ospf_area_diff():
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.helper.frr import \
        ospf_area_diff, ospf_area_uuid_to_id

    instance = _instance('0.0.0.1')
    instance.r['diff']['before'] = {'area': 'uuid-backbone', 'cost': 10}
    instance.r['diff']['after'] = {'area': 'uuid-area1', 'cost': 10}
    ospf_area_diff(instance)
    assert instance.r['diff']['before']['area'] == '0.0.0.0'
    assert instance.r['diff']['after']['area'] == '0.0.0.1'

    assert ospf_area_uuid_to_id(instance, '') == ''
    assert ospf_area_uuid_to_id(instance, 'uuid-unknown') == 'uuid-unknown'
