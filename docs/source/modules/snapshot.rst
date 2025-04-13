.. _modules_snapshot:

.. include:: ../_include/head.rst

========
Snapshot
========

**STATE**: unstable

**TESTS**: `Playbook <https://github.com/ansibleguy/collection_opnsense/blob/latest/tests/snapshot.yml>`_

**API Docs**: `Core - Core <https://docs.opnsense.org/development/api/core/core.html>`_

**Service Docs**: `Snapshots <https://docs.opnsense.org/manual/snapshots.html>`_


Definition
**********

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "name","string","true","\-","\-","Name of the snapshot"
    "activate","boolean","false","false","\-","Activate the snapshot for the next reboot"

.. include:: ../_include/param_basic.rst

Info
****

.. warning::

  Snapshots require ZFS as filesystem. UFS will not work since it does not support file system level snapshots.


Usage
*****

Allows you to create, activate and delete snapshots. Activation only marks the snapshot as thje default boot option.
It does **not** change the snapshot currently running.

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
          target: 'snapshot'

      tasks:
        # add optional parameters commented-out
        # required ones normally
        # add their default values to get a brief overview of how the module works
        - name: Example
          ansibleguy.opnsense.snapshot:
            name: 'known-good'
            # activate: false
            # state: 'absent'
            # debug: false

        - name: Create known-good snapshot
          ansibleguy.opnsense.snapshot:
            name: 'known-good'

        - name: Listing snapshots
          ansibleguy.opnsense.list:
          #  target: 'snapshot'
          register: existing_snapshots

        - name: Printing snapshots
          ansible.builtin.debug:
            var: existing_snapshots.data
