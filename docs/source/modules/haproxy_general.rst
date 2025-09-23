.. _modules_haproxy_general:

.. include:: ../_include/head.rst

=============================
HAProxy general configuration
=============================

**STATE**: unstable

**COMPATIBILITY**: OPNsense 24.1+

**TESTS**: 
`General Settings <https://github.com/O-X-L/ansible_opnsense/blob/latest/tests/haproxy_general_settings.yml>`_ |
`General Stats <https://github.com/O-X-L/ansible_opnsense/blob/latest/tests/haproxy_general_stats.yml>`_ |
`General Defaults <https://github.com/O-X-L/ansible_opnsense/blob/latest/tests/haproxy_general_defaults.yml>`_ |
`General Tuning <https://github.com/O-X-L/ansible_opnsense/blob/latest/tests/haproxy_general_tuning.yml>`_ |
`General Logging <https://github.com/O-X-L/ansible_opnsense/blob/latest/tests/haproxy_general_logging.yml>`_ |
`General Peers <https://github.com/O-X-L/ansible_opnsense/blob/latest/tests/haproxy_general_peers.yml>`_ |
`General Cache <https://github.com/O-X-L/ansible_opnsense/blob/latest/tests/haproxy_general_cache.yml>`_

**API Docs**: `HAProxy <https://docs.opnsense.org/development/api/plugins/haproxy.html>`_

These modules manage the general HAProxy configuration including settings, statistics, defaults, tuning, logging, peers, and caching.

----

.. _haproxy_general_settings:

ansibleguy.opnsense.haproxy_general_settings
==============================================

Manages the basic operational settings for HAProxy.

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "enabled","boolean","false","true","\-","Enable or disable HAProxy service"
    "graceful_stop","boolean","false","true","\-","Enable graceful stop mode which handles existing connections before stopping"
    "hard_stop_after","integer","false","\-","\-","Maximum time in seconds for a graceful stop, after which HAProxy terminates all connections"
    "close_spread_time","integer","false","\-","\-","Time window in seconds to spread connection closing during graceful shutdown"
    "seamless_reload","boolean","false","false","\-","Handle restarts without losing connections"
    "show_intro","boolean","false","true","\-","Show/hide introduction pages"

Examples
--------

.. code-block:: yaml

    - name: Configure HAProxy general settings
      ansibleguy.opnsense.haproxy_general_settings:
        enabled: true
        graceful_stop: true
        hard_stop_after: 60
        seamless_reload: true

    - name: Configure for zero-downtime deployments
      ansibleguy.opnsense.haproxy_general_settings:
        enabled: true
        graceful_stop: true
        hard_stop_after: 120
        close_spread_time: 30
        seamless_reload: true

----

.. _haproxy_general_stats:

ansibleguy.opnsense.haproxy_general_stats
==========================================

Manages HAProxy statistics and monitoring configuration. **Special Feature**: Automatic name-to-UUID resolution for users and groups.

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "enabled","boolean","false","true","\-","Enable statistics module"
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

Examples
--------

.. code-block:: yaml

    - name: Configure HAProxy statistics with name resolution
      ansibleguy.opnsense.haproxy_general_stats:
        enabled: true
        port: 8822
        auth_enabled: true
        allowed_users: ['admin_user', 'monitor_user']  # Names resolved to UUIDs automatically
        allowed_groups: ['administrators', 'monitoring']  # Names resolved to UUIDs automatically
        prometheus_enabled: true

    - name: Configure remote statistics access
      ansibleguy.opnsense.haproxy_general_stats:
        enabled: true
        port: 8822
        remote_enabled: true
        remote_bind:
          - '192.168.1.10:8822'
          - '[::1]:8822'
        auth_enabled: true
        users:
          - 'stats:password123'
        prometheus_enabled: true
        prometheus_bind:
          - '0.0.0.0:8404'
        prometheus_path: '/metrics'

----

.. _haproxy_general_defaults:

ansibleguy.opnsense.haproxy_general_defaults
=============================================

Manages HAProxy default connection and timeout settings.

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "enabled","boolean","false","true","\-","Enable defaults configuration"
    "max_connections","integer","false","\-","\-","Maximum connections per frontend/backend"
    "max_connections_servers","integer","false","\-","\-","Maximum connections per server"
    "timeout_client","string","false","30s","\-","Client timeout"
    "timeout_connect","string","false","30s","\-","Connect timeout"
    "timeout_check","string","false","\-","\-","Health check timeout"
    "timeout_server","string","false","30s","\-","Server timeout"
    "retries","integer","false","3","\-","Number of retries"
    "redispatch","string","false","\-","\-","Redispatch policy"
    "custom_options","string","false","\-","\-","Additional configuration lines"

Examples
--------

.. code-block:: yaml

    - name: Configure HAProxy defaults for web services
      ansibleguy.opnsense.haproxy_general_defaults:
        enabled: true
        max_connections: 1000
        max_connections_servers: 100
        timeout_client: '60s'
        timeout_connect: '10s'
        timeout_server: '60s'
        retries: 3
        redispatch: 'enabled'

    - name: Configure defaults for API services
      ansibleguy.opnsense.haproxy_general_defaults:
        enabled: true
        max_connections: 2000
        timeout_client: '30s'
        timeout_connect: '5s'
        timeout_server: '30s'
        timeout_check: '10s'
        retries: 2

----

.. _haproxy_general_tuning:

ansibleguy.opnsense.haproxy_general_tuning
===========================================

Manages HAProxy performance tuning parameters.

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "enabled","boolean","false","true","\-","Enable tuning configuration"
    "max_connections","integer","false","\-","\-","Maximum global connections"
    "nbthread","integer","false","1","\-","Number of threads"
    "max_dh_size","integer","false","2048","\-","Maximum DH key size"
    "buffer_size","integer","false","16384","\-","Buffer size"
    "spread_checks","integer","false","2","\-","Spread health checks"
    "lua_max_mem","integer","false","0","\-","Lua maximum memory (MB)"
    "custom_options","string","false","\-","\-","Additional tuning options"

Examples
--------

.. code-block:: yaml

    - name: Configure HAProxy performance tuning
      ansibleguy.opnsense.haproxy_general_tuning:
        enabled: true
        max_connections: 2000
        nbthread: 4
        buffer_size: 32768
        spread_checks: 5

    - name: High-performance tuning configuration
      ansibleguy.opnsense.haproxy_general_tuning:
        enabled: true
        max_connections: 10000
        nbthread: 8
        max_dh_size: 4096
        buffer_size: 65536
        lua_max_mem: 512

----

.. _haproxy_general_logging:

ansibleguy.opnsense.haproxy_general_logging
============================================

Manages HAProxy logging configuration.

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "enabled","boolean","false","true","\-","Enable logging configuration"
    "host","string","false","127.0.0.1","\-","Syslog server host"
    "facility","string","false","local0","\-","Syslog facility (local0-local7, mail, daemon, etc.)"
    "level","string","false","info","\-","Log level (emerg, alert, crit, err, warning, notice, info, debug)"
    "length","string","false","\-","\-","Log message length"

Examples
--------

.. code-block:: yaml

    - name: Configure HAProxy logging
      ansibleguy.opnsense.haproxy_general_logging:
        enabled: true
        host: '127.0.0.1'
        facility: 'local0'
        level: 'info'

    - name: Configure remote syslog
      ansibleguy.opnsense.haproxy_general_logging:
        enabled: true
        host: '192.168.1.100'
        facility: 'local1'
        level: 'notice'
        length: '4096'

----

.. _haproxy_general_peers:

ansibleguy.opnsense.haproxy_general_peers
==========================================

Manages HAProxy peer synchronization for clustering.

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "enabled","boolean","false","true","\-","Enable peer synchronization"
    "name1","string","false","\-","\-","First peer name"
    "listen1","string","false","\-","\-","First peer listen address"
    "port1","integer","false","1024","\-","First peer port"
    "name2","string","false","\-","\-","Second peer name"
    "listen2","string","false","\-","\-","Second peer listen address"
    "port2","integer","false","1024","\-","Second peer port"

Examples
--------

.. code-block:: yaml

    - name: Configure HAProxy peer synchronization
      ansibleguy.opnsense.haproxy_general_peers:
        enabled: true
        name1: 'haproxy1'
        listen1: '10.0.0.1'
        port1: 1024
        name2: 'haproxy2'
        listen2: '10.0.0.2'
        port2: 1024

----

.. _haproxy_general_cache:

ansibleguy.opnsense.haproxy_general_cache
==========================================

Manages HAProxy caching configuration.

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "enabled","boolean","false","true","\-","Enable caching"
    "total_max_size","integer","false","4","\-","Total maximum cache size (MB)"
    "max_age","integer","false","60","\-","Maximum age for cached objects (seconds)"
    "max_object_size","integer","false","\-","\-","Maximum size of a single cached object (bytes)"
    "process_vary","boolean","false","false","\-","Process Vary header for cache decisions"
    "max_secondary_entries","integer","false","10","\-","Maximum secondary entries per cache key"

Examples
--------

.. code-block:: yaml

    - name: Configure HAProxy caching
      ansibleguy.opnsense.haproxy_general_cache:
        enabled: true
        total_max_size: 64
        max_age: 3600
        max_object_size: 1048576
        process_vary: true
        max_secondary_entries: 20

----

Configuration scenarios
***********************

Complete general configuration
------------------------------

.. code-block:: yaml

    - name: Complete HAProxy general configuration
      hosts: opnsense
      tasks:
        - name: Configure general settings
          ansibleguy.opnsense.haproxy_general_settings:
            enabled: true
            graceful_stop: true
            hard_stop_after: 60
            seamless_reload: true

        - name: Configure statistics
          ansibleguy.opnsense.haproxy_general_stats:
            enabled: true
            port: 8822
            auth_enabled: true
            allowed_users: ['admin']
            prometheus_enabled: true

        - name: Configure defaults
          ansibleguy.opnsense.haproxy_general_defaults:
            enabled: true
            max_connections: 1000
            timeout_client: '30s'
            timeout_server: '30s'
            retries: 3

        - name: Configure tuning
          ansibleguy.opnsense.haproxy_general_tuning:
            enabled: true
            max_connections: 5000
            nbthread: 4
            buffer_size: 32768

        - name: Configure logging
          ansibleguy.opnsense.haproxy_general_logging:
            enabled: true
            host: '127.0.0.1'
            facility: 'local0'
            level: 'info'

        - name: Configure caching
          ansibleguy.opnsense.haproxy_general_cache:
            enabled: true
            total_max_size: 32
            max_age: 1800

High-availability configuration
--------------------------------

.. code-block:: yaml

    - name: Configure HAProxy for high availability
      hosts: opnsense
      tasks:
        - name: Configure HA settings
          ansibleguy.opnsense.haproxy_general_settings:
            enabled: true
            graceful_stop: true
            hard_stop_after: 120
            seamless_reload: true

        - name: Configure peer synchronization
          ansibleguy.opnsense.haproxy_general_peers:
            enabled: true
            name1: 'lb-primary'
            listen1: '{{ primary_ip }}'
            port1: 1024
            name2: 'lb-secondary'
            listen2: '{{ secondary_ip }}'
            port2: 1024

        - name: Configure HA defaults
          ansibleguy.opnsense.haproxy_general_defaults:
            enabled: true
            max_connections: 2000
            timeout_client: '60s'
            timeout_server: '60s'
            retries: 3
            redispatch: 'enabled'

Monitoring-focused configuration
---------------------------------

.. code-block:: yaml

    - name: Configure comprehensive monitoring
      hosts: opnsense
      tasks:
        - name: Configure statistics with authentication
          ansibleguy.opnsense.haproxy_general_stats:
            enabled: true
            port: 8822
            remote_enabled: true
            remote_bind:
              - '0.0.0.0:8822'
            auth_enabled: true
            allowed_users: ['monitoring_user']
            allowed_groups: ['monitoring_team']
            prometheus_enabled: true
            prometheus_bind:
              - '0.0.0.0:8404'
            prometheus_path: '/metrics'

        - name: Configure detailed logging
          ansibleguy.opnsense.haproxy_general_logging:
            enabled: true
            host: '{{ syslog_server }}'
            facility: 'local1'
            level: 'debug'
            length: '8192'

----

Best practices
**************

Statistics security
-------------------

- Always enable authentication for statistics
- Use strong passwords for stats users
- Limit remote access to specific IPs when possible
- Consider using separate users for human vs automated access

.. code-block:: yaml

    - name: Secure statistics configuration
      ansibleguy.opnsense.haproxy_general_stats:
        enabled: true
        port: 8822
        remote_enabled: true
        remote_bind:
          - '10.0.0.0/8:8822'  # Internal network only
        auth_enabled: true
        allowed_users: ['stats_admin']
        allowed_groups: ['monitoring']
        custom_options: |
          stats hide-version
          stats show-node

Performance optimization
------------------------

**Timeout configuration**

- Set appropriate timeouts based on application behavior
- Consider different timeouts for different service types
- Monitor timeout-related errors and adjust accordingly

.. code-block:: yaml

    - name: Optimized timeout configuration
      ansibleguy.opnsense.haproxy_general_defaults:
        enabled: true
        timeout_client: '{{ client_timeout | default("30s") }}'
        timeout_connect: '{{ connect_timeout | default("5s") }}'
        timeout_server: '{{ server_timeout | default("30s") }}'
        timeout_check: '{{ check_timeout | default("10s") }}'

**Buffer and thread tuning**

.. code-block:: yaml

    - name: Performance tuning based on system resources
      hosts: opnsense
      vars:
        cpu_cores: "{{ ansible_processor_cores }}"
      tasks:
        - name: Configure tuning
          ansibleguy.opnsense.haproxy_general_tuning:
            enabled: true
            max_connections: "{{ cpu_cores * 1000 }}"
            nbthread: "{{ cpu_cores }}"
            buffer_size: "{{ 16384 if cpu_cores <= 4 else 32768 }}"

Logging strategy
----------------

.. code-block:: yaml

    - name: Environment-specific logging
      hosts: opnsense
      tasks:
        - name: Production logging
          ansibleguy.opnsense.haproxy_general_logging:
            enabled: true
            host: '{{ syslog_host }}'
            facility: 'local0'
            level: 'warning'
          when: environment == 'production'

        - name: Development logging
          ansibleguy.opnsense.haproxy_general_logging:
            enabled: true
            host: '127.0.0.1'
            facility: 'local0'
            level: 'debug'
          when: environment == 'development'

Cache optimization
------------------

.. code-block:: yaml

    - name: Cache configuration for static content
      ansibleguy.opnsense.haproxy_general_cache:
        enabled: true
        total_max_size: 128  # 128MB for static assets
        max_age: 86400  # 24 hours
        max_object_size: 5242880  # 5MB max per object
        process_vary: true
        max_secondary_entries: 50

----

Integration examples
********************

Prometheus integration
----------------------

.. code-block:: yaml

    - name: Setup Prometheus monitoring
      hosts: opnsense
      tasks:
        - name: Configure HAProxy Prometheus exporter
          ansibleguy.opnsense.haproxy_general_stats:
            enabled: true
            prometheus_enabled: true
            prometheus_bind:
              - '{{ ansible_default_ipv4.address }}:8404'
            prometheus_path: '/metrics'

        - name: Configure Prometheus scrape config
          template:
            src: prometheus_haproxy.yml.j2
            dest: /etc/prometheus/targets/haproxy.yml
          delegate_to: prometheus_server

Centralized logging
-------------------

.. code-block:: yaml

    - name: Configure centralized logging
      hosts: opnsense
      vars:
        rsyslog_server: '192.168.100.50'
      tasks:
        - name: Configure HAProxy logging to rsyslog
          ansibleguy.opnsense.haproxy_general_logging:
            enabled: true
            host: '{{ rsyslog_server }}'
            facility: 'local1'
            level: 'info'

        - name: Configure rsyslog forwarding
          lineinfile:
            path: /etc/rsyslog.conf
            line: 'local1.*  @@{{ rsyslog_server }}:514'
            create: yes

----

Troubleshooting
***************

Statistics access issues
------------------------

**Cannot access stats page**

1. Verify statistics are enabled
2. Check port availability
3. Verify firewall rules
4. Check authentication settings

.. code-block:: yaml

    - name: Diagnose statistics issues
      hosts: opnsense
      tasks:
        - name: Check stats port
          wait_for:
            port: 8822
            host: 127.0.0.1
            timeout: 5

        - name: Test stats authentication
          uri:
            url: http://127.0.0.1:8822/stats
            user: "{{ stats_user }}"
            password: "{{ stats_password }}"
          register: stats_test

**Name resolution failures**

If users/groups are not resolved:

- Verify exact spelling (case-sensitive)
- Ensure users/groups exist and are enabled
- Check for UUID conflicts

Performance issues
------------------

**High memory usage**

- Reduce buffer_size if memory-constrained
- Adjust max_connections
- Monitor cache usage

**Thread contention**

- Ensure nbthread matches CPU cores
- Check CPU affinity settings
- Monitor thread utilization

Logging problems
----------------

**Missing logs**

- Verify syslog daemon is running
- Check syslog configuration
- Ensure proper facilities are configured
- Review firewall rules for remote logging

.. code-block:: yaml

    - name: Validate logging configuration
      hosts: opnsense
      tasks:
        - name: Test local syslog
          shell: |
            logger -p local0.info "HAProxy test message"

        - name: Check syslog for test message
          shell: |
            tail -n 50 /var/log/messages | grep "HAProxy test message"
          register: log_test

        - name: Display result
          debug:
            msg: "Logging {{ 'working' if log_test.stdout else 'not working' }}"

See also: :ref:`troubleshooting <troubleshooting>`