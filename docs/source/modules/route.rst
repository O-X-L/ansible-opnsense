.. _modules_routing:

.. include:: ../_include/head.rst

=======
Routing
=======

**STATE**: stable

Static Routes
=============

**TESTS**: `Playbook <https://github.com/ansibleguy/collection_opnsense/blob/latest/tests/route.yml>`_

**API Docs**: `Core - Routes <https://docs.opnsense.org/development/api/core/routes.html>`_

**Service Docs**: `Routes <https://docs.opnsense.org/manual/routes.html>`_

Gateway Groups
==============

**TESTS**: `Playbook <https://github.com/ansibleguy/collection_opnsense/blob/latest/tests/gateway.yml>`_

**API Docs**: `Core - routings <https://docs.opnsense.org/development/api/core/routing.html>`_

**Service Docs**: `routings <https://docs.opnsense.org/manual/gateways.html>`_

Contribution
************

Thanks to `@kdhlab <https://github.com/kdhlab>`_ for developing the :code:`gateway` module!


Definition
**********

.. include:: ../_include/param_basic.rst

ansibleguy.opnsense.route
=========================

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "gateway","string","true","\-","gw","An existing gateway that should be used as target for the network. The network ip protocol (*IPv4/IPv6*) must be the same! **WARNING**: You need to supply the gateways short-name as can be seen in the WEB-UI menu 'System - Gateways - Single - Name'"
    "network","string","true","\-","nw, net","Network to route. The network ip protocol (*IPv4/IPv6*) must be the same!"
    "description","string","false","\-","desc","Optional description for the route. Could be used as unique-identifier when set as only 'match_field'."
    "match_fields","list of strings","false","['network', 'gateway']","\-","Fields that are used to match configured routes with the running config - if any of those fields are changed, the module will think it's a new route"
    "reload","boolean","false","true","\-", .. include:: ../_include/param_reload.rst

ansibleguy.opnsense.gateway
===========================

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "name","string","true","\-","\-","Gateway Name"
    "interface","string","true","\-","int, if","Interface belonging to this gateway"
    "gateway","string","true","\-","gw, ip","Gateway IP"
    "description","string","false","\-","desc","Optional description for the Gateway. Could be used as unique-identifier when set as only 'match_field'."
    "default_gw","string","true","\-","default, internet, inet","This will select the above gateway as a default gateway candidate."
    "far_gw","string","false","\-","far","This will allow the gateway to exist outside of the interface subnet."
    "monitor_disable","boolean","false","false","\-","Disable gateway monitoring"
    "monitor_noroute","boolean","false","false","\-","Do not create a dedicated host route for this monitor."
    "monitor","string","false","\-","\-","IP address to use as a monitor IP for the gateway."
    "force_down","boolean","false","false","down","Force the gateway to be considered as down."
    "priority","integer","false","255","prio","Choose a value between 1 and 255. Influences sort order when selecting a (default) gateway, lower means more important."
    "weight","integer","false","1","\-","Weight for this gateway when used in a gateway group. Specificed as an integer number between 1 and 5."
    "latency_low","integer","false","200","\-","Latency threshold in milliseconds. If the latency is lower than this value, the gateway is considered as up."
    "latency_high","integer","false","500","\-","Latency threshold in milliseconds. If the latency is higher than this value, the gateway is considered as down."
    "loss_low","integer","false","10","\-","Packet loss threshold in percent. If the packet loss is lower than this value, the gateway is considered as up."
    "loss_high","integer","false","20","\-","Packet loss threshold in percent. If the packet loss is higher than this value, the gateway is considered as down."
    "interval","integer","false","1","\-","How often that an ICMP probe will be sent in seconds."
    "time_period","integer","false","60","\-","The time period over which results are averaged."
    "loss_interval","integer","false","4","\-","Time interval before packets are treated as lost."
    "data_length","integer","false","0","\-","Size of ICMP packets to send."
    "match_fields","list of strings","false","['name', 'gateway']","\-","Fields that are used to match configured gateways with the running config - if any of those fields are changed, the module will think it's a new gateway, possible options: ['name', 'gateway', 'description']"
    "reload","boolean","false","true","\-", .. include:: ../_include/param_reload.rst

Usage
*****

First you will have to know about **route-matching**.

The module somehow needs to link the configured and existing routes to manage them.

You can to set how this matching is done by setting the 'match_fields' parameter!

The default behaviour is that a route is matched by its 'gateway' and 'network'.

However - it is **recommended** to use/set 'description' as **unique identifier** if many routes are used.


Examples
********

ansibleguy.opnsense.route
=========================

.. code-block:: yaml

    - hosts: localhost
      gather_facts: no
      module_defaults:
        group/ansibleguy.opnsense.all:
          firewall: 'opnsense.template.ansibleguy.net'
          api_credential_file: '/home/guy/.secret/opn.key'

        ansibleguy.opnsense.route:
          match_fields: ['description']

        ansibleguy.opnsense.list:
          target: 'route'

      tasks:
        - name: Example
          ansibleguy.opnsense.route:
            description: 'test1'
            network: '172.16.0.0/12'
            gateway: 'LAN_GW'
            # match_fields: ['description']
            # enabled: true
            # debug: false
            # state: 'present'

        - name: Adding route
          ansibleguy.opnsense.route:
            description: 'test2'
            network: '10.206.0.0/16'
            gateway: 'VPN_GW'
            # match_fields: ['description']

        - name: Disabling route
          ansibleguy.opnsense.route:
            description: 'test3'
            network: '10.55.0.0/16'
            gateway: 'VPN_GW'
            enabled: false
            # match_fields: ['description']

        - name: Listing
          ansibleguy.opnsense.list:
          #  target: 'route'
          register: existing_entries

        - name: Printing routes
          ansible.builtin.debug:
            var: existing_entries.data

        - name: Removing route 'test3'
          ansibleguy.opnsense.route:
            description: 'test3'
            network: '10.55.0.0/16'
            gateway: 'VPN_GW'
            state: 'absent'
            match_fields: ['description']

ansibleguy.opnsense.gateway
===========================

.. code-block:: yaml

    - hosts: localhost
      gather_facts: false
      module_defaults:
        group/ansibleguy.opnsense.all:
          firewall: 'opnsense.template.ansibleguy.net'
          api_credential_file: '/home/guy/.secret/opn.key'

        ansibleguy.opnsense.gateway:
          match_fields: ['description']

        ansibleguy.opnsense.list:
          target: 'gateway'

      tasks:
        - name: List Gateways
          ansibleguy.opnsense.list:
          register: existing_entries

        - name: Add Gateway
          ansibleguy.opnsense.gateway:
            name: 'Test_GW'
            interface: 'wg1'
            gateway: '10.255.255.16'

        - name: Set Gateway Monitor IP
          ansibleguy.opnsense.gateway:
            name: 'Test_GW'
            interface: 'wg1'
            gateway: '10.255.255.16'
            monitor: '1.1.1.1'

        - name: Delete Gateway
          ansibleguy.opnsense.gateway:
            name: 'Test_GW'
            state: absent
