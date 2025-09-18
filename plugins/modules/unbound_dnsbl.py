#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (C) 2025, Pascal Rath <contact+opnsense@OXL.at>
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

# see: https://docs.opnsense.org/development/api/plugins/unbound.html

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.handler import \
    module_dependency_error, MODULE_EXCEPTIONS

try:
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.wrapper import module_wrapper
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.defaults.main import \
        OPN_MOD_ARGS, EN_ONLY_MOD_ARG, RELOAD_MOD_ARG
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.unbound_dnsbl import DnsBL

except MODULE_EXCEPTIONS:
    module_dependency_error()


# DOCUMENTATION = 'https://ansible-opnsense.oxl.app/modules/unbound_general.html'
# EXAMPLES = 'https://ansible-opnsense.oxl.app/modules/unbound_general.html'


def run_module():
    module_args = dict(
        safesearch=dict(
            type='bool', required=False, default=False,
            description='Force the usage of SafeSearch on Google, DuckDuckGo, Bing, Qwant, PixaBay and YouTube'
        ),
        type=dict(
            type='list', elements='str', required=False, default=[], aliases=['bl'],
            description='Select which kind of DNSBL you want to use'
        ),
        lists=dict(
            type='list', elements='str', required=False, default=[], aliases=['list'],
            description='List of urls from where blocklist will be downloaded'
        ),
        whitelists=dict(
            type='list', elements='str', required=False, default=[], aliases=['whitelist', 'allowlist', 'allowlists'],
            description='List of domains to whitelist. You can use regular expressions'
        ),
        blocklists=dict(
            type='list', elements='str', required=False, default=[], aliases=['blocklist'],
            description='List of domains to blocklist. Only exact matches are supported'
        ),
        wildcards=dict(
            type='list', elements='str', required=False, default=[], aliases=['wildcard'],
            description='List of wildcard domains to blocklist. All subdomains of the given domain will be blocked. '
                        'Blocking first-level domains is not supported'
        ),
        address=dict(
            type='str', required=False,
            description='Destination ip address for entries in the blocklist (leave empty to use default: 0.0.0.0). '
                        'Not used when "Return NXDOMAIN" is checked'
        ),
        nxdomain=dict(
            type='bool', required=False, default=False,
            description='Use the DNS response code NXDOMAIN instead of a destination address'
        ),
        **EN_ONLY_MOD_ARG,
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
