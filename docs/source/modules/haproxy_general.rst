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

oxlorg.opnsense.haproxy_general_settings
==============================================

Manages the basic operational settings for HAProxy.

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "enabled","boolean","false","true","\-","Enable or disable HAProxy service"
    "graceful_stop","boolean","false","true","\-","Enable graceful stop mode which handles existing connections before stopping"
    "hard_stop_after","integer","false","\-","\-","Maximum time in seconds for a graceful stop, after which HAProxy terminates all connections (0-86400)"
    "close_spread_time","integer","false","\-","\-","Time window in seconds to spread connection closing during graceful shutdown (0-3600)"
    "seamless_reload","boolean","false","false","\-","Handle restarts without losing connections"
    "show_intro","boolean","false","true","\-","Show/hide introduction pages"

Examples
--------

.. code-block:: yaml

    - name: Configure HAProxy basic settings
      oxlorg.opnsense.haproxy_general_settings:
        enabled: true
        graceful_stop: true
        hard_stop_after: 60
        seamless_reload: true

----

.. _haproxy_general_stats:

oxlorg.opnsense.haproxy_general_stats
==========================================

Manages HAProxy statistics and monitoring configuration.

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "enabled","boolean","false","true","\-","Enable or disable HAProxy statistics"
    "port","integer","false","8822","\-","TCP port for local statistics page (1024-65535)"
    "remote_enabled","boolean","false","false","\-","Enable remote access to HAProxy statistics page"
    "remote_bind","list","false","[]","\-","Configure listen addresses for statistics page remote access"
    "auth_enabled","boolean","false","false","\-","Enable authentication"
    "users","list","false","[]","\-","Allowed users in format user:password"
    "allowed_users","list","false","[]","\-","List of user names allowed to access statistics page (automatically resolved to UUIDs)"
    "allowed_groups","list","false","[]","\-","List of group names allowed to access statistics page (automatically resolved to UUIDs)"
    "custom_options","string","false","\-","\-","Additional lines for HAProxy statistics settings"
    "prometheus_enabled","boolean","false","false","\-","Enable HAProxy Prometheus exporter"
    "prometheus_bind","list","false","['*:8404']","\-","Listen addresses for prometheus exporter"
    "prometheus_path","string","false","/metrics","\-","Path where Prometheus exporter can be accessed"

Examples
--------

.. code-block:: yaml

    - name: Configure HAProxy statistics with authentication
      oxlorg.opnsense.haproxy_general_stats:
        enabled: true
        port: 8822
        auth_enabled: true
        allowed_users: ['admin']
        allowed_groups: ['admins']
        prometheus_enabled: true

----

.. _haproxy_general_defaults:

oxlorg.opnsense.haproxy_general_defaults
=============================================

Manages HAProxy default connection and timeout settings.

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "max_connections","integer","false","\-","\-","Maximum number of concurrent connections for public services (0-10000000)"
    "max_connections_servers","integer","false","\-","\-","Maximum number of concurrent connections for servers (0-10000000)"
    "timeout_client","string","false","30s","\-","Maximum inactivity time on client side"
    "timeout_connect","string","false","30s","\-","Maximum time to wait for server connection attempt"
    "timeout_check","string","false","\-","\-","Additional read timeout for health checks"
    "timeout_server","string","false","30s","\-","Maximum inactivity time on server side"
    "retries","integer","false","3","\-","Number of retries on server connection failure (0-100)"
    "redispatch","string","false","x-1","\-","Enable session redistribution on connection failure (x3, x2, x1, x0, x-1, x-2, x-3)"
    "init_addr","list","false","['last', 'libc']","\-","Order for server address resolution on startup"
    "custom_options","string","false","\-","\-","Additional lines for HAProxy defaults settings"

Examples
--------

.. code-block:: yaml

    - name: Configure HAProxy connection defaults
      oxlorg.opnsense.haproxy_general_defaults:
        max_connections: 2000
        timeout_client: '30s'
        timeout_server: '30s'
        timeout_connect: '5s'
        retries: 3

----

.. _haproxy_general_tuning:

oxlorg.opnsense.haproxy_general_tuning
===========================================

Manages HAProxy performance tuning and advanced configuration.

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "root","boolean","false","false","\-","Enable HAProxy running as user root (strongly discouraged)"
    "max_connections","integer","false","\-","\-","Maximum concurrent connections per HAProxy process (0-10000000)"
    "nbthread","integer","false","1","\-","Number of threads per HAProxy process (1-1024)"
    "resolvers_prefer","string","false","ipv4","\-","Preferred IP family for DNS resolution (ipv4, ipv6)"
    "ssl_server_verify","string","false","ignore","\-","SSL verify behavior for servers (ignore, required, none)"
    "max_dh_size","integer","false","2048","\-","Maximum Diffie-Hellman parameters size (1024-16384)"
    "buffer_size","integer","false","16384","\-","Buffer size in bytes (1024-1048576)"
    "spread_checks","integer","false","2","\-","Randomness in check interval (0-50)"
    "bogus_proxy_enabled","boolean","false","false","\-","Disable PROXY protocol support in bogus header"
    "lua_max_mem","integer","false","0","\-","Maximum RAM in megabytes per process for Lua (0-1024)"
    "custom_options","string","false","\-","\-","Custom HAProxy options for global section"
    "ocsp_update_enabled","boolean","false","false","\-","Enable automatic OCSP response updates"
    "ocsp_update_min_delay","integer","false","300","\-","Minimum delay between OCSP updates (1-86400)"
    "ocsp_update_max_delay","integer","false","3600","\-","Maximum delay between OCSP updates (1-86400)"
    "ssl_defaults_enabled","boolean","false","false","\-","Enable global SSL default values"
    "ssl_bind_options","list","false","['prefer-client-ciphers']","\-","SSL/TLS binding options"
    "ssl_min_version","string","false","TLSv1.2","\-","Minimum SSL/TLS version (SSLv3, TLSv1.0, TLSv1.1, TLSv1.2, TLSv1.3)"
    "ssl_max_version","string","false","\-","\-","Maximum SSL/TLS version (SSLv3, TLSv1.0, TLSv1.1, TLSv1.2, TLSv1.3)"
    "ssl_cipher_list","string","false","\-","\-","SSL cipher list for TLSv1.2 and below"
    "ssl_cipher_suites","string","false","\-","\-","SSL cipher suites for TLSv1.3"
    "h2_initial_window_size","integer","false","\-","\-","HTTP/2 initial window size (0-10000000)"
    "h2_initial_window_size_outgoing","integer","false","\-","\-","HTTP/2 initial window size for outgoing connections (0-10000000)"
    "h2_initial_window_size_incoming","integer","false","\-","\-","HTTP/2 initial window size for incoming connections (0-10000000)"
    "h2_max_concurrent_streams","integer","false","\-","\-","HTTP/2 maximum concurrent streams (0-10000000)"
    "h2_max_concurrent_streams_outgoing","integer","false","\-","\-","HTTP/2 maximum concurrent streams for outgoing connections (0-10000000)"
    "h2_max_concurrent_streams_incoming","integer","false","\-","\-","HTTP/2 maximum concurrent streams for incoming connections (0-10000000)"

Examples
--------

.. code-block:: yaml

    - name: Configure HAProxy performance tuning
      oxlorg.opnsense.haproxy_general_tuning:
        max_connections: 2000
        nbthread: 4
        buffer_size: 32768
        ssl_min_version: 'TLSv1.2'
        ssl_defaults_enabled: true

----

.. _haproxy_general_logging:

oxlorg.opnsense.haproxy_general_logging
============================================

Manages HAProxy logging configuration.

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "host","string","false","127.0.0.1","\-","IPv4 or IPv6 address where to send logs"
    "facility","string","false","local0","\-","Standard syslog facility (alert, audit, auth2, auth, cron2, cron, daemon, ftp, kern, local0-7, lpr, mail, news, ntp, syslog, user, uucp)"
    "level","string","false","info","\-","Filter for outgoing messages (alert, crit, debug, emerg, err, info, notice, warning)"
    "length","integer","false","\-","\-","Maximum line length in characters (64-65535)"

Examples
--------

.. code-block:: yaml

    - name: Configure HAProxy logging
      oxlorg.opnsense.haproxy_general_logging:
        host: '192.168.1.100'
        facility: 'local0'
        level: 'info'
        length: 1024

----

.. _haproxy_general_peers:

oxlorg.opnsense.haproxy_general_peers
==========================================

Manages HAProxy peer synchronization for high availability.

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "enabled","boolean","false","true","\-","Enable or disable peer synchronization"
    "name1","string","false","\-","\-","Name of the first peer (usually FQDN)"
    "listen1","string","false","\-","\-","Listen address of the first peer"
    "port1","integer","false","1024","\-","TCP port for first peer connections (1-65535)"
    "name2","string","false","\-","\-","Name of the second peer (usually FQDN)"
    "listen2","string","false","\-","\-","Listen address of the second peer"
    "port2","integer","false","1024","\-","TCP port for second peer connections (1-65535)"

Examples
--------

.. code-block:: yaml

    - name: Configure HAProxy peer synchronization
      oxlorg.opnsense.haproxy_general_peers:
        enabled: true
        name1: 'haproxy1.example.com'
        listen1: '192.168.1.10'
        port1: 1024
        name2: 'haproxy2.example.com'
        listen2: '192.168.1.11'
        port2: 1024

----

.. _haproxy_general_cache:

oxlorg.opnsense.haproxy_general_cache
==========================================

Manages HAProxy caching configuration.

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "enabled","boolean","false","true","\-","Enable or disable caching"
    "total_max_size","integer","false","4","\-","Cache size in RAM in megabytes (1-4095)"
    "max_age","integer","false","60","\-","Maximum expiration duration in seconds (1-3600)"
    "max_object_size","integer","false","\-","\-","Maximum size of cached objects (1-2146435072)"
    "process_vary","boolean","false","false","\-","Enable processing of Vary header"
    "max_secondary_entries","integer","false","10","\-","Maximum simultaneous secondary entries (min=1)"

Examples
--------

.. code-block:: yaml

    - name: Configure HAProxy caching
      oxlorg.opnsense.haproxy_general_cache:
        enabled: true
        total_max_size: 64
        max_age: 300
        process_vary: true
        max_secondary_entries: 20


See also: :ref:`modules_haproxy` and :ref:`troubleshooting <troubleshooting>`