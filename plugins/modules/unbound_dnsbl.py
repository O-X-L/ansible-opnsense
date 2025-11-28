#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (C) 2025, Pascal Rath <contact+opnsense@OXL.at>
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

# see: https://docs.opnsense.org/development/api/plugins/unbound.html

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.handler import \
    module_dependency_error, MODULE_EXCEPTIONS

try:
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.wrapper import module_wrapper
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.defaults.main import \
        OPN_MOD_ARGS, STATE_MOD_ARG, RELOAD_MOD_ARG
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.main.unbound_dnsbl import DnsBL

except MODULE_EXCEPTIONS:
    module_dependency_error()


# DOCUMENTATION = 'https://ansible-opnsense.oxl.app/modules/unbound_general.html'
# EXAMPLES = 'https://ansible-opnsense.oxl.app/modules/unbound_general.html'


def run_module():
    module_args = dict(
        name=dict(
            type='str', required=True, aliases=['description', 'desc'],
            description='Unique name to identify the entry',
        ),
        providers=dict(
            type='list', elements='str', required=False, default=[],
            aliases=['type', 'dnsbl', 'bl'],
            description='Select which kind of DNSBL you want to use.'
        ),
        download_urls=dict(
            type='list', elements='str', required=False, default=[],
            aliases=['download', 'lists'],
            description='List of URLs/domains from where blocklist will be downloaded'
        ),
        domains_allow=dict(
            type='list', elements='str', required=False, default=[], aliases=['allowlists'],
            description='List of domains to allow. You can use regular expressions. '
                        'This allow list only applies to blocklist matches on items in this policy'
        ),
        domains_block=dict(
            type='list', elements='str', required=False, default=[], aliases=['blocklists'],
            description='List of domains to blocklist. Only exact matches are supported'
        ),
        wildcard_domains_block=dict(
            type='list', elements='str', required=False, default=[],
            aliases=['wildcards_block', 'wildcard_domains', 'wildcards'],
            description='List of wildcard domains to blocklist. All subdomains of the given domain will be blocked. '
                        'Blocking first-level domains is not supported'
        ),
        source_networks=dict(
            type='list', elements='str', required=False, default=[],
            aliases=['networks', 'source_nets', 'src_nets'],
            description='Source networks to apply policy on. '
                        'Examples are 192.168.1.0/24 or 192.168.1.1. Leave empty to apply on everything. '
                        'All specified networks should use the same protocol family and '
                        'have equal sizes to avoid priority issue'
        ),
        cache_ttl=dict(
            type='int', required=False, default=72_000, aliases=['ttl'],
            description="TTL-seconds for the blocklists cache. "
                        "Remote blocklists don't usually update more often than once a day. "
                        "Therefore, when blocklists are downloaded, they are cached locally to prevent "
                        "unnecessary fetches over the internet. You can change this behavior here if you know "
                        "the remote files rotate faster than this"
        ),
        nxdomain_address=dict(
            type='str', required=False, aliases=['address', 'redirect_to'],
            description='Destination ip address for entries in the blocklist (leave empty to use default: 0.0.0.0). '
                        'Not used when "Return NXDOMAIN" is checked'
        ),
        nxdomain=dict(
            type='bool', required=False, default=False,
            description='Use the DNS response code NXDOMAIN instead of a destination address'
        ),
        **STATE_MOD_ARG,
        **OPN_MOD_ARGS,
        **RELOAD_MOD_ARG,
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

    module_wrapper(DnsBL(module=module, result=result))
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
