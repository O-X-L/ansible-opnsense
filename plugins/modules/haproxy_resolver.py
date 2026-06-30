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
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.main.haproxy_resolver import HaproxyResolver

except MODULE_EXCEPTIONS:
    module_dependency_error()


# DOCUMENTATION = 'https://ansible-opnsense.oxl.app/modules/haproxy.html'
# EXAMPLES = 'https://ansible-opnsense.oxl.app/modules/haproxy.html'


def run_module():
    module_args = dict(
        name=dict(
            type='str', required=True,
            description='Name for this resolver configuration (1-255 chars).'
        ),
        description=dict(
            type='str', required=False,
            description='Optional description for this resolver (1-255 chars).'
        ),
        nameservers=dict(
            type='list', elements='str', required=False, default=[],
            description='Nameservers (e.g. 127.0.0.1:53, tcp@192.168.1.1:53).'
        ),
        parse_resolv_conf=dict(
            type='bool', required=False, default=False,
            description='Add all nameservers found in /etc/resolv.conf to this resolver configuration.'
        ),
        resolve_retries=dict(
            type='int', required=False,
            description='This configures the number of queries to send to resolve a server name before giving up.'
        ),
        timeout_resolve=dict(
            type='str', required=False,
            description='Default time for name resolution (e.g. 1s, 500ms). Default: 1s.'
        ),
        timeout_retry=dict(
            type='str', required=False,
            description='Time between DNS retries (e.g. 1s, 500ms). Default: 1s.'
        ),
        accepted_payload_size=dict(
            type='int', required=False,
            description='Maximum DNS payload size accepted by HAProxy.'
        ),
        hold_valid=dict(
            type='str', required=False,
            description='Cache time for valid DNS responses (e.g. 10s, 1m).'
        ),
        hold_obsolete=dict(
            type='str', required=False,
            description='Time before cached DNS entry is considered obsolete.'
        ),
        hold_refused=dict(
            type='str', required=False,
            description='Wait time after DNS refuses request before retry.'
        ),
        hold_nx=dict(
            type='str', required=False,
            description='Wait time after NXDOMAIN error before retry.'
        ),
        hold_timeout=dict(
            type='str', required=False,
            description='Wait time after DNS timeout before retry.'
        ),
        hold_other=dict(
            type='str', required=False,
            description='Hold timeout for other DNS errors.'
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

    module_wrapper(HaproxyResolver(module=module, result=result))

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
