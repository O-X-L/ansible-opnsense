.. _modules_dhcrelay_relay:

.. include:: ../_include/head.rst

================
DHCRelay - Relay
================

**STATE**: stable

**TESTS**: `Playbook <https://github.com/O-X-L/ansible-opnsense/blob/latest/tests/dhcrelay_destination.yml>`_

**API Docs**: `Core - DHCRelay <https://docs.opnsense.org/development/api/core/dhcrelay.html>`_

**Service Docs**: `DHCRelay <https://docs.opnsense.org/manual/dhcp.html#dhcrelay>`_

Contribution
************

Thanks to `@jiuka <https://github.com/jiuka>`_ for developing this module!

----

Definition
**********

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "enabled","boolean","false","false","\-","Enable or disable this relay"
    "interface","string","true","","i, int"," The interface to relay DHCP requests from"
    "destination","string","true","\-","dest"," The destination server group to relay DHCP requests to"
    "agent_info","boolean","false","false","\-","Add the relay agent information option"
    "reload","boolean","false","true","\-", .. include:: ../_include/param_reload.rst

.. include:: ../_include/param_basic.rst

----

Info
****

This module manages DHCRelay relays. Each interface can be assigned a single relay.

Note: You can also use the shortform module name: :code:`oxlorg.opnsense.dhcrelay`

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

        oxlorg.opnsense.list:
          target: 'dhcrelay_relay'

      tasks:
        - name: Example
          oxlorg.opnsense.dhcrelay_relay:
            interface: 'lan'
            destination: mydhcp
            # enabled: false
            # agent_info: false
            # state: 'present'
            # reload: true
            # debug: false

        - name: Adding
          oxlorg.opnsense.dhcrelay_relay:
            interface: 'lan'
            destination: mydhcp

        - name: Removing
          oxlorg.opnsense.dhcrelay_relay:
            interface: 'lan'
            destination: mydhcp
            state: 'absent'

        - name: Listing
          oxlorg.opnsense.list:
          #  target: 'dhcrelay_relay'
          register: existing_entries

        - name: Printing dhcrelay relays
          ansible.builtin.debug:
            var: existing_entries.data
