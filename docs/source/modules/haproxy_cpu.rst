.. _modules_haproxy_cpu:

.. include:: ../_include/head.rst

=======================
HAProxy - CPU Affinity
=======================

**STATE**: stable

**COMPATIBILITY**: OPNsense 24.1+

**Note**: Most functions should work on earlier OPNsense versions, but full compatibility is tested with OPNsense 24.1+. For compatibility with earlier versions, please check the configuration differences at: `HAProxy Configuration Reference <https://github.com/opnsense/plugins/blob/master/net/haproxy/src/opnsense/mvc/app/models/OPNsense/HAProxy/HAProxy.xml>`_

**TESTS**: `Playbook <https://github.com/ansibleguy/collection_opnsense/blob/latest/tests/haproxy_cpu.yml>`_

**API Docs**: `Core - HAProxy <https://docs.opnsense.org/development/api/core/haproxy.html>`_

**Service Docs**: `HAProxy <https://docs.opnsense.org/manual/how-tos/haproxy.html>`_


Contribution
************

This module was contributed by **MaximeWewer** (@MaximeWewer).

If you encounter any issues or have suggestions for improvements, please feel free to contribute to the project.


Prerequisites
*************

You need to install and configure HAProxy on the target system.

.. include:: ../_include/haproxy.rst

Definition
**********

.. include:: ../_include/param_basic.rst

ansibleguy.opnsense.haproxy_cpu
*******************************

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "name","string","true","\-","n","Name of the CPU affinity rule"
    "thread_id","string","true","\-","\-","Thread ID to bind. Options: 'all', 'odd', 'even', 'x1'-'x63'"
    "cpu_id","string","true","\-","\-","CPU ID to bind to. Options: 'all', 'odd', 'even', 'x0'-'x63'"

.. include:: ../_include/param_basic_en_state.rst

Examples
********

.. code-block:: yaml

    - ansibleguy.opnsense.haproxy_cpu:
        name: 'bind_thread1_cpu0'
        description: 'Bind HAProxy thread 1 to CPU 0'
        thread_id: 'x1'
        cpu_id: 'x0'

    - ansibleguy.opnsense.haproxy_cpu:
        name: 'bind_odd_threads'
        description: 'Bind odd threads to odd CPUs'
        thread_id: 'odd'
        cpu_id: 'odd'

    - ansibleguy.opnsense.haproxy_cpu:
        name: 'bind_all_threads'
        description: 'Bind all threads to all CPUs'
        thread_id: 'all'
        cpu_id: 'all'
