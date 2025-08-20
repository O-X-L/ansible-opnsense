.. _modules_haproxy_action:

.. include:: ../_include/head.rst

================
HAProxy - Action
================

**STATE**: stable

**COMPATIBILITY**: OPNsense 24.1+

**Note**: Most functions should work on earlier OPNsense versions, but full compatibility is tested with OPNsense 24.1+. For compatibility with earlier versions, please check the configuration differences at: `HAProxy Configuration Reference <https://github.com/opnsense/plugins/blob/master/net/haproxy/src/opnsense/mvc/app/models/OPNsense/HAProxy/HAProxy.xml>`_

**TESTS**: `Playbook <https://github.com/ansibleguy/collection_opnsense/blob/latest/tests/haproxy_action.yml>`_

**API Docs**: `Core - HAProxy <https://docs.opnsense.org/development/api/core/haproxy.html>`_

**Service Docs**: `HAProxy <https://docs.opnsense.org/manual/how-tos/haproxy.html>`_


Contribution
************

This module was contributed by **MaximeWewer** (@MaximeWewer).

If you encounter any issues or have suggestions for improvements, please feel free to contribute to the project.


Prerequisites
*************

You need to install and configure HAProxy on the target system.

.. include:: ../_include/haproxy.rst

Definition
**********

.. include:: ../_include/param_basic.rst

ansibleguy.opnsense.haproxy_action
***********************************

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "name","string","true","\-","n","Name of the HAProxy action"
    "description","string","false","\-","desc","Description for the action"
    "test_type","string","false","if","\-","Test type for the action. One of: 'if', 'unless'"
    "linked_acls","list","false","\-","acls","**NEW**: List of ACL names to link to this action - supports automatic UUID resolution"
    "operator","string","false","and","\-","Logical operator for multiple ACLs. One of: 'and', 'or'"
    "action_type","string","true","\-","type","Type of action to perform. One of: 'use_backend', 'use_server', 'map_use_backend', 'http-request_*', 'http-response_*', 'tcp-request_*', 'tcp-response_*', 'fcgi_*', 'monitor_fail', 'custom'"
    "use_backend","string","false","\-","backend","**NEW**: Backend name to use (for use_backend action type) - supports automatic UUID resolution"
    "use_server","list","false","\-","servers","**NEW**: List of server names to use (for use_server action type) - supports automatic UUID resolution"
    "http_request_auth","string","false","\-","\-","HTTP request authentication config"
    "http_request_redirect","string","false","\-","\-","HTTP request redirect config"
    "http_request_lua","string","false","\-","\-","HTTP request Lua script config"
    "custom_lua","string","false","\-","\-","Custom Lua code"
    "map_use_backend_file","string","false","\-","\-","Map file for backend selection"
    "map_use_backend_default","string","false","\-","\-","**NEW**: Default backend name for map-based selection - supports automatic UUID resolution"

.. include:: ../_include/param_basic_en_state.rst

Usage
*****

This module manages HAProxy actions on OPNsense. Actions define what should be done when certain conditions (defined by ACLs) are met during request processing.

Key features:

- **Automatic UUID Resolution**: All relationship fields accept names and automatically resolve to UUIDs
- **Name-based Linking**: Users can specify ACL names, backend names, and server names instead of UUIDs
- **UI Compatibility**: All selections appear correctly in the OPNsense web interface
- **Multi-select Support**: Lists support multiple items with proper comma-separated format
- **Flexible Action Types**: Support for HTTP requests/responses, TCP requests/responses, backend routing, and custom actions

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
          target: 'haproxy_action'

      tasks:
        - name: Create HTTPS redirect action with name-based ACL linking
          ansibleguy.opnsense.haproxy_action:
            name: 'redirect_to_https'
            description: 'Redirect HTTP to HTTPS'
            action_type: 'http-request_redirect'
            http_request_redirect: 'scheme https'
            test_type: 'unless'
            linked_acls: ['ssl_fc', 'is_secure']  # Uses ACL names, not UUIDs

        - name: Route API requests using name-based backend linking
          ansibleguy.opnsense.haproxy_action:
            name: 'use_api_backend'
            description: 'Route API requests to API backend'
            action_type: 'use_backend'
            use_backend: 'api_backend'  # Uses backend name, not UUID
            linked_acls: ['is_api_request', 'valid_token']

        - name: Load balance to specific servers by name
          ansibleguy.opnsense.haproxy_action:
            name: 'use_priority_servers'
            description: 'Route to priority servers'
            action_type: 'use_server'
            use_server: ['web01', 'web02']  # Uses server names, not UUIDs
            linked_acls: ['high_priority_users']

        - name: Deny blocked IPs with multiple ACL conditions
          ansibleguy.opnsense.haproxy_action:
            name: 'deny_blocked_ips'
            description: 'Deny requests from blocked IP ranges'
            action_type: 'http-request_deny'
            linked_acls: ['blocked_ips', 'suspicious_patterns']
            operator: 'or'  # Match any of the linked ACLs

        - name: Map-based backend selection with default
          ansibleguy.opnsense.haproxy_action:
            name: 'map_backend_routing'
            description: 'Route based on domain mapping'
            action_type: 'map_use_backend'
            map_use_backend_file: 'domain_backend_map'
            map_use_backend_default: 'default_backend'  # Uses backend name
            linked_acls: ['valid_domain']

        - name: Complex authentication action
          ansibleguy.opnsense.haproxy_action:
            name: 'require_admin_auth'
            description: 'Require authentication for admin pages'
            action_type: 'http-request_auth'
            http_request_auth: 'realm admin'
            test_type: 'if'
            linked_acls: ['admin_path', 'not_authenticated']
            operator: 'and'

        - name: Custom Lua processing
          ansibleguy.opnsense.haproxy_action:
            name: 'custom_processing'
            description: 'Custom request processing'
            action_type: 'http-request_lua'
            http_request_lua: 'process_request'
            custom_lua: |
              -- Custom Lua code here
              core.Debug("Processing custom request")
            linked_acls: ['needs_processing']

        - name: List all actions
          ansibleguy.opnsense.list:
          register: haproxy_actions

        - name: Show actions
          ansible.builtin.debug:
            var: haproxy_actions.data
