.. _modules_haproxy_general:

.. include:: ../_include/head.rst

=====================
HAProxy General
=====================

**STATE**: stable

**COMPATIBILITY**: OPNsense 24.1+

**Note**: Most functions should work on earlier OPNsense versions, but full compatibility is tested with OPNsense 24.1+. For compatibility with earlier versions, please check the configuration differences at: `HAProxy Configuration Reference <https://github.com/opnsense/plugins/blob/master/net/haproxy/src/opnsense/mvc/app/models/OPNsense/HAProxy/HAProxy.xml>`_

**TESTS**: `Playbook <https://github.com/O-X-L/ansible_opnsense/blob/latest/tests/haproxy_general.yml>`_


Contribution
************

This module was contributed by **MaximeWewer** (@MaximeWewer).

If you encounter any issues or have suggestions for improvements, please feel free to contribute to the project.


Definition
**********

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "enabled","boolean","false","false","\-","Enable or disable HAProxy service"
    "graceful_stop","boolean","false","false","\-","Enable graceful stop"
    "hard_stop_after","string","false","60s","\-","Hard stop after timeout"
    "close_spread_time","string","false","\-","\-","Close spread time"
    "seamless_reload","boolean","false","false","\-","Enable seamless reload"
    "show_intro","boolean","false","true","\-","Show introduction page"
    "store_ocsp","boolean","false","false","\-","Store OCSP responses"
    "tuning_max_connections","integer","false","\-","\-","Maximum number of connections (tuning)"
    "tuning_nbthread","integer","false","1","\-","Number of threads"
    "tuning_resolvers_prefer","string","false","ipv4","\-","DNS resolver preference (ipv4/ipv6)"
    "tuning_ssl_server_verify","string","false","ignore","\-","SSL server verification (ignore/required)"
    "tuning_root","boolean","false","false","\-","Run as root user"
    "tuning_max_dh_size","integer","false","2048","\-","Maximum DH key size (1024-16384)"
    "tuning_buffer_size","integer","false","16384","\-","Buffer size (1024-1048576)"
    "tuning_spread_checks","integer","false","2","\-","Spread health checks (0-50)"
    "tuning_bogus_proxy_enabled","boolean","false","false","\-","Enable bogus proxy protocol"
    "tuning_lua_max_mem","integer","false","0","\-","Maximum Lua memory (0-1024 MB)"
    "tuning_custom_options","string","false","\-","\-","Custom tuning options"
    "tuning_ocsp_update_enabled","boolean","false","false","\-","Enable OCSP auto-updates"
    "tuning_ocsp_update_min_delay","integer","false","300","\-","OCSP min delay (1-86400s)"
    "tuning_ocsp_update_max_delay","integer","false","3600","\-","OCSP max delay (1-86400s)"
    "tuning_ssl_defaults_enabled","boolean","false","false","\-","Enable SSL defaults"
    "tuning_ssl_bind_options","list","false","\-","\-","SSL bind options"
    "tuning_ssl_min_version","string","false","TLSv1.2","\-","Minimum SSL/TLS version"
    "tuning_ssl_max_version","string","false","\-","\-","Maximum SSL/TLS version"
    "peers_enabled","boolean","false","false","\-","Enable peer synchronization"
    "peers_name1","string","false","\-","\-","First peer name"
    "peers_listen1","string","false","\-","\-","First peer listen address"
    "peers_port1","integer","false","1024","\-","First peer port (1-65535)"
    "peers_name2","string","false","\-","\-","Second peer name"
    "peers_listen2","string","false","\-","\-","Second peer listen address"
    "peers_port2","integer","false","1024","\-","Second peer port (1-65535)"
    "defaults_max_connections","integer","false","\-","\-","Default max connections per process"
    "defaults_max_connections_servers","integer","false","\-","\-","Default max connections to servers"
    "defaults_timeout_client","string","false","30s","\-","Default client timeout"
    "defaults_timeout_connect","string","false","30s","\-","Default connection timeout"
    "defaults_timeout_check","string","false","\-","\-","Default health check timeout"
    "defaults_timeout_server","string","false","30s","\-","Default server timeout"
    "defaults_retries","integer","false","3","\-","Default number of retries (0-100)"
    "defaults_redispatch","string","false","x-1","\-","Redispatch configuration"
    "defaults_init_addr","list","false","[last,libc]","\-","Default server address init methods"
    "defaults_custom_options","string","false","\-","\-","Custom default options"
    "logging_host","string","false","127.0.0.1","\-","Syslog server hostname/IP"
    "logging_facility","string","false","local0","\-","Syslog facility"
    "logging_level","string","false","info","\-","Syslog level"
    "logging_length","integer","false","\-","\-","Max syslog message length (64-65535)"
    "stats_enabled","boolean","false","false","\-","Enable HAProxy statistics"
    "stats_port","integer","false","8822","\-","Statistics port (1024-65535)"
    "stats_remote_enabled","boolean","false","false","\-","Enable remote statistics access"
    "stats_remote_bind","list","false","\-","\-","Remote bind addresses for stats"
    "stats_auth_enabled","boolean","false","false","\-","Enable statistics authentication"
    "stats_users","list","false","\-","\-","Statistics users (user:password format)"
    "stats_custom_options","string","false","\-","\-","Custom statistics options"
    "stats_prometheus_enabled","boolean","false","false","\-","Enable Prometheus metrics"
    "stats_prometheus_bind","list","false","[*:8404]","\-","Prometheus bind addresses"
    "stats_prometheus_path","string","false","/metrics","\-","Prometheus metrics path"
    "reload","boolean","false","true","\-", .. include:: ../_include/param_reload.rst

.. include:: ../_include/param_basic.rst

Usage
*****

This module configures the comprehensive HAProxy general settings on OPNsense. It provides complete control over:

- **Basic service control**: Enable/disable, graceful shutdown, seamless reloads
- **Performance tuning**: Connection limits, threading, buffer sizes, SSL optimization
- **High availability**: Peer synchronization for load balancer clustering  
- **Logging**: Syslog integration with facility and level control
- **Statistics & monitoring**: Built-in stats interface and Prometheus metrics
- **SSL/TLS security**: Version control, cipher management, OCSP handling
- **Default behaviors**: Timeouts, retries, connection handling

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
          target: 'haproxy_general'

      tasks:
        - name: Basic HAProxy configuration
          ansibleguy.opnsense.haproxy_general:
            enabled: true
            graceful_stop: true
            hard_stop_after: '60s'
            seamless_reload: true
            show_intro: false

        - name: High-performance configuration
          ansibleguy.opnsense.haproxy_general:
            enabled: true
            tuning_max_connections: 10000
            tuning_nbthread: 4
            tuning_buffer_size: 32768
            tuning_spread_checks: 5
            defaults_timeout_client: '60s'
            defaults_timeout_server: '60s'
            defaults_retries: 5

        - name: SSL/TLS security hardening
          ansibleguy.opnsense.haproxy_general:
            enabled: true
            tuning_ssl_min_version: 'TLSv1.2'
            tuning_ssl_max_version: 'TLSv1.3'
            tuning_max_dh_size: 4096
            tuning_ssl_defaults_enabled: true
            tuning_ocsp_update_enabled: true

        - name: Enable statistics and monitoring
          ansibleguy.opnsense.haproxy_general:
            enabled: true
            stats_enabled: true
            stats_port: 8080
            stats_auth_enabled: true
            stats_users:
              - "admin:secret123"
            stats_prometheus_enabled: true
            stats_prometheus_bind:
              - "*:9090"

        - name: Configure high availability with peers
          ansibleguy.opnsense.haproxy_general:
            enabled: true
            peers_enabled: true
            peers_name1: "node1"
            peers_listen1: "10.0.1.10"
            peers_port1: 1024
            peers_name2: "node2"
            peers_listen2: "10.0.1.11"
            peers_port2: 1024

        - name: Advanced logging configuration
          ansibleguy.opnsense.haproxy_general:
            enabled: true
            logging_host: "syslog.example.com"
            logging_facility: "local1"
            logging_level: "info"
            logging_length: 1024

        - name: List HAProxy configuration
          ansibleguy.opnsense.list:
          register: haproxy_config

        - name: Show configuration
          ansible.builtin.debug:
            var: haproxy_config.data