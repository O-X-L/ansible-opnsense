.. _modules_dhcp:

.. include:: ../_include/head.rst

====
DHCP
====

**STATE**: unstable

**TESTS**: `Reservation <https://github.com/ansibleguy/collection_opnsense/blob/latest/tests/dhcp_reservation.yml>`_ |
`ControlAgent <https://github.com/ansibleguy/collection_opnsense/blob/latest/tests/dhcp_controlagent.yml>`_

**API Docs**: `Core - KEA <https://docs.opnsense.org/development/api/core/kea.html>`_

**Service Docs**: `DHCP <https://docs.opnsense.org/manual/dhcp.html#kea-dhcp>`_

Contribution
************

Thanks to `@KalleDK <https://github.com/KalleDK>`_ for developing these modules!

----

Definition
**********

.. include:: ../_include/param_basic.rst

ansibleguy.opnsense.dhcp_reservation
====================================

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "ip","string","true","","ip_address","IP address to offer to the client"
    "mac","string","false for state changes, else true","","mac_address","MAC/Ether address of the client in question"
    "subnet","string","false for state changes, else true","","\-","Subnet this reservation belongs to"
    "hostname","string","false","","\-","Offer a hostname to the client"
    "description","string","false","","\-","Optional description"
    "reload","boolean","false","true","\-", .. include:: ../_include/param_reload.rst

ansibleguy.opnsense.dhcp_controlagent
=====================================

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "enabled","boolean","false","true","\-","Enable or disable the control agent"
    "http_host","string","false","127.0.0.1","","Address on which the RESTful interface should be available"
    "http_port","int","false","8000","","MAC/Ether address of the client in question"
    "reload","boolean","false","true","\-", .. include:: ../_include/param_reload.rst

----

ansibleguy.opnsense.dhcp_subnet
===============================

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "subnet","string","true","\-","\-","Subnet to use. should be large enough to hold the specified pools and reservations"
    "description","string","false","\-","desc","Optional description of the subnet"
    "pools","list","false","\-","\-","List of pools, one per line in range or subnet format (e.g. 192.168.0.100 - 192.168.0.200)"
    "auto_options","bool,"false","true","option_data_autocollect","Automatically update option data for relevant attributes as routers, dns servers and ntp servers when applying settings from the gui."
    "gateway","list","false","gw,routers","\-","Default gateways to offer to the clients"
    "routes","str","false","static_routes","\-","Static routes that the client should install in its routing cache, defined as dest-ip1,router-ip1;dest-ip2,router-ip2"
    "dns","list","false","dns_servers,dns_srv","\-","DNS servers to offer to the clients"
    "domain","str","false","domain_name,dom_name,dom","\-","The domain name to offer to the client, set to this firewall's domain name when left empty"
    "domain_search","list","false","dom_search","\-","Specifies a 'search list' of Domain Names to be used by the client to locate not-fully-qualified domain names."
    "ntp_servers","list","false","ntp_srv,ntp","\-","Specifies a list of IP addresses indicating NTP (RFC 5905) servers available to the client."
    "time_servers","list","false","time_srv","\-","Specifies a list of RFC 868 time servers available to the client."
    "next_server","str","false","next_srv","\-","Next server IP address"
    "tftp_server","str","false","tftp,tftp_srv,tftp_server_name","\-","TFTP server address or fqdn"
    "tftp_file","str","false","tftp_boot_file,boot_file_name","\-","Boot filename to request"


Examples
********

ansibleguy.opnsense.dhcp_reservation
====================================

.. code-block:: yaml

    - hosts: localhost
      gather_facts: no
      module_defaults:
        group/ansibleguy.opnsense.all:
          firewall: 'opnsense.template.ansibleguy.net'
          api_credential_file: '/home/guy/.secret/opn.key'

        ansibleguy.opnsense.list:
          target: 'dhcp_reservation'

      tasks:
        - name: Example
          ansibleguy.opnsense.dhcp_reservation:
            ip: '192.168.0.1'
            subnet: '192.168.0.0/24'
            mac: 'aa:aa:aa:bb:bb:bb'
            # hostname: 'test'
            # description: ''
            # state: 'present'
            # reload: true
            # debug: false

        - name: Adding
          ansibleguy.opnsense.dhcp_reservation:
            subnet: '192.168.0.0/24'
            ip: '192.168.0.1'
            mac: 'aa:aa:aa:bb:bb:bb'

        - name: Removing
          ansibleguy.opnsense.dhcp_reservation:
            ip: '192.168.0.1'
            state: 'absent'

        - name: Listing
          ansibleguy.opnsense.list:
          #  target: 'dhcp_reservation'
          register: existing_entries

        - name: Show existing reservations
          ansible.builtin.debug:
            var: existing_entries.data

----

ansibleguy.opnsense.dhcp_controlagent
=====================================

.. code-block:: yaml

    - hosts: localhost
      gather_facts: no
      module_defaults:
        group/ansibleguy.opnsense.all:
          firewall: 'opnsense.template.ansibleguy.net'
          api_credential_file: '/home/guy/.secret/opn.key'

      tasks:
        - name: Example
          ansibleguy.opnsense.dhcp_controlagent:
            enabled: true
            http_host: 127.0.0.1
            http_port: 8000
            # reload: true
            # debug: false

        - name: Stopping
          ansibleguy.opnsense.dhcp_controlagent:
            enabled: false
            reload: true

----

ansibleguy.opnsense.dhcp_subnet

.. code-block:: yaml

    - host: localhost
      gather_facts: no
      module_defaults:

      tasks:
        - name: Add subnet
          ansibleguy.opnsense.dhcp_subnet:
          subnet: '10.0.100.0/24'

        - name: Remove subnet
          ansibleguy.opnsense.dhcp_subnet:
          subnet: '10.0.100.0/24'
          state: absent
