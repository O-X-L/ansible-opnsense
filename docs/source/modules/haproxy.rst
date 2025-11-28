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

You can also install it using the :ref:`oxlorg.opnsense.package <modules_package>` module.

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
          oxlorg.opnsense.haproxy_user:
            name: "{{ item.name }}"
            description: "{{ item.description }}"
            password: "{{ item.password }}"
            enabled: true
          loop:
            - {name: 'admin', description: 'Administrator', password: '{{ vault_admin_pass }}'}
            - {name: 'monitor', description: 'Monitor user', password: '{{ vault_monitor_pass }}'}

        # Create groups
        - name: Create HAProxy groups
          oxlorg.opnsense.haproxy_group:
            name: "{{ item.name }}"
            description: "{{ item.description }}"
            members: "{{ item.members }}"
            enabled: true
          loop:
            - {name: 'admins', description: 'Administrators', members: ['admin']}
            - {name: 'monitors', description: 'Monitoring users', members: ['monitor']}

        # Configure basic settings
        - name: Configure HAProxy general settings
          oxlorg.opnsense.haproxy_general_settings:
            enabled: true
            graceful_stop: true
            hard_stop_after: 60
            seamless_reload: true

        # Configure monitoring with name resolution
        - name: Configure HAProxy statistics
          oxlorg.opnsense.haproxy_general_stats:
            enabled: true
            port: 8822
            auth_enabled: true
            allowed_users: ['admin']      # Automatically resolved to UUID
            allowed_groups: ['admins']    # Automatically resolved to UUID
            prometheus_enabled: true

        # Configure performance
        - name: Configure HAProxy performance tuning
          oxlorg.opnsense.haproxy_general_tuning:
            max_connections: 2000
            nbthread: 4
            buffer_size: 32768

        # Configure CPU affinity
        - name: Configure HAProxy CPU affinity
          oxlorg.opnsense.haproxy_cpu:
            name: 'web_threads'
            thread_id: 'x1'
            cpu_id: ['x0', 'x1']
            enabled: true

        # Configure maintenance
        - name: Configure HAProxy maintenance
          oxlorg.opnsense.haproxy_maintenance:
            sync_certs: true
            reload_service: false
            restart_service: false

**Advanced HAProxy setup with ACLs, Actions, and custom features:**

.. code-block:: yaml

    - name: Advanced HAProxy configuration with ACLs and Actions
      hosts: opnsense_firewalls
      tasks:
        # Create ACLs for traffic filtering
        - name: Create HAProxy ACL for URL path matching
          oxlorg.opnsense.haproxy_acl:
            name: 'acl_api_path'
            description: 'Match API paths'
            expression: 'path_beg'
            value: '/api/'
            enabled: true

        - name: Create HAProxy ACL for header matching
          oxlorg.opnsense.haproxy_acl:
            name: 'acl_mobile_user'
            description: 'Match mobile user agents'
            expression: 'hdr_sub(user-agent)'
            value: 'Mobile'
            enabled: true

        # Create Actions based on ACL conditions
        - name: Create HAProxy Action for custom header
          oxlorg.opnsense.haproxy_action:
            name: 'action_add_api_header'
            description: 'Add custom header for API traffic'
            operator: 'http-request'
            action: 'set-header'
            header_name: 'X-API-Request'
            header_value: 'true'
            acl: ['acl_api_path']
            enabled: true

        # Add Lua scripts for custom logic
        - name: Add HAProxy Lua script
          oxlorg.opnsense.haproxy_lua:
            name: 'custom_routing'
            description: 'Custom routing logic'
            script: "{{ lookup('file', 'haproxy_scripts/routing.lua') }}"
            enabled: true

        # Configure FastCGI application
        - name: Configure HAProxy FastCGI application
          oxlorg.opnsense.haproxy_fcgi:
            name: 'php_app'
            description: 'PHP FastCGI application'
            docroot: '/var/www/html'
            pass_header: ['HTTP_AUTHORIZATION']
            enabled: true

        # Add custom error pages
        - name: Add HAProxy custom error page
          oxlorg.opnsense.haproxy_errorfile:
            name: 'custom_503'
            description: 'Custom 503 error page'
            code: '503'
            content: "{{ lookup('file', 'error_pages/503.html') }}"
            enabled: true

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