.. _modules_tunable:

.. include:: ../_include/head.rst

========
Tunables
========

**STATE**: unstable

**TESTS**: `Playbook <https://github.com/O-X-L/ansible-opnsense/blob/latest/tests/tunable.yml>`_

**API Docs**: `Core - Core <https://docs.opnsense.org/development/api/core/core.html>`_

**Service Docs**: `System Tunables <https://docs.opnsense.org/manual/settingsmenu.html#tunables>`_

Contribution
************

Thanks to `@Pablo1 <https://github.com/Pablo1>`_ for developing this module!

----

Definition
**********

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "tunable","string","true","\-","name, sysctl","Name of the tunable, for example 'net.inet.ip.redirect'. Used to match the entry."
    "value","string","true for state present","\-","\-","Value of the tunable. An empty string sets it back to the system default."
    "description","string","false","\-","desc, descr","Description of the tunable. If unset, the existing one is kept."
    "reload","boolean","false","false","\-", .. include:: ../_include/param_reload.rst

.. include:: ../_include/param_basic.rst

----

Usage
*****

OPNsense lists many tunables by default, with their default values, before they are set. Such a tunable is stored in the config only when you set it. Setting it with this module creates that entry.

:code:`state: absent` deletes the stored entry. A tunable that OPNsense lists by default then shows its default value again; deleting one that is not stored changes nothing.

The changes are applied with :code:`reload: true`, or with the :code:`reload` module (target :code:`tunable`) once after all tunables are set.

----

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

      tasks:
        - name: Example
          oxlorg.opnsense.tunable:
            tunable: 'net.inet6.icmp6.rediraccept'
            value: '0'
            # description: 'Do not accept ICMPv6 redirects'
            # reload: false
            # state: 'present'
            # debug: false

        - name: Setting a tunable that is listed by default
          oxlorg.opnsense.tunable:
            tunable: 'net.inet.icmp.drop_redirect'
            value: '1'
            reload: true

        - name: Removing the stored value
          oxlorg.opnsense.tunable:
            tunable: 'net.inet6.icmp6.rediraccept'
            state: 'absent'
