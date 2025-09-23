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

Advanced HAProxy setup with ACLs, Actions, and custom pages:

.. code-block:: yaml

    - name: Advanced HAProxy configuration with rules and custom features
      hosts: opnsense_firewalls
      tasks:
        # Create ACLs for traffic filtering
        - name: Create ACL for API domain
          ansibleguy.opnsense.haproxy_acl:
            name: 'acl_api_domain'
            description: 'API domain filter'
            expression: 'hdr'
            hdr: 'api.example.com'

        - name: Create ACL for rate limiting
          ansibleguy.opnsense.haproxy_acl:
            name: 'acl_rate_limit'
            description: 'Rate limiting'
            expression: 'src_conn_rate'
            src_conn_rate_comparison: 'gt'
            src_conn_rate: 100

        - name: Create ACL for admin paths
          ansibleguy.opnsense.haproxy_acl:
            name: 'acl_admin_path'
            description: 'Admin paths'
            expression: 'path_beg'
            path_beg: '/admin'

        # Create Actions for rule enforcement
        - name: Create allow action for API
          ansibleguy.opnsense.haproxy_action:
            name: 'action_allow_api'
            description: 'Allow API access'
            test_type: 'if'
            linked_acls: ['acl_api_domain']
            type: 'http-request_allow'

        - name: Create header action for rate limiting
          ansibleguy.opnsense.haproxy_action:
            name: 'action_rate_header'
            description: 'Add rate limit header'
            test_type: 'if'
            linked_acls: ['acl_rate_limit']
            type: 'http-request_add-header'
            http_request_add_header_name: 'X-Rate-Limited'
            http_request_add_header_content: 'true'

        - name: Create deny action for admin
          ansibleguy.opnsense.haproxy_action:
            name: 'action_deny_admin'
            description: 'Deny admin access'
            test_type: 'if'
            linked_acls: ['acl_admin_path']
            type: 'http-request_deny'

        # Deploy Lua scripts for custom logic
        - name: Create Lua scripts
          ansibleguy.opnsense.haproxy_lua:
            name: 'auth_script'
            description: 'JWT authentication script'
            enabled: true
            preload: true
            filename_scheme: 'id'
            content: |
              function authenticate_jwt(txn)
                local headers = txn.http:req_get_headers()
                local auth_header = headers["authorization"]
                if auth_header and string.find(auth_header, "Bearer ") then
                  core.Info("Valid JWT token found")
                  return "AUTHORIZED"
                else
                  core.Info("No valid JWT token")
                  return "UNAUTHORIZED"
                end
              end

        # Configure FastCGI for PHP applications
        - name: Create FastCGI applications
          ansibleguy.opnsense.haproxy_fcgi:
            name: 'php_api_app'
            description: 'PHP API application'
            enabled: true
            docroot: '/var/www/api'
            index: 'api.php'
            path_info: '^(/.+\.php)(/.*)?$'
            log_stderr: true
            max_reqs: 50

        # Create custom error pages
        - name: Create custom error pages
          ansibleguy.opnsense.haproxy_errorfile:
            name: 'maintenance_503'
            description: 'Maintenance mode page'
            code: 'x503'
            content: |
              HTTP/1.0 503 Service Unavailable
              Content-Type: text/html
              Cache-Control: no-cache
              Connection: close

              <!DOCTYPE html>
              <html>
              <head><title>Maintenance Mode</title></head>
              <body>
                <h1>🔧 We'll be right back!</h1>
                <p>We're performing scheduled maintenance.</p>
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

**ACL and action UUID resolution**

The HAProxy action module automatically resolves ACL names to UUIDs. If you encounter errors like "Related ACL item not found":

1. Ensure the ACL exists before creating the action
2. Check ACL name spelling (case-sensitive)
3. Verify the ACL is properly configured

**FCGI action resolution**

The HAProxy FCGI module automatically resolves action names to UUIDs. If you encounter errors like "Related action item not found":

1. Create actions before linking them to FCGI applications
2. Ensure action names match exactly
3. Verify actions are of compatible types (fcgi_pass_header, fcgi_set_param)

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