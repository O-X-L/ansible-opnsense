.. _modules_alias_multi:

.. include:: ../_include/head.rst

=======================
Alias - Mass Management
=======================


**STATE**: stable

**TESTS**: `Playbook <https://github.com/O-X-L/ansible_opnsense/blob/latest/tests/alias_multi.yml>`_

**API Docs**: `Core - Firewall <https://docs.opnsense.org/development/api/core/firewall.html>`_

**Service Docs**: `Aliases <https://docs.opnsense.org/manual/aliases.html>`_

This module allows you to manage multiple aliases.

It is faster than the 'alias' module as it reduces the needed api/http calls.

Contribution
************

Thanks to `@Rath <https://github.com/superstes>`_ for developing these modules!

----

Info
****

For more detailed information on what alias types are supported - see the `OPNSense documentation <https://docs.opnsense.org/manual/aliases.html>`_.

Multi
*****

- Each alias has the attributes as defined in the :ref:`oxlorg.opnsense.alias <modules_alias>` module

- To ensure valid configuration - the attributes of each alias get verified using ansible's built-in verifier

Definition
**********

See: :ref:`Mass Management Arguments <modules_multi>`


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

      tasks:
        - name: Creation
          oxlorg.opnsense.alias:
            aliases:
              - name: 'test1'
                content: '1.1.1.1'

              - name: 'test2'
                content: ['1.1.1.1', '1.1.1.2']
                description: 'to be deleted'

              - name: 'test3'
                type: 'network'
                content: '10.0.0.0/24'
                description: 'to be disabled'

            multi_control:
              fail_verify: true
              # fail_processing: false
              # output_info: false

        - name: Changes
          oxlorg.opnsense.alias:
            aliases:
              - name: 'test1'
                content: ['1.1.1.3']

              - name: 'test2'
                state: 'absent'

              - name: 'test3'
                enabled: false

        - name: Change state of all
          oxlorg.opnsense.alias:
            aliases:
              - name: 'test1'
              - name: 'test3'

            multi_control:
              state: 'absent'
              # enabled: true

        - name: Listing
          oxlorg.opnsense.list:
            target: 'alias'
          register: existing_entries

        - name: Printing aliases
          ansible.builtin.debug:
            var: existing_entries.data

        - name: Purging all non-configured aliases
          oxlorg.opnsense.alias:
            aliases: {...}

            multi_control:
              purge_all: true
              # action: 'disable'  # default = delete

        - name: Purging all port aliases
          oxlorg.opnsense.alias:
            multi_control:
              purge_all: true
              filters:  # filtering aliases to purge by alias-parameters
                type: 'port'

              # filter_invert: true
