#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (C) 2025, MaximeWewer
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

# see: https://docs.opnsense.org/development/api/plugins/haproxy.html

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.handler import \
    module_dependency_error, MODULE_EXCEPTIONS

try:
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.wrapper import module_wrapper
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.defaults.main import \
        OPN_MOD_ARGS, STATE_MOD_ARG, RELOAD_MOD_ARG
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.main.haproxy_fcgi import HaproxyFcgi

except MODULE_EXCEPTIONS:
    module_dependency_error()


# DOCUMENTATION = 'https://ansible-opnsense.oxl.app/modules/haproxy.html'
# EXAMPLES = 'https://ansible-opnsense.oxl.app/modules/haproxy.html'


def run_module():
    module_args = dict(
        name=dict(
            type='str', required=True,
            description='Name to identify this FastCGI application'
        ),
        description=dict(
            type='str', required=False, default='',
            description='Description for this FastCGI application'
        ),
        docroot=dict(
            type='str', required=False, default='',
            description='Define the document root on the remote host. '
            'Used to build SCRIPT_FILENAME and PATH_TRANSLATED parameters'
        ),
        index=dict(
            type='str', required=False, default='',
            description='Define the script name that will be appended after a URI'
        ),
        path_info=dict(
            type='str', required=False, default='',
            description='Define a regular expression to extract script-name and path-info from URL-decoded path'
        ),
        log_stderr=dict(
            type='bool', required=False, default=False,
            description='Enable logging of STDERR messages reported by the FastCGI application'
        ),
        keep_conn=dict(
            type='bool', required=False, default=True,
            description='Instruct the FastCGI application to keep connection open'
        ),
        get_values=dict(
            type='bool', required=False, default=False,
            description='Enable retrieval of connection management variables by sending FCGI_GET_VALUES on connection'
        ),
        mpxs_conns=dict(
            type='bool', required=False, default=False,
            description='Enable support for connection multiplexing'
        ),
        max_reqs=dict(
            type='int', required=False, default=None,
            description='Define maximum number of concurrent requests (1-100000)'
        ),
        linked_actions=dict(
            type='list', elements='str', required=False, default=[],
            description='Choose FastCGI rules to be included in this FastCGI application'
        ),
        **STATE_MOD_ARG,
        **RELOAD_MOD_ARG,
        **OPN_MOD_ARGS,
    )

    result = dict(
        changed=False,
        diff={
            'before': {},
            'after': {},
        }
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
    )

    module_wrapper(HaproxyFcgi(module=module, result=result))

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
