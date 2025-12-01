.. _modules_system:

.. include:: ../_include/head.rst

======
System
======

**STATE**: stable

**TESTS**: `Playbook <https://github.com/oxlorg/collection_opnsense/blob/latest/tests/system.yml>`_

**API Docs**: `Core - Firmware <https://docs.opnsense.org/development/api/core/firmware.html>`_

Contribution
************

Thanks to `@Rath <https://github.com/superstes>`_ for developing this module!

----

.. warning::

    **Only** use the :code:`upgrade` action in **test-environments**!

    When in production - use the WebUI to upgrade your boxes.

    The box is rebooted while performing an update - it might be dead.


Definition
**********

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "action","string","true","\-","Action to execute. One of: 'poweroff', 'reboot', 'update', 'upgrade', 'audit'. **WARNING**: the target firewall will be temporarily unavailable if running action 'upgrade' or 'reboot', or permanently if running action 'poweroff' (;"
    "wait","boolean","false","true","If the module should wait for the action to finish. Available for 'upgrade' and 'reboot'"
    "wait_timeout","int","false","90","Seconds to wait for the action to finish - if 'wait' is enabled"
    "poll_interval","int","false","2","Interval in which to check if the firewall is online"

.. include:: ../_include/param_basic.rst

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
        - name: Reboot the box - will wait until finished
          oxlorg.opnsense.system:
            action: 'reboot'

        - name: Reboot the box - don't wait
          oxlorg.opnsense.system:
            action: 'reboot'
            wait: false

        - name: Shutdown the box
          oxlorg.opnsense.system:
            action: 'poweroff'

        - name: Pull updates
          oxlorg.opnsense.system:
            action: 'update'

        - name: Start upgrade - will wait until finished (WARNING: ONLY USE IN TEST-ENVIRONMENTS)
          oxlorg.opnsense.system:
            action: 'upgrade'
            timeout: 120  # depends on your download speed and firmware-version
            force_upgrade: true

        - name: Run audit
          oxlorg.opnsense.system:
            action: 'audit'
