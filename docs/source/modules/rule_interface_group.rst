.. _modules_rule_interface_group:

.. include:: ../_include/head.rst

====
Rule Interface Group
====

**STATE**: unstable

**TESTS**: `Playbook <https://github.com/ansibleguy/collection_opnsense/blob/latest/tests/rule_interface_group.yml>`_

**API Docs**: `Core - Firewall <https://docs.opnsense.org/development/api/core/firewall.html>`_

**Service Docs**: `Interface Groups <https://docs.opnsense.org/manual/firewall_groups.html>`_


Definition
**********

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "name","string","true","\-","ifname","Name of the interface group. Only texts containing letters, digits and underscores with a maximum length of 15 characters are allowed and the name may not end with a digit."
    "members","list","false","ints, interfaces","Member interfaces - you must provide the network port as shown in 'Interfaces - Assignments - Network port"
    "gui_group","boolean","false","true","\-","Grouping these members in the interfaces menu section"
    "sequence","int","false","0","seq","Sequence used in sorting the groups"
    "description","string","false","\-","desc","Optional description"

.. include:: ../_include/param_basic.rst


Examples
********

.. code-block:: yaml

    - hosts: localhost
      gather_facts: no
      module_defaults:
        group/ansibleguy.opnsense.all:
          firewall: 'opnsense.template.ansibleguy.net'
          api_credential_file: '/home/guy/.secret/opn.key'

        ansibleguy.opnsense.list:
          target: 'rule_interface_group'

      tasks:
        - name: Example
          ansibleguy.opnsense.rule_interface_group:
            name: Internal
            members: ['vtnet0', 'vtnet1']
            # gui_group: true
            # sequence: 0
            # description: 'Optional description'

        - name: Adding 1
          ansibleguy.opnsense.rule_interface_group:
            name: Internal
            members: ['vtnet0', 'vtnet1']

        - name: Listing
          ansibleguy.opnsense.list:
          #  target: 'rule_interface_group'
          register: existing_entries

        - name: Printing rules
          ansible.bultin.debug:
            var: existing_entries.data
