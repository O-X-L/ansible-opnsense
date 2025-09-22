.. _modules_haproxy:

.. include:: ../_include/head.rst

=======
HAProxy
=======

**STATE**: unstable

**COMPATIBILITY**: OPNsense 24.1+

**Note**: Most functions should work on earlier OPNsense versions, but full compatibility is tested with OPNsense 24.1+. For compatibility with earlier versions, please check the configuration differences at: `HAProxy Configuration Reference <https://github.com/opnsense/plugins/blob/master/net/haproxy/src/opnsense/mvc/app/models/OPNsense/HAProxy/HAProxy.xml>`_

**TESTS**: `User <https://github.com/O-X-L/ansible_opnsense/blob/latest/tests/haproxy_user.yml>`_ |
`Group <https://github.com/O-X-L/ansible_opnsense/blob/latest/tests/haproxy_group.yml>`_ |
`CPU <https://github.com/O-X-L/ansible_opnsense/blob/latest/tests/haproxy_cpu.yml>`_ |
`Maintenance <https://github.com/O-X-L/ansible_opnsense/blob/latest/tests/haproxy_maintenance.yml>`_ |
`General Settings <https://github.com/O-X-L/ansible_opnsense/blob/latest/tests/haproxy_general_settings.yml>`_ |
`General Stats <https://github.com/O-X-L/ansible_opnsense/blob/latest/tests/haproxy_general_stats.yml>`_ |
`General Defaults <https://github.com/O-X-L/ansible_opnsense/blob/latest/tests/haproxy_general_defaults.yml>`_ |
`General Tuning <https://github.com/O-X-L/ansible_opnsense/blob/latest/tests/haproxy_general_tuning.yml>`_ |
`General Logging <https://github.com/O-X-L/ansible_opnsense/blob/latest/tests/haproxy_general_logging.yml>`_ |
`General Peers <https://github.com/O-X-L/ansible_opnsense/blob/latest/tests/haproxy_general_peers.yml>`_ |
`General Cache <https://github.com/O-X-L/ansible_opnsense/blob/latest/tests/haproxy_general_cache.yml>`_

**API Docs**: `HAProxy <https://docs.opnsense.org/development/api/plugins/haproxy.html>`_

These modules allow you to manage HAProxy load balancer configuration on OPNsense.

Contribution
************

Thanks to `@MaximeWewer <https://github.com/MaximeWewer>`_ for developing this module!

If you encounter any issues or have suggestions for improvements, please feel free to contribute to the project.

----

Info
****

HAProxy is a powerful load balancer and proxy server that provides high availability, load balancing, and proxying for TCP and HTTP-based applications.

Prerequisites
*************

You need to install the following plugin:

.. code-block:: bash

    os-haproxy

You can also install it using the :ref:`ansibleguy.opnsense.package <modules_package>` module.

Function
********

All HAProxy modules support these **default** options:

.. include:: ../_include/param_basic.rst

----

Modules Overview
****************

The HAProxy functionality is split into multiple modules organized by function:

**Authentication & Access Control:**

- :ref:`haproxy_user <haproxy_user>` - Manage HAProxy authentication users
- :ref:`haproxy_group <haproxy_group>` - Manage HAProxy authentication groups

**Performance & System:**

- :ref:`haproxy_cpu <haproxy_cpu>` - Manage CPU affinity rules for HAProxy processes
- :ref:`haproxy_maintenance <haproxy_maintenance>` - Manage HAProxy maintenance and monitoring settings

**General Configuration:**

- :ref:`haproxy_general_settings <haproxy_general_settings>` - Manage general HAProxy configuration
- :ref:`haproxy_general_stats <haproxy_general_stats>` - Manage HAProxy statistics and monitoring (with automatic name-to-UUID resolution)
- :ref:`haproxy_general_defaults <haproxy_general_defaults>` - Manage HAProxy default settings
- :ref:`haproxy_general_tuning <haproxy_general_tuning>` - Manage HAProxy performance tuning
- :ref:`haproxy_general_logging <haproxy_general_logging>` - Manage HAProxy logging configuration
- :ref:`haproxy_general_peers <haproxy_general_peers>` - Manage HAProxy peer synchronization
- :ref:`haproxy_general_cache <haproxy_general_cache>` - Manage HAProxy caching configuration

----

Authentication & Access Control
********************************

.. _haproxy_user:

ansibleguy.opnsense.haproxy_user
=================================

Manages HAProxy authentication users for access control.

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "name","string","true","\-","\-","Choose a name for this user (must be unique)"
    "description","string","false","\-","\-","You may enter a description here for your reference"
    "password","string","true","\-","\-","Password for this user (stored securely)"
    "enabled","boolean","false","true","\-","Enable this user"

.. code-block:: yaml

    - name: Create HAProxy user
      ansibleguy.opnsense.haproxy_user:
        name: 'web_admin'
        description: 'Web administration user'
        password: 'secure_password123'
        enabled: true

.. _haproxy_group:

ansibleguy.opnsense.haproxy_group
==================================

Manages HAProxy authentication groups for organizing users.

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "name","string","true","\-","\-","Choose a name for this group (must be unique)"
    "description","string","false","\-","\-","You may enter a description here for your reference"
    "members","list","false","[]","\-","List of user names that are members of this group"
    "add_userlist","boolean","false","false","\-","Add this group to the userlist"
    "enabled","boolean","false","true","\-","Enable this group"

.. code-block:: yaml

    - name: Create HAProxy group
      ansibleguy.opnsense.haproxy_group:
        name: 'administrators'
        description: 'Admin group for HAProxy'
        members: ['admin_user1', 'admin_user2']
        add_userlist: true
        enabled: true

----

Performance & System
*********************

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

.. code-block:: yaml

    - name: Create CPU affinity rule
      ansibleguy.opnsense.haproxy_cpu:
        name: 'web_threads'
        thread_id: 'x1'
        cpu_id: ['x0', 'x1']
        enabled: true

.. _haproxy_maintenance:

ansibleguy.opnsense.haproxy_maintenance
========================================

Manages HAProxy maintenance and automated tasks.

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

.. code-block:: yaml

    - name: Configure HAProxy maintenance
      ansibleguy.opnsense.haproxy_maintenance:
        sync_certs: true
        sync_certs_cron: '0 2 * * *'
        update_ocsp: true
        update_ocsp_cron: '*/30 * * * *'

----

General Configuration
**********************

.. _haproxy_general_settings:

ansibleguy.opnsense.haproxy_general_settings
==============================================

Manages the basic operational settings for HAProxy.

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "graceful_stop","boolean","false","true","\-","Enable graceful stop mode which handles existing connections before stopping"
    "hard_stop_after","integer","false","\-","\-","Maximum time in seconds for a graceful stop, after which HAProxy terminates all connections"
    "close_spread_time","integer","false","\-","\-","Time window in seconds to spread connection closing during graceful shutdown"
    "seamless_reload","boolean","false","false","\-","Handle restarts without losing connections"
    "show_intro","boolean","false","true","\-","Show/hide introduction pages"

.. code-block:: yaml

    - name: Configure HAProxy general settings
      ansibleguy.opnsense.haproxy_general_settings:
        enabled: true
        graceful_stop: true
        hard_stop_after: 60
        seamless_reload: true

.. _haproxy_general_stats:

ansibleguy.opnsense.haproxy_general_stats
==========================================

Manages HAProxy statistics and monitoring configuration. **Special Feature**: Automatic name-to-UUID resolution for users and groups.

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "port","integer","false","8822","\-","Choose a TCP port to be used for the local statistics page"
    "remote_enabled","boolean","false","false","\-","Enable remote access to HAProxy statistics page"
    "remote_bind","list","false","[]","\-","Configure listen addresses for the statistics page"
    "auth_enabled","boolean","false","false","\-","Enable authentication"
    "users","list","false","[]","\-","Allowed users in format user:password"
    "allowed_users","list","false","[]","\-","List of user names that are allowed to access the statistics page. User names will be automatically resolved to UUIDs"
    "allowed_groups","list","false","[]","\-","List of group names that are allowed to access the statistics page. Group names will be automatically resolved to UUIDs"
    "custom_options","string","false","\-","\-","These lines will be added to the statistics settings of the HAProxy configuration file"
    "prometheus_enabled","boolean","false","false","\-","Enable HAProxy Prometheus exporter"
    "prometheus_bind","list","false","['*:8404']","\-","Configure listen addresses for the prometheus exporter"
    "prometheus_path","string","false","'/metrics'","\-","The path where the Prometheus exporter can be accessed"

.. code-block:: yaml

    - name: Configure HAProxy statistics with name resolution
      ansibleguy.opnsense.haproxy_general_stats:
        enabled: true
        port: 8822
        auth_enabled: true
        allowed_users: ['admin_user', 'monitor_user']  # Names resolved to UUIDs automatically
        allowed_groups: ['administrators', 'monitoring']  # Names resolved to UUIDs automatically
        prometheus_enabled: true

.. _haproxy_general_defaults:

ansibleguy.opnsense.haproxy_general_defaults
=============================================

Manages HAProxy default connection and timeout settings.

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "max_connections","integer","false","\-","\-","Maximum connections per frontend/backend"
    "max_connections_servers","integer","false","\-","\-","Maximum connections per server"
    "timeout_client","string","false","30s","\-","Client timeout"
    "timeout_connect","string","false","30s","\-","Connect timeout"
    "timeout_check","string","false","\-","\-","Health check timeout"
    "timeout_server","string","false","30s","\-","Server timeout"
    "retries","integer","false","3","\-","Number of retries"
    "redispatch","string","false","\-","\-","Redispatch policy"
    "custom_options","string","false","\-","\-","Additional configuration lines"

.. _haproxy_general_tuning:

ansibleguy.opnsense.haproxy_general_tuning
===========================================

Manages HAProxy performance tuning parameters.

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "max_connections","integer","false","\-","\-","Maximum global connections"
    "nbthread","integer","false","1","\-","Number of threads"
    "max_dh_size","integer","false","2048","\-","Maximum DH key size"
    "buffer_size","integer","false","16384","\-","Buffer size"
    "spread_checks","integer","false","2","\-","Spread health checks"
    "lua_max_mem","integer","false","0","\-","Lua maximum memory (MB)"
    "custom_options","string","false","\-","\-","Additional tuning options"

.. _haproxy_general_logging:

ansibleguy.opnsense.haproxy_general_logging
============================================

Manages HAProxy logging configuration.

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "host","string","false","127.0.0.1","\-","Syslog server host"
    "facility","string","false","local0","\-","Syslog facility (local0-local7, mail, daemon, etc.)"
    "level","string","false","info","\-","Log level (emerg, alert, crit, err, warning, notice, info, debug)"
    "length","string","false","\-","\-","Log message length"

.. _haproxy_general_peers:

ansibleguy.opnsense.haproxy_general_peers
==========================================

Manages HAProxy peer synchronization for clustering.

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "name1","string","false","\-","\-","First peer name"
    "listen1","string","false","\-","\-","First peer listen address"
    "port1","integer","false","1024","\-","First peer port"
    "name2","string","false","\-","\-","Second peer name"
    "listen2","string","false","\-","\-","Second peer listen address"
    "port2","integer","false","1024","\-","Second peer port"

.. _haproxy_general_cache:

ansibleguy.opnsense.haproxy_general_cache
==========================================

Manages HAProxy caching configuration.

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "total_max_size","integer","false","4","\-","Total maximum cache size (MB)"
    "max_age","integer","false","60","\-","Maximum age for cached objects (seconds)"
    "max_object_size","integer","false","\-","\-","Maximum size of a single cached object (bytes)"
    "process_vary","boolean","false","false","\-","Process Vary header for cache decisions"
    "max_secondary_entries","integer","false","10","\-","Maximum secondary entries per cache key"

----

Usage Examples
***************

Complete HAProxy setup with authentication and monitoring:

.. code-block:: yaml

    - name: Complete HAProxy configuration
      hosts: opnsense_firewalls
      tasks:
        # Create authentication users
        - name: Create HAProxy users
          ansibleguy.opnsense.haproxy_user:
            name: "{{ item.name }}"
            description: "{{ item.description }}"
            password: "{{ item.password }}"
            enabled: true
          loop:
            - {name: 'admin', description: 'Administrator', password: '{{ vault_admin_pass }}'}
            - {name: 'monitor', description: 'Monitor user', password: '{{ vault_monitor_pass }}'}

        # Create groups
        - name: Create HAProxy groups
          ansibleguy.opnsense.haproxy_group:
            name: "{{ item.name }}"
            description: "{{ item.description }}"
            members: "{{ item.members }}"
            enabled: true
          loop:
            - {name: 'admins', description: 'Administrators', members: ['admin']}
            - {name: 'monitors', description: 'Monitoring users', members: ['monitor']}

        # Configure basic settings
        - name: Configure HAProxy general settings
          ansibleguy.opnsense.haproxy_general_settings:
            enabled: true
            graceful_stop: true
            hard_stop_after: 60
            seamless_reload: true

        # Configure monitoring with name resolution
        - name: Configure HAProxy statistics
          ansibleguy.opnsense.haproxy_general_stats:
            enabled: true
            port: 8822
            auth_enabled: true
            allowed_users: ['admin']      # Automatically resolved to UUID
            allowed_groups: ['admins']    # Automatically resolved to UUID
            prometheus_enabled: true

        # Configure performance
        - name: Configure HAProxy performance tuning
          ansibleguy.opnsense.haproxy_general_tuning:
            enabled: true
            max_connections: 2000
            nbthread: 4
            buffer_size: 32768

        # Configure CPU affinity
        - name: Configure HAProxy CPU affinity
          ansibleguy.opnsense.haproxy_cpu:
            name: 'web_threads'
            thread_id: 'x1'
            cpu_id: ['x0', 'x1']
            enabled: true

        # Configure maintenance
        - name: Configure HAProxy maintenance
          ansibleguy.opnsense.haproxy_maintenance:
            sync_certs: true
            sync_certs_cron: '0 2 * * *'
            update_ocsp: true
            update_ocsp_cron: '*/30 * * * *'

----

Troubleshooting
***************

**Name Resolution in Stats Module**

The HAProxy stats module automatically resolves user and group names to UUIDs. If you encounter errors like "User 'username' not found", ensure:

1. The user/group exists in HAProxy configuration
2. The name spelling is exact (case-sensitive)
3. The user/group is enabled

**CPU Affinity Configuration**

- Use string values for thread_id and cpu_id (e.g., 'x1', 'x0')
- Ensure CPU IDs don't exceed available CPU cores
- Thread IDs should not exceed the configured nbthread value

**Performance Tuning**

For high-traffic scenarios:

- Increase ``max_connections`` in tuning
- Use multiple ``nbthread`` (typically number of CPU cores)
- Increase ``buffer_size`` for large requests/responses
- Adjust ``timeout_*`` values based on your application needs

See: :ref:`troubleshooting <troubleshooting>`