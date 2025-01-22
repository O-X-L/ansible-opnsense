.. _modules_category:

.. include:: ../_include/head.rst

=================
Firewall Category
=================

**STATE**: unstable

**TESTS**: `category <https://github.com/ansibleguy/collection_opnsense/blob/latest/tests/category.yml>`_

**API Docs**: `Firewall - category <https://docs.opnsense.org/development/api/core/firewall.html>`_

**Service Docs**: `Categories <https://docs.opnsense.org/manual/firewall_categories.html>`_


Definition
**********

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "name","string","true","\-","\-","Name of the category."
    "color","string","false","\-","\-","Color of the category."
    "auto","boolean","false","false","\-","Mark category as Automatically added, will be removed when unused."

.. include:: ../_include/param_basic.rst

Usage
*****

Manage categories to ease maintenance of larger rulesets.

It currently just works with the 'Firewall' plugin:

- :ref:`ansibleguy.opnsense.alias <modules_alias>`, :ref:`ansibleguy.opnsense.alias_multi <modules_alias_multi>`
- :ref:`ansibleguy.opnsense.rule <modules_rule>`, :ref:`ansibleguy.opnsense.rule_multi <modules_rule_multi>`
- :ref:`ansibleguy.opnsense.source_nat <modules_source_nat>`

Examples
********

.. code-block:: yaml

    - hosts: localhost
      gather_facts: false
      module_defaults:
        group/ansibleguy.opnsense.all:
          firewall: 'opnsense.template.ansibleguy.net'
          api_credential_file: '/home/guy/.secret/opn.key'

        ansibleguy.opnsense.list:
          target: 'category'

      tasks:
        # add optional parameters commented-out
        # required ones normally
        # add their default values to get a brief overview of how the module works
        - name: Example
          ansibleguy.opnsense.category:
            name: 'Ansible Managed'
            # color: 028482
            # auot: false
            # state: 'absent'
            # debug: false

        - name: Adding something
          ansibleguy.opnsense.category:
            name: 'Ansible Managed'

        - name: Changing something
          ansibleguy.opnsense.category:
            name: 'Ansible Managed'
            color: 028482

        - name: Listing categories
          ansibleguy.opnsense.list:
          #  target: 'category'
          register: existing_categories

        - name: Printing
          ansible.builtin.debug:
            var: existing_categories.data
