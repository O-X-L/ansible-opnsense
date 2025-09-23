.. _modules_haproxy_system:

.. include:: ../_include/head.rst

============================
HAProxy performance & system
============================

**STATE**: unstable

**COMPATIBILITY**: OPNsense 24.1+

**TESTS**: 
`CPU <https://github.com/O-X-L/ansible_opnsense/blob/latest/tests/haproxy_cpu.yml>`_ |
`Maintenance <https://github.com/O-X-L/ansible_opnsense/blob/latest/tests/haproxy_maintenance.yml>`_ |

**API Docs**: `HAProxy <https://docs.opnsense.org/development/api/plugins/haproxy.html>`_

**HAproxy Docs**: `<https://www.haproxy.com/documentation/haproxy-configuration-tutorials/performance/performance-tuning/>`_

These modules manage HAProxy system performance, CPU affinity, and maintenance tasks.

----

.. _haproxy_cpu:

ansibleguy.opnsense.haproxy_cpu
================================

Manages CPU affinity rules for HAProxy processes to optimize performance.

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "name","string","true","\-","\-","Choose a name for this CPU affinity rule (must be unique)"
    "thread_id","string","false","\-","\-","Thread ID that should bind to a specific CPU set. Values: all, odd, even, x1, x2, x3, etc."
    "cpu_id","list","false","\-","\-","Bind the process/thread ID to this CPU. Values: all, odd, even, x0, x1, x2, etc."
    "enabled","boolean","false","true","\-","Enable this CPU affinity rule"

Examples
--------

.. code-block:: yaml

    - name: Create CPU affinity rule for single thread
      ansibleguy.opnsense.haproxy_cpu:
        name: 'web_threads'
        thread_id: 'x1'
        cpu_id: ['x0', 'x1']
        enabled: true

    - name: Bind all threads to all CPUs
      ansibleguy.opnsense.haproxy_cpu:
        name: 'all_cpus'
        thread_id: 'all'
        cpu_id: ['all']
        enabled: true

    - name: Bind odd threads to odd CPUs
      ansibleguy.opnsense.haproxy_cpu:
        name: 'odd_affinity'
        thread_id: 'odd'
        cpu_id: ['odd']
        enabled: true

    - name: Bind specific thread to specific CPUs
      ansibleguy.opnsense.haproxy_cpu:
        name: 'dedicated_thread'
        thread_id: 'x0'
        cpu_id: ['x0', 'x4']  # Thread 0 can run on CPU 0 or 4
        enabled: true

----

.. _haproxy_maintenance:

ansibleguy.opnsense.haproxy_maintenance
========================================

Manages HAProxy maintenance tasks and automated operations.

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "sync_certs","boolean","false","false","\-","Enable automatic certificate synchronization"
    "sync_certs_cron","string","false","\-","\-","Certificate sync cron schedule (e.g., '0 2 * * *')"
    "update_ocsp","boolean","false","false","\-","Enable automatic OCSP response updates"
    "update_ocsp_cron","string","false","\-","\-","OCSP update cron schedule (e.g., '0 3 * * *')"
    "reload_service","boolean","false","false","\-","Enable automatic service reload"
    "reload_service_cron","string","false","\-","\-","Service reload cron schedule (e.g., '0 4 * * 0')"
    "restart_service","boolean","false","false","\-","Enable automatic service restart"
    "restart_service_cron","string","false","\-","\-","Service restart cron schedule (e.g., '0 5 * * 0')"

Examples
--------

.. code-block:: yaml

    - name: Configure HAProxy maintenance with daily certificate sync
      ansibleguy.opnsense.haproxy_maintenance:
        sync_certs: true
        sync_certs_cron: '0 2 * * *'  # Daily at 2 AM
        update_ocsp: true
        update_ocsp_cron: '*/30 * * * *'  # Every 30 minutes

    - name: Setup weekly service reload
      ansibleguy.opnsense.haproxy_maintenance:
        reload_service: true
        reload_service_cron: '0 4 * * 0'  # Sunday at 4 AM

    - name: Complete maintenance configuration
      ansibleguy.opnsense.haproxy_maintenance:
        sync_certs: true
        sync_certs_cron: '0 2 * * *'
        update_ocsp: true
        update_ocsp_cron: '0 */4 * * *'  # Every 4 hours
        reload_service: true
        reload_service_cron: '0 3 * * 1'  # Monday at 3 AM
        restart_service: true
        restart_service_cron: '0 5 1 * *'  # First day of month at 5 AM

----

Performance optimization scenarios
***********************************

High-performance setup
----------------------

Configure HAProxy for high-performance environments:

.. code-block:: yaml

    - name: High-performance HAProxy configuration
      hosts: opnsense
      vars:
        cpu_count: 8
      tasks:
        # Configure CPU affinity for optimal performance
        - name: Bind thread pairs to CPU pairs
          ansibleguy.opnsense.haproxy_cpu:
            name: "thread_pair_{{ item }}"
            thread_id: "x{{ item }}"
            cpu_id: ["x{{ item }}", "x{{ item + 4 }}"]
            enabled: true
          loop: "{{ range(0, 4) | list }}"

        # Setup maintenance for high availability
        - name: Configure maintenance tasks
          ansibleguy.opnsense.haproxy_maintenance:
            sync_certs: true
            sync_certs_cron: '*/15 * * * *'  # Every 15 minutes
            update_ocsp: true
            update_ocsp_cron: '*/10 * * * *'  # Every 10 minutes
            reload_service: true
            reload_service_cron: '0 */6 * * *'  # Every 6 hours

NUMA-aware configuration
------------------------

Configure CPU affinity for NUMA systems:

.. code-block:: yaml

    - name: NUMA-aware CPU affinity
      hosts: opnsense
      tasks:
        # Node 0 CPUs: 0-7
        - name: Bind threads 0-3 to NUMA node 0
          ansibleguy.opnsense.haproxy_cpu:
            name: "numa0_thread_{{ item }}"
            thread_id: "x{{ item }}"
            cpu_id: "{{ ['x%d' | format(i) for i in range(0, 8)] }}"
            enabled: true
          loop: "{{ range(0, 4) | list }}"

        # Node 1 CPUs: 8-15
        - name: Bind threads 4-7 to NUMA node 1
          ansibleguy.opnsense.haproxy_cpu:
            name: "numa1_thread_{{ item }}"
            thread_id: "x{{ item }}"
            cpu_id: "{{ ['x%d' | format(i) for i in range(8, 16)] }}"
            enabled: true
          loop: "{{ range(4, 8) | list }}"

Energy-efficient setup
----------------------

Configure for energy efficiency with lower performance requirements:

.. code-block:: yaml

    - name: Energy-efficient configuration
      hosts: opnsense
      tasks:
        # Use fewer CPUs for HAProxy
        - name: Limit HAProxy to efficiency cores
          ansibleguy.opnsense.haproxy_cpu:
            name: 'efficiency_cores'
            thread_id: 'all'
            cpu_id: ['x0', 'x1']  # Only use first 2 cores
            enabled: true

        # Less frequent maintenance tasks
        - name: Configure low-frequency maintenance
          ansibleguy.opnsense.haproxy_maintenance:
            sync_certs: true
            sync_certs_cron: '0 3 * * *'  # Once daily at 3 AM
            update_ocsp: true
            update_ocsp_cron: '0 */12 * * *'  # Twice daily
            reload_service: false  # No automatic reloads
            restart_service: false  # No automatic restarts

----

Maintenance strategies
**********************

Certificate management
----------------------

Automated certificate synchronization and OCSP updates:

.. code-block:: yaml

    - name: Certificate automation
      hosts: opnsense
      tasks:
        - name: Setup certificate maintenance
          ansibleguy.opnsense.haproxy_maintenance:
            sync_certs: true
            sync_certs_cron: '0 1,13 * * *'  # Twice daily at 1 AM and 1 PM
            update_ocsp: true
            update_ocsp_cron: '*/20 * * * *'  # Every 20 minutes for fresh OCSP

        - name: Weekend certificate refresh
          ansibleguy.opnsense.haproxy_maintenance:
            sync_certs: true
            sync_certs_cron: '0 2 * * 6'  # Saturday at 2 AM
            update_ocsp: true
            update_ocsp_cron: '0 3 * * 6'  # Saturday at 3 AM

Service lifecycle management
-----------------------------

.. code-block:: yaml

    - name: Service lifecycle management
      hosts: opnsense
      vars:
        maintenance_window: '2-5'  # 2 AM to 5 AM
      tasks:
        # Daily reload during maintenance window
        - name: Daily service reload
          ansibleguy.opnsense.haproxy_maintenance:
            reload_service: true
            reload_service_cron: '0 3 * * *'  # 3 AM daily

        # Weekly restart for cleanup
        - name: Weekly service restart
          ansibleguy.opnsense.haproxy_maintenance:
            restart_service: true
            restart_service_cron: '0 4 * * 0'  # Sunday at 4 AM

        # Monthly full maintenance
        - name: Monthly full maintenance
          ansibleguy.opnsense.haproxy_maintenance:
            sync_certs: true
            sync_certs_cron: '0 2 1 * *'  # First of month at 2 AM
            update_ocsp: true
            update_ocsp_cron: '30 2 1 * *'  # First of month at 2:30 AM
            restart_service: true
            restart_service_cron: '0 3 1 * *'  # First of month at 3 AM

----

Best practices
**************

CPU affinity guidelines
-----------------------

**Thread-to-CPU ratio**

- For best performance: 1 thread per physical CPU core
- Avoid oversubscription unless necessary
- Consider hyperthreading when mapping threads

**NUMA considerations**

- Keep threads on the same NUMA node as their memory
- Avoid cross-NUMA node communication
- Test different configurations for your workload

.. code-block:: yaml

    - name: Optimal CPU affinity for 16-core system
      hosts: opnsense
      tasks:
        - name: Configure 8 HAProxy threads on 16 cores
          ansibleguy.opnsense.haproxy_cpu:
            name: "optimal_thread_{{ item }}"
            thread_id: "x{{ item }}"
            cpu_id: ["x{{ item * 2 }}", "x{{ item * 2 + 1 }}"]  # 2 CPUs per thread
            enabled: true
          loop: "{{ range(0, 8) | list }}"

Maintenance scheduling
----------------------

**Cron best practices**

- Avoid scheduling all tasks at the same time
- Use different minutes to spread load
- Consider time zones for global deployments
- Test cron expressions before deployment

.. code-block:: yaml

    - name: Staggered maintenance schedule
      hosts: opnsense
      tasks:
        - name: Configure staggered maintenance
          ansibleguy.opnsense.haproxy_maintenance:
            sync_certs: true
            sync_certs_cron: '15 2 * * *'  # 2:15 AM
            update_ocsp: true
            update_ocsp_cron: '30 2 * * *'  # 2:30 AM
            reload_service: true
            reload_service_cron: '45 2 * * *'  # 2:45 AM

**Maintenance windows**

- Schedule restarts during low-traffic periods
- Coordinate with change management
- Monitor service availability after maintenance
- Keep maintenance logs for troubleshooting

----

Monitoring and validation
*************************

CPU affinity validation
-----------------------

.. code-block:: yaml

    - name: Validate CPU affinity configuration
      hosts: opnsense
      tasks:
        - name: Check HAProxy process affinity
          ansible.builtin.shell: |
            taskset -pc $(pidof haproxy) 2>/dev/null || echo "HAProxy not running"
          register: cpu_affinity
          changed_when: false

        - name: Display CPU affinity
          debug:
            msg: "HAProxy CPU affinity: {{ cpu_affinity.stdout }}"

        - name: Check thread count
          ansible.builtin.shell: |
            ps -eLf | grep haproxy | grep -v grep | wc -l
          register: thread_count
          changed_when: false

        - name: Display thread count
          debug:
            msg: "HAProxy threads: {{ thread_count.stdout }}"

Maintenance task monitoring
---------------------------

.. code-block:: yaml

    - name: Monitor maintenance tasks
      hosts: opnsense
      tasks:
        - name: Check cron jobs for HAProxy
          ansible.builtin.shell: |
            crontab -l | grep haproxy || echo "No HAProxy cron jobs"
          register: cron_jobs
          changed_when: false

        - name: Display maintenance schedule
          debug:
            msg: "HAProxy maintenance tasks: {{ cron_jobs.stdout_lines }}"

        - name: Check last certificate sync
          ansible.builtin.stat:
            path: /var/log/haproxy/cert_sync.log
          register: cert_sync_log

        - name: Display last sync time
          debug:
            msg: "Last cert sync: {{ cert_sync_log.stat.mtime | default('Never') }}"

----

Troubleshooting
***************

CPU affinity issues
-------------------

**Common problems**

- **Invalid CPU ID**: Ensure CPU IDs don't exceed available cores
- **Thread ID mismatch**: Thread IDs should match configured nbthread
- **Performance degradation**: May indicate poor affinity choices

**Debugging steps**

1. Check available CPUs:

   .. code-block:: bash

       nproc
       lscpu

2. Verify HAProxy thread configuration
3. Monitor CPU usage per core
4. Test different affinity configurations

Maintenance task failures
-------------------------

**Certificate sync issues**

- Check network connectivity
- Verify certificate paths
- Review HAProxy logs
- Ensure proper permissions

**OCSP update problems**

- Verify OCSP responder availability
- Check certificate validity
- Review firewall rules
- Monitor OCSP response times

**Service reload/restart failures**

- Check HAProxy configuration validity
- Review system logs
- Verify resource availability
- Test manual reload/restart

.. code-block:: yaml

    - name: Troubleshoot maintenance issues
      hosts: opnsense
      tasks:
        - name: Test HAProxy configuration
          ansible.builtin.shell: |
            haproxy -c -f /usr/local/etc/haproxy/haproxy.conf
          register: config_check
          failed_when: config_check.rc != 0

        - name: Check HAProxy service status
          ansible.builtin.service:
            name: haproxy
            state: started
          check_mode: yes
          register: service_status

        - name: Display service status
          debug:
            var: service_status

See also: :ref:`troubleshooting <troubleshooting>`