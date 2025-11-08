.. _modules_nat_one_to_one:

.. include:: ../_include/head.rst

==============
NAT One-To-One
==============

**STATE**: stable

**TESTS**: `Playbook <https://github.com/oxlorg/collection_opnsense/blob/latest/tests/nat_one_to_one.yml>`_

**API Docs**: `Core - Firewall <https://docs.opnsense.org/development/api/core/firewall.html>`_

**Service Docs**: `One-to-one NAT <https://docs.opnsense.org/manual/nat.html#one-to-one>`_

Contribution
************

Thanks to `@jiuka <https://github.com/jiuka>`_ for developing this module!

----

Info
****

Savepoint
=========

You can prevent lockout-situations using the savepoint systems:

- :ref:`oxlorg.opnsense.savepoint <modules_savepoint>`


Definition
**********

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "match_fields","list","false","['interface', 'external'']","\-","Fields that are used to match configured rules with the running config - if any of those fields are changed, the module will think it's a new rule. At least one of: 'sequence', 'action', 'interface', 'direction', 'ip_protocol', 'protocol', 'source_invert', 'source_net', 'source_port', 'destination_invert', 'destination_net', 'destination_port', 'gateway', 'description', 'uuid'"
    "sequence","int","false","1","seq","Sequence for rule processing, Integer between 1 and 1000000"
    "log","boolean","false","true","l","If rule matches should be shown in the firewall logs"
    "interface","string","false for deletion, else true","\-","i, int","The interface to match this rule on"
    "type","string","false","binnat","\-","NAT type to use. ONE of: binat or nat. See `Some terms explained <https://docs.opnsense.org/manual/nat.html#some-terms-explained>`_."
    "external","string","false for deletion, else true","\-","external_net, ext, e","External subnet's starting address for the 1:1 mapping or network. This is the address or network the traffic will translate to/from."
    "source_net","string","false for deletion, else true","\-","s, src, source","Internal subnet for the 1:1 mapping."
    "source_invert","boolean","false","false","si, src_inv, src_not","Inverted matching of the source."
    "destination_net","string","false","'any'","d, dest, destination","The 1:1 mapping will only be used for connections to or from the specified destination. Hint: this is usually 'any'."
    "destination_invert","boolean","false","false","di, dest_inv, dest_not","Inverted matching of the destination"
    "nat_reflection","string","false","''","\-","One of: '', enable, disable. See `Some terms explained <https://docs.opnsense.org/manual/nat.html#some-terms-explained>`_."
    "description","string","false","\-","desc","Description for the rule"
    "state","string","false","'present'","st","State of the rule. One of: 'present', 'absent'"
    "enabled","boolean","false","true","en","If the rule should be en- or disabled"
    "uuid","string","false","\-","\-","Optionally you can supply the uuid of an existing rule"
    "reload","boolean","false","true","apply", .. include:: ../_include/param_reload.rst

.. include:: ../_include/param_basic.rst

----

Usage
*****

To add One-to-One NAT rules - see: `OPNsense Documentation <https://docs.opnsense.org/manual/nat.html#one-to-one>`_

----

Examples
********

.. code-block:: yaml

    - hosts: localhost
      gather_facts: false
      module_defaults:
        group/oxlorg.opnsense.all:
          firewall: 'opnsense.template.opnsense.oxl.app'
          api_credential_file: '/home/guy/.secret/opn.key'

        oxlorg.opnsense.list:
          target: 'nat_one_to_one'

      tasks:
        # add optional parameters commented-out
        # required ones normally
        # add their default values to get a brief overview of how the module works
        - name: Example
          oxlorg.opnsense.nat_one_to_one:
            #sequence: 1
            interface: 'lan'
            #type: binnat
            external: '8.8.8.8'
            source_net: '192.168.0.1'
            #source_invert: false
            #destination_net: 'any'
            #destination_invert: false
            #nat_reflection: ''
            description: 'Map External IP 8.8.8.8 to Internal 192.168.0.1'
            # enabled: true
            # state: 'absent'
            # debug: false

        - name: Listing jobs
          oxlorg.opnsense.list:
          #  target: 'nat_one_to_one'
          register: existing_one_to_one

        - name: Printing
          ansible.builtin.debug:
            var: existing_one_to_one.data
