.. _modules_dnsmasq:

.. include:: ../_include/head.rst

=======
Dnsmasq
=======

**STATE**: unstable

**TESTS**: `General <https://github.com/O-X-L/ansible_opnsense/blob/latest/tests/dnsmasq_general.yml>`_ |
`Domain <https://github.com/O-X-L/ansible_opnsense/blob/latest/tests/dnsmasq_domain.yml>`_ |
`Host <https://github.com/O-X-L/ansible_opnsense/blob/latest/tests/dnsmasq_host.yml>`_ |
`Range <https://github.com/O-X-L/ansible_opnsense/blob/latest/tests/dnsmasq_range.yml>`_ |
`Option <https://github.com/O-X-L/ansible_opnsense/blob/latest/tests/dnsmasq_option.yml>`_ |
`Boot <https://github.com/O-X-L/ansible_opnsense/blob/latest/tests/dnsmasq_boot.yml>`_ |
`Tag <https://github.com/O-X-L/ansible_opnsense/blob/latest/tests/dnsmasq_tag.yml>`_

**API Docs**: `Core - Dnsmasq <https://docs.opnsense.org/development/api/core/dnsmasq.html>`_

**Service Docs**: `Dnsmasq DNS & DHCP <https://docs.opnsense.org/manual/dnsmasq.html>`_

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
    "interfaces","list","false","[]","ints","Interfaces for dnsmasq to listen on"
    "strictbind","boolean","false","false","\-","Force bindings to interfaces listening on"
    "port","int","false","53","dns_port","Port used for DNS Queries"
    "dnssec","boolean","false","false","\-","Secure DNS"
    "no_hosts","boolean","false","false","\-","Do not read hostnames from /etc/hosts"
    "log_queries","boolean","false","false","\-","Log DNS queries"
    "dns_forward_max","integer","false","\-","\-","Maximum number of concurrent DNS queries"
    "cache_size","integer","false","\-","\-","Size of the cache. Setting the cache size to zero disables caching"
    "local_ttl","integer","false","\-","\-","Time-to-live (in seconds) to be given for local DNS entries, i.e. /etc/hosts or DHCP leases"
    "no_ident","boolean","false","false","\-","Do not respond to CHAOS or TXT bind queries"
    "strict_order","boolean","false","false","\-","Query DNS Servers sequentially"
    "domain_needed","boolean","false","false","\-","Forward A or AAAA queries"
    "resolv_system","boolean","false","false","\-","Forward DNS queries to system nameservers"
    "no_private_reverse","boolean","false","false","\-","No forwarding PTR records"
    "add_mac","string","false","\-","\-","Add the MAC address of the requestor to DNS queries which are forwarded upstream. One of: '', 'standard', 'base64', 
 text'"
    "add_subnet","boolean","false","false","\-","Add the real client addresses to DNS queries which are forwarded upstream"
    "strip_subnet","boolean","false","false","\-","Strip the subnet received by a downstream DNS server"
    "regdhcp","boolean","false","false","\-","Specify hostname when requesting DHCP lease"
    "regdhcpdomain","str","false","false","\-","Domain used for DHCP hostname registrations"
    "regdhcpstatic","boolean","false","false","\-","Register DHCP Static mappings"
    "dhcpfirst","boolean","false","false","\-","DHCP Mappings resolved before manual list. Affects PTR records"
    "reload","boolean","false","true","\-", .. include:: ../_include/param_reload.rst

ansibleguy.opnsense.dnsmasq_domain
==================================

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "domain","string","true","\-","name","Domain to override."
    "sequence","int","false","1","seq","Sort with a sequence number."
    "ip","string","false","\-","\-","IP address of the authoritative DNS server for this domain, leave empty to prevent lookups for this domain."
    "port","int","false","\-","\-","Specify a non standard port number. Leave blank for default."
    "src_ip","string","false","\-","\-","Source IP address for queries to the DNS server for the override domain."
    "ipset","string","false","\-","alias","Choose an 'external' type alias from 'Firewall - Aliases'. Whenever a client successfully resolves the domain, the resolved IP addresses will be automatically added to the chosen alias."
    "description","string","false","\-","desc","A description for your reference (not parsed)."
    "reload","boolean","false","true","\-", .. include:: ../_include/param_reload.rst

ansibleguy.opnsense.dnsmasq_host
================================

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "description","string","true","\-","desc","The unique description used to match the configured entries to the existing ones"
    "host","string","false","\-","h","Name of the host, without the domain part. Use '*' to create a wildcard entry."
    "domain","string",false","\-","d"," Domain of the host,"
    "local","boolean","false","false","\-","Set the domain as local. This will configure this DNS server as authoritative."
    "ip","list","false","\-","\-","IP addresses of the host. Can be multiple IPv4 and IPv6 addresses for dual stack configurations."
    "alias","list","false","\-","\-","Adds additional static A, AAAA and PTR records for the given alternative names (FQDN). Please note that these records are only created if IP addresses are configured in this host entry."
    "cname","list","false","\-","\-","Adds additional static A, AAAA and PTR records for the given alternative names (FQDN)."
    "client_id","string","false","\-","\-","Match the identifier of the client. Setting the special character '*'' will ignore the client identifier for DHCPv4 leases if a client offers both as choice."
    "hardware_addr","list","false","\-","mac","Match the hardware address of the client. Can be multiple addresses, e.g., if the client has multiple network cards."
    "lease_time","int","false","\-","\-"," Defines how long the addresses (leases) given out by the server are valid (in seconds). Set 0 for infinite."
    "set_tag","string","false","\-","\-","Tag to set for matching requests."
    "ignore","boolean","false","false","\-","Ignore any DHCP packets of this host. Useful if it should get served by a different DHCP server."
    "comments","string","false","\-","\-","A comment for your reference (not parsed)."
    "reload","boolean","false","true","\-", .. include:: ../_include/param_reload.rst

ansibleguy.opnsense.dnsmasq_range
=================================

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "description","string","true","\-","desc","The unique description used to match the configured entries to the existing ones"
    "interface","string","false","\-","int","Interface this range is for."
    "set_tag","string","false","\-","\-","Tag to set for matching requests."
    "start_addr","string","true","\-","\-","Start of the range, e.g. 192.168.1.100 for DHCPv4, 2000::1 for DHCPv6 or when a constructor is used a suffix like ::1"
    "end_addr","string","true","\-","\-","End of the range."
    "subnet_mask","stzring","false","\-","\-","Leave empty to auto-calculate the subnet mask from the interface or the network class of the start address."
    "constructor","string","false","\-","\-","Interface to use to calculate a DHCPv6 or RA range. Start address can then be specified as a suffix (e.g. ::, ::1 or ::400)."
    "mode","list","false","[]","\-","Mode flags to set for this range, 'static' means no addresses will be automatically assigned."
    "prefix_len","int","false","64","\-","Prefix length offered to the DHCPv6 client. Custom values in this field will be ignored if Router Advertisements are enabled."
    "lease_time","int","false","86400","\-","Defines how long the addresses (leases) given out by the server are valid (in seconds). Set 0 for infinite."
    "domain_type","string","false","range","\-","Choose if the domain will only match clients in this range, or all clients in any subnets on the selected interface. If you create both IPv4 and IPv6 ranges, setting this to 'interface' on both ranges is recommended. On of: 'range', 'interface'"
    "domain","string","false","\-","\-","Offer this domain to DHCP clients."
    "sync","boolean","false","true","\-","Sync this range by ha sync."
    "ra_mode","string","false","\-","\-","Control how IPv6 clients receive their addresses. Enabling Router Advertisements in general settings will enable it for all configured DHCPv6 ranges with the managed address bits set, and the use SLAAC bit reset. To change this default, select a combination of the possible options here. 'slaac', 'ra-stateless' and 'ra-names' can be freely combined, all other options shall remain single selections. Options: 'ra-only', 'slaac', 'ra-names', 'ra-stateless', 'ra-advrouter', 'off-link'"
    "ra_priority","string","false","''","\-","Priority of the RA announcements. One of: '', 'high', 'low'"
    "ra_mtu","int","false","\-","\-","Optional MTU to send to clients via Router Advertisements."
    "ra_interval","int","false","60","\-","Time in seconds between Router Advertisements."
    "ra_router_lifetime","int","false","1200","\-","The lifetime of the route may be changed or set to zero, which allows a router to advertise prefixes but not a route via itself."
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
        - name: Example
          ansibleguy.opnsense.dnsmasq_general:
            # enabled: true
            # interfaces: ['wan','opt1']
            # strictbind: true
            # port: 53 # config-based.. not in memory.. probably needs a reboot of the service?
            # dnssec: true
            # no_hosts: true
            # log_queries: true
            # cache_size:
            # local_ttl:
            # no_ident: false
            # strict_order: true
            # domain_needed: true
            # resolv_system: false
            # no_private_reverse: true
            # add_mac: ''
            # add_subnet: false
            # strip_subnet: false
            # regdhcp: true
            # regdhcpdomain: 'test.domain'
            # regdhcpstatic: true
            # dhcpfirst: true

        - name: Configuring General settings for dnsmasq
          ansibleguy.opnsense.dnsmasq_general:
            enabled: true
            interfaces: ['wan','opt1']
            strictbind: true
            dnssec: true
            no_hosts: true
            log_queries: true
            no_ident: false
            strict_order: true
            domain_needed: true
            no_private_reverse: true
            regdhcp: True
            regdhcpdomain: 'test.domain'
            regdhcpstatic: true
            dhcpfirst: true

        - name: Listing dnsmasq settings
          ansibleguy.opnsense.list:
            target: 'dnsmasq_general'
          register: dnsmasq_general_settings

        - name: Printing settings
          ansible.builtin.debug:
            var: dnsmasq_general_settings

----

ansibleguy.opnsense.dnsmasq_domain
==================================

.. code-block:: yaml

    - hosts: localhost
      gather_facts: false
      module_defaults:
        group/ansibleguy.opnsense.all:
          firewall: 'opnsense.template.ansibleguy.net'
          api_credential_file: '/home/guy/.secret/opn.key'

        ansibleguy.opnsense.list:
          target: 'dnsmasq_domain'

      tasks:
        - name: Example
          ansibleguy.opnsense.dnsmasq_domain:
            domain: 'template.ansibleguy'
            # sequence: 1
            # ip:
            # port:
            # src_ip:
            # ipset:
            # description:
            # state: 'absent'
            # debug: false

        - name: Adding Domain
          ansibleguy.opnsense.dnsmasq_domain:
            domain: 'template.ansibleguy'
            ip: 192.168.0.1

        - name: Change Domain
          ansibleguy.opnsense.dnsmasq_domain:
            domain: 'template.ansibleguy'
            ip: 192.168.0.1
            port: 5353

        - name: Listing Domain
          ansibleguy.opnsense.list:
          #  target: 'dnsmasq_domain'
          register: existing_domain

        - name: Printing
          ansible.builtin.debug:
            var: existing_domain.data

----

ansibleguy.opnsense.dnsmasq_host
================================

.. code-block:: yaml

    - hosts: localhost
      gather_facts: false
      module_defaults:
        group/ansibleguy.opnsense.all:
          firewall: 'opnsense.template.ansibleguy.net'
          api_credential_file: '/home/guy/.secret/opn.key'

        ansibleguy.opnsense.list:
          target: 'dnsmasq_host'

      tasks:
        - name: Example
          ansibleguy.opnsense.dnsmasq_host:
            description: Host Description
            host: 'example'
            domain: 'template.ansibleguy'
            # local: false
            ip: 192.168.0.1
            # alias:
            # cname:
            # client_id:
            # hardware_addr:
            # lease_time:
            # set_tag:
            # ignore: false
            # comments:
            # state: 'absent'
            # debug: false

        - name: Adding DNS entry
          ansibleguy.opnsense.dnsmasq_host:
            description: DNS example.template.ansibleguy
            host: 'example'
            domain: 'template.ansibleguy'
            ip: 192.168.0.1

        - name: Adding DHCP entry
          ansibleguy.opnsense.dnsmasq_host:
            description: DHCP example.template.ansibleguy
            ip: '192.168.0.2'
            hardware_addr: 'aa:aa:aa:bb:bb:bb'

        - name: Listing Host
          ansibleguy.opnsense.list:
          #  target: 'dnsmasq_host'
          register: existing_host

        - name: Printing
          ansible.builtin.debug:
            var: existing_host.data

----

ansibleguy.opnsense.dnsmasq_range
=================================

.. code-block:: yaml

    - hosts: localhost
      gather_facts: false
      module_defaults:
        group/ansibleguy.opnsense.all:
          firewall: 'opnsense.template.ansibleguy.net'
          api_credential_file: '/home/guy/.secret/opn.key'

        ansibleguy.opnsense.list:
          target: 'dnsmasq_range'

      tasks:
        - name: Example v4
          ansibleguy.opnsense.dnsmasq_range:
            description: IPv4 Range
            # interface:
            # set_tag:
            start_addr: 192.168.1.100
            end_addr: 192.168.1.200
            # mode: static
            # lease_time: 86400
            # domain_type: range
            # damin:
            # sync: true
            # state: 'absent'
            # debug: false

        - name: Example v6
          ansibleguy.opnsense.dnsmasq_range:
            description: IPv6 Range
            # interface:
            # set_tag:
            start_addr: 2000::100
            end_addr: 2000::100
            # contructor:
            # prefix_len: 64
            # ra_mode:
            # ra_priority:
            # ra_mtu:
            # ra_interval: 60
            # ra_router_lifetime: 1200
            # mode: static
            # lease_time: 86400
            # domain_type: range
            # damin:
            # sync: true
            # state: 'absent'
            # debug: false

        - name: Adding range
          ansibleguy.opnsense.dnsmasq_range:
            description: IPv4 Range
            start_addr: 192.168.1.100
            end_addr: 192.168.1.200

        - name: Changing range
          ansibleguy.opnsense.dnsmasq_range:
            description: IPv4 Range
            start_addr: 192.168.1.100
            end_addr: 192.168.1.150
            domain: opn.local

        - name: Listing Range
          ansibleguy.opnsense.list:
          #  target: 'dnsmasq_range'
          register: existing_range

        - name: Printing
          ansible.builtin.debug:
            var: existing_range.data

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
