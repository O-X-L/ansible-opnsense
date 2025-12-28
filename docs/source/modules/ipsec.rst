.. _modules_ipsec:

.. include:: ../_include/head.rst

=====
IPSec
=====

**STATE**: stable

**TESTS**: `ipsec_cert <https://github.com/O-X-L/ansible-opnsense/blob/stable/tests/ipsec_cert.yml>`_ |
`ipsec_psk <https://github.com/O-X-L/ansible-opnsense/blob/stable/tests/ipsec_psk.yml>`_ |
`ipsec_connection <https://github.com/O-X-L/ansible-opnsense/blob/stable/tests/ipsec_connection.yml>`_ |
`ipsec_pool <https://github.com/O-X-L/ansible-opnsense/blob/stable/tests/ipsec_pool.yml>`_ |
`ipsec_vti <https://github.com/O-X-L/ansible-opnsense/blob/stable/tests/ipsec_vti.yml>`_ |
`ipsec_manual_spd <https://github.com/O-X-L/ansible-opnsense/blob/stable/tests/ipsec_manual_spd.yml>`_ |
`ipsec_general <https://github.com/O-X-L/ansible-opnsense/blob/stable/tests/ipsec_general.yml>`_

**API Docs**: `Core - IPSec <https://docs.opnsense.org/development/api/core/ipsec.html>`_

**Service Docs**: `IPSec <https://docs.opnsense.org/manual/vpnet.html#ipsec>`_ |
`IPSec Examples <https://docs.opnsense.org/manual/vpnet.html#new-23-1-vpn-ipsec-connections>`_ |
`IPSec VTI <https://docs.opnsense.org/manual/how-tos/ipsec-s2s-conn-route.html>`_

Contribution
************

Thanks to `@atammy-narmi <https://github.com/atammy-narmi>`_ for developing the :code:`ipsec_psk` module!
Thanks to `@jiuka <https://github.com/jiuka>`_ for developing the :code:`ipsec_manual_spd` module!

Thanks to `@Rath <https://github.com/superstes>`_ for developing the other modules!

----

Definition
**********

.. include:: ../_include/param_basic.rst

oxlorg.opnsense.ipsec_connection
================================

Module alias: oxlorg.opnsense.ipsec_tunnel

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "name","string","true","\-","description, desc","Unique connection/tunnel name"
    "local_addresses","list","false","\-","local_addr, local","Local address[es] to use for IKE communication. Accepts single IPv4/IPv6 addresses, DNS names, CIDR subnets or IP address ranges. As an initiator, the first non-range/non-subnet is used to initiate the connection from. As a responder the local destination address must match at least to one of the specified addresses, subnets or ranges. If FQDNs are assigned, they are resolved every time a configuration lookup is done. If DNS resolution times out, the lookup is delayed for that time. When left empty %any is choosen as default"
    "local_port","string","false","500","\-","UDP port for IKE communication. If the default of port 500 is used, automatic IKE port floating to port 4500 is used to work around NAT issues"
    "remote_addresses","list","false","\-","remote_addr, remote","Remote address[es] to use for IKE communication. Accepts single IPv4/IPv6 addresses, DNS names, CIDR subnets or IP address ranges. As an initiator, the first non-range/non-subnet is used to initiate the connection to. As a responder the local destination address must match at least to one of the specified addresses, subnets or ranges. If FQDNs are assigned, they are resolved every time a configuration lookup is done. If DNS resolution times out, the lookup is delayed for that time. To initiate a connection, at least one specific address or DNS name must be specified"
    "remote_port","string","false","500","\-","UDP port for IKE communication. If the default of port 500 is used, automatic IKE port floating to port 4500 is used to work around NAT issues"
    "pools","list","false","\-","networks","List of named IP pools to allocate virtual IP addresses and other configuration attributes from. Each name references a pool by name from either the pools section or an external pool. Note that the order in which they are queried primarily depends on the plugin order"
    "proposals","list","false","['default']","props","A proposal is a set of algorithms. For non-AEAD algorithms this includes IKE an encryption algorithm, an integrity algorithm, a pseudo random function (PRF) and a Diffie-Hellman key exchange group. For AEAD algorithms, instead of encryption and integrity algorithms a combined algorithm is used. With IKEv2 multiple algorithms of the same kind can be specified in a single proposal, from which one gets selected. For IKEv1 only one algorithm per kind is allowed per proposal, more algorithms get implicitly stripped. Use multiple proposals to offer different algorithm combinations with IKEv1. Algorithm keywords get separated using dashes. Multiple proposals may be separated by commas. The special value default adds a default proposal of supported algorithms considered safe and is usually a good choice for interoperability."
    "unique","string","false","no","\-","One of: 'no', 'never', 'keep', 'replace'; Connection uniqueness policy to enforce. To avoid multiple connections from the same user, a uniqueness policy can be enforced."
    "aggressive","boolean","false","false","aggr","Enables IKEv1 Aggressive Mode instead of IKEv1 Main Mode with Identity Protection. Aggressive Mode is considered less secure because the ID and HASH payloads are exchanged unprotected. This allows a passive attacker to snoop peer identities and even worse, start dictionary attacks on the Preshared Key"
    "version","string","false","ike","vers, v","One of: 'ike', 'ikev1', 'ikev2'; IKE major version to use for connection. 1 uses IKEv1 aka ISAKMP, 2 uses IKEv2. A connection using IKEv1+IKEv2 accepts both IKEv1 and IKEv2 as a responder and initiates the connection actively with IKEv2"
    "mobike","boolean","false","true","mob","Enables MOBIKE on IKEv2 connections. MOBIKE is enabled by default on IKEv2 connections and allows mobility of clients and multi-homing on servers by migrating active IPsec tunnels. Usually keeping MOBIKE enabled is unproblematic, as it is not used if the peer does not indicate support for it. However, due to the design of MOBIKE, IKEv2 always floats to UDP port 4500 starting from the second exchange. Some implementations don’t like this behavior, hence it can be disabled"
    "encapsulation","boolean","false","false","udp_encapsulation, encap","To enforce UDP encapsulation of ESP packets, the IKE daemon can manipulate the NAT detection payloads. This makes the peer believe that a NAT situation exist on the transmission path, forcing it to encapsulate ESP packets in UDP. Usually this is not required but it can help to work around connectivity issues with too restrictive intermediary firewalls that block ESP packets"
    "reauth_seconds","integer","false","\-","reauth, reauth_sec, reauth_time","Time to schedule IKE reauthentication. IKE reauthentication recreates the IKE/ISAKMP SA from scratch and re-evaluates the credentials. In asymmetric configurations (with EAP or configuration payloads) it might not be possible to actively reauthenticate as responder. The IKEv2 reauthentication lifetime negotiation can instruct the client to perform reauthentication. Reauthentication is disabled by default (0). Enabling it usually may lead to small connection interruptions as strongSwan uses a break-before-make policy with IKEv2 by default"
    "rekey_seconds","integer","false","\-","rekey, rekey_sec, rekey_time","IKE rekeying refreshes key material using a Diffie-Hellman key exchange, but does not re-check associated credentials. It is supported with IKEv2 only. IKEv1 performs a reauthentication procedure instead. With the default value, IKE rekeying is scheduled every 4 hours minus the configured rand_time. If a reauth_time is configured, rekey_time defaults to zero, disabling rekeying. In that case set rekey_time explicitly to both enforce rekeying and reauthentication"
    "over_seconds","integer","false","\-","over, over_sec, over_time","Hard IKE_SA lifetime if rekey/reauth does not complete, as time. To avoid having an IKE or ISAKMP connection kept alive if IKE reauthentication or rekeying fails perpetually, a maximum hard lifetime may be specified. If the IKE_SA fails to rekey or reauthenticate within the specified time, the IKE_SA gets closed. In contrast to CHILD_SA rekeying, over_time is relative in time to the rekey_time and reauth_time values, as it applies to both. The default is 10% of either rekey_time or reauth_time, whichever value is larger. [0.1 * max(rekey_time, reauth_time)]"
    "dpd_delay_seconds","integer","false","\-","dpd_delay, dpd_delay_sec, dpd_delay_time","Interval to check the liveness of a peer actively using IKEv2 INFORMATIONAL exchanges or IKEv1 R_U_THERE messages. Active DPD checking is only enforced if no IKE or ESP/AH packet has been received for the configured DPD delay. Defaults to 0s"
    "dpd_timeout_seconds","integer","false","\-","dpd_timeout, dpd_timeout_sec","Charon by default uses the normal retransmission mechanism and timeouts to check the liveness of a peer, as all messages are used for liveness checking. For compatibility reasons, with IKEv1 a custom interval may be specified. This option has no effect on IKEv2 connections"
    "send_certificate_request","boolean","false","true","send_cert_req","Send certificate request payloads to offer trusted root CA certificates to the peer. Certificate requests help the peer to choose an appropriate certificate/private key for authentication and are enabled by default. Disabling certificate requests can be useful if too many trusted root CA certificates are installed, as each certificate request increases the size of the initial IKE packets"
    "send_certificate","string","false","\-","send_cert","One of: '' (default), 'ifasked', 'never', 'always'; Send certificate payloads when using certificate authentication. With the default of [ifasked] the daemon sends certificate payloads only if certificate requests have been received. [never] disables sending of certificate payloads altogether whereas [always] causes certificate payloads to be sent unconditionally whenever certificate-based authentication is used"
    "keying_tries","integer","false","\-","keyingtries","Number of retransmission sequences to perform during initial connect. Instead of giving up initiation after the first retransmission sequence with the default value of 1, additional sequences may be started according to the configured value. A value of 0 initiates a new sequence until the connection establishes or fails with a permanent error"
    "reload","boolean","false","true","\-", .. include:: ../_include/param_reload.rst

oxlorg.opnsense.ipsec_pool
==========================

Module alias: oxlorg.opnsense.ipsec_network

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "name","string","true","\-","\-","Unique pool/network name"
    "network","string","false for state changes, else true","\-","net, cidr","Pool network in CIDR format"
    "dns","list of strings","false","\-","\-","DNS servers to push as configuration payload. Accepts multiple IPv4/IPv6 addresses"
    "reload","boolean","false","true","\-", .. include:: ../_include/param_reload.rst

oxlorg.opnsense.ipsec_child
===========================

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "name","string","true","\-","description, desc","Unique name to identify the entry"
    "connection","string","false for state changes, else true","\-","tunnel, conn, tun","Connection to link this child to"
    "mode","string","false","tunnel","\-","One of: 'tunnel', 'transport', 'pass', 'drop'; IPsec Mode to establish CHILD_SA with. tunnel negotiates the CHILD_SA in IPsec Tunnel Mode whereas transport uses IPsec Transport Mode. pass and drop are used to install shunt policies which explicitly bypass the defined traffic from IPsec processing or drop it, respectively"
    "local_net","list","true","\-","local_traffic_selectors, local_cidr, local_ts, local","List of local traffic selectors to include in CHILD_SA. Each selector is a CIDR subnet definition"
    "remote_net","list","true","\-","remote_traffic_selectors, remote_cidr, remote_ts, remote","List of remote traffic selectors to include in CHILD_SA. Each selector is a CIDR subnet definition"
    "sha256_96","boolean","false","false","sha256","HMAC-SHA-256 is used with 128-bit truncation with IPsec. For compatibility with implementations that incorrectly use 96-bit truncation this option may be enabled to configure the shorter truncation length in the kernel. This is not negotiated, so this only works with peers that use the incorrect truncation length (or have this option enabled)"
    "start_action","string","false","start","start","One of: 'none', 'trap|start', 'route', 'start', 'trap'; Action to perform after loading the configuration. The default of none loads the connection only, which then can be manually initiated or used as a responder configuration. The value trap installs a trap policy which triggers the tunnel as soon as matching traffic has been detected. The value start initiates the connection actively. To immediately initiate a connection for which trap policies have been installed, user Trap|start"
    "close_action","string","false","none","close","One of: 'none', 'trap', 'start'; Action to perform after a CHILD_SA gets closed by the peer. The default of none does not take any action. trap installs a trap policy for the CHILD_SA (note that this is redundant if start_action includes trap). start tries to immediately re-create the CHILD_SA. close_action does not provide any guarantee that the CHILD_SA is kept alive. It acts on explicit close messages only but not on negotiation failures. Use trap policies to reliably re-create failed CHILD_SAs"
    "dpd_action","string","false","clear","dpd","One of: 'clear', 'trap', 'start'; Action to perform for this CHILD_SA on DPD timeout. The default clear closes the CHILD_SA and does not take further action. trap installs a trap policy, which will catch matching traffic and tries to re-negotiate the tunnel on-demand (note that this is redundant if start_action includes trap. restart immediately tries to re-negotiate the CHILD_SA under a fresh IKE_SA"
    "policies","boolean","false","true","pols","Whether to install IPsec policies or not. Disabling this can be useful in some scenarios e.g. VTI where policies are not managed by the IKE daemon"
    "request_id","integer","false","\-","req_id, reqid","This might be helpful in some scenarios, like route based tunnels (VTI), but works only if each CHILD_SA configuration is instantiated not more than once. The default uses dynamic reqids, allocated incrementally"
    "esp_proposals","list","false","['default']","esp_props, esp","Choose 'default' or at least one of the options shown in the Web-UI"
    "rekey_seconds","integer","false","3600","rekey_time, rekey","Time to schedule CHILD_SA rekeying. CHILD_SA rekeying refreshes key material, optionally using a Diffie-Hellman exchange if a group is specified in the proposal. To avoid rekey collisions initiated by both ends simultaneously, a value in the range of rand_time gets subtracted to form the effective soft lifetime. By default CHILD_SA rekeying is scheduled every hour, minus rand_time"
    "reload","boolean","false","true","\-", .. include:: ../_include/param_reload.rst

oxlorg.opnsense.ipsec_vti
=========================

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "name","string","true","\-","description, desc","Unique name to identify the entry"
    "request_id","integer","false for state changes, else true","\-","req_id, reqid","This might be helpful in some scenarios, like route based tunnels (VTI), but works only if each CHILD_SA configuration is instantiated not more than once. The default uses dynamic reqids, allocated incrementally"
    "local_address","string","false","\-","local_addr, local","Local tunnel address used for the outer IP header of ESP packets"
    "remote_address","string","false","\-","remote_addr, remote","Remote tunnel address used for the outer IP header of ESP packets"
    "local_tunnel_address","string","false","\-","local_tun_addr, tunnel_local, local_tun","Inner tunnel local address to be used for routing purposes"
    "remote_tunnel_address","string","false","\-","remote_tun_addr, tunnel_remote, remote_tun","Inner tunnel remote address to be used for routing purposes"
    "local_tunnel_secondary_address","string","false","\-","local_tun_addr, tunnel_local, local_tun","Secondary inner tunnel local address to be used for routing purposes"
    "remote_tunnel_secondary_address","string","false","\-","remote_tun_addr, tunnel_remote, remote_tun","Secondary nner tunnel remote address to be used for routing purposes"
    "skip_firewall","boolean","false","false","skip_fw","Skip this  interface in our firewall rules which removes this inconsistencies"
    "reload","boolean","false","true","\-", .. include:: ../_include/param_reload.rst

oxlorg.opnsense.ipsec_auth_local
================================

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "name","string","true","\-","description, desc","Unique name to identify the entry"
    "connection","string","false for state changes, else true","\-","tunnel, conn, tun","Connection to use this local authentication with"
    "round","integer","false","0","\-","Numeric identifier by which authentication rounds are sorted"
    "authentication","string","false","psk","auth","One of: 'psk', 'pubkey', 'eap-tls', 'eap-mschapv2', 'xauth-pam', 'eap-radius'; Authentication to perform for this round, when using Pre-Shared key make sure to define one under 'VPN->IPsec->Pre-Shared Keys'"
    "id","string","false","\-","ike_id","IKE identity to use for authentication round. When using certificate authentication. The IKE identity must be contained in the certificate, either as the subject DN or as a subjectAltName (the identity will default to the certificate’s subject DN if not specified). Refer to https://docs.strongswan.org/docs/5.9/config/identityParsing.html for details on how identities are parsed and may be configured"
    "eap_id","string","false","\-","\-","Must be defined if authentication is set to one of: ['eap-tls', 'eap-mschapv2', 'eap-radius']; Client EAP-Identity to use in EAP-Identity exchange and the EAP method"
    "certificates","list","false","\-","certs","Certificate or public-key must be defined if authentication is set to 'pubkey'; List of certificate candidates to use for authentication"
    "public_keys","list","false","\-","pubkeys","Certificate or public-key must be defined if authentication is set to 'pubkey'; List of raw public key candidates to use for authentication"
    "reload","boolean","false","true","\-", .. include:: ../_include/param_reload.rst

oxlorg.opnsense.ipsec_auth_remote
=================================

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "name","string","true","\-","description, desc","Unique name to identify the entry"
    "connection","string","false for state changes, else true","\-","tunnel, conn, tun","Connection to use this local authentication with"
    "round","integer","false","0","\-","Numeric identifier by which authentication rounds are sorted"
    "authentication","string","false","psk","auth","One of: 'psk', 'pubkey', 'eap-tls', 'eap-mschapv2', 'xauth-pam', 'eap-radius'; Authentication to perform for this round, when using Pre-Shared key make sure to define one under 'VPN->IPsec->Pre-Shared Keys'"
    "id","string","false","\-","ike_id","IKE identity to use for authentication round. When using certificate authentication. The IKE identity must be contained in the certificate, either as the subject DN or as a subjectAltName (the identity will default to the certificate’s subject DN if not specified). Refer to https://docs.strongswan.org/docs/5.9/config/identityParsing.html for details on how identities are parsed and may be configured"
    "eap_id","string","false","\-","\-","Must be defined if authentication is set to one of: ['eap-tls', 'eap-mschapv2', 'eap-radius']; Client EAP-Identity to use in EAP-Identity exchange and the EAP method"
    "certificates","list","false","\-","certs","Certificate or public-key must be defined if authentication is set to 'pubkey'; List of certificate candidates to use for authentication"
    "public_keys","list","false","\-","pubkeys","Certificate or public-key must be defined if authentication is set to 'pubkey'; List of raw public key candidates to use for authentication"
    "ca_certificates","list","false","\-","ca_certs","List of certificate authority candidates to use for authentication"
    "eap_radius_groups","list","false","\-","radius_groups, groups","List of group memberships to require. The client must prove membership to at least one of the specified groups"
    "reload","boolean","false","true","\-", .. include:: ../_include/param_reload.rst

oxlorg.opnsense.ipsec_cert
==========================

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "name","string","true","\-","\-","Name of the key-pair - used to identify the entry."
    "public_key","string","false for state changes, else true","\-","pub_key, pub","\-"
    "private_key","string","false for state changes, else true","\-","priv_key, priv","\-"
    "type","string","false","rsa","\-","Type of the key. One of: 'rsa' or 'ecdsa'"
    "reload","boolean","false","true","\-", .. include:: ../_include/param_reload.rst

oxlorg.opnsense.ipsec_psk
=========================

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "identity_local","string","true","\-","identity, ident","This can be either an IP address, fully qualified domain name or an email address."
    "identity_remote","string","false","\-","remote_ident","(optional) This can be either an IP address, fully qualified domain name or an email address to identify the remote host."
    "psk","string","true","\-","key, secret","\-"
    "type","string","false","\-","kind","One of: 'PSK', 'EAP'"
    "match_fields","list of strings","false","identity_local","\-","At least one of: 'identity_local', 'identity_remote'. Fields that are used to match configured routes with the running config - if any of those fields are changed, the module will think it's a new route"

oxlorg.opnsense.ipsec_manual_spd
================================

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "name","string","true","\-","description, desc","Unique name to identify the entry"
    "request_id","integer","false","\-","req_id, reqid","Reqestid to register this manual spd entry on."
    "connection_child","string","false","\-","\-","Connection child to register this manual spd entry on."
    "source","string","false for deletion, else true","\-","s, src, source_net","Source network, usually the networks you would like to accept using network address translation."
    "destination","string","false","\-","d, dest, destination_net","Destination network, leave empty to use the networks propagated in the child sa."

oxlorg.opnsense.ipsec_general
=============================

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "prefer_old_sa","boolean","False","False","\-","If several SAs match always prefer old SAs over new ones"
    "disable_vpn_rules","boolean","False","False","\-","This option only applies to legacy tunnel configurations, connections do require manual firewall rules being setup"
    "passthrough_networks","list of strings","False","[]","\-","Exempts traffic for one or more subnets from getting processed by the IPsec stack in the kernel"
    "authentication","list of strings","False","[]","\-","Select authentication methods to use, leave empty if no challenge response authentication is needed"
    "local_group","strings","False","\-","\-","Restrict access to users in the selected local group"
    "radius_servers","list of strings","False","[]","\-","RADIUS servers to configure"
    "radius_accounting","boolean","False","False","\-","Enable RADIUS accounting"
    "radius_class_group","boolean","False","False","\-","Enable RADIUS Group selection (class_group)"
    "pam_service","strings","False","ipsec","\-","PAM service to use for authentication"
    "pam_session","boolean","False","False","\-","Open/close a PAM session for each active IKE_SA"
    "pam_trim_email","boolean","False","True","\-","If an email address is received as an XAuth username, trim it to just the username part"
    "charon_max_ikev1_exchanges","integer","False","\-","\-","Maximum number of IKEv1 phase 2 exchanges per IKE_SA to keep state about and track concurrently"
    "charon_threads","integer","False","16","\-","Number of worker threads,several of these are reserved for long running tasks in internal modules and plugins"
    "charon_ikesa_table_size","integer","False","32","\-","Size of the IKE SA hash table"
    "charon_ikesa_table_segments","integer","False","4","\-","Number of exclusively locked segments in the hash table"
    "charon_init_limit_half_open","integer","False","1000","\-","Limit new connections based on the current number of half open IKE_SAs"
    "charon_ignore_acquire_ts","boolean","False","True","\-","Prefix each log entry with the connection name and a unique numerical identifier for each IKE_SA"
    "charon_make_before_break","boolean","False","False","\-","Initiate IKEv2 reauthentication with a make-before-break instead of a break-before-make scheme"
    "charon_install_routes","boolean","False","False","\-","Install routes into a separate routing table for established IPsec tunnels"
    "charon_cisco_unity","boolean","False","False","\-","Send Cisco Unity vendor ID payload (IKEv1 only)"
    "retransmit_tries","integer","False","\-","\-","Number of retransmissions to send before giving up"
    "retransmit_timeout","integer","False","\-","\-","Timeout in seconds"
    "retransmit_base","integer","False","\-","\-","Base of exponential backoff"
    "retransmit_jitter","integer","False","\-","\-","Maximum jitter in percent to apply randomly to calculated retransmission timeout (0 to disable)"
    "retransmit_limit","integer","False","\-","\-","Upper limit in seconds for calculated retransmission timeout (0 to disable)"
    "syslog_log_name","boolean","False","True","\-","Prefix each log entry with the connection name and a unique numerical identifier for each IKE_SA"
    "syslog_log_level","boolean","False","False","\-","Add the log level of each message after the subsystem (e.g. [IKE2])"
    "syslog_app","integer","False","1","\-","Log level for applications other than daemons"
    "syslog_asn","integer","False","1","\-","Log level for low-level encoding/decoding (ASN.1, X.509 etc.)"
    "syslog_cfg","integer","False","1","\-","Log level for configuration management and plugins"
    "syslog_chd","integer","False","1","\-","Log level for CHILD_SA/IPsec SA"
    "syslog_dmn","integer","False","1","\-","Log level for main daemon setup/cleanup/signal handling"
    "syslog_enc","integer","False","1","\-","Log level for packet encoding/decoding encryption/decryption operations"
    "syslog_esp","integer","False","1","\-","Log level for libipsec library messages"
    "syslog_ike","integer","False","1","\-","Log level for IKE_SA/ISAKMP SA"
    "syslog_imc","integer","False","1","\-","Log level for Integrity Measurement Collector"
    "syslog_imv","integer","False","1","\-","Log level for Integrity Measurement Verifier"
    "syslog_job","integer","False","1","\-","Log level for jobs queuing/processing and thread pool management"
    "syslog_knl","integer","False","1","\-","Log level for IPsec/Networking kernel interface"
    "syslog_lib","integer","False","1","\-","Log level for libstrongwan library messages"
    "syslog_mgr","integer","False","1","\-","Log level for IKE_SA manager, handling synchronization for IKE_SA access"
    "syslog_net","integer","False","1","\-","Log level for IKE network communication"
    "syslog_pts","integer","False","1","\-","Log level for Platform Trust Service"
    "syslog_tls","integer","False","1","\-","Log level for libtls library messages"
    "syslog_tnc","integer","False","1","\-","Log level for Trusted Network Connect"
    "attr_subnet","list of strings","False","[]","\-","The protected sub-networks that this edge-device protects (in CIDR notation). Usually ignored in deference to local_ts, though macOS clients will use this for routes"
    "attr_dns","list of strings","False","[]","\-","DNS server"
    "attr_nbns","list of strings","False","[]","attr_wins","WINS server"
    "unity_split_include","list of strings","False","[]","\-","Comma-separated list of subnets to tunnel. The unity plugin provides a connection specific approach to assign this attribute"
    "unity_dns_search","strings","False","\-","\-","Default search domain used when resolving host names via the assigned DNS servers"
    "unity_dns_split","strings","False","\-","\-","If split tunneling is used clients might not install the assigned DNS servers globally. This space-separated list of domain names allows clients, such as macOS, to selectively query the assigned DNS servers"
    "unity_login_banner","strings","False","\-","\-","Message displayed on certain clients after login"
    "unity_save_password","boolean","False","False","\-","Allow client to save Xauth password in local storage"
    "reload","boolean","false","true","\-", .. include:: ../_include/param_reload.rst


Usage
*****

To apply changes to the keys, you need to set 'reload: true' on each call or use the :ref:`oxlorg.opnsense.reload <modules_reload>` module to apply it once you finished modifying all entries!

As far as I can tell - the IPSec service gets restarted one you do so - be aware of that.

Vault
=====

You may want to use '**ansible-vault**' to **encrypt** your 'private_key' content!

.. code-block:: bash

    ansible-vault encrypt_string '-----BEGIN RSA PRIVATE KEY-----\n...-----END RSA PRIVATE KEY-----\n'

    # or encrypt the private_key file beforehand (might be easier)
    ansible-vault encrypt /path/to/private/key/file.pem

----

Examples
********

oxlorg.opnsense.ipsec_connection
================================

.. code-block:: yaml

    - hosts: firewalls
      connection: local
      gather_facts: false
      module_defaults:
        group/oxlorg.opnsense.all:
          firewall: 'opnsense.template.oxlorg.net'
          api_credential_file: '/home/guy/.secret/opn.key'

        oxlorg.opnsense.list:
          target: 'ipsec_connection'

      tasks:
        - name: Example
          oxlorg.opnsense.ipsec_connection:
            name: IPSec Connection
            # state: 'absent'
            # local_addresses: []
            # local_port: 500
            # remote_addresses: []
            # remote_port: 500
            # pools: []
            # proposals: ['default']
            # unique: false
            # aggressive: false
            # version: ike
            # mobike: true
            # encapsulation: false
            # reauth_seconds:
            # rekey_seconds:
            # over_seconds:
            # dpd_delay_seconds:
            # dpd_timeout_seconds:
            # send_certificate_request: true
            # send_certificate:
            # keying_tries:
            # debug: false

        - name: Adding IPSec Site A
          oxlorg.opnsense.ipsec_connection:
            name: IPSec Example Siet2Site
            local_addresses: 10.10.1.1
            remote_addresses: 10.10.1.2

        - name: Changing IPSec Site A
          oxlorg.opnsense.ipsec_connection:
            name: IPSec Example Siet2Site
            version: ike2
            local_addresses: 10.10.1.1
            remote_addresses: 10.10.1.2

        - name: Listing IPSec connections
          oxlorg.opnsense.list:
          #  target: 'ipsec_connection'
          register: existing_ipsec_connections

        - name: Printing
          ansible.builtin.debug:
            var: existing_ipsec_connections.data

----

oxlorg.opnsense.ipsec_pool
==========================

.. code-block:: yaml

    - hosts: firewalls
      connection: local
      gather_facts: false
      module_defaults:
        group/oxlorg.opnsense.all:
          firewall: 'opnsense.template.oxlorg.net'
          api_credential_file: '/home/guy/.secret/opn.key'

        oxlorg.opnsense.list:
          target: 'ipsec_pool'

      tasks:
        - name: Example
          oxlorg.opnsense.ipsec_pool:
            name: IPSec POOL
            network: 192.168.1.0/28
            # dns:
            # state: 'absent'
            # debug: false

        - name: Listing IPSec pools
          oxlorg.opnsense.list:
          #  target: 'ipsec_pool'
          register: existing_ipsec_pool

        - name: Printing
          ansible.builtin.debug:
            var: existing_ipsec_pool.data

----

oxlorg.opnsense.ipsec_cert
==========================

.. code-block:: yaml

    - hosts: firewalls
      connection: local
      gather_facts: false
      module_defaults:
        group/oxlorg.opnsense.all:
          firewall: 'opnsense.template.opnsense.oxl.app'
          api_credential_file: '/home/guy/.secret/opn.key'

        oxlorg.opnsense.list:
          target: 'ipsec_cert'

      tasks:
        - name: Example
          oxlorg.opnsense.ipsec_cert:
            name: 'example'
            public_key: |
              -----BEGIN PUBLIC KEY-----
              ...
              -----END PUBLIC KEY-----
            private_key: |
              -----BEGIN RSA PRIVATE KEY-----
              ...
              -----END RSA PRIVATE KEY-----

            # reload: false

        - name: Adding key-pair and applying it
          oxlorg.opnsense.ipsec_cert:
            name: 'test1'
            public_key: |
              -----BEGIN PUBLIC KEY-----
              ...
              -----END PUBLIC KEY-----
            private_key: !vault ...
            reload: true

        - name: Listing
          oxlorg.opnsense.list:
          #  target: 'ipsec_cert'
          no_log: true  # could log private keys
          register: existing_entries

        - name: Printing Certificates
          ansible.builtin.debug:
            var: existing_entries.data

        - name: Manually reloading/applying config
          oxlorg.opnsense.reload:
            target: 'ipsec'

----

oxlorg.opnsense.ipsec_psk
=========================

.. code-block:: yaml

    - hosts: firewalls
      connection: local
      gather_facts: false
      module_defaults:
        group/oxlorg.opnsense.all:
          firewall: 'opnsense.template.opnsense.oxl.app'
          api_credential_file: '/home/guy/.secret/opn.key'

        oxlorg.opnsense.list:
          target: 'ipsec_psk'

      tasks:
        - name: Example
          oxlorg.opnsense.ipsec_psk:
            identity: 'example'
            psk: 'secret'
            # type: 'PSK'
            # identity_remote: ''

        - name: Adding
          oxlorg.opnsense.ipsec_psk:
            identity: 'test1'
            psk: 'my-super-secret'

        - name: Removing
          oxlorg.opnsense.ipsec_psk:
            identity: 'test1'
            state: 'absent'

----

oxlorg.opnsense.ipsec_manual_spd
================================

.. code-block:: yaml

    - hosts: firewalls
      connection: local
      gather_facts: false
      module_defaults:
        group/oxlorg.opnsense.all:
          firewall: 'opnsense.template.opnsense.oxl.app'
          api_credential_file: '/home/guy/.secret/opn.key'

        oxlorg.opnsense.list:
          target: 'ipsec_manual_spd'

      tasks:
        - name: Example
          oxlorg.opnsense.ipsec_manual_spd:
            name: 'example'
            # request_id: 42
            connection_child: 'Connection Name - Child Name'
            source: 192.168.100.0/24
            # destination: 172.16.0.0/24
            # state: 'absent'
            # debug: false

        - name: Adding Manual SPD
          oxlorg.opnsense.ipsec_manual_spd:
            name: 'example'
            request_id: 100
            source: 10.0.99.0/24

        - name: Change Manual SPD
          oxlorg.opnsense.ipsec_manual_spd:
            name: 'example'
            connection_child: 'Connection Name - Child Name'
            source: 10.0.99.0/24

        - name: Removing Manual SPD
          oxlorg.opnsense.ipsec_manual_spd:
            name: 'example'
            state: 'absent'

        - name: Listing Manual SPD
          oxlorg.opnsense.list:
          #  target: 'ipsec_manual_spd'
          register: existing_manual_spd

        - name: Printing
          ansible.builtin.debug:
            var: existing_manual_spd.data

----

oxlorg.opnsense.ipsec_general
=============================

.. code-block:: yaml

  
    - hosts: firewalls
      connection: local
      gather_facts: false
      module_defaults:
        group/oxlorg.opnsense.all:
          firewall: 'opnsense.template.oxlorg.net'
          api_credential_file: '/home/guy/.secret/opn.key'

      tasks:
        - name: Example - General
          oxlorg.opnsense.ipsec_general:
            # prefer_old_sa: false
            # disable_vpn_rules: false
            # passthrough_networks: []
            # authentication: []
            # local_group
            # radius_servers: []
            # radius_accounting: false
            # radius_class_group: false
            # pam_service: ipsec
            # pam_session: false
            # pam_trim_email: true
            # charon_max_ikev1_exchanges:
            # charon_threads: 16
            # charon_ikesa_table_size: 32
            # charon_ikesa_table_segments: 4
            # charon_ignore_acquire_ts: true
            # charon_make_before_break: false
            # charon_install_routes: false
            # charon_cisco_unity: false
            # retransmit_tries:
            # retransmit_timeout:
            # retransmit_base:
            # retransmit_jitter:
            # retransmit_limit:
            # syslog_log_name: true
            # syslog_log_level: false
            # syslog_app: 1
            # syslog_asn: 1
            # syslog_cfg: 1
            # syslog_chd: 1
            # syslog_dmn: 1
            # syslog_enc: 1
            # syslog_esp: 1
            # syslog_ike: 1
            # syslog_imc: 1
            # syslog_imv: 1
            # syslog_job: 1
            # syslog_knl: 1
            # syslog_lib: 1
            # syslog_mgr: 1
            # syslog_net: 1
            # syslog_pts: 1
            # syslog_tls: 1
            # syslog_tnc: 1
            # attr_subnet: []
            # attr_dns: []
            # attr_wins: []
            # unity_split_include: []
            # unity_dns_search:
            # unity_dns_split:
            # unity_login_banner:
            # unity_save_password: false

        - name: Setup Syslog
          oxlorg.opnsense.ipsec_general:
            syslog_log_name: true
            syslog_log_level: true
            syslog_chd: 2
            syslog_ike: 2
            syslog_mgr: 2
