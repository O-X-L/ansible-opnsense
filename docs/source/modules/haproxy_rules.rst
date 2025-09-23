.. _modules_haproxy_rules:

.. include:: ../_include/head.rst

========================================
HAProxy access control & traffic rules
========================================

**STATE**: stable

**COMPATIBILITY**: OPNsense 24.1+

**TESTS**:
`ACL <https://github.com/O-X-L/ansible_opnsense/blob/latest/tests/haproxy_acl.yml>`_ |
`Action <https://github.com/O-X-L/ansible_opnsense/blob/latest/tests/haproxy_action.yml>`_ |

**API Docs**: `HAProxy <https://docs.opnsense.org/development/api/plugins/haproxy.html>`_

**HAProxy Docs**: `ACL <https://www.haproxy.com/documentation/haproxy-configuration-tutorials/proxying-essentials/custom-rules/acls/>`_

These modules manage HAProxy Access Control Lists (ACLs) and Actions for traffic filtering and rule-based processing.

----

.. _haproxy_acl:

ansibleguy.opnsense.haproxy_acl
=================================

Manages HAProxy Access Control Lists (ACLs) for traffic filtering and condition matching.

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "name","string","true","\-","\-","Choose a name for this ACL (must be unique)"
    "description","string","false","\-","\-","You may enter a description here for your reference"
    "expression","string","true","\-","\-","The ACL expression type to evaluate (e.g., hdr, path_beg, src_conn_rate)"
    "negate","boolean","true","false","\-","Negate the ACL condition"
    "case_sensitive","boolean","false","false","\-","Enable case-sensitive matching"
    "hdr","string","false","\-","\-","HTTP Host header value to match (when expression is 'hdr')"
    "hdr_beg","string","false","\-","\-","HTTP Host header starts with value (when expression is 'hdr_beg')"
    "hdr_end","string","false","\-","\-","HTTP Host header ends with value (when expression is 'hdr_end')"
    "path","string","false","\-","\-","HTTP path value to match (when expression is 'path')"
    "path_beg","string","false","\-","\-","HTTP path starts with value (when expression is 'path_beg')"
    "path_end","string","false","\-","\-","HTTP path ends with value (when expression is 'path_end')"
    "cust_hdr_name","string","false","\-","\-","Custom HTTP header name (when expression is 'cust_hdr*')"
    "cust_hdr","string","false","\-","\-","Custom HTTP header value to match"
    "src_conn_rate","integer","false","\-","\-","Source IP connection rate value"
    "src_conn_rate_comparison","string","false","\-","\-","Comparison operator for connection rate (gt, ge, eq, lt, le)"
    "src_http_req_rate","integer","false","\-","\-","Source IP HTTP request rate value"
    "src_http_req_rate_comparison","string","false","\-","\-","Comparison operator for HTTP request rate"
    "allowed_users","list","false","[]","\-","List of user names for HTTP auth ACLs (automatically resolved to UUIDs)"
    "allowed_groups","list","false","[]","\-","List of group names for HTTP auth ACLs (automatically resolved to UUIDs)"

Examples
--------

.. code-block:: yaml

    - name: Create ACL for specific domain
      ansibleguy.opnsense.haproxy_acl:
        name: 'acl_api_domain'
        description: 'Match API domain'
        expression: 'hdr'
        hdr: 'api.example.com'
        negate: false

    - name: Create ACL for API paths
      ansibleguy.opnsense.haproxy_acl:
        name: 'acl_api_path'
        description: 'Match API paths'
        expression: 'path_beg'
        path_beg: '/api/v1'

    - name: Create ACL for rate limiting
      ansibleguy.opnsense.haproxy_acl:
        name: 'acl_rate_limit'
        description: 'Block high connection rate'
        expression: 'src_conn_rate'
        src_conn_rate: 100
        src_conn_rate_comparison: 'gt'

    - name: Create ACL with custom header
      ansibleguy.opnsense.haproxy_acl:
        name: 'acl_api_key'
        description: 'Check API key header'
        expression: 'cust_hdr'
        cust_hdr_name: 'X-API-Key'
        cust_hdr: 'secret123'
        case_sensitive: true

    - name: Create multiple ACLs for traffic filtering
      ansibleguy.opnsense.haproxy_acl:
        name: "{{ item.name }}"
        description: "{{ item.description }}"
        expression: "{{ item.expression }}"
        "{{ item.field }}": "{{ item.value }}"
        negate: "{{ item.negate | default(false) }}"
      loop:
        - {name: 'acl_admin_domain', description: 'Admin domain', expression: 'hdr', field: 'hdr', value: 'admin.example.com'}
        - {name: 'acl_mobile_path', description: 'Mobile paths', expression: 'path_beg', field: 'path_beg', value: '/mobile'}
        - {name: 'acl_blocked_ips', description: 'Blocked source IPs', expression: 'src', field: 'src', value: '192.168.1.100'}

----

.. _haproxy_action:

ansibleguy.opnsense.haproxy_action
====================================

Manages HAProxy Actions that execute when ACL conditions are met.

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "name","string","true","\-","\-","Choose a name for this action (must be unique)"
    "description","string","false","\-","\-","You may enter a description here for your reference"
    "test_type","string","true","if","\-","Test condition type (if or unless)"
    "linked_acls","list","false","[]","\-","List of ACL names to link (automatically resolved to UUIDs)"
    "operator","string","false","and","\-","Logical operator for multiple ACLs (and or or)"
    "type","string","true","\-","\-","Action type to execute (e.g., http-request_deny, http-request_add-header)"
    "http_request_add_header_name","string","false","\-","\-","HTTP request header name to add"
    "http_request_add_header_content","string","false","\-","\-","HTTP request header content to add"
    "http_request_set_header_name","string","false","\-","\-","HTTP request header name to set"
    "http_request_set_header_content","string","false","\-","\-","HTTP request header content to set"
    "http_request_del_header_name","string","false","\-","\-","HTTP request header name to delete"
    "http_request_set_var_scope","string","false","\-","\-","Variable scope for set-var actions (proc/sess/txn/req/res)"
    "http_request_set_var_name","string","false","\-","\-","Variable name for set-var actions"
    "http_request_set_var_expr","string","false","\-","\-","Variable expression for set-var actions"
    "use_backend","string","false","\-","\-","Backend name to use (for use_backend actions)"
    "use_server","string","false","\-","\-","Server name to use (for use_server actions)"

Examples
--------

.. code-block:: yaml

    - name: Create deny action
      ansibleguy.opnsense.haproxy_action:
        name: 'action_deny_bots'
        description: 'Deny bot traffic'
        test_type: 'if'
        linked_acls: ['acl_bot_user_agent']
        type: 'http-request_deny'

    - name: Add security header action
      ansibleguy.opnsense.haproxy_action:
        name: 'action_add_security'
        description: 'Add security headers'
        test_type: 'if'
        type: 'http-request_add-header'
        http_request_add_header_name: 'X-Rate-Limited'
        http_request_add_header_content: 'true'

    - name: Set authentication variable
      ansibleguy.opnsense.haproxy_action:
        name: 'action_set_auth'
        description: 'Mark authenticated requests'
        test_type: 'if'
        linked_acls: ['acl_valid_token']
        type: 'http-request_set-var'
        http_request_set_var_scope: 'txn'
        http_request_set_var_name: 'authenticated'
        http_request_set_var_expr: 'str(true)'

    - name: Create complex action with multiple ACLs
      ansibleguy.opnsense.haproxy_action:
        name: 'action_rate_limit'
        description: 'Rate limit high traffic'
        test_type: 'if'
        linked_acls: ['acl_high_rate', 'acl_api_path']
        operator: 'or'
        type: 'http-request_add-header'
        http_request_add_header_name: 'X-Rate-Limited'
        http_request_add_header_content: 'true'

----

Traffic filtering scenarios
****************************

Basic traffic control
----------------------

Set up basic traffic filtering with ACLs and Actions:

.. code-block:: yaml

    - name: Setup basic traffic filtering
      hosts: opnsense
      tasks:
        # Create ACLs for different traffic types
        - name: Create traffic filtering ACLs
          ansibleguy.opnsense.haproxy_acl:
            name: "{{ item.name }}"
            description: "{{ item.description }}"
            expression: "{{ item.expression }}"
            "{{ item.field }}": "{{ item.value }}"
            negate: "{{ item.negate | default(false) }}"
          loop:
            - {name: 'acl_api_traffic', description: 'API traffic', expression: 'path_beg', field: 'path_beg', value: '/api'}
            - {name: 'acl_admin_section', description: 'Admin section', expression: 'path_beg', field: 'path_beg', value: '/admin'}
            - {name: 'acl_mobile_app', description: 'Mobile app', expression: 'hdr', field: 'hdr', value: 'mobile.example.com'}

        # Create actions for traffic control
        - name: Create traffic control actions
          ansibleguy.opnsense.haproxy_action:
            name: "{{ item.name }}"
            description: "{{ item.description }}"
            test_type: "{{ item.test_type }}"
            linked_acls: "{{ item.acls }}"
            type: "{{ item.type }}"
          loop:
            - {name: 'action_allow_api', description: 'Allow API access', test_type: 'if', acls: ['acl_api_traffic'], type: 'http-request_allow'}
            - {name: 'action_deny_admin', description: 'Deny admin access', test_type: 'if', acls: ['acl_admin_section'], type: 'http-request_deny'}
            - {name: 'action_mobile_backend', description: 'Route mobile to backend', test_type: 'if', acls: ['acl_mobile_app'], type: 'use_backend'}

Rate limiting implementation
----------------------------

Implement rate limiting using source metrics:

.. code-block:: yaml

    - name: Rate limiting configuration
      hosts: opnsense
      tasks:
        # Create rate limiting ACLs
        - name: Create rate limiting ACLs
          ansibleguy.opnsense.haproxy_acl:
            name: "{{ item.name }}"
            description: "{{ item.description }}"
            expression: "{{ item.expression }}"
            "{{ item.rate_field }}": "{{ item.rate_value }}"
            "{{ item.comparison_field }}": "{{ item.comparison }}"
          loop:
            - {name: 'acl_conn_rate_high', description: 'High connection rate', expression: 'src_conn_rate',
               rate_field: 'src_conn_rate', rate_value: 100, comparison_field: 'src_conn_rate_comparison', comparison: 'gt'}
            - {name: 'acl_http_req_rate_high', description: 'High HTTP request rate', expression: 'src_http_req_rate',
               rate_field: 'src_http_req_rate', rate_value: 50, comparison_field: 'src_http_req_rate_comparison', comparison: 'ge'}

        # Create rate limiting actions
        - name: Create rate limiting actions
          ansibleguy.opnsense.haproxy_action:
            name: "{{ item.name }}"
            description: "{{ item.description }}"
            test_type: 'if'
            linked_acls: "{{ item.acls }}"
            type: "{{ item.type }}"
            "{{ item.action_field }}": "{{ item.action_value }}"
          loop:
            - {name: 'action_rate_limit_header', description: 'Add rate limit header', acls: ['acl_conn_rate_high'],
               type: 'http-request_add-header', action_field: 'http_request_add_header_name', action_value: 'X-Rate-Limited'}
            - {name: 'action_deny_high_rate', description: 'Deny high rate requests', acls: ['acl_http_req_rate_high'],
               type: 'http-request_deny'}

Authentication-based access control
------------------------------------

Configure authentication-based access control:

.. code-block:: yaml

    - name: Authentication-based access control
      hosts: opnsense
      vars:
        api_users: ['api_user1', 'api_user2']
        admin_groups: ['administrators', 'super_admins']
      tasks:
        # Create authentication ACLs
        - name: Create authentication ACLs
          ansibleguy.opnsense.haproxy_acl:
            name: 'acl_api_auth'
            description: 'API user authentication'
            expression: 'http_auth'
            allowed_users: "{{ api_users }}"  # Automatically resolved to UUIDs

        - name: Create admin group ACL
          ansibleguy.opnsense.haproxy_acl:
            name: 'acl_admin_auth'
            description: 'Admin group authentication'
            expression: 'http_auth'
            allowed_groups: "{{ admin_groups }}"  # Automatically resolved to UUIDs

        # Create authentication actions
        - name: Create authentication actions
          ansibleguy.opnsense.haproxy_action:
            name: "{{ item.name }}"
            description: "{{ item.description }}"
            test_type: "{{ item.test_type }}"
            linked_acls: "{{ item.acls }}"
            type: "{{ item.type }}"
          loop:
            - {name: 'action_api_allow', description: 'Allow API users', test_type: 'if', acls: ['acl_api_auth'], type: 'http-request_allow'}
            - {name: 'action_admin_allow', description: 'Allow admin groups', test_type: 'if', acls: ['acl_admin_auth'], type: 'http-request_allow'}

----

Advanced rule combinations
***************************

Complex multi-condition rules
------------------------------

Create complex rules combining multiple ACLs:

.. code-block:: yaml

    - name: Complex multi-condition rules
      hosts: opnsense
      tasks:
        # Create multiple condition ACLs
        - name: Create condition ACLs
          ansibleguy.opnsense.haproxy_acl:
            name: "{{ item.name }}"
            description: "{{ item.description }}"
            expression: "{{ item.expression }}"
            "{{ item.field }}": "{{ item.value }}"
          loop:
            - {name: 'acl_production_domain', description: 'Production domain', expression: 'hdr', field: 'hdr', value: 'prod.example.com'}
            - {name: 'acl_maintenance_path', description: 'Maintenance path', expression: 'path_beg', field: 'path_beg', value: '/maintenance'}
            - {name: 'acl_internal_source', description: 'Internal source IP', expression: 'src', field: 'src', value: '10.0.0.0/8'}

        # Create complex combined actions
        - name: Create complex actions with OR conditions
          ansibleguy.opnsense.haproxy_action:
            name: 'action_maintenance_access'
            description: 'Allow maintenance access from internal IPs OR maintenance path'
            test_type: 'if'
            linked_acls: ['acl_internal_source', 'acl_maintenance_path']
            operator: 'or'
            type: 'http-request_allow'

        - name: Create complex actions with AND conditions
          ansibleguy.opnsense.haproxy_action:
            name: 'action_prod_internal_only'
            description: 'Production access only from internal IPs'
            test_type: 'if'
            linked_acls: ['acl_production_domain', 'acl_internal_source']
            operator: 'and'
            type: 'http-request_allow'

Header manipulation rules
-------------------------

Advanced header manipulation for security and tracking:

.. code-block:: yaml

    - name: Header manipulation rules
      hosts: opnsense
      tasks:
        # Create header-based ACLs
        - name: Create header ACLs
          ansibleguy.opnsense.haproxy_acl:
            name: "{{ item.name }}"
            description: "{{ item.description }}"
            expression: "{{ item.expression }}"
            "{{ item.header_name_field }}": "{{ item.header_name }}"
            "{{ item.header_value_field }}": "{{ item.header_value }}"
            case_sensitive: "{{ item.case_sensitive | default(false) }}"
          loop:
            - {name: 'acl_api_key_header', description: 'Valid API key', expression: 'cust_hdr',
               header_name_field: 'cust_hdr_name', header_name: 'X-API-Key',
               header_value_field: 'cust_hdr', header_value: 'valid-key-123', case_sensitive: true}
            - {name: 'acl_mobile_user_agent', description: 'Mobile user agent', expression: 'cust_hdr',
               header_name_field: 'cust_hdr_name', header_name: 'User-Agent',
               header_value_field: 'cust_hdr_sub', header_value: 'Mobile'}

        # Create header manipulation actions
        - name: Create header manipulation actions
          ansibleguy.opnsense.haproxy_action:
            name: "{{ item.name }}"
            description: "{{ item.description }}"
            test_type: "{{ item.test_type }}"
            linked_acls: "{{ item.acls | default([]) }}"
            type: "{{ item.type }}"
            "{{ item.header_name_field }}": "{{ item.header_name }}"
            "{{ item.header_content_field }}": "{{ item.header_content }}"
          loop:
            - {name: 'action_add_auth_header', description: 'Add authenticated header', test_type: 'if', acls: ['acl_api_key_header'],
               type: 'http-request_add-header', header_name_field: 'http_request_add_header_name', header_name: 'X-Authenticated',
               header_content_field: 'http_request_add_header_content', header_content: 'true'}
            - {name: 'action_add_mobile_header', description: 'Add mobile device header', test_type: 'if', acls: ['acl_mobile_user_agent'],
               type: 'http-request_add-header', header_name_field: 'http_request_add_header_name', header_name: 'X-Device-Type',
               header_content_field: 'http_request_add_header_content', header_content: 'mobile'}

----

Best practices
**************

ACL design principles
---------------------

**Naming conventions**

- Use descriptive, consistent naming patterns
- Include purpose in the name (e.g., acl_rate_limit, acl_api_auth)
- Group related ACLs with common prefixes
- Document complex ACLs thoroughly

**Performance considerations**

- Order ACLs by frequency of matching (most common first)
- Use specific expressions rather than broad regex when possible
- Combine related conditions into single ACLs when appropriate
- Test ACL performance under load

.. code-block:: yaml

    - name: Optimized ACL configuration
      hosts: opnsense
      tasks:
        # Fast-matching ACLs first
        - name: Create performance-optimized ACLs
          ansibleguy.opnsense.haproxy_acl:
            name: "{{ item.name }}"
            description: "{{ item.description }}"
            expression: "{{ item.expression }}"
            "{{ item.field }}": "{{ item.value }}"
          loop:
            # Most frequent matches first
            - {name: 'acl_static_content', description: 'Static content (fast)', expression: 'path_beg', field: 'path_beg', value: '/static'}
            - {name: 'acl_api_endpoints', description: 'API endpoints (medium)', expression: 'path_beg', field: 'path_beg', value: '/api'}
            - {name: 'acl_admin_complex', description: 'Admin complex rules (slow)', expression: 'path_reg', field: 'path_reg', value: '^/admin/.*\\.php$'}

Action chaining strategy
------------------------

**Logical flow design**

- Plan action execution order carefully
- Use meaningful test_type (if/unless) for clarity
- Group related actions logically
- Consider action interdependencies

**Error handling**

- Create fallback actions for edge cases
- Use deny actions as final safeguards
- Log important decision points
- Test negative scenarios

.. code-block:: yaml

    - name: Action chaining best practices
      hosts: opnsense
      tasks:
        # Early security checks
        - name: Create security action chain
          ansibleguy.opnsense.haproxy_action:
            name: "{{ item.name }}"
            description: "{{ item.description }}"
            test_type: "{{ item.test_type }}"
            linked_acls: "{{ item.acls }}"
            type: "{{ item.type }}"
          loop:
            # 1. Rate limiting first
            - {name: 'action_01_rate_check', description: 'Check rate limits', test_type: 'if', acls: ['acl_high_rate'], type: 'http-request_deny'}
            # 2. Authentication second
            - {name: 'action_02_auth_check', description: 'Check authentication', test_type: 'unless', acls: ['acl_authenticated'], type: 'http-request_auth'}
            # 3. Authorization third
            - {name: 'action_03_authz_check', description: 'Check authorization', test_type: 'if', acls: ['acl_authorized'], type: 'http-request_allow'}
            # 4. Final deny as fallback
            - {name: 'action_99_final_deny', description: 'Final fallback deny', test_type: 'if', acls: [], type: 'http-request_deny'}

----

Troubleshooting
***************

ACL resolution issues
---------------------

**User/Group UUID resolution**

The HAProxy ACL module automatically resolves user and group names to UUIDs. If you encounter errors like "User 'username' not found":

1. Verify the user/group exists in HAProxy configuration
2. Check name spelling (case-sensitive)
3. Ensure the user/group is enabled
4. Confirm user/group was created before ACL

**Expression validation**

- Ensure expression matches the field being set
- Verify required fields for each expression type
- Check value formats (IPs, rates, etc.)
- Test expressions individually

Action linking problems
-----------------------

**ACL UUID resolution**

The HAProxy action module automatically resolves ACL names to UUIDs. If you encounter errors like "Related ACL item not found":

1. Create ACLs before referencing them in actions
2. Check ACL name spelling (case-sensitive)
3. Verify ACL configuration is valid
4. Test ACL individually before linking

**Action type compatibility**

- Ensure action type supports configured parameters
- Verify parameter requirements for each action type
- Check parameter value formats and constraints
- Test actions with minimal configuration first

.. code-block:: yaml

    - name: Troubleshooting ACL and Action issues
      hosts: opnsense
      tasks:
        # Validate ACL configuration
        - name: Test ACL creation
          ansibleguy.opnsense.haproxy_acl:
            name: 'test_acl'
            description: 'Test ACL for validation'
            expression: 'hdr'
            hdr: 'test.example.com'
            negate: false

        # Validate action with simple configuration
        - name: Test action creation
          ansibleguy.opnsense.haproxy_action:
            name: 'test_action'
            description: 'Test action for validation'
            test_type: 'if'
            linked_acls: ['test_acl']
            type: 'http-request_allow'

        # Clean up test objects
        - name: Remove test action
          ansibleguy.opnsense.haproxy_action:
            name: 'test_action'
            state: absent

        - name: Remove test ACL
          ansibleguy.opnsense.haproxy_acl:
            name: 'test_acl'
            state: absent

See also: :ref:`troubleshooting <troubleshooting>`