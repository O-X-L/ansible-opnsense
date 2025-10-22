.. _modules_rule_multi:

.. include:: ../_include/head.rst

======================
Rule - Mass Management
======================

**STATE**: stable

**TESTS**: `rule_multi <https://github.com/O-X-L/ansible-opnsense/blob/latest/tests/rule_multi.yml>`_ |
`rule_purge <https://github.com/O-X-L/ansible-opnsense/blob/latest/tests/rule_multi.yml>`_

**API Docs**: `Core - Firewall <https://docs.opnsense.org/development/api/core/firewall.html>`_

**Service Docs**: `Rules <https://docs.opnsense.org/manual/firewall.html#rules.html>`_

Contribution
************

Thanks to `@Rath <https://github.com/superstes>`_ for developing these modules!

----

Info
****

For basic info, limitations and must-know to the rule-handling see the :ref:`oxlorg.opnsense.rule <modules_rule>` module!

Multi
*****

- Each rule has the attributes as defined in the :ref:`'single' oxlorg.opnsense.rule <modules_rule>` module

- To ensure valid configuration - the attributes of each rule get verified using ansible's built-in verifier

----

Definition
**********

See: :ref:`Mass Management Arguments <modules_multi>`

----

Usage
*****

You could either invoke this module:

- once for all rules
- once per logical grouping of rules

----

Examples
********

Basics
======

.. code-block:: yaml

    - hosts: localhost
      gather_facts: no
      module_defaults:
        group/oxlorg.opnsense.all:
          firewall: 'opnsense.template.opnsense.oxl.app'
          api_credential_file: '/home/guy/.secret/opn.key'

        oxlorg.opnsense.rule:
          match_fields: ['description']

      tasks:
        - name: Changing
          oxlorg.opnsense.rule:
            rules:
              - name: 'test1'
                source_net: '192.168.1.0/24'
                destination_invert: true
                destination_net: '10.1.0.0/8'
                action: 'block'

              - name: 'test2'
                source_net: '192.168.0.0/16'
                destination_net: '10.156.10.0/24'
                destination_port: 8080
                protocol: 'TCP'
                interface: ['lan', 'opt1']

              - name: 'test3'
                src: 'ALIAS_URLTABLE_TOR_EXIT_NODES'
                int: 'wan'
                action: 'block'

              - name: 'test4'
                src: 'ALIAS_URLTABLE_TOR_EXIT_NODES'
                int: 'wan'
                action: 'block'
                ip_proto: 'inet6'
                state: 'absent'

            # match_fields: ['description']
            # reload: true

            multi_control:
              fail_verify: true
              # fail_processing: false
              # output_info: false

        - name: Pulling existing rules
          oxlorg.opnsense.list:
            target: 'rule'
          register: existing_entries

        - name: Printing rules
          ansible.builtin.debug:
            var: existing_entries.data

        - name: Purging all non-configured rules
          oxlorg.opnsense.rule:
            rules: {...}

            match_fields: ['description']
            multi_control:
              purge_all: true
              # action: 'disable'  # default = delete

        - name: Purging allow-rules on interface opt2 that use IPv4
          oxlorg.opnsense.rule:
            multi_control:
              purge_all: true
              filters:  # filtering rules to purge by rule-parameters
                  ip_protocol: 'inet'
                  action: 'allow'
                  interface: ['opt2']

              # filter_invert: true

Options
=======

You can also override all rule parameters as needed.

.. code-block:: yaml

    - name: Changing
      oxlorg.opnsense.rule:
        rules: {...}

        multi_control:
            # set parameters and/or states to all rules
            override:
              interface: ['lan', 'opt1', 'opt2']
              log: true

            state: 'absent'
            enabled: false

        # match_fields: ['description']

To simplify the modules usage and config - you can also use shorter parameter aliases.

.. code-block:: yaml

    - name: Changing
      oxlorg.opnsense.rule:
        rules:
          - name: 'test1'
            src: 'ALIAS_URLTABLE_TOR_EXIT_NODES'
            int: 'wan'
            action: 'block'

          - name: 'test2'
            src: 'ALIAS_URLTABLE_TOR_EXIT_NODES'
            int: 'wan'
            action: 'block'
            ip_proto: 'inet6'
            state: 'absent'

          - name: 'test3'
            s: '192.168.0.0/16'  # source
            d: '10.81.53.0/24'  # destination
            dp: 443  # destination_port
            p: 'TCP'  # protocol
            i: ['lan', 'opt1']  # interface
            en: false  # enabled

        # match_fields: ['description']

Logical grouping
================

This example shows an option how to manage complexer rule-sets and/or template rules across multiple sites.

Basically we are abstracting the rule-set into interface-groups (*I'll call them zones*)

.. code-block:: yaml

    to be done
