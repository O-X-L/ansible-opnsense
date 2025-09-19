#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (C) 2025, AnsibleGuy <guy@ansibleguy.net>
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.handler import \
    module_dependency_error, MODULE_EXCEPTIONS

try:
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.wrapper import module_wrapper
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.defaults.main import \
        OPN_MOD_ARGS, EN_ONLY_MOD_ARG
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.ipsec_general import General

except MODULE_EXCEPTIONS:
    module_dependency_error()

# DOCUMENTATION = 'https://ansible-opnsense.oxl.app/modules/postfix.html'
# EXAMPLES = 'https://ansible-opnsense.oxl.app/modules/postfix.html'


def run_module():
    module_args = dict(
        prefer_old_sa=dict(
          type='bool', required=False, default=False,
          description='If several SAs match always prefer old SAs over new ones',
        ),
        disable_vpn_rules=dict(
          type='bool', required=False, default=False,
          description='This option only applies to legacy tunnel configurations, connections do require manual '
                      'firewall rules being setup',
        ),
        passthrough_networks=dict(
          type='list', elements='str', required=False, default=[],
          description='Exempts traffic for one or more subnets from getting processed by the IPsec stack in the kernel',
        ),
        authentication=dict(
          type='list', elements='str', required=False, default=[],
          description='Select authentication methods to use, leave empty if no challenge response authentication '
                      'is needed',
        ),
        local_group=dict(
          type='str', required=False,
          description='Restrict access to users in the selected local group',
        ),
        # eap-radius
        radius_servers=dict(
          type='list', elements='str', required=False, default=[],
          description='RADIUS servers to configure',
        ),
        radius_accounting=dict(
          type='bool', required=False, default=False,
          description='Enable RADIUS accounting',
        ),
        radius_class_group=dict(
          type='bool', required=False, default=False,
          description='Enable RADIUS Group selection (class_group)',
        ),
        # xauth-pam
        pam_service=dict(
          type='str', required=False, default='ipsec',
          description='PAM service to use for authentication',
        ),
        pam_session=dict(
          type='bool', required=False, default=False,
          description='Open/close a PAM session for each active IKE_SA',
        ),
        pam_trim_email=dict(
          type='bool', required=False, default=True,
          description='If an email address is received as an XAuth username, trim it to just the username part',
        ),
        # Charon
        charon_max_ikev1_exchanges=dict(
          type='int', required=False,
          description='Maximum number of IKEv1 phase 2 exchanges per IKE_SA to keep state about and track concurrently',
        ),
        charon_threads=dict(
          type='int', required=False, default=16,
          description='Number of worker threads, several of these are reserved for long running tasks '
                      'in internal modules and plugins',
        ),
        charon_ikesa_table_size=dict(
          type='int', required=False, default=32,
          description='Size of the IKE SA hash table',
        ),
        charon_ikesa_table_segments=dict(
          type='int', required=False, default=4,
          description='Number of exclusively locked segments in the hash table',
        ),
        charon_init_limit_half_open=dict(
          type='int', required=False, default=1000,
          description='Limit new connections based on the current number of half open IKE_SAs',
        ),
        charon_ignore_acquire_ts=dict(
          type='bool', required=False, default=True,
          description='Prefix each log entry with the connection name and a unique identifier for each IKE_SA',
        ),
        charon_make_before_break=dict(
          type='bool', required=False, default=False,
          description='Initiate IKEv2 reauthentication with a make-before-break instead of a break-before-make scheme',
        ),
        charon_install_routes=dict(
          type='bool', required=False, default=False,
          description='Install routes into a separate routing table for established IPsec tunnels',
        ),
        charon_cisco_unity=dict(
          type='bool', required=False, default=False,
          description='Send Cisco Unity vendor ID payload (IKEv1 only)',
        ),
        # Retransmission
        retransmit_tries=dict(
          type='int', required=False,
          description='Number of retransmissions to send before giving up',
        ),
        retransmit_timeout=dict(
          type='int', required=False,
          description='Timeout in seconds',
        ),
        retransmit_base=dict(
          type='int', required=False,
          description='Base of exponential backoff',
        ),
        retransmit_jitter=dict(
          type='int', required=False,
          description='Maximum jitter in percent to apply randomly to calculated retransmission timeout (0 to disable)',
        ),
        retransmit_limit=dict(
          type='int', required=False,
          description='Upper limit in seconds for calculated retransmission timeout (0 to disable)',
        ),
        # Syslog
        syslog_log_name=dict(
          type='bool', required=False, default=True,
          description='Prefix each log entry with the connection name and a unique numerical identifier '
                      'for each IKE_SA',
        ),
        syslog_log_level=dict(
          type='bool', required=False, default=False,
          description='Add the log level of each message after the subsystem (e.g. [IKE2])',
        ),
        syslog_app=dict(
          type='int', required=False, default=1,
          description='Log level for applications other than daemons',
        ),
        syslog_asn=dict(
          type='int', required=False, default=1,
          description='Log level for low-level encoding/decoding (ASN.1, X.509 etc.)',
        ),
        syslog_cfg=dict(
          type='int', required=False, default=1,
          description='Log level for configuration management and plugins',
        ),
        syslog_chd=dict(
          type='int', required=False, default=1,
          description='Log level for CHILD_SA/IPsec SA',
        ),
        syslog_dmn=dict(
          type='int', required=False, default=1,
          description='Log level for main daemon setup/cleanup/signal handling',
        ),
        syslog_enc=dict(
          type='int', required=False, default=1,
          description='Log level for packet encoding/decoding encryption/decryption operations',
        ),
        syslog_esp=dict(
          type='int', required=False, default=1,
          description='Log level for libipsec library messages',
        ),
        syslog_ike=dict(
          type='int', required=False, default=1,
          description='Log level for IKE_SA/ISAKMP SA',
        ),
        syslog_imc=dict(
          type='int', required=False, default=1,
          description='Log level for Integrity Measurement Collector',
        ),
        syslog_imv=dict(
          type='int', required=False, default=1,
          description='Log level for Integrity Measurement Verifier',
        ),
        syslog_job=dict(
          type='int', required=False, default=1,
          description='Log level for jobs queuing/processing and thread pool management',
        ),
        syslog_knl=dict(
          type='int', required=False, default=1,
          description='Log level for IPsec/Networking kernel interface',
        ),
        syslog_lib=dict(
          type='int', required=False, default=1,
          description='Log level for libstrongwan library messages',
        ),
        syslog_mgr=dict(
          type='int', required=False, default=1,
          description='Log level for IKE_SA manager, handling synchronization for IKE_SA access',
        ),
        syslog_net=dict(
          type='int', required=False, default=1,
          description='Log level for IKE network communication',
        ),
        syslog_pts=dict(
          type='int', required=False, default=1,
          description='Log level for Platform Trust Service',
        ),
        syslog_tls=dict(
          type='int', required=False, default=1,
          description='Log level for libtls library messages',
        ),
        syslog_tnc=dict(
          type='int', required=False, default=1,
          description='Log level for Trusted Network Connect',
        ),
        # Attr
        attr_subnet=dict(
          type='list', elements='str', required=False, default=[],
          description='The protected sub-networks that this edge-device protects (in CIDR notation). '
                      'Usually ignored in deference to local_ts, though macOS clients will use this for routes',
        ),
        attr_dns=dict(
          type='list', elements='str', required=False, default=[],
          description='DNS server',
        ),
        attr_nbns=dict(
          type='list', elements='str', required=False, default=[], aliases=['attr_wins'],
          description='WINS server',
        ),
        # Cisco Unity
        unity_split_include=dict(
          type='list', elements='str', required=False, default=[],
          description='Comma-separated list of subnets to tunnel. The unity plugin provides a connection specific '
                      'approach to assign this attribute',
        ),
        unity_dns_search=dict(
          type='str', required=False,
          description='Default search domain used when resolving host names via the assigned DNS servers',
        ),
        unity_dns_split=dict(
          type='str', required=False,
          description='If split tunneling is used clients might not install the assigned DNS servers globally. '
                      'This space-separated list of domain names allows clients, such as macOS, to selectively '
                      'query the assigned DNS servers',
        ),
        unity_login_banner=dict(
          type='str', required=False,
          description='Message displayed on certain clients after login',
        ),
        unity_save_password=dict(
          type='bool', required=False, default=False,
          description='Allow client to save Xauth password in local storage',
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
    )

    module_wrapper(General(module=module, result=result))
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
