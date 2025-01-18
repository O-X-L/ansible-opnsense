from ansible.module_utils.basic import AnsibleModule


def resolve_categories(module: AnsibleModule, params: dict) -> None:
    if not hasattr(module, 'existing_categories'):
        categories = module.s.get(cnf={
            'module': 'firewall',
            'controller': 'category',
            'command': 'get',
        })

        module.existing_categories = {
            category['name']: uuid
            for uuid, category in categories['category']['categories']['category'].items()
        }

    if not isinstance(params['categories'], list):
        params['categories'] = [params['categories']]

    params['categories'] = [
        module.existing_categories.get(name, name)
        for name in params['categories']
    ]
