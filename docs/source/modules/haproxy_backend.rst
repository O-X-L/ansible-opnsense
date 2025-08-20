.. _modules_haproxy_backend:

.. include:: ../_include/head.rst

================
HAProxy Backend
================

**STATE**: stable

**COMPATIBILITY**: OPNsense 24.1+

**Note**: Most functions should work on earlier OPNsense versions, but full compatibility is tested with OPNsense 24.1+. For compatibility with earlier versions, please check the configuration differences at: `HAProxy Configuration Reference <https://github.com/opnsense/plugins/blob/master/net/haproxy/src/opnsense/mvc/app/models/OPNsense/HAProxy/HAProxy.xml>`_

**TESTS**: `Playbook <https://github.com/O-X-L/ansible_opnsense/blob/latest/tests/haproxy_backend.yml>`_


Contribution
************

This module was contributed by **MaximeWewer** (@MaximeWewer).

If you encounter any issues or have suggestions for improvements, please feel free to contribute to the project.


Definition
**********

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "name","string","true","\-","\-","Backend name"
    "description","string","false","\-","\-","Backend description"
    "enabled","boolean","false","true","\-","Enable or disable backend"
    "mode","string","false","http","\-","Backend mode (http, tcp)"
    "algorithm","string","false","roundrobin","\-","Load balancing algorithm: roundrobin, static-rr, leastconn, first, source, uri, random, rdp-cookie"
    "source","string","false","\-","\-","Source IP address for backend connections"
    "health_check_enabled","boolean","false","false","\-","Enable health checks"
    "health_check","string","false","\-","\-","Health check configuration name"
    "health_check_interval","string","false","2s","\-","Health check interval (e.g., 2s, 30s, 1m)"
    "health_check_timeout","string","false","2s","\-","Health check timeout (e.g., 2s, 30s, 1m)"
    "health_check_retries","integer","false","3","\-","Number of health check retries"
    "linked_servers","list","false","\-","\-","**NEW**: List of server names to link (automatic UUID resolution)"
    "linked_actions","list","false","\-","\-","**NEW**: List of action names to link (automatic UUID resolution)"
    "linked_errorfiles","list","false","\-","\-","**NEW**: List of errorfile names to link (automatic UUID resolution)"
    "basic_auth_users","list","false","\-","\-","**NEW**: List of user names for authentication (automatic UUID resolution)"
    "basic_auth_groups","list","false","\-","\-","**NEW**: List of group names for authentication (automatic UUID resolution)"
    "linked_resolver","string","false","\-","\-","Resolver name for DNS resolution"
    "http_reuse","string","false","never","\-","HTTP connection reuse: never, safe, aggressive, always"
    "state","string","false","present","\-","State of the backend (present, absent)"
    "reload","boolean","false","true","\-", .. include:: ../_include/param_reload.rst

.. include:: ../_include/param_basic.rst

Usage
*****

This module manages HAProxy backend configurations. Backends define pools of servers that can handle requests from frontends. You can configure load balancing algorithms, health checks, server linking, authentication, error handling, and advanced routing features.

**Key Features:**

* **Automatic UUID Resolution**: All relationship fields (servers, actions, users, groups, etc.) accept names and automatically resolve to UUIDs
* **Name-based Linking**: Link servers, actions, errorfiles, and authentication resources by name instead of UUID
* **UI Compatibility**: All selections appear correctly in the OPNsense web interface
* **Multi-select Support**: Lists support multiple items with proper comma-separated UUID format

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
          target: 'haproxy_backend'

      tasks:
        - name: Create comprehensive backend with all features
          ansibleguy.opnsense.haproxy_backend:
            name: 'web_backend'
            description: 'Main web backend with full configuration'
            enabled: true
            mode: 'http'
            algorithm: 'roundrobin'
            source: '10.0.1.100'
            health_check_enabled: true
            health_check: 'web_health_check'
            health_check_interval: '30s'
            health_check_timeout: '5s'
            health_check_retries: 3
            linked_servers: ['web1', 'web2', 'web3']
            linked_actions: ['log_requests', 'add_security_headers']
            linked_errorfiles: ['custom_404', 'custom_500']
            basic_auth_users: ['admin', 'operator']
            basic_auth_groups: ['admins', 'operators']
            http_reuse: 'safe'

        - name: Create simple HTTP backend with servers
          ansibleguy.opnsense.haproxy_backend:
            name: 'api_backend'
            description: 'API servers backend'
            mode: 'http'
            algorithm: 'leastconn'
            linked_servers: ['api1', 'api2']
            health_check_enabled: true

        - name: Create TCP backend for databases
          ansibleguy.opnsense.haproxy_backend:
            name: 'database_backend'
            description: 'Database servers backend'
            mode: 'tcp'
            algorithm: 'source'
            linked_servers: ['db_primary', 'db_replica']

        - name: Create backend with authentication
          ansibleguy.opnsense.haproxy_backend:
            name: 'secure_backend'
            description: 'Backend with user authentication'
            mode: 'http'
            basic_auth_users: ['secure_user1', 'secure_user2']
            basic_auth_groups: ['secure_group']
            linked_errorfiles: ['auth_error']

        - name: Remove backend
          ansibleguy.opnsense.haproxy_backend:
            name: 'old_backend'
            state: 'absent'

        - name: List all backends
          ansibleguy.opnsense.list:
          register: haproxy_backends

        - name: Show backends
          ansible.builtin.debug:
            var: haproxy_backends.data