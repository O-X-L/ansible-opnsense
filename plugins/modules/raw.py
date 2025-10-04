#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (C) 2025, Pascal Rath <contact+opnsense@OXL.at>
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

# module to interact with system services

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.handler import \
    module_dependency_error, MODULE_EXCEPTIONS

try:
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.defaults.main import \
        OPN_MOD_ARGS
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.api import \
        single_get, single_post, DEFAULT_TIMEOUT

except MODULE_EXCEPTIONS:
    module_dependency_error()


# DOCUMENTATION = 'https://ansible-opnsense.oxl.app/general/raw.html'
# EXAMPLES = 'https://ansible-opnsense.oxl.app/general/raw.html'


# pylint: disable=R0915
def run_module():
    module_args = dict(
        module=dict(
            type='str', aliases=['m', 'mod'], default=None,
            description='The API-module to target'
        ),
        controller=dict(
            type='str',aliases=['co', 'cont'],
            description='The API-controller to target'
        ),
        command=dict(
            type='str', aliases=['c', 'cmd'],
            description='The API-command to target'
        ),
        parameters=dict(
            type='list', elements='str', aliases=['p', 'params'],
            description='Optional: Parameters to send'
        ),
        url=dict(
            type='str', aliases=['u'], default=None,
            description='Alternative to module/controller/command</params>'
        ),
        action=dict(
            type='str', aliases=['a', 'method'],
            choices=['get', 'post'], default='get',
        ),
        data=dict(
            type='dict', default=None, aliases=['d'],
            description='Optional: Supply data to send'
        ),
        headers=dict(
            type='dict', default=None, aliases=['h'],
            description='Optional: Supply headers to send'
        ),
        timeout=dict(
            type='float', aliases=['t'], default=DEFAULT_TIMEOUT,
            description='Timeout in seconds for request + response',
        ),
        **OPN_MOD_ARGS,
    )

    result = dict(
        changed=False,
        response={},
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
        required_if=[
            ('url', None, ('module', 'controller', 'command')),
            ('module', 'None', 'url'),
        ],
        mutually_exclusive=[
            ('url', 'module'),
        ],
    )

    p = module.params
    m = p['module']
    c = p['controller']
    cmd = p['command']
    par = p['parameters']

    if p['url'] is not None:
        try:
            m, c, cmd_params = p['url'].split('/', 2)
            if cmd_params.find('/'):
                cmd_params = cmd_params.split('/')
                cmd = cmd_params[0]
                par = cmd_params[1:]

            else:
                cmd = cmd_params
                par = None

        except ValueError:
            module.fail_json(
                "Provided URL has too few parts. "
                "Example: '<module>/<controller>/<command>(/<parameters>)"
            )

    req = dict(
        module=module,
        cnf=dict(
            module=m,
            controller=c,
            command=cmd,
            params=par,
            data=p['data'],
        ),
        timeout=p['timeout'],
    )

    if p['action'] == 'get':
        result['response'] = single_get(**req)

    else:
        if module.check_mode:
            module.warn('Post actions are not performed in check-mode!')

        else:
            result['changed'] = True
            result['response'] = single_post(**req, headers=p['headers'])


    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
