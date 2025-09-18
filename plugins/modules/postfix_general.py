#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (C) 2025, Pascal Rath <contact+opnsense@OXL.at>
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.handler import \
    module_dependency_error, MODULE_EXCEPTIONS

try:
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.wrapper import module_wrapper
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.defaults.main import \
        OPN_MOD_ARGS, EN_ONLY_MOD_ARG
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.postfix_general import General

except MODULE_EXCEPTIONS:
    module_dependency_error()

# DOCUMENTATION = 'https://ansible-opnsense.oxl.app/modules/postfix.html'
# EXAMPLES = 'https://ansible-opnsense.oxl.app/modules/postfix.html'


def run_module():
    module_args = dict(
        myhostname=dict(
            type='str', required=False,
            description='The \'System Hostname\' parameter specifies the internet hostname of this mail system. '
                        'The default is to use the fully-qualified domain name from gethostname(). It is used as a '
                        'default value for many other configuration parameters.',
        ),
        mydomain=dict(
            type='str', required=False,
            description='The \'System Domain\' parameter specifies the local internet domain name. The default is to '
                        'use \'System Hostname\' minus the first component. It is used as a default value for many '
                        'other configuration parameters.',
        ),
        myorigin=dict(
            type='str', required=False,
            description='The \'System Origin\' parameter specifies the domain that locally-posted mail appears to '
                        'come from. The default is to append \'System Hostname\', which is fine for small sites.',
        ),
        inet_interfaces=dict(
            type='list', required=False, default=['all'],
            description='The \'Listen IPs\' parameter specifies a comma-separated list of IP addresses to listen to. '
                        'Default is to listen on all interfaces.',
        ),
        inet_port=dict(
            type='int', required=False, default=25,
            description='Port to listen on. Default is to listen on port 25.',
        ),
        ip_version=dict(
            type='str', required=False, choices=['all', 'ipv4', 'ipv6'], default='all',
            description='Choose which IP versions are allowed, defaults to all. One of: all, ipv4 or ipv6.',
        ),
        bind_address=dict(
            type='str', required=False,
            description='Specify the IPv4 address the server should bind to for outgoing connections. '
                        'In most cases empty is fine.',
        ),
        bind_address6=dict(
            type='str', required=False,
            description='Specify the IPv6 address the server should bind to for outgoing connections. '
                        'In most cases empty is fine.',
        ),
        mynetworks=dict(
            type='list', required=False, elements='str',
            default=['127.0.0.0/8', '[::ffff:127.0.0.0]/104', '[::1]/128'],
            description='The \'Trusted Networks\' parameter specifies the list of trusted SMTP clients. '
                        'In particular, trusted SMTP clients are allowed to relay mail through Postfix. '
                        'Please use CIDR notation like 192.168.0.0/24 separated by spaces. IPv6 addresses '
                        'have to be in square brackets like [::1]/128.',
        ),
        banner=dict(
            type='str', required=False,
            description='The smtpd_banner parameter specifies the text that follows the 220 code in the SMTP '
                        'server\'s greeting banner. Default is "\'System Hostname\' ESMTP Postfix".',
        ),
        message_size_limit=dict(
            type='int', required=False, default=51200000,
            description='Set the max size for messages to accept, default is 51200000 Bytes which is 50MB. '
                        'Values must be entered in Bytes.',
        ),
        masquerade_domains=dict(
            type='list', required=False, elements='str', default=[],
            description='Masquerade internal domains to the outside. When you set example.com, the domain '
                        'host.internal.example.com will be rewritten to example.com when mail leaves the system.'
        ),
        tls_server_compatibility=dict(
            type='str', required=False, choices=['modern', 'intermediate', 'old'], default='intermediate',
            description='TLS version/cipher compatibility of the SMTP service. One of: modern, intermediate or old.'
                    'Default to intermediate.',
        ),
        tls_client_compatibility=dict(
            type='str', required=False, choices=['modern', 'intermediate', 'old'], default='intermediate',
            description='TLS version/cipher compatibility of the SMTP Client. One of: modern, intermediate or old.'
                    'Default to intermediate.',
        ),
        tlswrappermode=dict(
            type='bool', required=False, default=0,
            description='If enabled it allows you to use SMTPS.',
        ),
        certificate=dict(
            type='str', required=False,
            description='Choose the certificate to use when other servers want to do TLS with you.',
        ),
        ca=dict(
            type='str', required=False,
            description='Choose the Certificate Authority which signed your certificate.',
        ),
        smtpclient_security=dict(
            type='str', required=False, choices=['none', 'may', 'encrypt', 'dane'], default='may',
            description='\'none\' will disable TLS for sending mail. \'may\' will use TLS when offered. '
                        '\'encrypt\' will enforce TLS on all connections. '
                        '\'dane\' will enforce TLS if a TLSA-Record is published.',
        ),
        relayhost=dict(
            type='str', required=False, aliases=['smarthost'],
            description='Set the IP address or FQDN where all outgoing mails are sent to.',
        ),
        smtpauth_enabled=dict(
            type='bool', required=False, default=False,
            description='Check this to enable authentication against your Smarthost.',
        ),
        smtpauth_user=dict(
            type='str', required=False,
            description='The username to use for SMTP authentication.',
        ),
        smtpauth_password=dict(
            type='str', required=False, no_log=True,
            description='The password to use for SMTP authentication.',
        ),
        enforce_recipient_check=dict(type='bool', required=False, default=False),
        extensive_helo_restrictions=dict(type='bool', required=False, default=False),
        extensive_sender_restrictions=dict(type='bool', required=False, default=False),
        reject_unknown_client_hostname=dict(type='bool', required=False, default=False),
        reject_non_fqdn_helo_hostname=dict(type='bool', required=False, default=False),
        reject_invalid_helo_hostname=dict(type='bool', required=False, default=False),
        reject_unknown_helo_hostname=dict(type='bool', required=False, default=False),
        reject_unauth_pipelining=dict(type='bool', required=False, default=True),
        reject_unknown_sender_domain=dict(
            type='bool', required=False, default=True,
            description='This will reject mails from domains which do not exist.',
        ),
        reject_unknown_recipient_domain=dict(type='bool', required=False, default=True),
        reject_non_fqdn_sender=dict(
            type='bool', required=False, default=True,
            description='For example senders without a domain or only a hostname.',
        ),
        reject_non_fqdn_recipient=dict(
            type='bool', required=False, default=True,
            description='For example recipients without a domain or only a hostname.',
        ),
        permit_sasl_authenticated=dict(
            type='bool', required=False, default=True,
            description='Allow SASL authenticated senders to relay. Will also enable smtpd_sasl_auth.',
        ),
        permit_tls_clientcerts=dict(type='bool', required=False, default=True),
        permit_mynetworks=dict(type='bool', required=False, default=True),
        reject_unauth_destination=dict(type='bool', required=False, default=True),
        reject_unverified_recipient=dict(
            type='bool', required=False, default=False,
            description='Use Recipient Address Verification. Please keep in mind that this could put significant '
                        'load onto the next server.',
        ),
        delay_warning_time=dict(
            type='int', required=False, default=0,
            description='Time until we send a notification to the sender if mail is delayed (in hours). '
                        '0 or empty to disable.',
        ),
        **EN_ONLY_MOD_ARG,
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
        required_if=[
            ('smtpauth_enabled', True, ('smtpauth_user', 'smtpauth_password')),
        ],
    )

    module_wrapper(General(module=module, result=result))
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
