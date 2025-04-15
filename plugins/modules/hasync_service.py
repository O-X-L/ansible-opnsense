#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (C) 2025, AnsibleGuy <guy@ansibleguy.net>
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)


from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.handler import \
    module_dependency_error, MODULE_EXCEPTIONS

try:
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import Session
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.defaults.main import \
        OPN_MOD_ARGS

except MODULE_EXCEPTIONS:
    module_dependency_error()

# DOCUMENTATION = 'https://opnsense.ansibleguy.net/modules/hasync.html'
# EXAMPLES = 'https://opnsense.ansibleguy.net/modules/hasync.html'


# pylint: disable=R0915
def run_module():
    module_args = dict(
        name=dict(
            type='str', required=False, default='all', aliases=['service', 'svc', 'target', 'n'],
            description='What service to interact with',
        ),
        action=dict(
            type='str', required=True, aliases=['do', 'a'],
            choices=['restart', 'start', 'stop'],
            description='What action to execute. Some services may not support all of these actions - '
                        'the module will inform you in that case',
        ),
        ignore_version_mismatch=dict(
            type='bool', required=False, default=False,
            description='Report a version missmatch as warning and do not fail.',
        ),
        **OPN_MOD_ARGS,
    )

    result = dict(
        changed=False,
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
    )

    with Session(module=module) as session:
        version = session.get(cnf={
             'module': 'core',
             'controller': 'hasync_status',
             'command': 'version',
        })

        if not isinstance(version.get('response'), dict):
            module.fail_json(msg='The backup firewall is not accessible.', resp=version)

        peer_version = version['response'].get('firmware', {}).get('version')
        my_version = version['response'].get('firmware', {}).get('_my_version')

        if peer_version != my_version:
            if not module.params['ignore_version_mismatch']:
                module.fail_json(msg='Remote version differs from this machines, please update first before '
                                     'using any of the actions below to avoid breakage.')
            module.warn('Remote version differs from this machines, please update first before using any of '
                        'the actions below to avoid breakage.')

        # Restart all
        if module.params['name'] == 'all':
            if module.params['action'] != 'restart':
                module.fail_json('All services only supports action restart')
            result['changed'] = True
            if not module.check_mode:
                session.post(cnf={
                    'module': 'core',
                    'controller': 'hasync_status',
                    'command': 'restartAll',
                })
            module.exit_json(**result)

        # Restart named service(s)
        services = session.get(cnf={
             'module': 'core',
             'controller': 'hasync_status',
             'command': 'services',
        })

        for service in services['rows']:
            if service['name'] != module.params['name']:
                continue

            if module.params['action'] == 'stop' and service['status'] is False:
                continue
            if module.params['action'] == 'start' and service['status'] is True:
                continue
            if module.params['action'] != 'restart' and service.get('nocheck') is True:
                module.fail_json(msg=f"{service['description']} can only be restarted")

            result['changed'] = True
            if not module.check_mode:
                resp = session.post(cnf={
                    'module': 'core',
                    'controller': 'hasync_status',
                    'command': module.params['action'],
                    'params': service['uid'],
                })
                if resp['status'] != 'ok':
                    module.fail_json(msg=f"Action {module.params['action']} for {service['description']} "
                                         f"failed with {resp['status']}")

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
