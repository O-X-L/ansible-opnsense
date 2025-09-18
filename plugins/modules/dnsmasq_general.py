#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (C) 2024, AnsibleGuy <guy@ansibleguy.net>
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

# see: https://docs.opnsense.org/development/api/plugins/dnsmasq.html

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.handler import \
    module_dependency_error, MODULE_EXCEPTIONS
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.wrapper import module_wrapper

try:
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.defaults.main import \
        EN_ONLY_MOD_ARG, OPN_MOD_ARGS, RELOAD_MOD_ARG
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.dnsmasq_general import General
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import \
        is_true, to_digit


except MODULE_EXCEPTIONS:
    module_dependency_error()

# DOCUMENTATION = 'https://opnsense.ansibleguy.net/modules/dhcp.html'
# EXAMPLES = 'https://opnsense.ansibleguy.net/modules/dhcp.html'


def run_module():
    module_args = dict(
        interfaces=dict(
            type='list', elements='str', required=False, default=[], aliases=[''],
            description='Interface IPs used by Dnsmasq for responding to queries from clients.'
                        'If an interface has both IPv4 and IPv6 IPs, both are used.'
                        'Queries to other interface IPs not selected below are discarded.'
                        'The default behavior is to respond to queries on every available IPv4 and IPv6 address.',
        ),
        regdhcp=dict(
            type='bool', default=False, required=False,
            description='If this option is set, then machines that specify their hostname when requesting a '
                        'DHCP lease will be registered, so that their name can be resolved.'
        ),
        regdhcpstatic=dict(
            type='bool', default='False', required=False,
            description='If this option is set, then DHCP static mappings will be registered, so that their name can be resolved.'
        ),
        domain_needed=dict(
            type='bool', default='False',
            description='If this option is set, we will not forward A or AAAA queries for plain names,'
                        'without dots or domain parts, to upstream name servers. If the name is not known from /etc/hosts or DHCP then a "not found" answer is returned.'
        ),
        port=dict(
            type='int', required=False, default=53, aliases=['dns_port'],
            description='The port used for responding to DNS queries. It should normally be left blank unless'
                        'another service needs to bind to TCP/UDP port 53. Setting this to zero (0) completely disables DNS function'
        ),
        dnssec=dict(
            type='bool', default='False',
            description='Secure DNS'
        ),
        no_hosts=dict(
            type='bool', default='False',
            description='Do not read hostnames in /etc/hosts'
        ),
        dhcpfirst=dict(
            type='bool', default='False',
            description='If this option is set, then DHCP mappings will be resolved before the manual list of names below.'
                        'This only affects the name given for a reverse lookup (PTR).'
        ),
        strict_order=dict(
            type='bool', default='False',
            description='If this option is set, we will query the DNS servers sequentially in the order specified (System: General Setup: DNS Servers),'
                        'rather than all at once in parallel.'
        ),
        strictbind=dict(
            type='bool', required=False,
            description='By default we bind the wildcard address, even when listening on some interfaces. Requests that shouldnt'
                        'be handled are discarded, this has the advantage of working even when interfaces come and go and change address.'
                        'This option forces binding to only the interfaces we are listening on, which is less stable in non static environments.'
        ),
        no_private_reverse=dict(
            type='bool', default='False',
            description='If this option is set, we will not forward reverse DNS lookups (PTR) for private addresses (RFC 1918) to upstream name servers.'
                        'Any entries in the Domain Overrides section forwarding private "n.n.n.in-addr.arpa" names to a specific server are still forwarded.'
                        'If the IP to name is not known from /etc/hosts, DHCP or a specific domain override then a "not found" answer is immediately returned.'
        ),
        log_queries=dict(
            type='bool', default='False',
            description='If this option is set, we will log the DNS query'
        ),
        no_ident=dict(
            type='bool', default='true',
            description='Do not respond to class CHAOS and type TXT in domain bind queries. Without this option being set, the cache statistics are'
                        'also available in the DNS as answers to queries of class CHAOS and type TXT in domain bind.'
        ),
        regdhcpdomain=dict(
            type='str', default='',
            description='The domain name to use for DHCP hostname registration. If empty, the default system domain is used.'
                        'Note that all DHCP leases will be assigned to the same domain. If this is undesired, static DHCP lease registration is able to provide coherent mappings.'
        ),
        **EN_ONLY_MOD_ARG,
        **RELOAD_MOD_ARG,
        **OPN_MOD_ARGS,
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
    )

    result = dict(
        changed=False,
        diff={
            'before': {},
            'after': {},
        }
    )

    module_wrapper(General(module=module, result=result))
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
