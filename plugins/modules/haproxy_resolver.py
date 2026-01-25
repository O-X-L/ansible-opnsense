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
            description='Choose a name for this resolver configuration. Must be 1-255 characters, cannot contain tabs, commas, semicolons, dots, or brackets.'
        ),
        description=dict(
            type='str', required=False,
            description='Choose a optional description for this resolver configuration. Must be 1-255 characters if provided.'
        ),
        nameservers=dict(
            type='list', elements='str', required=False, default=[],
            description='Add nameservers to this resolver configuration. They may be prefixed with either tcp@ or udp@ to use the TCP or UDP protocol respectively. Format: [protocol@]address:port[-port_range], e.g. 127.0.0.1:53, [::1]:53, tcp@192.168.1.1:53.'
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
            description='This configures the default time to trigger name resolutions when no other time applied. Format: 1-8 digit number optionally followed by time unit (us, ms, s, m, h, d). Default: 1s.'
        ),
        timeout_retry=dict(
            type='str', required=False,
            description='This configures the default time between two DNS queries, when no valid response has been received. Format: 1-8 digit number optionally followed by time unit (us, ms, s, m, h, d). Default: 1s.'
        ),
        accepted_payload_size=dict(
            type='int', required=False,
            description='Defines the maximum payload size accepted by HAProxy and announced to all the name servers configured in this resolvers section.'
        ),
        hold_valid=dict(
            type='str', required=False,
            description='When haproxy receives a valid NS response it will not query DNS until valid time expires. Format: 1-8 digit number optionally followed by time unit (us, ms, s, m, h, d).'
        ),
        hold_obsolete=dict(
            type='str', required=False,
            description='As a DNS server may not answer all the IPs in one DNS request, haproxy keeps a cache of previous answers. An answer will be considered obsolete after hold obsolete seconds without the IP returned. Format: 1-8 digit number optionally followed by time unit (us, ms, s, m, h, d).'
        ),
        hold_refused=dict(
            type='str', required=False,
            description='When the DNS server refuses the resolve request haproxy will not retry until hold refused elapses. Format: 1-8 digit number optionally followed by time unit (us, ms, s, m, h, d).'
        ),
        hold_nx=dict(
            type='str', required=False,
            description='When haproxy receives a NXDOMAIN error message (domain does not exist) from the resolver it will not retry until hold nx elapses. Format: 1-8 digit number optionally followed by time unit (us, ms, s, m, h, d).'
        ),
        hold_timeout=dict(
            type='str', required=False,
            description='When a DNS resolve request times out haproxy will not retry until hold timeout elapses. Format: 1-8 digit number optionally followed by time unit (us, ms, s, m, h, d).'
        ),
        hold_other=dict(
            type='str', required=False,
            description='Sets the hold other timeout value for the resolver. Format: 1-8 digit number optionally followed by time unit (us, ms, s, m, h, d).'
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