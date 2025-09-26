.. _modules_haproxy:

.. include:: ../_include/head.rst

=======
HAProxy
=======

**STATE**: unstable

**COMPATIBILITY**: OPNsense 24.1+

**Note**: Most functions should work on earlier OPNsense versions, but full compatibility is tested with OPNsense 24.1+. For compatibility with earlier versions, please check the configuration differences at: `HAProxy Configuration Reference <https://github.com/opnsense/plugins/blob/master/net/haproxy/src/opnsense/mvc/app/models/OPNsense/HAProxy/HAProxy.xml>`_

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

Modules documentation
*********************

The HAProxy functionality is split into multiple modules organized by function:

.. toctree::
   :maxdepth: 1

   haproxy_auth
   haproxy_system
   haproxy_general
   haproxy_rules
   haproxy_advanced

Quick overview
**************

**Authentication & access control:**

- :ref:`haproxy_user <haproxy_user>` - Manage HAProxy authentication users
- :ref:`haproxy_group <haproxy_group>` - Manage HAProxy authentication groups

**Performance & system:**

- :ref:`haproxy_cpu <haproxy_cpu>` - Manage CPU affinity rules for HAProxy processes
- :ref:`haproxy_maintenance <haproxy_maintenance>` - Manage HAProxy maintenance and monitoring settings

**General configuration:**

- :ref:`haproxy_general_settings <haproxy_general_settings>` - Manage general HAProxy configuration
- :ref:`haproxy_general_stats <haproxy_general_stats>` - Manage HAProxy statistics and monitoring (with automatic name-to-UUID resolution)
- :ref:`haproxy_general_defaults <haproxy_general_defaults>` - Manage HAProxy default settings
- :ref:`haproxy_general_tuning <haproxy_general_tuning>` - Manage HAProxy performance tuning
- :ref:`haproxy_general_logging <haproxy_general_logging>` - Manage HAProxy logging configuration
- :ref:`haproxy_general_peers <haproxy_general_peers>` - Manage HAProxy peer synchronization
- :ref:`haproxy_general_cache <haproxy_general_cache>` - Manage HAProxy caching configuration

**Rules & traffic control:**

- :ref:`haproxy_acl <haproxy_acl>` - Manage HAProxy Access Control Lists (ACLs) for traffic filtering and condition matching
- :ref:`haproxy_action <haproxy_action>` - Manage HAProxy Actions that execute when ACL conditions are met

**Advanced features:**

- :ref:`haproxy_lua <haproxy_lua>` - Manage HAProxy Lua scripts for custom logic and processing
- :ref:`haproxy_fcgi <haproxy_fcgi>` - Manage HAProxy FastCGI applications for dynamic content processing
- :ref:`haproxy_errorfile <haproxy_errorfile>` - Manage HAProxy custom error pages for better user experience

----

Usage examples
***************

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
            reload_service: false
            restart_service: false

Advanced HAProxy setup with ACLs, Actions, and custom features:

.. code-block:: yaml

    - name: Advanced HAProxy configuration with rules and custom features
      hosts: opnsense_firewalls
      tasks:
        # Create ACLs for traffic filtering
        - name: Create ACL for admin path
          ansibleguy.opnsense.haproxy_acl:
            name: 'admin_path_acl'
            description: 'ACL to match admin paths'
            expression: 'path_beg'
            path_beg: '/admin'

        - name: Create ACL for API endpoints
          ansibleguy.opnsense.haproxy_acl:
            name: 'api_path_acl'
            description: 'ACL to match API paths'
            expression: 'path_reg'
            path_reg: '^/api/v[0-9]+/'

        # Create actions based on ACLs
        - name: Redirect admin traffic to secure backend
          ansibleguy.opnsense.haproxy_action:
            name: 'redirect_admin'
            description: 'Redirect admin paths to secure backend'
            type: 'use_backend'
            use_backend: 'secure_backend'
            test_type: 'if'
            linked_acls:
              - 'admin_path_acl'

        - name: Add security headers for API
          ansibleguy.opnsense.haproxy_action:
            name: 'api_security_headers'
            description: 'Add security headers to API responses'
            type: 'http-response_add-header'
            http_response_add_header_name: 'X-Content-Type-Options'
            http_response_add_header_content: 'nosniff'
            test_type: 'if'
            linked_acls:
              - 'api_path_acl'

        # Configure Lua script for custom logic
        - name: Create Lua script for request processing
          ansibleguy.opnsense.haproxy_lua:
            name: 'request_processor'
            description: 'Custom request processing logic'
            preload: true
            filename_scheme: 'name'
            content: |
              function process_request(txn)
                local path = txn.http:req_get_path()
                if string.match(path, "^/internal/") then
                  txn:Alert("Blocked internal path access: " .. path)
                  txn:done(403)
                end
              end

        # Configure FastCGI application
        - name: Create FastCGI application for PHP
          ansibleguy.opnsense.haproxy_fcgi:
            name: 'php_app'
            description: 'PHP FastCGI application'
            docroot: '/var/www/html'
            index: 'index.php'
            max_reqs: 1000
            keep_conn: true

        # Configure custom error pages
        - name: Create custom 503 error page
          ansibleguy.opnsense.haproxy_errorfile:
            name: 'maintenance_page'
            description: 'Custom maintenance page for 503 errors'
            code: '503'
            content: |
              HTTP/1.1 503 Service Unavailable
              Content-Type: text/html
              Cache-Control: no-cache
              Connection: close

              <!DOCTYPE html>
              <html>
              <head><title>Maintenance</title></head>
              <body>
                <h1>Service Temporarily Unavailable</h1>
                <p>We are currently performing maintenance. Please try again later.</p>
              </body>
              </html>

----

Troubleshooting
***************

**Name resolution in stats module**

The HAProxy stats module automatically resolves user and group names to UUIDs. If you encounter errors like "User 'username' not found", ensure:

1. The user/group exists in HAProxy configuration
2. The name spelling is exact (case-sensitive)
3. The user/group is enabled

**CPU affinity configuration**

- Use string values for thread_id and cpu_id (e.g., 'x1', 'x0')
- Ensure CPU IDs don't exceed available CPU cores
- Thread IDs should not exceed the configured nbthread value

**Performance tuning**

For high-traffic scenarios:

- Increase ``max_connections`` in tuning
- Use multiple ``nbthread`` (typically number of CPU cores)
- Increase ``buffer_size`` for large requests/responses
- Adjust ``timeout_*`` values based on your application needs

See: :ref:`troubleshooting <troubleshooting>`