.. _modules_interface:

.. include:: ../_include/head.rst

=========
Interface
=========


**STATE**: stable

**TESTS**: `vlan <https://github.com/O-X-L/ansible_opnsense/blob/latest/tests/interface_vlan.yml>`_ |
`vxlan <https://github.com/O-X-L/ansible_opnsense/blob/latest/tests/interface_vxlan.yml>`_ |
`vip <https://github.com/O-X-L/ansible_opnsense/blob/latest/tests/interface_vip.yml>`_ |
`lagg <https://github.com/O-X-L/ansible_opnsense/blob/latest/tests/interface_lagg.yml>`_ |
`loopback <https://github.com/O-X-L/ansible_opnsense/blob/latest/tests/interface_loopback.yml>`_ |
`gre <https://github.com/O-X-L/ansible_opnsense/blob/latest/tests/interface_gre.yml>`_

**API Docs**: `Core - Interfaces <https://docs.opnsense.org/development/api/core/interfaces.html>`_

**Service Docs**: `VLAN Docs <https://docs.opnsense.org/manual/other-interfaces.html?highlight=vlan#vlan>`_ |
`VxLAN Docs <https://docs.opnsense.org/manual/other-interfaces.html?highlight=vlan#vxlan>`_ |
`VIP Docs <https://docs.opnsense.org/manual/firewall_vip.html>`_ |
`LAGG Docs <https://docs.opnsense.org/manual/other-interfaces.html?highlight=lagg#lagg>`_ |
`GRE Docs <https://docs.opnsense.org/manual/other-interfaces.html?highlight=gre#gre>`_


Info
****

ansibleguy.opnsense.interface_vlan
==================================

This module manages VLAN configuration that can be found in the WEB-UI menu: 'Interfaces - Other Types - VLAN'

ansibleguy.opnsense.interface_vxlan
===================================

This module manages VXLAN configuration that can be found in the WEB-UI menu: 'Interfaces - Other Types - VXLAN'

ansibleguy.opnsense.interface_vip
===================================

This module manages VIP configuration that can be found in the WEB-UI menu: 'Interfaces - Virtual IPs - Settings'

ansibleguy.opnsense.interface_lagg
===================================

This module manages LAGG configuration that can be found in the WEB-UI menu: 'Interfaces - Other Types - LAGG'

ansibleguy.opnsense.interface_loopback
======================================

This module manages Loopback configuration that can be found in the WEB-UI menu: 'Interfaces - Other Types - Loopback'

ansibleguy.opnsense.interface_gre
===================================

This module manages GRE Tunnel configuration that can be found in the WEB-UI menu: 'Interfaces - Other Types - GRE'


Contribution
************

Thanks to `@jiuka <https://github.com/jiuka>`_ for developing the :code:`interface_loopback` and :code:`interface_gre` modules!

Thanks to `@Rath <https://github.com/superstes>`_ for developing the other modules!

----

Definition
**********

.. include:: ../_include/param_basic.rst

ansibleguy.opnsense.interface_vlan
==================================

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "description","string","true","\-","desc, name","The unique description used to match the configured entries to the existing ones"
    "interface","string","false for state changes, else true","\-","parent, port, int, if","The parent interface to add the vlan to. Existing VLAN capable interface - you must provide the network port as shown in 'Interfaces - Assignments - Network port'"
    "vlan","integer","false for state changes, else true","\-","tag, id","802.1Q VLAN tag (between 1 and 4094)"
    "priority","integer","false","0","prio","802.1Q VLAN PCP (between 0 and 7)"
    "reload","boolean","false","true","\-", .. include:: ../_include/param_reload.rst


ansibleguy.opnsense.interface_vxlan
===================================

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "id","integer","true","\-","vxlanid, vni","The unique ID of the VxLAN"
    "interface","string","false for state changes, else true","\-","vxlandev, device, int","Optionally set an interface to bind the VxLAN to. You must provide the network port as shown in 'Interface - Assignments - Interface ID (in brackets)'"
    "local","string","false for state changes, else true","\-","source_address, source_ip, vxlanlocal, source, src","Source IP for the VxLAN tunnel. The source address used in the encapsulating IPv4/IPv6 header. The address should already be assigned to an existing interface. When the interface is configured in unicast mode, the listening socket is bound to this address."
    "local_port","integer","false","\-","source_port, vxlanlocalport, srcport","Define the port to be used"
    "remote","string","false","\-","remote_address, remote_ip, destination, vxlanremote, dest","Remote IP for the VxLAN tunnel - if unicast is used. The interface can be configured in a unicast, or point-to-point, mode to create a tunnel between two hosts. This is the IP address of the remote end of the tunnel."
    "remote_port","integer","false","\-","destination_port, vxlanremoteport, destport","Define the port to be used"
    "group","string","false","\-","multicast_group, multicast_address, multicast_ip, vxlangroup","Remote IP for the VxLAN tunnel - if multicast is used. The interface can be configured in a multicast mode to create a virtual network of hosts. This is the IP multicast group address the interface will join."
    "reload","boolean","false","true","\-", .. include:: ../_include/param_reload.rst


ansibleguy.opnsense.interface_vip
=================================

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "match_fields","list","false","['address', 'interface']","\-","Fields that are used to match configured VIPs with the running config - if any of those fields are changed, the module will think it's a new entry. At least one of: 'address', 'interface', 'cidr', 'description'"
    "address", "string", "true", "\-", "addr, ip, network, net", "Provide an address and subnet to use. (e.g 192.168.0.1/24)"
    "interface", "string", "true", "\-", "port, int, if", "Existing interface - you must provide the network port as shown in 'Interfaces - Assignments - Network port'"
    "mode", "string", "false", "ipalias", "m", "One of: 'ipalias', 'carp', 'proxyarp', 'other'"
    "expand", "boolean", "false", "true", "\-", "\-"
    "bind", "boolean", "false", "true", "\-", "Assigning services to the virtual IP's interface will automatically include this address. Uncheck to prevent binding to this address instead"
    "gateway", "string", "false", "\-", "gw", "For some interface types a gateway is required to configure an IP Alias (ppp/pppoe/tun), leave this field empty for all other interface types"
    "password", "string", "false", "\-", "pwd", "VHID group password"
    "vhid", "integer", "false", "\-", "group, grp, id", "VHID group that the machines will share"
    "advertising_base", "integer", "false", "1", "adv_base, base", "The frequency that this machine will advertise. 0 usually means master. Otherwise the lowest combination of both values in the cluster determines the master"
    "advertising_skew", "integer", "false", "0", "adv_skew, skew", "\-"
    "description","string","false","\-","desc, name","Optional description"
    "reload","boolean","false","true","\-", .. include:: ../_include/param_reload.rst


ansibleguy.opnsense.interface_lagg
==================================

.. warning::

    This feature is only available in OPNSense version >= 23.7

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "match_fields","list","false","['members']","\-","Fields that are used to match configured LAGG with the running config - if any of those fields are changed, the module will think it's a new entry. At least one of: 'device', 'members', 'primary_member', 'proto', 'description'"
    "device", "string", "false", "\-", "laggif", "Optional 'device' of the entry. Needs to start with 'lagg'"
    "members", "list", "false", "\-", "port, int, if", "Existing LAGG capable interface - you must provide the network port as shown in 'Interfaces - Assignments - Network port'"
    "primary_member", "string", "false", "\-", "\-", "This interface will be added first in the lagg making it the primary one - you must provide the network port as shown in 'Interfaces - Assignments - Network port'"
    "proto", "string", "false", "lacp", "p", "The protocol to use. One of: 'none', 'lacp', 'failover', 'fec', 'loadbalance', 'roundrobin'"
    "lacp_fast_timeout", "boolean", "false", "false", "\-", "Enable lacp fast-timeout on the interface."
    "use_flowid", "string", "false", "\-", "\-", "Use the RSS hash from the network card if available, otherwise a hash is locally calculated. The default depends on the system tunable in net.link.lagg.default_use_flowid. One of: 'default', 'yes', 'no'"
    "lagghash", "list", "false", "['l2']", "\-", "Set the packet layers to hash for aggregation protocols which load balance. At least one of: 'l2', 'l3', 'l4'"
    "lacp_strict", "string", "false", "\-", "\-", "Enable lacp strict compliance on the interface. The default depends on the system tunable in net.link.lagg.lacp.default_strict_mode. One of: 'default', 'yes', 'no'"
    "mtu", "integer", "false", "false", "\-", "If you leave this field blank, the smallest mtu of this laggs children will be used."
    "description","string","true","\-","desc, name","The description used to match the configured entries to the existing ones"
    "reload","boolean","false","true","\-", .. include:: ../_include/param_reload.rst

ansibleguy.opnsense.interface_loopback
======================================

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "description","string","true","\-","desc, name","The unique description used to match the configured entries to the existing ones"
    "reload","boolean","false","true","\-", .. include:: ../_include/param_reload.rst

ansibleguy.opnsense.interface_gre
======================================

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "description","string","true","\-","desc, name","The unique description used to match the configured entries to the existing ones"
    "local","string","true","\-","l, local_addr","The local address or interface to use."
    "remote","string","true","\-","r, remote_addr","Peer address where encapsulated gre packets will be sent."
    "tunnel_local","string","true","\-","tl, tunnel_local_addr","Local gre tunnel endpoint."
    "tunnel_remote","string","true","\-","tr, tunnel_remote_addr","Remote gre tunnel endpoint."
    "tunnel_remote_net","integer","false","32","\-","Netmask `ipv4` or prefix `ipv6` to use for this tunnel "
    "reload","boolean","false","true","\-", .. include:: ../_include/param_reload.rst

----

Examples
********

ansibleguy.opnsense.interface_vlan
==================================

.. code-block:: yaml

    - hosts: localhost
      gather_facts: no
      module_defaults:
        group/ansibleguy.opnsense.all:
          firewall: 'opnsense.template.ansibleguy.net'
          api_credential_file: '/home/guy/.secret/opn.key'
    
        ansibleguy.opnsense.list:
          target: 'interface_vlan'
    
      tasks:
        - name: Example
          ansibleguy.opnsense.interface_vlan:
            description: 'example'
            interface: 'vtnet0'
            vlan: 100
            # priority: 0
            # debug: false
            # state: 'present'
            # reload: true
    
        - name: Adding VLAN
          ansibleguy.opnsense.interface_vlan:
            description: 'test1'
            interface: 'vtnet0'
            vlan: 100
    
        - name: Listing
          ansibleguy.opnsense.list:
          #  target: 'interface_vlan'
          register: existing_entries
    
        - name: Printing VLANs
          ansible.builtin.debug:
            var: existing_entries.data
    
        - name: Removing VLAN
          ansibleguy.opnsense.interface_vlan:
            description: 'test1'
            state: 'absent'

ansibleguy.opnsense.interface_vxlan
===================================

.. code-block:: yaml

    - hosts: localhost
      gather_facts: no
      module_defaults:
        group/ansibleguy.opnsense.all:
          firewall: 'opnsense.template.ansibleguy.net'
          api_credential_file: '/home/guy/.secret/opn.key'
    
        ansibleguy.opnsense.list:
          target: 'interface_vxlan'
    
      tasks:
        - name: Example
          ansibleguy.opnsense.interface_vxlan:
            id: 100
            local: '192.168.0.1'
            # remote: ''
            # group: ''
            # interface: 'lan'
            # debug: false
            # state: 'present'
            # reload: true
    
        - name: Adding VxLAN
          ansibleguy.opnsense.interface_vxlan:
            id: 100
            local: '192.168.0.1'
            interface: 'lan'
    
        - name: Listing
          ansibleguy.opnsense.list:
          #  target: 'interface_vxlan'
          register: existing_entries
    
        - name: Printing VxLANs
          ansible.builtin.debug:
            var: existing_entries.data
    
        - name: Removing VxLAN
          ansibleguy.opnsense.interface_vxlan:
            id: 100
            state: 'absent'

ansibleguy.opnsense.interface_vip
=================================

.. code-block:: yaml

    - hosts: localhost
      gather_facts: no
      module_defaults:
        group/ansibleguy.opnsense.all:
          firewall: 'opnsense.template.ansibleguy.net'
          api_credential_file: '/home/guy/.secret/opn.key'
    
        ansibleguy.opnsense.list:
          target: 'interface_vip'
    
      tasks:
        - name: Example
          ansibleguy.opnsense.interface_vip:
            interface: 'opt1'
            address: '192.168.0.100/24'
            # match_fields: ['address', 'interface]
            # mode: 'ipalias'
            # expand: true
            # bind: true
            # gateway: ''
            # password: ''
            # vhid: ''
            # advertising_base: 1
            # advertising_skew: 0
            # description: ''
            # debug: false
            # state: 'present'
            # reload: true
    
        - name: Adding VIP
          ansibleguy.opnsense.interface_vip:
            interface: 'opt1'
            address: '192.168.0.100/24'
            mode: 'carp'
            vhid: 10
            password: 'secret'
    
        - name: Listing
          ansibleguy.opnsense.list:
          #  target: 'interface_vip'
          register: existing_entries
    
        - name: Printing VIPs
          ansible.builtin.debug:
            var: existing_entries.data
    
        - name: Removing VIP
          ansibleguy.opnsense.interface_vip:
            interface: 'opt1'
            address: '192.168.0.100/24'
            state: 'absent'

ansibleguy.opnsense.interface_lagg
==================================

.. code-block:: yaml

    - hosts: localhost
      gather_facts: no
      module_defaults:
        group/ansibleguy.opnsense.all:
          firewall: 'opnsense.template.ansibleguy.net'
          api_credential_file: '/home/guy/.secret/opn.key'
    
        ansibleguy.opnsense.list:
          target: 'interface_lagg'
    
      tasks:
        - name: Example
          ansibleguy.opnsense.interface_lagg:
            # device: lagg0
            # description: LACP ax0/1
            members:
              - ax0
              - ax1
            # primary_member: ax0
            # proto: lacp
            # lacp_fast_timeout: 'default'
            # use_flowid: 'default'
            # lagghash: ['l2']
            # lacp_strict: 'default'
            # mtu: 9000
            # match_fields: ['members']
    
        - name: Adding LAGG
          ansibleguy.opnsense.interface_lagg:
            members:
              - ax0
              - ax1
    
        - name: Listing
          ansibleguy.opnsense.list:
          #  target: 'interface_lagg'
          register: existing_entries
    
        - name: Printing LAGGs
          ansible.builtin.debug:
            var: existing_entries.data
    
        - name: Removing LAGG
          ansibleguy.opnsense.interface_lagg:
            device: lagg0
            match_fields: ['device']
            state: 'absent'

ansibleguy.opnsense.interface_loopback
======================================

.. code-block:: yaml

    - hosts: localhost
      gather_facts: no
      module_defaults:
        group/ansibleguy.opnsense.all:
          firewall: 'opnsense.template.ansibleguy.net'
          api_credential_file: '/home/guy/.secret/opn.key'
    
        ansibleguy.opnsense.list:
          target: 'interface_loopback'
    
      tasks:
        - name: Example
          ansibleguy.opnsense.interface_loopback:
            description: 'MyLoopback'
            # debug: false
            # state: 'present'
            # reload: true
    
        - name: Adding Loopback
          ansibleguy.opnsense.interface_loopback:
            description: 'MyLoopback'
    
        - name: Listing
          ansibleguy.opnsense.list:
          #  target: 'interface_loopback'
          register: existing_entries
    
        - name: Printing Loopbacks
          ansible.builtin.debug:
            var: existing_entries.data
    
        - name: Removing Loopback
          ansibleguy.opnsense.interface_loopback:
            description: 'MyLoopback'
            state: 'absent'

ansibleguy.opnsense.interface_gre
======================================

.. code-block:: yaml

    - hosts: localhost
      gather_facts: no
      module_defaults:
        group/ansibleguy.opnsense.all:
          firewall: 'opnsense.template.ansibleguy.net'
          api_credential_file: '/home/guy/.secret/opn.key'
    
        ansibleguy.opnsense.list:
          target: 'interface_gre'
    
      tasks:
        - name: Example
          ansibleguy.opnsense.interface_gre:
            description: 'MyGRETunnel'
            local: 'lan'
            remote: '192.168.100.1'
            tunnel_local: '10.0.0.1'
            tunnel_remote: '10.0.0.2'
            # tunnel_remote_net: 32
            # debug: false
            # state: 'present'
            # reload: true
    
        - name: Adding GRE Tunnel
          ansibleguy.opnsense.interface_gre:
            description: 'MyGRETunnel'
            local: 'lan'
            remote: '192.168.100.1'
            tunnel_local: '10.0.0.1'
            tunnel_remote: '10.0.0.2'
    
        - name: Listing
          ansibleguy.opnsense.list:
          #  target: 'interface_gre'
          register: existing_entries
    
        - name: Printing Loopbacks
          ansible.builtin.debug:
            var: existing_entries.data
    
        - name: Removing GRE
          ansibleguy.opnsense.interface_gre:
            description: 'MyGRETunnel'
            state: 'absent'
