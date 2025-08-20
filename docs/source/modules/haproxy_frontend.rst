.. _modules_haproxy_frontend:

.. include:: ../_include/head.rst

================
HAProxy Frontend
================

**STATE**: stable

**COMPATIBILITY**: OPNsense 24.1+

**Note**: Most functions should work on earlier OPNsense versions, but full compatibility is tested with OPNsense 24.1+. For compatibility with earlier versions, please check the configuration differences at: `HAProxy Configuration Reference <https://github.com/opnsense/plugins/blob/master/net/haproxy/src/opnsense/mvc/app/models/OPNsense/HAProxy/HAProxy.xml>`_

**TESTS**: `Playbook <https://github.com/O-X-L/ansible_opnsense/blob/latest/tests/haproxy_frontend.yml>`_

**API Docs**: `HAProxy <https://docs.opnsense.org/development/api/plugins/haproxy.html>`_

**Service Docs**: `HAProxy <https://docs.opnsense.org/manual/how-tos/haproxy.html>`_


Contribution
************

This module was contributed by **MaximeWewer** (@MaximeWewer).

If you encounter any issues or have suggestions for improvements, please feel free to contribute to the project.


Definition
**********

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "name","string","true","\-","\-","Frontend name (unique identifier)"
    "description","string","false","\-","\-","Frontend description"
    "enabled","boolean","false","true","\-","Enable or disable frontend"
    "bind_address","string","true","\-","\-","IP address to bind to"
    "bind_port","integer","true","\-","\-","Port to bind to (1-65535)"
    "ssl_enabled","boolean","false","false","\-","Enable SSL/TLS encryption"
    "ssl_certificates","list","false","\-","\-","List of SSL certificate names"
    "default_backend","string","false","\-","\-","**NEW**: Default backend name (automatic UUID resolution)"
    "linked_actions","list","false","\-","\-","**NEW**: List of action names to apply (automatic UUID resolution)"
    "linked_errorfiles","list","false","\-","\-","**NEW**: List of errorfile names for custom errors (automatic UUID resolution)"
    "basic_auth_users","list","false","\-","\-","**NEW**: List of user names for authentication (automatic UUID resolution)"
    "basic_auth_groups","list","false","\-","\-","**NEW**: List of group names for authentication (automatic UUID resolution)"
    "mode","string","false","http","\-","Frontend mode (http, tcp)"
    "max_connections","integer","false","\-","\-","Maximum number of concurrent connections"
    "log_enabled","boolean","false","false","\-","Enable logging for this frontend"
    "advanced_options","string","false","\-","\-","Advanced HAProxy configuration options"
    "state","string","false","present","\-","State of the frontend (present, absent)"
    "reload","boolean","false","true","\-", .. include:: ../_include/param_reload.rst

.. include:: ../_include/param_basic.rst

Usage
*****

This module manages HAProxy frontend configurations on OPNsense. Frontends define the entry points for client connections, handling SSL termination, protocol selection, and routing to appropriate backends.

**Key Features:**

* **Network binding**: Configure IP addresses and ports for client connections
* **SSL/TLS termination**: Handle encrypted connections with certificate management  
* **Protocol handling**: Support for HTTP and TCP modes
* **Automatic UUID Resolution**: All relationship fields (backends, actions, users, groups, etc.) accept names and automatically resolve to UUIDs
* **Name-based Linking**: Link backends, actions, errorfiles, and authentication resources by name instead of UUID
* **UI Compatibility**: All selections appear correctly in the OPNsense web interface
* **Multi-select Support**: Lists support multiple items with proper comma-separated UUID format
* **Connection limits**: Control concurrent connection limits per frontend
* **Logging integration**: Optional per-frontend logging configuration

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
          target: 'haproxy_frontend'

      tasks:
        - name: Create comprehensive frontend with all features
          ansibleguy.opnsense.haproxy_frontend:
            name: "web_frontend"
            description: "Main web frontend with full configuration"
            enabled: true
            bind_address: "10.0.0.100"
            bind_port: 443
            ssl_enabled: true
            ssl_certificates: ['web-cert', 'backup-cert']
            mode: "http"
            default_backend: "web_backend"
            linked_actions: ['log_requests', 'security_headers', 'rate_limit']
            linked_errorfiles: ['custom_404', 'custom_500', 'maintenance']
            basic_auth_users: ['admin', 'support']
            basic_auth_groups: ['admins', 'operators']
            max_connections: 1000
            log_enabled: true

        - name: Create simple HTTP frontend
          ansibleguy.opnsense.haproxy_frontend:
            name: "api_frontend"
            description: "API frontend"
            bind_address: "0.0.0.0"
            bind_port: 80
            mode: "http"
            default_backend: "api_backend"
            linked_actions: ['cors_headers']

        - name: Create HTTPS frontend with authentication
          ansibleguy.opnsense.haproxy_frontend:
            name: "secure_frontend"
            description: "Secure HTTPS frontend with auth"
            bind_address: "10.0.0.200"
            bind_port: 443
            ssl_enabled: true
            ssl_certificates: ['secure-cert']
            mode: "http"
            default_backend: "secure_backend"
            basic_auth_users: ['admin_user']
            basic_auth_groups: ['admin_group']
            linked_errorfiles: ['auth_required']

        - name: Create TCP frontend for database
          ansibleguy.opnsense.haproxy_frontend:
            name: "db_frontend"
            description: "Database TCP frontend"
            bind_address: "10.0.1.10"
            bind_port: 5432
            mode: "tcp"
            default_backend: "database_backend"

        - name: Create frontend with custom bind addresses
          ansibleguy.opnsense.haproxy_frontend:
            name: "multi_bind_frontend"
            description: "Frontend with different bind examples"
            bind_address: "*"        # All interfaces
            bind_port: 8080
            mode: "http"
            default_backend: "web_backend"

        - name: Remove old frontend
          ansibleguy.opnsense.haproxy_frontend:
            name: "old_frontend"
            state: absent

        - name: List all frontends
          ansibleguy.opnsense.list:
          register: haproxy_frontends

        - name: Show frontends
          ansible.builtin.debug:
            var: haproxy_frontends.data