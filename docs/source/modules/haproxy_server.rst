.. _modules_haproxy_server:

.. include:: ../_include/head.rst

================
HAProxy Server
================

**STATE**: stable

**COMPATIBILITY**: OPNsense 24.1+

**Note**: Most functions should work on earlier OPNsense versions, but full compatibility is tested with OPNsense 24.1+. For compatibility with earlier versions, please check the configuration differences at: `HAProxy Configuration Reference <https://github.com/opnsense/plugins/blob/master/net/haproxy/src/opnsense/mvc/app/models/OPNsense/HAProxy/HAProxy.xml>`_

**TESTS**: `Playbook <https://github.com/O-X-L/ansible_opnsense/blob/latest/tests/haproxy_server.yml>`_

**API Docs**: `HAProxy <https://docs.opnsense.org/development/api/plugins/haproxy.html>`_

**Service Docs**: `HAProxy <https://docs.opnsense.org/manual/how-tos/haproxy.html>`_


Contribution
************

This module was contributed by **MaximeWewer** (@MaximeWewer).

If you encounter any issues or have suggestions for improvements, please feel free to contribute to the project.


Definition
**********

.. include:: ../_include/param_basic.rst

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "name","string","true","\-","\-","Server name (unique identifier)"
    "description","string","false","\-","\-","Server description"
    "enabled","boolean","false","true","\-","Enable or disable the server"
    "address","string","true","\-","\-","Server IP address or hostname"
    "port","integer","true","\-","\-","Server port (1-65535)"
    "ssl","boolean","false","false","\-","Use SSL for backend connection"
    "ssl_ca","string","false","\-","\-","CA certificate UUID for SSL verification"
    "weight","integer","false","1","\-","Server weight for load balancing (0-256)"
    "check_interval","string","false","2s","\-","Health check interval (format: number + optional suffix: us/ms/s/m/h/d)"
    "check_down_interval","string","false","\-","\-","Health check interval when server is down (format: number + optional suffix: us/ms/s/m/h/d)"
    "source","string","false","\-","\-","Source address for connections to this server"
    "linked_resolver","string","false","\-","\-","**NEW**: Resolver name to use for server name resolution - supports automatic UUID resolution"
    "unix_socket","string","false","\-","\-","**NEW**: Frontend name for Unix socket binding - supports automatic UUID resolution"
    "advanced","string","false","\-","\-","Advanced HAProxy server configuration options"

Usage
*****

This module manages individual HAProxy server configurations on OPNsense. Servers are backend endpoints that handle client requests routed through HAProxy frontends and backends.

Key features:

- **Automatic UUID Resolution**: All relationship fields accept names and automatically resolve to UUIDs
- **Name-based Linking**: Users can specify resolver names and frontend names instead of UUIDs
- **UI Compatibility**: All selections appear correctly in the OPNsense web interface
- **Server endpoint definition**: Configure IP addresses and ports for backend services
- **Health monitoring**: Set up health checks with custom intervals and failure detection
- **Load balancing**: Control server weights and traffic distribution
- **SSL backend connections**: Enable encrypted connections to backend servers
- **Connection control**: Manage source addresses and connection parameters
- **Resolver integration**: Link servers to specific DNS resolvers for dynamic resolution
- **Unix socket support**: Connect to Unix domain sockets via frontend names
- **Server states**: Enable/disable servers without removing configuration

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
          target: 'haproxy_server'

      tasks:
        - name: Create basic web server
          ansibleguy.opnsense.haproxy_server:
            name: "web01"
            description: "Primary web server"
            enabled: true
            address: "192.168.1.10"
            port: 80
            weight: 10
            check_interval: "5s"

        - name: Create SSL backend server
          ansibleguy.opnsense.haproxy_server:
            name: "api_server"
            description: "API server with SSL"
            enabled: true
            address: "api.internal.com"
            port: 443
            ssl: true
            ssl_ca: "{{ ca_cert_uuid }}"
            weight: 5

        - name: Create database server with custom health check
          ansibleguy.opnsense.haproxy_server:
            name: "db_server"
            description: "PostgreSQL database server"
            enabled: true
            address: "10.0.2.5"
            port: 5432
            weight: 1
            check_interval: "10s"
            check_down_interval: "5s"
            source: "10.0.1.100"

        - name: Create server with name-based resolver linking
          ansibleguy.opnsense.haproxy_server:
            name: "dynamic_server"
            description: "Server with dynamic DNS resolution"
            enabled: true
            address: "app.example.com"
            port: 8080
            weight: 10
            linked_resolver: "cloudflare_resolver"  # Uses resolver name, not UUID
            check_interval: "5s"

        - name: Create Unix socket server with frontend linking
          ansibleguy.opnsense.haproxy_server:
            name: "local_service"
            description: "Local service via Unix socket"
            enabled: true
            address: "/var/run/app.sock"
            port: 80
            unix_socket: "unix_frontend"  # Uses frontend name, not UUID
            weight: 15

        - name: Create server with advanced configuration
          ansibleguy.opnsense.haproxy_server:
            name: "custom_server"
            description: "Server with advanced options"
            enabled: true
            address: "192.168.2.20"
            port: 8080
            weight: 8
            advanced: |
              backup
              maxconn 100
              send-proxy

        - name: Disable server temporarily
          ansibleguy.opnsense.haproxy_server:
            name: "maintenance_server"
            enabled: false

        - name: Remove old server
          ansibleguy.opnsense.haproxy_server:
            name: "deprecated_server"
            state: absent

        - name: List all servers
          ansibleguy.opnsense.list:
          register: haproxy_servers

        - name: Show servers
          ansible.builtin.debug:
            var: haproxy_servers.data