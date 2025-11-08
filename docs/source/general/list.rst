.. _modules_list:

.. include:: ../_include/head.rst

====
List
====

**STATE**: stable

**TESTS**: Used in multiple ones

Contribution
************

Thanks to `@Rath <https://github.com/superstes>`_ for developing this module!

----

Info
****

This module can list existing items/entries of a specified part of the OPNsense system.

In most cases the returned type of this module ist a list of dictionaries.

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "target","string","true","\-","tgt, t","What part of the running config should be queried/listed. One of: 'alias', 'rule', 'route', 'cron', 'syslog', 'package', 'unbound_general', 'unbound_acl', 'unbound_host', 'unbound_dot', 'unbound_forward', 'unbound_host_alias', 'ipsec_cert', 'shaper_pipe', 'shaper_queue', 'shaper_rule', 'monit_service', 'monit_test', 'monit_alert', 'wireguard_server', 'wireguard_peer', 'interface_lagg', 'interface_vlan', 'interface_vxlan', 'nat_source', 'nat_one_to_one', 'frr_bfd', 'frr_bgp_general', 'frr_bgp_neighbor', 'frr_bgp_prefix_list', 'frr_bgp_community_list', 'frr_bgp_as_path', 'frr_bgp_route_map', 'frr_ospf_general', 'frr_ospf_prefix_list', 'frr_ospf_interface', 'frr_ospf_route_map', 'frr_ospf_network', 'frr_ospf3_general', 'frr_ospf3_interface', 'frr_rip', 'bind_general', 'bind_blocklist', 'bind_acl', 'bind_domain', 'bind_record', 'interface_vip', 'webproxy_general', 'webproxy_cache', 'webproxy_parent', 'webproxy_traffic', 'webproxy_forward', 'webproxy_acl', 'webproxy_icap', 'webproxy_auth', 'webproxy_remote_acl', 'webproxy_pac_proxy', 'webproxy_pac_match', 'webproxy_pac_rule', 'unbound_dnsbl', 'interface_gre', 'postfix_general', 'postfix_domain', 'postfix_recipient', 'postfix_recipientbcc', 'postfix_sender', 'postfix_senderbcc', 'postfix_sendercanonical', 'postfix_headercheck', 'postfix_address', 'ipsec_manual_spd'"

.. include:: ../_include/param_basic.rst

----

Examples
********

.. code-block:: yaml

    - hosts: localhost
      gather_facts: no
      module_defaults:
        group/oxlorg.opnsense.all:
          firewall: 'opnsense.template.opnsense.oxl.app'
          api_credential_file: '/home/guy/.secret/opn.key'

      tasks:
        - name: Pulling aliases
          oxlorg.opnsense.list:
            target: 'alias'
          register: existing_aliases

        - name: Printing
          ansible.builtin.debug:
            var: existing_aliases.data

        - name: Pulling routes
          oxlorg.opnsense.list:
            target: 'route'
          register: existing_routes

        - name: Printing
          ansible.builtin.debug:
            var: existing_routes.data
