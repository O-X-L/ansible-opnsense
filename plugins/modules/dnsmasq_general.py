#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (C) 2024, AnsibleGuy <guy@ansibleguy.net>
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

# see: https://docs.opnsense.org/development/api/core/dnsmasq.html

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.handler import \
    module_dependency_error, MODULE_EXCEPTIONS
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.wrapper import module_wrapper

try:
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.defaults.main import \
        EN_ONLY_MOD_ARG, OPN_MOD_ARGS, RELOAD_MOD_ARG
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.dnsmasq_general import General

except MODULE_EXCEPTIONS:
    module_dependency_error()

# DOCUMENTATION = 'https://ansible-opnsense.oxl.app/modules/dnsmasq.html'
# EXAMPLES = 'https://ansible-opnsense.oxl.app/modules/dnsmasq.html'


def run_module():
    module_args = dict(
        # Default
        interfaces=dict(
            type='list', elements='str', required=False, default=[], aliases=['ints'],
            description='Interface IPs used by Dnsmasq for responding to queries from clients. '
                        'If an interface has both IPv4 and IPv6 IPs, both are used. '
                        'Queries to other interface IPs not selected below are discarded. '
                        'The default behavior is to respond to queries on every available IPv4 and IPv6 address.',
        ),
        strictbind=dict(
            type='bool', required=False,
            description='By default we bind the wildcard address, even when listening on some interfaces. '
                        'Requests that shouldnt be handled are discarded, this has the advantage of working '
                        'even when interfaces come and go and change address. '
                        'This option forces binding to only the interfaces we are listening on, '
                        'which is less stable in non static environments.'
        ),
        # DNS
        port=dict(
            type='int', required=False, default=53, aliases=['dns_port'],
            description='The port used for responding to DNS queries. '
                        'It should normally be left blank unless'
                        'another service needs to bind to TCP/UDP port 53. '
                        'Setting this to zero (0) completely disables DNS function'
        ),
        dnssec=dict(
            type='bool', default='False',
            description='Secure DNS'
        ),
        no_hosts=dict(
            type='bool', default='False',
            description='Do not read hostnames in /etc/hosts'
        ),
        log_queries=dict(
            type='bool', default='False',
            description='If this option is set, we will log the DNS query'
        ),
        dns_forward_max=dict(
            type='int', required=False,
            description='Maximum number of concurrent DNS queries',
        ),
        cache_size=dict(
            type='int', required=False,
            description='Size of the DNS cache. Setting the cache size to zero disables caching',
        ),
        local_ttl=dict(
            type='int', required=False,
            description='Time-to-live (in seconds) to be given for local DNS entries, i.e. /etc/hosts or DHCP leases',
        ),
        no_ident=dict(
            type='bool', default='true',
            description='Do not respond to class CHAOS and type TXT in domain bind queries. '
                        'Without this option being set, the cache statistics are also available in the DNS '
                        'as answers to queries of class CHAOS and type TXT in domain bind.'
        ),
        # DNS Query Forwarding
        strict_order=dict(
            type='bool', default='False',
            description='If this option is set, we will query the DNS servers sequentially '
                        'in the order specified (System: General Setup: DNS Servers),'
                        'rather than all at once in parallel.'
        ),
        domain_needed=dict(
            type='bool', default='False',
            description='If this option is set, we will not forward A or AAAA queries for plain names, '
                        'without dots or domain parts, to upstream name servers. '
                        'If the name is not known from /etc/hosts or DHCP then a "not found" answer is returned.'
        ),
        resolv_system=dict(
            type='bool', required=False, default=True,
            description='Forward DNS queries to system nameservers',
        ),
        no_private_reverse=dict(
            type='bool', default='False',
            description='If this option is set, we will not forward reverse DNS lookups (PTR) for '
                        'private addresses (RFC 1918) to upstream name servers. '
                        'Any entries in the Domain Overrides section forwarding private "n.n.n.in-addr.arpa" '
                        'names to a specific server are still forwarded. '
                        'If the IP to name is not known from /etc/hosts, DHCP or a specific domain override then '
                        'a "not found" answer is immediately returned.'
        ),
        add_mac=dict(
            type='str', required=False, options=['', 'standard', 'base64', 'text'], default='',
            description='Add the MAC address of the requestor to DNS queries which are forwarded upstream.',
        ),
        add_subnet=dict(
            type='bool', required=False, default=False,
            description='Add the real client addresses to DNS queries which are forwarded upstream.',
        ),
        strip_subnet=dict(
            type='bool', required=False, default=False,
            description='Strip the subnet received by a downstream DNS server.',
        ),
        # DHCP
        dhcp_disable_interfaces=dict(
            type='list', elements='str', required=False, default=[], aliases=['dhcp_dis_ints', 'ints_no_dhcp'],
            description='Do not provide DHCP, TFTP or router advertisement on the specified interfaces.',
        ),
        dhcp_fqdn=dict(
            type='bool', required=False, default=False,
            description='Registers the qualified names of DHCP clients into the DNS.',
        ),
        dhcp_domain=dict(
            type='str', required=False,
            description='Domain part to registers the qualified names of DHCP clients into the DNS.',
        ),
        dhcp_local=dict(
            type='bool', required=False, default=True,
            description='Sets all DHCP domains as local.',
        ),
        dhcp_lease_max=dict(
            type='int', required=False,
            description='Limits Dnsmasq to the specified maximum number of DHCP leases.',
        ),
        dhcp_authoritative=dict(
            type='bool', required=False, default=False,
            description='Should be set when Dnsmasq is definitely the only DHCP server on a network.',
        ),
        dhcp_reply_delay=dict(
            type='int', required=False,
            description='Delays sending DHCPOFFER and PROXYDHCP replies for at least the specified number of seconds',
        ),
        dhcp_default_fw_rules=dict(
            type='bool', required=False, default=True,
            description='Automatically register firewall rules to allow DHCP traffic for all selected interfaces.',
        ),
        dhcp_enable_ra=dict(
            type='bool', required=False, default=False,
            description='Enable Router Advertisements for all configured DHCPv6 ranges.',
        ),
        dhcp_hasync=dict(
            type='bool', required=False, default=True,
            description='HA sync DHCP general settings.',
        ),
        # ISC / KEA DHCP (legacy)
        regdhcp=dict(
            type='bool', default=False, required=False,
            description='If this option is set, then machines that specify their hostname when requesting a '
                        'DHCP lease will be registered, so that their name can be resolved.'
        ),
        regdhcpdomain=dict(
            type='str', default='',
            description='The domain name to use for DHCP hostname registration. '
                        'If empty, the default system domain is used. '
                        'Note that all DHCP leases will be assigned to the same domain. '
                        'If this is undesired, static DHCP lease registration is able to provide coherent mappings.'
        ),
        regdhcpstatic=dict(
            type='bool', default='False', required=False,
            description='If this option is set, then DHCP static mappings will be registered, '
                        'so that their name can be resolved.'
        ),
        dhcpfirst=dict(
            type='bool', default='False',
            description='If this option is set, then DHCP mappings will be resolved before '
                        'the manual list of names below.'
                        'This only affects the name given for a reverse lookup (PTR).'
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
