.. _modules_nut_diagnostics:

.. include:: ../_include/head.rst

=====================================
NUT - Network UPS Tools - Diagnostics
=====================================

**State:** Unstable

**Tests:** `nut_diagnostics.yml <https://github.com/O-X-L/ansible_opnsense/blob/latest/tests/nut_diagnostics.yml>`_

**API Docs**: `Plugins - NUT <https://docs.opnsense.org/development/api/plugins/nut.html>`_

**Service Docs**: `NUT - Network UPS Tools <https://docs.opnsense.org/manual/how-tos/nut.html>`_

Contribution
************

Author: `@wmatusiak <https://github.com/wmatusiak>`_

If you encounter any issues or have suggestions for improvements, please feel free to contribute to the project.

----

Prerequisites
*************

You need to install the NUT plugin:

```
os-nut
```
You can also install it using the :ref:`oxlorg.opnsense.package <modules_package>` module.

----

Functions
*********

This module allows you to read UPS Status from Network UPS Tools on OPNsense firewall.

Parameters
##########

.. include:: ../_include/param_basic.rst

.. include:: ../_include/param_reload.rst

----

Examples
********

.. code-block:: yaml

   - hosts: firewalls
     connection: local
     gather_facts: false
     module_defaults:
        group/oxlorg.opnsense.all:
            firewall: 'opnsense.template.oxlorg.net'
            api_credential_file: '/home/guy/.secret/opn.key'

    tasks:
        - name: Read UPS status
          oxlorg.opnsense.nut_diagnostics:
          register: ups_status

        - name: Display UPS status
          ansible.builtin.debug:
            msg: " {{ ups_status.data }}"
            
