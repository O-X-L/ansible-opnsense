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
            description='Choose a name for this resolver configuration.'
        ),
        description=dict(
            type='str', required=False,
            description='Choose a optional description for this resolver configuration.'
        ),
        nameservers=dict(
            type='list', elements='str', required=False, default=[],
            description='Add nameservers to this resolver. Format: [protocol@]address:port.'
        ),
        parse_resolv_conf=dict(
            type='bool', required=False, default=False,
            description='Add all nameservers found in /etc/resolv.conf.'
        ),
        resolve_retries=dict(
            type='int', required=False,
            description='Number of queries to send to resolve a server name before giving up.'
        ),
        timeout_resolve=dict(
            type='str', required=False,
            description='Default time to trigger name resolutions. Format: number + unit (us/ms/s/m/h/d).'
        ),
        timeout_retry=dict(
            type='str', required=False,
            description='Time between two DNS queries when no valid response received.'
        ),
        accepted_payload_size=dict(
            type='int', required=False,
            description='Maximum payload size accepted by HAProxy for DNS responses.'
        ),
        hold_valid=dict(
            type='str', required=False,
            description='Time HAProxy will not query DNS after receiving valid response.'
        ),
        hold_obsolete=dict(
            type='str', required=False,
            description='Time after which a cached DNS answer is considered obsolete.'
        ),
        hold_refused=dict(
            type='str', required=False,
            description='Time to wait before retrying after DNS server refuses request.'
        ),
        hold_nx=dict(
            type='str', required=False,
            description='Time to wait before retrying after NXDOMAIN error.'
        ),
        hold_timeout=dict(
            type='str', required=False,
            description='Time to wait before retrying after DNS request times out.'
        ),
        hold_other=dict(
            type='str', required=False,
            description='Hold other timeout value for the resolver.'
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
