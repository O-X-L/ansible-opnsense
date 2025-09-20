.. _modules_dnsmasq:

.. include:: ../_include/head.rst

=======
Dnsmasq
=======

**STATE**: unstable

**TESTS**: `General <https://github.com/O-X-L/ansible_opnsense/blob/latest/tests/dnsmasq_general.yml>`_ |
`Option <https://github.com/O-X-L/ansible_opnsense/blob/latest/tests/dnsmasq_option.yml>`_ |
`Boot <https://github.com/O-X-L/ansible_opnsense/blob/latest/tests/dnsmasq_boot.yml>`_ |
`Tag <https://github.com/O-X-L/ansible_opnsense/blob/latest/tests/dnsmasq_tag.yml>`_

**API Docs**: `dnsmasq_general <https://docs.opnsense.org/development/api/core/dnsmasq.html>`_

**Service Docs**: `dnsmasq_general <https://docs.opnsense.org/manual/dnsmasq.html>`_

This module allows you to manage the general requirements for the dnsmasq service.

Contribution
************

Thanks to `@kalsto <https://github.com/kalsto>`_ for working on this module!

----

Info
****

For more detailed information on what kinds of things you can do with the dnsmasq module - see `the documentation <https://docs.opnsense.org/manual/dnsmasq.html>`_.


Definition
**********

.. include:: ../_include/param_basic.rst

ansibleguy.opnsense.dnsmasq_general
===================================

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "enabled","boolean","false","false","\-","En- or disable the dnsmasq service"
    "interfaces","list","false","[]","[]","Interfaces for dnsmasq to listen on"
    "regdhcp","boolean","false","false","\-","Specify hostname when requesting DHCP lease"
    "regdhcpstatic","boolean","false","false","\-","Register DHCP Static mappings"
    "domain_needed","boolean","false","false","\-","Forward A or AAAA queries"
    "dns_port","int","false","53","\-","Port used for DNS Queries"
    "dnssec","boolean","false","false","\-","Secure DNS"
    "no_hosts","boolean","false","false","\-","Do not read hostnames from /etc/hosts"
    "dhcpfirst","boolean","false","false","\-","DHCP Mappings resolved before manual list. Affects PTR records"
    "strict_order","boolean","false","false","\-","Query DNS Servers sequentially"
    "strictbind","boolean","false","false","\-","Force bindings to interfaces listening on"
    "no_private_reverse","boolean","false","false","\-","No forwarding PTR records"
    "log_queries","boolean","false","false","\-","Log DNS queries"
    "no_ident","boolean","false","false","\-","Do not respond to CHAOS or TXT bind queries"
    "regdhcpdomain","str","false","false","\-","Domain used for DHCP hostname registrations"
    "reload","boolean","false","true","\-", .. include:: ../_include/param_reload.rst

ansibleguy.opnsense.dnsmasq_option
==================================

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "description","string","true","\-","desc","The unique description used to match the configured entries to the existing ones"
    "type","string","false","set","\-","'Set' option to send it to a client in a DHCP offer or 'Match' option to dynamically tag clients that send it in the initial DHCP request."
    "option","int","false","\-","\-","DHCPv4 option to offer to the client."
    "option6","int","false","\-","\-","DHCPv6 option to offer to the client."
    "interface","string","false","\-","int","Interface this options is set for."
    "tag","list","false","[]","t","DHCP option is only sent when all the tags are matched."
    "set_tag","string","false","\-","\-","Tag to set for matching requests when using 'Match'."
    "value","string","false","\-","\-","Value (or values) to send to the client. When using 'Match', leave empty to match on the option only."
    "force","boolean","false","false","\-","Always send the option, also when the client does not ask for it in the parameter request list."
    "reload","boolean","false","true","\-", .. include:: ../_include/param_reload.rst

ansibleguy.opnsense.dnsmasq_boot
================================

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "description","string","true","\-","desc","The unique description used to match the configured entries to the existing ones"
    "interface","string","false","\-","int","Interface this boot options is set for."
    "tag","list","false","[]","t","DHCP boot option is only sent when all the tags are matched."
    "filename","string","true","\-","file, f","DHCP boot file path."
    "servername","string","false","\-","\-","DHCP boot server name."
    "address","string","false","\-","\-","DHCP boot server address."
    "reload","boolean","false","true","\-", .. include:: ../_include/param_reload.rst

ansibleguy.opnsense.dnsmasq_tag
===============================

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "tag","string","true","\-","t, name, n","An alphanumeric label which marks a network so that DHCP options may be specified on a per-network basis."
    "reload","boolean","false","true","\-", .. include:: ../_include/param_reload.rst

Usage
*****

Starting implementation of Dnsmasq API in Ansible modules

Work in progress - you should make sure that your interfaces are already created, and that unbound (current default) is disabled before enabling dnsmasq.

Examples
********

ansibleguy.opnsense.dnsmasq_general
===================================

.. code-block:: yaml

    - hosts: localhost
      gather_facts: false
      module_defaults:
        group/ansibleguy.opnsense.all:
          firewall: 'opnsense.template.ansibleguy.net'
          api_credential_file: '/home/guy/.secret/opn.key'

        ansibleguy.opnsense.list:
          target: 'dnsmasq'

        ansibleguy.opnsense.reload:
          target: 'dnsmasq'


      tasks:
        # add optional parameters commented-out
        # required ones normally
        # add their default values to get a brief overview of how the module works
        - name: Example
          ansibleguy.opnsense.dnsmasq_general:
            # enabled: true
            # interfaces: ['wan','opt1']
            # regdhcp: True
            # regdhcpstatic: 1
            # domain_needed: 1
            # dns_port: 54 # config-based.. not in memory.. probably needs a reboot of the service?
            # dnssec: True
            # no_hosts: true
            # dhcpfirst: true
            # strict_order: true
            # strictbind: true
            # no_private_reverse: true
            # log_queries: true
            # no_ident: false
            # regdhcpdomain: 'test.domain'

        - name: Configuring General settings for dnsmasq
          ansibleguy.opnsense.dnsmasq_general:
            enabled: true
            interfaces: ['wan','opt1']
            regdhcp: True
            regdhcpstatic: true
            domain_needed: true
            dnssec: True
            no_hosts: true
            dhcpfirst: true
            strict_order: true
            strictbind: true
            no_private_reverse: true
            log_queries: true
            no_ident: false
            regdhcpdomain: 'test.domain'

        - name: Listing dnsmasq settings
          ansibleguy.opnsense.list:
            target: 'dnsmasq_general'
          register: dnsmasq_general_settings

        - name: Printing settings
          ansible.builtin.debug:
            var: dnsmasq_general_settings

----

ansibleguy.opnsense.dnsmasq_option
==================================

.. code-block:: yaml

    - hosts: localhost
      gather_facts: false
      module_defaults:
        group/ansibleguy.opnsense.all:
          firewall: 'opnsense.template.ansibleguy.net'
          api_credential_file: '/home/guy/.secret/opn.key'

        ansibleguy.opnsense.list:
          target: 'dnsmasq_option'

      tasks:
        - name: Example Set
          ansibleguy.opnsense.dnsmasq_option:
            # type: 'set'
            option: 4 # time-server
            # option6:
            # interface:
            # tag:
            value: pool.ntp.org
            # force: false
            # state: 'absent'
            # debug: false

        - name: Example Match
          ansibleguy.opnsense.dnsmasq_option:
            type: 'match'
            option: 60 # vendor-class
            # option6:
            value: SIPPhone
            set_tag: voip
            # state: 'absent'
            # debug: false

        - name: Adding Match Vendor-Class SIPPhone
          ansibleguy.opnsense.dnsmasq_option:
            type: 'match'
            option: 60 # vendor-class
            value: SIPPhone
            set_tag: voip

        - name: Adding Set time-server for SIPPhone
          ansibleguy.opnsense.dnsmasq_option:
            option: 4 # time-server
            value: pool.ntp.org
            tag: voip

        - name: Listing Option
          ansibleguy.opnsense.list:
          #  target: 'dnsmasq_option'
          register: existing_option

        - name: Printing
          ansible.builtin.debug:
            var: existing_option.data

----

ansibleguy.opnsense.dnsmasq_boot
================================

.. code-block:: yaml

    - hosts: localhost
      gather_facts: false
      module_defaults:
        group/ansibleguy.opnsense.all:
          firewall: 'opnsense.template.ansibleguy.net'
          api_credential_file: '/home/guy/.secret/opn.key'

        ansibleguy.opnsense.list:
          target: 'dnsmasq_boot'

      tasks:
        - name: Example
          ansibleguy.opnsense.dnsmasq_boot:
            description: 'Boot PXELinux'
            # interface:
            # tag:
            filename: '/tftpboot/pxelinux.0'
            # servername:
            # address:
            # state: 'absent'
            # debug: false

        - name: Adding something
          ansibleguy.opnsense.dnsmasq_boot:
            description: 'Boot PXELinux'
            filename: '/tftpboot/pxelinux.0'

        - name: Changing something
          ansibleguy.opnsense.dnsmasq_boot:
            description: 'Boot PXELinux'
            filename: '/tftpboot/pxelinux.0'
            address: '192.168.1.1'

        - name: Listing Boot
          ansibleguy.opnsense.list:
          #  target: 'dnsmasq_boot'
          register: existing_boot

        - name: Printing
          ansible.builtin.debug:
            var: existing_boot.data

----

ansibleguy.opnsense.dnsmasq_tag
===============================

.. code-block:: yaml

    - hosts: localhost
      gather_facts: false
      module_defaults:
        group/ansibleguy.opnsense.all:
          firewall: 'opnsense.template.ansibleguy.net'
          api_credential_file: '/home/guy/.secret/opn.key'

        ansibleguy.opnsense.list:
          target: 'dnsmasq_tag'

      tasks:
        - name: Example
          ansibleguy.opnsense.dnsmasq_tag:
            tag: 'test1'
            # state: 'absent'
            # debug: false

        - name: Adding a tag
          ansibleguy.opnsense.dnsmasq_tag:
            tag: 'Tag1'

        - name: Listing tags
          ansibleguy.opnsense.list:
          #  target: 'dnsmasq_tag'
          register: existing_tags

        - name: Printing
          ansible.builtin.debug:
            var: existing_tags.data
