.. _modules_haproxy_rules:

.. include:: ../_include/head.rst

================================
HAProxy traffic control modules
================================

**STATE**: unstable

**COMPATIBILITY**: OPNsense 24.1+

**TESTS**:
`ACL <https://github.com/O-X-L/ansible_opnsense/blob/latest/tests/haproxy_acl.yml>`_ |
`Action <https://github.com/O-X-L/ansible_opnsense/blob/latest/tests/haproxy_action.yml>`_

**API Docs**: `HAProxy <https://docs.opnsense.org/development/api/plugins/haproxy.html>`_

These modules manage HAProxy traffic control through ACLs (Access Control Lists) and Actions.

----

.. _haproxy_acl:

oxlorg.opnsense.haproxy_acl
===========================

Manages HAProxy Access Control Lists for traffic filtering and condition matching.

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "name","string","true","\-","\-","Name to identify this condition"
    "description","string","false","\-","\-","Description for this condition"
    "expression","string","false","\-","\-","Choose condition type. Options: hdr_beg, hdr_end, hdr, hdr_reg, hdr_sub, path_beg, path_end, path, path_reg, path_dir, path_sub, ssl_c_verify, ssl_c_ca_commonname, ssl_hello_type, src, src_port, nbsrv, ssl_fc_sni, ssl_sni, ssl_sni_sub, ssl_sni_beg, ssl_sni_end, ssl_sni_reg, cust_hdr_beg, cust_hdr_end, cust_hdr, cust_hdr_reg, cust_hdr_sub, url_param, auth, src_bytes_in_rate, src_bytes_out_rate, src_conn_cnt, src_conn_cur, src_conn_rate, src_http_err_cnt, src_http_err_rate, src_http_req_cnt, src_http_req_rate, src_kbytes_in, src_kbytes_out, src_sess_cnt, src_sess_rate, custom"
    "negate","boolean","false","false","\-","Negate the condition. Use this to invert the meaning of the expression"
    "case_sensitive","boolean","false","false","\-","Use to make condition case-sensitive. Enable to make the condition case-sensitive"
    "custom_acl","string","false","\-","\-","Custom ACL expression. Specify a HAProxy condition/ACL not supported by the GUI"
    "hdr_beg","string","false","\-","\-","HTTP host header begins with value. The Host header starts with the specified string"
    "hdr_end","string","false","\-","\-","HTTP host header ends with value. The Host header ends with the specified string"
    "hdr","string","false","\-","\-","HTTP host header exact match. The Host header matches the specified string exactly"
    "hdr_reg","string","false","\-","\-","HTTP host header regex pattern. The Host header matches the specified regular expression"
    "hdr_sub","string","false","\-","\-","HTTP host header substring match. The Host header contains the specified substring"
    "path_beg","string","false","\-","\-","HTTP URL path begins with value. The request URL path starts with the specified string"
    "path_end","string","false","\-","\-","HTTP URL path ends with value. The request URL path ends with the specified string"
    "path","string","false","\-","\-","HTTP URL path exact match. The request URL path matches the specified string exactly"
    "path_reg","string","false","\-","\-","HTTP URL path regex pattern. The request URL path matches the specified regular expression"
    "path_dir","string","false","\-","\-","HTTP URL path directory match. The request URL path contains the specified directory path"
    "path_sub","string","false","\-","\-","HTTP URL path substring match. The request URL path contains the specified substring"
    "ssl_c_verify_code","integer","false","\-","\-","SSL client certificate verify error code. Match SSL client certificate verify error result (0-8)"
    "ssl_c_ca_commonname","string","false","\-","\-","SSL client certificate CA common name. Match SSL client certificate issued by specified CA common-name"
    "ssl_hello_type","string","false","\-","\-","SSL hello type. Match SSL handshake hello type (1=client hello, 2=server hello, 3=hello request)"
    "src","string","false","\-","\-","Source IP address or network. Match source IP address or CIDR network range"
    "src_port","integer","false","\-","\-","Source TCP port number. Match source TCP port (1-65535)"
    "src_port_comparison","string","false","\-","\-","Source port comparison operator (gt, ge, eq, lt, le). Choose comparison operator for source port"
    "nbsrv","integer","false","\-","\-","Minimum usable servers count. Match minimum number of usable servers in the specified backend"
    "nbsrv_backend","string","false","\-","\-","Backend name for server count check. Backend to check for minimum number of usable servers"
    "ssl_fc_sni","string","false","\-","\-","SSL/TLS SNI server name (frontend connection). Match SNI TLS extension (locally deciphered)"
    "ssl_sni","string","false","\-","\-","SSL/TLS SNI server name (request inspection). Match SNI TLS extension via TCP request content inspection"
    "ssl_sni_sub","string","false","\-","\-","SSL/TLS SNI substring match. SNI TLS extension contains substring via TCP request content inspection"
    "ssl_sni_beg","string","false","\-","\-","SSL/TLS SNI prefix match. SNI TLS extension starts with value via TCP request content inspection"
    "ssl_sni_end","string","false","\-","\-","SSL/TLS SNI suffix match. SNI TLS extension ends with value via TCP request content inspection"
    "ssl_sni_reg","string","false","\-","\-","SSL/TLS SNI regex pattern. SNI TLS extension matches regex via TCP request content inspection"
    "cust_hdr_beg_name","string","false","\-","\-","Custom HTTP header name for starts with condition"
    "cust_hdr_beg","string","false","\-","\-","HTTP Header starts with string"
    "cust_hdr_end_name","string","false","\-","\-","Custom HTTP header name for ends with condition"
    "cust_hdr_end","string","false","\-","\-","HTTP Header ends with string"
    "cust_hdr_name","string","false","\-","\-","Custom HTTP header name for exact match condition"
    "cust_hdr","string","false","\-","\-","HTTP Header matches exact string"
    "cust_hdr_reg_name","string","false","\-","\-","Custom HTTP header name for regex condition"
    "cust_hdr_reg","string","false","\-","\-","HTTP Header matches regular expression"
    "cust_hdr_sub_name","string","false","\-","\-","Custom HTTP header name for contains condition"
    "cust_hdr_sub","string","false","\-","\-","HTTP Header contains string"
    "url_param","string","false","\-","\-","URL parameter name"
    "url_param_value","string","false","\-","\-","URL parameter value"
    "allowed_users","list","false","\-","\-","Select one or more users for HTTP Basic Auth"
    "allowed_groups","list","false","\-","\-","Select one or more groups for HTTP Basic Auth"
    "src_bytes_in_rate_comparison","string","false","\-","\-","Source IP incoming bytes rate comparison operator (gt/ge/eq/lt/le)"
    "src_bytes_in_rate","integer","false","\-","\-","Source IP incoming bytes rate threshold"
    "src_bytes_out_rate_comparison","string","false","\-","\-","Source IP outgoing bytes rate comparison operator (gt/ge/eq/lt/le)"
    "src_bytes_out_rate","integer","false","\-","\-","Source IP outgoing bytes rate threshold"
    "src_conn_cnt_comparison","string","false","\-","\-","Source IP connection count comparison operator (gt/ge/eq/lt/le)"
    "src_conn_cnt","integer","false","\-","\-","Source IP cumulative number of connections threshold"
    "src_conn_cur_comparison","string","false","\-","\-","Source IP current connections comparison operator (gt/ge/eq/lt/le)"
    "src_conn_cur","integer","false","\-","\-","Source IP concurrent connections threshold"
    "src_conn_rate_comparison","string","false","\-","\-","Source IP connection rate comparison operator (gt/ge/eq/lt/le)"
    "src_conn_rate","integer","false","\-","\-","Source IP connection rate threshold"
    "src_http_err_cnt_comparison","string","false","\-","\-","Source IP HTTP error count comparison operator (gt/ge/eq/lt/le)"
    "src_http_err_cnt","integer","false","\-","\-","Source IP cumulative number of HTTP errors threshold"
    "src_http_err_rate_comparison","string","false","\-","\-","Source IP HTTP error rate comparison operator (gt/ge/eq/lt/le)"
    "src_http_err_rate","integer","false","\-","\-","Source IP rate of HTTP errors threshold"
    "src_http_req_cnt_comparison","string","false","\-","\-","Source IP HTTP request count comparison operator (gt/ge/eq/lt/le)"
    "src_http_req_cnt","integer","false","\-","\-","Source IP number of HTTP requests threshold"
    "src_http_req_rate_comparison","string","false","\-","\-","Source IP HTTP request rate comparison operator (gt/ge/eq/lt/le)"
    "src_http_req_rate","integer","false","\-","\-","Source IP rate of HTTP requests threshold"
    "src_kbytes_in_comparison","string","false","\-","\-","Source IP kilobytes in comparison operator (gt/ge/eq/lt/le)"
    "src_kbytes_in","integer","false","\-","\-","Source IP amount of data received in kilobytes threshold"
    "src_kbytes_out_comparison","string","false","\-","\-","Source IP kilobytes out comparison operator (gt/ge/eq/lt/le)"
    "src_kbytes_out","integer","false","\-","\-","Source IP amount of data sent in kilobytes threshold"
    "src_sess_cnt_comparison","string","false","\-","\-","Source IP session count comparison operator (gt/ge/eq/lt/le)"
    "src_sess_cnt","integer","false","\-","\-","Source IP cumulative number of sessions threshold"
    "src_sess_rate_comparison","string","false","\-","\-","Source IP session rate comparison operator (gt/ge/eq/lt/le)"
    "src_sess_rate","integer","false","\-","\-","Source IP session rate threshold"

Examples
--------

.. code-block:: yaml

    - name: Create ACL for API domain
      oxlorg.opnsense.haproxy_acl:
        name: 'acl_api_domain'
        description: 'API domain filter'
        expression: 'hdr'
        hdr: 'api.example.com'

----

.. _haproxy_action:

oxlorg.opnsense.haproxy_action
==============================

Manages HAProxy Actions that execute when ACL conditions are met.

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "name","string","true","\-","\-","Name to identify this rule"
    "description","string","false","\-","\-","Description for this rule"
    "test_type","string","false","\-","\-","Condition test type. Choose how to test the condition. IF [default] tests if condition is true, UNLESS tests if condition is false"
    "linked_acls","list","false","\-","\-","Associated ACL conditions. Select one or more conditions to be used for this rule"
    "operator","string","false","\-","\-","Logical operator for multiple ACLs. Choose a logical operator to combine conditions: AND [default] or OR"
    "type","string","false","\-","\-","HAProxy action type. Select HAProxy action type to execute when condition matches. Options: use_backend, use_server, map_use_backend, fcgi_pass_header, fcgi_set_param, http-request_allow, http-request_deny, http-request_tarpit, http-request_auth, http-request_redirect, http-request_lua, http-request_use-service, http-request_add-header, http-request_set-header, http-request_del-header, http-request_replace-header, http-request_replace-value, http-request_set-path, http-request_set-var, http-response_allow, http-response_deny, http-response_lua, http-response_add-header, http-response_set-header, http-response_del-header, http-response_replace-header, http-response_replace-value, http-response_set-status, http-response_set-var, monitor_fail, tcp-request_connection_accept, tcp-request_connection_reject, tcp-request_content_accept, tcp-request_content_reject, tcp-request_content_lua, tcp-request_content_use-service, tcp-request_inspect-delay, tcp-response_content_accept, tcp-response_content_close, tcp-response_content_reject, tcp-response_content_lua, tcp-response_inspect-delay, custom"
    "use_backend","string","false","\-","\-","Backend pool selection. HAProxy will use this backend pool if the condition evaluates to true"
    "use_server","string","false","\-","\-","Specific server selection. HAProxy will use this server instead of other servers that are specified in the Backend Pool"
    "custom_rule","string","false","\-","\-","Custom HAProxy rule. Custom rule (option pass-through)"
    "fcgi_pass_header","string","false","\-","\-","FastCGI pass-header"
    "fcgi_set_param","string","false","\-","\-","FastCGI set-param"
    "http_request_auth","string","false","\-","\-","HTTP request auth realm"
    "http_request_redirect","string","false","\-","\-","HTTP request redirect location"
    "http_request_lua","string","false","\-","\-","HTTP request lua action"
    "http_request_use_service","string","false","\-","\-","HTTP request lua service"
    "http_request_add_header_name","string","false","\-","\-","HTTP request header name to add"
    "http_request_add_header_content","string","false","\-","\-","HTTP request header content to add"
    "http_request_set_header_name","string","false","\-","\-","HTTP request header name to set"
    "http_request_set_header_content","string","false","\-","\-","HTTP request header content to set"
    "http_request_del_header_name","string","false","\-","\-","HTTP request header name to delete"
    "http_request_replace_header_name","string","false","\-","\-","HTTP request header name to replace"
    "http_request_replace_header_regex","string","false","\-","\-","HTTP request header regex to replace"
    "http_request_replace_value_name","string","false","\-","\-","HTTP request value name to replace"
    "http_request_replace_value_regex","string","false","\-","\-","HTTP request value regex to replace"
    "http_request_set_path","string","false","\-","\-","HTTP request set-path value"
    "http_request_set_var_scope","string","false","\-","\-","HTTP request variable scope. Variable scope: proc (whole process), sess (whole session), txn (transaction), req (request only), res (response only)"
    "http_request_set_var_name","string","false","\-","\-","HTTP request set-var name"
    "http_request_set_var_expr","string","false","\-","\-","HTTP request set-var expression"
    "http_response_lua","string","false","\-","\-","HTTP response lua script"
    "http_response_add_header_name","string","false","\-","\-","HTTP response header name to add"
    "http_response_add_header_content","string","false","\-","\-","HTTP response header content to add"
    "http_response_set_header_name","string","false","\-","\-","HTTP response header name to set"
    "http_response_set_header_content","string","false","\-","\-","HTTP response header content to set"
    "http_response_del_header_name","string","false","\-","\-","HTTP response header name to delete"
    "http_response_replace_header_name","string","false","\-","\-","HTTP response header name to replace"
    "http_response_replace_header_regex","string","false","\-","\-","HTTP response header regex to replace"
    "http_response_replace_value_name","string","false","\-","\-","HTTP response value name to replace"
    "http_response_replace_value_regex","string","false","\-","\-","HTTP response value regex to replace"
    "http_response_set_status_code","integer","false","\-","\-","HTTP response status code. HTTP response status code (100-999)"
    "http_response_set_status_reason","string","false","\-","\-","HTTP response status reason"
    "http_response_set_var_scope","string","false","\-","\-","HTTP response variable scope. Variable scope: proc (whole process), sess (whole session), txn (transaction), req (request only), res (response only)"
    "http_response_set_var_name","string","false","\-","\-","HTTP response set-var name"
    "http_response_set_var_expr","string","false","\-","\-","HTTP response set-var expression"
    "tcp_request_content_lua","string","false","\-","\-","TCP request content lua script"
    "tcp_request_content_use_service","string","false","\-","\-","TCP request content use-service"
    "tcp_request_inspect_delay","string","false","\-","\-","TCP request inspect-delay"
    "tcp_response_content_lua","string","false","\-","\-","TCP response content lua script"
    "tcp_response_inspect_delay","string","false","\-","\-","TCP response inspect-delay"
    "monitor_fail_uri","string","false","\-","\-","Monitor fail URI"
    "map_use_backend_file","string","false","\-","\-","Map file for backend selection"
    "map_use_backend_default","string","false","\-","\-","Default backend for map-based selection"

Examples
--------

.. code-block:: yaml

    - name: Create allow action for API
      oxlorg.opnsense.haproxy_action:
        name: 'action_allow_api'
        description: 'Allow API access'
        test_type: 'if'
        linked_acls: ['acl_api_domain']
        type: 'http-request_allow'


See also: :ref:`modules_haproxy <modules_haproxy>` and :ref:`troubleshooting <modules_haproxy_troubleshooting>`
