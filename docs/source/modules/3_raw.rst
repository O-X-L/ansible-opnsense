.. _modules_raw:

.. include:: ../_include/head.rst

=======
3 - Raw
=======

**STATE**: unstable

**TESTS**: `Playbook <https://github.com/ansibleguy/collection_opnsense/blob/latest/tests/raw.yml>`_

Contribution
************

Thanks to `@Rath <https://github.com/superstes>`_ for developing this module!

----

Info
****

This module can perform any OPNSense API-query or -action.

It is meant to be used for your custom needs or provide you with features that are not yet implemented as dedicated modules.

Post-actions are not performed while in check-mode.

Definition
**********

You need to either provide :code:`module + controller + command` or :code:`url`!

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "module","string","false","\-","m, mod","The API-module to target"
    "controller","string","false","\-","co, cont","The API-controller to target"
    "command","string","false","\-","c, cmd","The API-command to target"
    "parameters","string","false","\-","p, params","Optional: Parameters to send"
    "url","string","false","\-","u","Alternative to module/controller/command</params>"
    "action","string","false","get","a, method","Choices: get, post"
    "data","dict","false","\-","d","Optional: Supply data to send"
    "headers","dict","false","\-","h","Optional: Supply headers to send"
    "timeout","float","false","20","t","Timeout in seconds for request + response"

.. include:: ../_include/param_basic.rst

----

Examples
********

.. code-block:: yaml

    - hosts: localhost
      gather_facts: no
      module_defaults:
        group/ansibleguy.opnsense.all:
          firewall: 'opnsense.template.ansibleguy.net'
          api_credential_file: '/home/guy/.secret/opn.key'

      tasks:
        - name: Query interfaces
          ansibleguy.opnsense.raw:
            url: 'interfaces/overview/interfacesInfo'
          register: interfaces

        - ansible.builtin.debug:
            var: interfaces.rows

        - name: Execute action
          ansibleguy.opnsense.raw:
            module: 'syslog'
            controller: 'service'
            command: 'restart'
            action: 'post'
