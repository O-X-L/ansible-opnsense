.. _modules_neighbor:

.. include:: ../_include/head.rst

=========
Neighbors
=========

**STATE**: unstable

**TESTS**: `Playbook <https://github.com/O-X-L/ansible-opnsense/blob/latest/tests/neighbor.yml>`_

**API Docs**: `neighbor <https://docs.opnsense.org/development/api/core/interfaces.html>`_

**Service Docs**: `Neighbors <https://docs.opnsense.org/manual/neighbors.html>`_


Definition
**********

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "description","string","true","\-","desc, name","The unique description used to match the configured entries to the existing ones"
    "ethernet_address","string","true","\-","mac","Hardware MAC address of the neighbor (format xx:xx:xx:xx:xx:xx)"
    "ip_address","string","true","\-","ip","IP address to assign to the provided MAC address"
    "reload","boolean","false","true","\-", .. include:: ../_include/param_reload.rst

.. include:: ../_include/param_basic.rst

Usage
*****

Create static entries in the `ARP` or `NDP` table.

Examples
********

.. code-block:: yaml

    - hosts: firewalls
      connection: local
      gather_facts: false
      module_defaults:
        group/oxlorg.opnsense.all:
          firewall: 'opnsense.template.opnsense.oxl.app'
          api_credential_file: '/home/guy/.secret/opn.key'

        oxlorg.opnsense.list:
          target: 'neighbor'

      tasks:
        - name: Example
          oxlorg.opnsense.neighbor:
            description: 'MyNeighbor'
            ethernet_address: 00:11:22:33:44:55
            ip_address: 192.168.100.100
            # state: 'absent'
            # debug: false

        - name: Adding a neighbor
          oxlorg.opnsense.neighbor:
            description: 'MyNeighbor'
            ethernet_address: 00:11:22:33:44:55
            ip_address: 192.168.100.100

        - name: Changing a neighbor
          oxlorg.opnsense.neighbor:
            description: 'MyNeighbor'
            ethernet_address: 00:11:22:33:44:55
            ip_address: 192.168.100.101

        - name: Listing neighbors
          oxlorg.opnsense.list:
          #  target: 'neighbor'
          register: existing_neighbors

        - name: Printing neighbors
          ansible.builtin.debug:
            var: existing_neighbors.data
