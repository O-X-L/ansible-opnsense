.. _modules_postfix:

.. include:: ../_include/head.rst

=======
Postfix
=======

**STATE**: stable

**TESTS**: `postfix_general <https://github.com/ansibleguy/collection_opnsense/blob/latest/tests/postfix_general.yml>`_ |
`postfix_domain <https://github.com/ansibleguy/collection_opnsense/blob/latest/tests/postfix_domain.yml>`_ |
`postfix_recipient <https://github.com/ansibleguy/collection_opnsense/blob/latest/tests/postfix_recipient.yml>`_ |
`postfix_recipientbcc <https://github.com/ansibleguy/collection_opnsense/blob/latest/tests/postfix_recipientbcc.yml>`_ |
`postfix_sender <https://github.com/ansibleguy/collection_opnsense/blob/latest/tests/postfix_sender.yml>`_ |
`postfix_senderbcc <https://github.com/ansibleguy/collection_opnsense/blob/latest/tests/postfix_senderbcc.yml>`_ |
`postfix_sendercanonical <https://github.com/ansibleguy/collection_opnsense/blob/latest/tests/postfix_sendercanonical.yml>`_ |
`postfix_headercheck <https://github.com/ansibleguy/collection_opnsense/blob/latest/tests/postfix_headercheck.yml>`_ |
`postfix_address <https://github.com/ansibleguy/collection_opnsense/blob/latest/tests/postfix_address.yml>`_

**API Docs**: `Plugins - Postfix <https://docs.opnsense.org/development/api/plugins/postfix.html>`_

**Service Docs**: `How To: Setting Up A Mail Gateway <https://docs.opnsense.org/manual/how-tos/mailgateway.html>`_


Contribution
************

Thanks to `@jiuka <https://github.com/jiuka>`_ for developing these modules!

----

Prerequisites
*************

You need to install the postfix plugin:

```
os-postfix
```

You can also install it using the :ref:`ansibleguy.opnsense.package <modules_package>` module.

----

Definition
**********

.. include:: ../_include/param_basic.rst

ansibleguy.opnsense.postfix_general
===================================

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "enable","boolean","false","false","\-","Enable Postfix daemon."
    "myhostname","string","false","\-","\-","The internet hostname of this mail system. The default is to use the fully-qualified domain name (FQDN). See `postconf(5) myhostname <https://www.postfix.org/postconf.5.html#myhostname>`_"
    "mydomain","string","false","\-","\-","The internet domain name of this mail system. The default is to use `myhostname` minus the first component. See `postconf(5) mydomain <https://www.postfix.org/postconf.5.html#mydomain>`_"
    "myorigin","string","false","\-","\-","The domain name that locally-posted mail appears to come from. Default to `myhostname`. See `postconf(5) myorigin <https://www.postfix.org/postconf.5.html#myorigin>`_"
    "inet_interfaces","list","false","['all']","\-","Specifies a comma-separated list of IP addresses to listen to. See `postconf(5) inet_interfaces <https://www.postfix.org/postconf.5.html#inet_interfaces>`_"
    "inet_port","int","false","25","\-","Port to listen on."
    "ip_version","string","false","all","\-","The Internet protocols Postfix will attempt to use when making or accepting connections. One of: all, ipv4 or ipv6. See `postconf(5) inet_protocols <https://www.postfix.org/postconf.5.html#inet_protocols>`_"
    "bind_address","string","false","\-","\-","IPv4 address the server should bind to for outgoing connections. See `postconf(5) smtp_bind_address <https://www.postfix.org/postconf.5.html#smtp_bind_address>`_"
    "bind_address6","string","false","\-","\-","IPv6 address the server should bind to for outgoing connections. See `postconf(5) smtp_bind_address6 <https://www.postfix.org/postconf.5.html#smtp_bind_address6>`_"
    "mynetworks","list","false","['127.0.0.0/8', '[::ffff:127.0.0.0]/104', '[::1]/128']","\-","List of 'trusted' remote SMTP clients. See `postconf(5) mynetworks <https://www.postfix.org/postconf.5.html#mynetworks>`_"
    "banner","string","false","\-","\-","The text that follows the 220 status code in the SMTP greeting banner. See `postconf(5) smtpd_banner <https://www.postfix.org/postconf.5.html#smtpd_banner>`_"
    "message_size_limit","integer","false","51200000","\-","The max size for messages to accept, default is 51200000 Bytes which is 50MB. See `postconf(5) message_size_limit <https://www.postfix.org/postconf.5.html#message_size_limit>`_"
    "masquerade_domains","list","false","[]","\-","List of domains whose subdomain structure will be stripped off in email addresses. See `postconf(5) masquerade_domains <https://www.postfix.org/postconf.5.html#masquerade_domains>`_"
    "tls_server_compatibility","string","false","intermediate","\-","TLS version/cipher compatibility of the SMTP service. One of: modern, intermediate or old."
    "tls_client_compatibility","string","false","intermediate","\-","TLS version/cipher compatibility of the SMTP client. One of: modern, intermediate or old."
    "tlswrappermode","bool","false","false","\-","Request that the Postfix SMTP client connects using the SUBMISSIONS/SMTPS protocol instead of using the STARTTLS command.  See `postconf(5) smtp_tls_wrappermode <https://www.postfix.org/postconf.5.html#smtp_tls_wrappermode>`_"
    "certificate","string","false","\-","\-","Choose the certificate to use when other servers want to do TLS with you."
    "ca","string","false","\-","\-","Choose the Certificate Authority which signed your certificate."
    "smtpclient_security","string","false","may","\-","'none' will disable TLS for sending mail. 'may' will use TLS when offered. 'encrypt' will enforce TLS on all connections. 'dane' will enforce TLS if a TLSA-Record is published."
    "relayhost","string","false","\-","smarthost","The next-hop destination(s) for non-local mail. See `postconf(5) relayhost <https://www.postfix.org/postconf.5.html#relayhost>`_"
    "smtpauth_enabled","boolean","false","false","\-","Enable authentication against your relayhost."
    "smtpauth_user","string","false","\-","\-","The username to use for SMTP authentication against your relayhost."
    "smtpauth_password","string","false","\-","\.","The password to use for SMTP authentication against your relayhost."
    "enforce_recipient_check","boolean","false","false","\-","Activates recipient restrictions managed by ansibleguy.opnsense.postfix_recipient."
    "extensive_helo_restrictions","boolean","false","false","\-","Activate hello restrictions."
    "extensive_sender_restrictions","boolean","false","false","\-","Activate sender restrictions."
    "reject_unknown_client_hostname","boolean","false","false","\-","Add `reject_unknown_client_hostname <https://www.postfix.org/postconf.5.html#reject_unknown_client_hostname>`_ to `smtpd_recipient_restrictions <https://www.postfix.org/postconf.5.html#smtpd_recipient_restrictions>`_."
    "reject_non_fqdn_helo_hostname","boolean","false","false","\-","Add `reject_non_fqdn_helo_hostname <https://www.postfix.org/postconf.5.html#reject_non_fqdn_helo_hostname>`_ to `smtpd_recipient_restrictions <https://www.postfix.org/postconf.5.html#smtpd_recipient_restrictions>`_."
    "reject_invalid_helo_hostname","boolean","false","false","\-","Add `reject_invalid_helo_hostname <https://www.postfix.org/postconf.5.html#reject_invalid_helo_hostname>`_ to `smtpd_recipient_restrictions <https://www.postfix.org/postconf.5.html#smtpd_recipient_restrictions>`_."
    "reject_unknown_helo_hostname","boolean","false","false","\-","Add `reject_unknown_helo_hostname <https://www.postfix.org/postconf.5.html#reject_unknown_helo_hostname>`_ to `smtpd_recipient_restrictions <https://www.postfix.org/postconf.5.html#smtpd_recipient_restrictions>`_."
    "reject_unauth_pipelining","boolean","false","true","\-","Add `reject_unauth_pipelining <https://www.postfix.org/postconf.5.html#reject_unauth_pipelining>`_ to `smtpd_recipient_restrictions <https://www.postfix.org/postconf.5.html#smtpd_recipient_restrictions>`_."
    "reject_unknown_sender_domain","boolean","false","true","\-","Reject mails from domains which do not exist. See `postconf(5) reject_unknown_sender_domain <https://www.postfix.org/postconf.5.html#reject_unknown_sender_domain>`_"
    "reject_unknown_recipient_domain","boolean","false","true","\-","Reject mails to domains which do not exist. See `postconf(5) reject_unknown_recipient_domain <https://www.postfix.org/postconf.5.html#reject_unknown_recipient_domain>`_"
    "reject_non_fqdn_sender","bool","false","true","\-","Reject senders without a domain or only a hostname. See `postconf(5) reject_non_fqdn_sender <https://www.postfix.org/postconf.5.html#reject_non_fqdn_sender>`_"
    "reject_non_fqdn_recipient","bool","false","true","\-","Rejects recipients without a domain or only a hostname. See `postconf(5) reject_non_fqdn_recipient <https://www.postfix.org/postconf.5.html#reject_non_fqdn_recipient>`_"
    "permit_sasl_authenticated","bool","false","true","\-","Allow SASL authenticated senders to relay. Will also enable smtpd_sasl_auth."
    "permit_tls_clientcerts","boolean","false","true","\-","Allow mTLS authenticated senders to relay."
    "permit_mynetworks","boolean","false","true","\-","Allow client from `mynetworks` to relay."
    "reject_unauth_destination","boolean","false","true","\-","Add `reject_unauth_destination <https://www.postfix.org/postconf.5.html#reject_unauth_destination>`_ to `smtpd_recipient_restrictions <https://www.postfix.org/postconf.5.html#smtpd_recipient_restrictions>`_."
    "reject_unverified_recipient","bool","false","false","\-","Use Recipient Address Verification. Please keep in mind that this could put significant load onto the next server."
    "delay_warning_time","int","false","0","\-","Time in hours until we send a notification to the sender if mail is delayed. 0 or empty to disable."
    "reload","boolean","false","true","\-", .. include:: ../_include/param_reload.rst


ansibleguy.opnsense.postfix_domain
==================================

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "enable","boolean","false","false","\-","Enable or disable domain routing for this entry."
    "domainname","string","true","\-","name","Set the domain name to relay for."
    "destination","string","false","\-","\-","Set the IP or FQDN to where to send the mails to. Empty means MX will be used. You can also add custom ports via :225 or disable MX lookup via squared brackets."
    "reload","boolean","false","true","\-", .. include:: ../_include/param_reload.rst


ansibleguy.opnsense.postfix_recipient
=====================================

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "enable","boolean","false","false","\-","Enable or disable the recipient rule in this entry."
    "address","string","true","\-","\-","Recipient address to match."
    "action","string","false","\-","\-","Action for this address. One of: OK or REJECT."
    "reload","boolean","false","true","\-", .. include:: ../_include/param_reload.rst


ansibleguy.opnsense.postfix_recipientbcc
========================================

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "enable","boolean","false","false","\-","Enable or disable the BCC recipient rewriting setting."
    "address","string","true","\-","from","Pattern to match like user@example.com"
    "to","list","false","\-","\-","Recipient address to send the mail as BCC."
    "reload","boolean","false","true","\-", .. include:: ../_include/param_reload.rst


ansibleguy.opnsense.postfix_sender
==================================

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "enable","boolean","false","false","\-","Enable or disable the sender address to match for."
    "address","string","true","\-","\-","Sender address to match."
    "action","string","false","\-","\-","Action for this address. One of: OK or REJECT."
    "reload","boolean","false","true","\-", .. include:: ../_include/param_reload.rst


ansibleguy.opnsense.postfix_senderbcc
=====================================

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "enable","boolean","false","false","\-","Enable or disable the BCC sender rewriting setting."
    "address","string","true","\-","from","Pattern to match like user@example.com"
    "to","list","false","\-","\-","Recipient address to send the mail as BCC."
    "reload","boolean","false","true","\-", .. include:: ../_include/param_reload.rst


ansibleguy.opnsense.postfix_sendercanonical
===========================================

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "enable","boolean","false","false","\-","Enable or disable the sender canonical rewriting setting."
    "address","string","true","\-","from","Pattern to match line user@example.com or @example.com"
    "to","list","false","\-","\-","How to rewrite the Rewrite From pattern."
    "reload","boolean","false","true","\-", .. include:: ../_include/param_reload.rst


ansibleguy.opnsense.postfix_headercheck
=======================================

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "enable","boolean","false","false","\-","Enable or disable the header check."
    "expression","string","true","\-","from","Regexp (POSIX regular expression) and an action to process like ``/^\s*User-Agent/ IGNORE``. See the `Postfix manual about header_checks(5) <https://www.postfix.org/header_checks.5.html>`_"
    "filter","string","true","\-","\-","When the header_check should be processed. One of: WHILE_DELIVERING or WHILE_RECEIVING"
    "reload","boolean","false","true","\-", .. include:: ../_include/param_reload.rst


ansibleguy.opnsense.postfix_address
===================================

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "enable","boolean","false","false","\-","Enable or disable the address entry."
    "address","string","true","\-","from","Pattern to match line user@example.com or @example.com"
    "to","list","false","\-","\-","How to rewrite the Rewrite From pattern."
    "reload","boolean","false","true","\-", .. include:: ../_include/param_reload.rst

----

Usage
*****

ansibleguy.opnsense.postfix_general
===================================

Use ``ansibleguy.opnsense.postfix_general`` to setup the postfix daemon. 

ansibleguy.opnsense.postfix_domain
==================================

Manage accepted domains and the target to forward mails to using the
`relay_domains <https://www.postfix.org/postconf.5.html#relay_domains>`_ and
`transport_maps <https://www.postfix.org/postconf.5.html#transport_maps>`_.

ansibleguy.opnsense.postfix_recipient / postfix_sender
======================================================

Manage addresses on the
`smtpd_recipient_restrictions <https://www.postfix.org/postconf.5.html#smtpd_recipient_restrictions>`_ and
`check_sender_access <https://www.postfix.org/postconf.5.html#check_sender_access>`_ maps respectively.

ansibleguy.opnsense.postfix_recipientbcc / postfix_senderbcc
============================================================

Manage entries for the
`recipient_bcc_maps <https://www.postfix.org/postconf.5.html#recipient_bcc_maps>`_ and
`sender_bcc_maps <https://www.postfix.org/postconf.5.html#sender_bcc_maps>`_ maps respectively.


ansibleguy.opnsense.postfix_canonical
=====================================

Manage entries for the
`sender_canonical_maps <https://www.postfix.org/postconf.5.html#sender_canonical_maps>`_ map.


ansibleguy.opnsense.postfix_headercheck
=======================================

Manage entries for the
`header_checks <https://www.postfix.org/postconf.5.html#header_checks>`_ (type: WHILE_RECEIVING) and 
`smtp_header_checks <https://www.postfix.org/postconf.5.html#smtp_header_checks>`_ (type: WHILE_DELIVERING) maps.


ansibleguy.opnsense.postfix_address
===================================

Manage entries for the
`virtual_alias_maps <https://www.postfix.org/postconf.5.html#virtual_alias_maps>`_ map. The table format and lookups
are documented in `virtual(5) <https://www.postfix.org/access.5.html>`_ .

----

Examples
********

.. code-block:: yaml

    - hosts: localhost
      gather_facts: false
      module_defaults:
        group/ansibleguy.opnsense.all:
          firewall: 'opnsense.template.opnsense.oxl.app'
          api_credential_file: '/home/guy/.secret/opn.key'

      tasks:
        - name: Setup Postfix
          ansibleguy.opnsense.postfix_general:
            enable: true
            # myhostname:
            # mydomain:
            # myorigin:
            # inet_interfaces: ['all']
            # inet_port: 25
            # ip_version: all
            # bind_address:
            # bind_address6
            # mynetworks: ['127.0.0.0/8', '[::ffff:127.0.0.0]/104', '[::1]/128']
            # banner:
            # message_size_limit: 51200000
            # masquerade_domains:
            # tls_server_compatibility: intermediate
            # tls_client_compatibility: intermediate
            # tlswrappermode: false
            # certificate:
            # ca:
            # smtpclient_security: may
            # relayhost:
            # smtpauth_enabled: false
            # smtpauth_user:
            # smtpauth_password:
            # enforce_recipient_check: false
            # extensive_helo_restrictions: false
            # extensive_sender_restrictions: false
            # reject_unknown_client_hostname: false
            # reject_non_fqdn_helo_hostname: false
            # reject_invalid_helo_hostname: false
            # reject_unknown_helo_hostname: false
            # reject_unauth_pipelining: true
            # reject_unknown_sender_domain: true
            # reject_unknown_recipient_domain: true
            # reject_non_fqdn_sender: true
            # reject_non_fqdn_recipient: true
            # permit_sasl_authenticated: true
            # permit_tls_clientcerts: true
            # permit_mynetworks: true
            # reject_unauth_destination: true
            # reject_unverified_recipient: false
            # delay_warning_time: 0
            # auto_renewal: true
            # challenge_port: 43580
            # tls_challenge_port: 43581
            # restart_timeout: 600
            # haproxy_integration: false
            # log_level: normal
            # show_intro: true
            # debug: false

        - name: Add Domain
          ansibleguy.opnsense.postfix_domain:
            domainname: opnsense.oxl.app
            # destination: mail.opnsense.oxl.app
            # enable: true

        - name: Block Recipient
          ansibleguy.opnsense.postfix_recipient:
            address: noreply@opnsense.oxl.app
            action: REJECT
            # enable: true

        - name: Auto BCC Recipient
          ansibleguy.opnsense.postfix_recipient:
            address: alice@opnsense.oxl.app
            to: bob@opnsense.oxl.app
            # enable: true

        - name: Block Sender
          ansibleguy.opnsense.postfix_recipient:
            address: internal-only@opnsense.oxl.app
            action: REJECT
            # enable: true

        - name: Auto BCC Sender
          ansibleguy.opnsense.postfix_recipient:
            address: alice@opnsense.oxl.app
            to: bob@opnsense.oxl.app
            # enable: true

        - name: Sender Canonical Rewriting
          ansibleguy.opnsense.postfix_sendercanonical:
            address: '@ansibleguy.com'
            to: '@opnsense.oxl.app'
            # enable: true

        - name: Strip User-Agent header
          ansibleguy.opnsense.header_check:
            expression: /^\s*User-Agent/ IGNORE
            filter: WHILE_DELIVERING
            # enable: true

        - name: Address Rewriting
          ansibleguy.opnsense.postfix_address:
            address: root@opnsense.oxl.app
            to: alice@opnsense.oxl.app
            # enable: true

        - name: Listing jobs
          ansibleguy.opnsense.list:
            target: 'postfix_address'
          register: existing_postfix_address

        - name: Printing
          ansible.builtin.debug:
            var: existing_postfix_address.data
