.. _modules_haproxy_system:

.. include:: ../_include/head.rst

====================================
HAProxy performance & system modules
====================================

**STATE**: unstable

**COMPATIBILITY**: OPNsense 24.1+

**TESTS**:
`CPU <https://github.com/O-X-L/ansible_opnsense/blob/latest/tests/haproxy_cpu.yml>`_ |
`Maintenance <https://github.com/O-X-L/ansible_opnsense/blob/latest/tests/haproxy_maintenance.yml>`_

**API Docs**: `HAProxy <https://docs.opnsense.org/development/api/plugins/haproxy.html>`_

These modules manage HAProxy system performance and maintenance settings.

----

.. _haproxy_cpu:

oxlorg.opnsense.haproxy_cpu
===========================

Manages CPU affinity rules for HAProxy processes.

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "name","string","true","\-","\-","Choose a name for this CPU affinity rule"
    "enabled","boolean","false","true","\-","Enable or disable this CPU affinity rule"
    "thread_id","string","false","\-","\-","Thread ID that should bind to a specific CPU set. Values: all, odd, even, x1, x2, etc."
    "cpu_id","list","false","\-","\-","Bind the process/thread ID to this CPU"

Examples
--------

.. code-block:: yaml

    - name: Configure CPU affinity for web threads
      oxlorg.opnsense.haproxy_cpu:
        name: 'web_threads'
        description: 'CPU affinity for web processing'
        thread_id: 'x1'
        cpu_id: ['x0', 'x1']
        enabled: true

----

.. _haproxy_maintenance:

oxlorg.opnsense.haproxy_maintenance
===================================

Manages HAProxy maintenance and monitoring settings.

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "sync_certs","boolean","false","false","\-","Periodically sync SSL certificate changes into the running HAProxy service. Useful for short-lived Let's Encrypt certificates"
    "reload_service","boolean","false","false","\-","Periodically perform a reload of the HAProxy service. May cause minor service disruption. Can apply configuration changes outside business hours"
    "restart_service","boolean","false","false","\-","Periodically perform a full restart of the HAProxy service. Causes notable service disruption. Required when reload doesn't work due to long-running connections"

Examples
--------

.. code-block:: yaml

    - name: Configure HAProxy maintenance
      oxlorg.opnsense.haproxy_maintenance:
        sync_certs: true
        reload_service: false
        restart_service: false


**Note**: For general HAProxy configuration like tuning, logging, cache, and other settings, see :ref:`modules_haproxy_general <modules_haproxy_general>`.

See also: :ref:`modules_haproxy <modules_haproxy>` and :ref:`troubleshooting <modules_haproxy_troubleshooting>`
