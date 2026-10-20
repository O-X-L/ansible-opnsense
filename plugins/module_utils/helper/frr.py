from ansible_collections.oxlorg.opnsense.plugins.module_utils.helper.main import is_unset


# since os-frr 2.0 (OPNsense 26.7) OSPF/OSPFv3 areas are separate records
#   networks and interfaces reference them by UUID
#   see: https://github.com/opnsense/plugins/commit/737b48342


def _ospf_areas(instance) -> dict:
    if isinstance(instance.existing_areas, dict):
        return instance.existing_areas

    return {}


def find_ospf_area(instance) -> None:
    # needs to run before the entry-matching, as the area could be one of the 'match_fields'
    area = instance.p['area']
    if is_unset(area):
        instance.p['area'] = ''
        return

    for uuid, entry in _ospf_areas(instance).items():
        if entry['id'] == area:
            instance.p['area'] = uuid
            return

    if instance.p['state'] == 'present':
        instance.m.fail_json(
            f"The provided area '{area}' does not exist! "
            'Since OPNsense 26.7 (os-frr 2.0) areas are separate entries - you need to create it first.'
        )


def ospf_area_uuid_to_id(instance, uuid: str) -> str:
    areas = _ospf_areas(instance)
    if uuid in areas:
        return areas[uuid]['id']

    return uuid


def ospf_area_diff(instance) -> None:
    for state in ['before', 'after']:
        diff = instance.r['diff'].get(state, {})
        if 'area' in diff and not is_unset(diff['area']):
            diff['area'] = ospf_area_uuid_to_id(instance, diff['area'])
