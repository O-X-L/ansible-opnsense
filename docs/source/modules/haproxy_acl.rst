.. _modules_haproxy_acl:

.. include:: ../_include/head.rst

===========
HAProxy ACL
===========

**STATE**: stable

**COMPATIBILITY**: OPNsense 24.1+

**Note**: Most functions should work on earlier OPNsense versions, but full compatibility is tested with OPNsense 24.1+. For compatibility with earlier versions, please check the configuration differences at: `HAProxy Configuration Reference <https://github.com/opnsense/plugins/blob/master/net/haproxy/src/opnsense/mvc/app/models/OPNsense/HAProxy/HAProxy.xml>`_

**TESTS**: `Playbook <https://github.com/O-X-L/ansible_opnsense/blob/latest/tests/haproxy_acl.yml>`_


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

    "name","string","true","\-","\-","ACL name"
    "description","string","false","\-","\-","ACL description"
    "enabled","boolean","false","true","\-","Enable or disable ACL"
    "expression","string","true","\-","\-","ACL expression type. One of: 'http_auth', 'hdr_beg', 'hdr_end', 'hdr', 'hdr_reg', 'hdr_sub', 'path_beg', 'path_end', 'path', 'path_reg', 'path_dir', 'path_sub', 'cust_hdr_beg', 'cust_hdr_end', 'cust_hdr', 'cust_hdr_reg', 'cust_hdr_sub', 'url_param', 'ssl_c_verify', 'ssl_c_verify_code', 'ssl_c_ca_commonname', 'ssl_hello_type', 'src', 'src_is_local', 'src_port', 'src_bytes_in_rate', 'src_bytes_out_rate', 'src_kbytes_in', 'src_kbytes_out', 'src_conn_cnt', 'src_conn_cur', 'src_conn_rate'"
    "value","string","false","\-","\-","ACL match value (required for most expressions, except 'ssl_c_verify', 'src_is_local', and 'http_auth')"
    "negate","boolean","false","false","\-","Negate the ACL condition"
    "case_sensitive","boolean","false","true","\-","Case sensitive matching"
    "allowedUsers","list","false","\-","\-","**NEW**: List of user names for HTTP auth - supports automatic UUID resolution"
    "allowedGroups","list","false","\-","\-","**NEW**: List of group names for HTTP auth - supports automatic UUID resolution"

Usage
*****

This module manages HAProxy Access Control Lists (ACLs) on OPNsense. ACLs allow you to create rules that match client requests based on various criteria such as headers, paths, source IP addresses, SSL properties, and authentication.

Key features:

- **Automatic UUID Resolution**: All relationship fields accept names and automatically resolve to UUIDs
- **Name-based Linking**: Users can specify user names and group names instead of UUIDs
- **UI Compatibility**: All selections appear correctly in the OPNsense web interface
- **Multi-select Support**: Lists support multiple items with proper comma-separated format
- **Flexible expressions**: Support for HTTP headers, paths, SSL properties, source matching, and authentication
- **Authentication ACLs**: Integrate with HAProxy users and groups for HTTP authentication
- **Pattern matching**: Support for regular expressions, case-sensitive/insensitive matching, and negation

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
          target: 'haproxy_acl'

      tasks:
        - name: Create path-based ACL
          ansibleguy.opnsense.haproxy_acl:
            name: 'api_path'
            description: 'Match API paths'
            enabled: true
            expression: 'path_beg'
            value: '/api/'

        - name: Create source IP ACL
          ansibleguy.opnsense.haproxy_acl:
            name: 'internal_ips'
            description: 'Match internal IP addresses'
            enabled: true
            expression: 'src'
            value: '192.168.1.0/24'

        - name: Create HTTP auth ACL with name-based user/group linking
          ansibleguy.opnsense.haproxy_acl:
            name: 'admin_auth'
            description: 'Admin authentication'
            enabled: true
            expression: 'http_auth'
            allowedUsers: ['admin', 'operator', 'superuser']  # Uses user names, not UUIDs
            allowedGroups: ['administrators', 'power_users']  # Uses group names, not UUIDs

        - name: Create SSL client verification ACL
          ansibleguy.opnsense.haproxy_acl:
            name: 'valid_client_cert'
            description: 'Client has valid SSL certificate'
            enabled: true
            expression: 'ssl_c_verify'
            value: '0'  # 0 means certificate is valid

        - name: Create custom header ACL with case-insensitive matching
          ansibleguy.opnsense.haproxy_acl:
            name: 'api_token_present'
            description: 'API token header present'
            enabled: true
            expression: 'cust_hdr'
            value: 'X-API-Token'
            case_sensitive: false

        - name: Create source rate limiting ACL
          ansibleguy.opnsense.haproxy_acl:
            name: 'rate_limited'
            description: 'Source exceeds rate limit'
            enabled: true
            expression: 'src_conn_rate'
            value: '10'

        - name: Create negated path ACL
          ansibleguy.opnsense.haproxy_acl:
            name: 'not_static_content'
            description: 'Not static content paths'
            enabled: true
            expression: 'path_beg'
            value: '/static/'
            negate: true

        - name: Create URL parameter ACL
          ansibleguy.opnsense.haproxy_acl:
            name: 'debug_mode'
            description: 'Debug parameter present'
            enabled: true
            expression: 'url_param'
            value: 'debug'

        - name: Create complex authentication ACL
          ansibleguy.opnsense.haproxy_acl:
            name: 'privileged_access'
            description: 'Privileged user authentication'
            enabled: true
            expression: 'http_auth'
            allowedUsers: ['admin']
            allowedGroups: ['security_team', 'infrastructure_team']

        - name: Remove ACL
          ansibleguy.opnsense.haproxy_acl:
            name: 'old_acl'
            state: 'absent'

        - name: List all ACLs
          ansibleguy.opnsense.list:
          register: haproxy_acls

        - name: Show ACLs
          ansible.builtin.debug:
            var: haproxy_acls.data