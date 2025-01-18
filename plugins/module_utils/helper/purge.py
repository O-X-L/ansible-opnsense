from ansible.module_utils.basic import AnsibleModule


def purge(
        module: AnsibleModule, result: dict,
        item_to_purge: dict, diff_param: str, obj_func
) -> None:
    result['changed'] = True

    if module.params['action'] == 'delete':
        result['diff']['before'][item_to_purge[diff_param]] = item_to_purge
        result['diff']['after'][item_to_purge[diff_param]] = None

    if not module.check_mode:
        _obj = obj_func(item_to_purge)
        _obj.exists = True

        if module.params['action'] == 'delete':
            _obj.delete()

        else:
            if _obj.b.is_enabled():
                result['diff']['before'][item_to_purge[diff_param]] = {'enabled': True}
                result['diff']['after'][item_to_purge[diff_param]] = {'enabled': False}
                _obj.b.disable()


def check_purge_filter(module: AnsibleModule, item: dict) -> bool:
    matched = not module.params['filter_invert']

    for filter_key, filter_value in module.params['filters'].items():
        if isinstance(filter_value, list):
            if module.params['filter_partial']:
                if any(fv not in item[filter_key] for fv in filter_value):
                    return not matched
            elif isinstance(filter_value, list):
                if sorted(item[filter_key]) != sorted(filter_value):
                    return not matched
        else:

            if module.params['filter_partial']:
                if filter_value not in str(item[filter_key]):
                    return not matched
            elif item[filter_key] != filter_value:
                return not matched

    return matched
