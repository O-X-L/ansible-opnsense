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

Thanks to `@KalleDK <https://github.com/KalleDK>`_ for developing these module!

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
