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

ansibleguy.opnsense.haproxy_acl
=================================

Manages HAProxy Access Control Lists for traffic filtering and condition matching.

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "name","string","true","\-","\-","Name to identify this condition"
    "description","string","false","\-","\-","Description for this condition"
    "expression","string","false","\-","\-","Select condition type"
    "negate","boolean","false","false","\-","Use this to invert the meaning of the expression"
    "case_sensitive","boolean","false","false","\-","Enable to make the condition case-sensitive"
    "custom_acl","string","false","\-","\-","Specify a HAProxy condition/ACL not supported by the GUI"
    "hdr_beg","string","false","\-","\-","HTTP host header starts with string"
    "hdr_end","string","false","\-","\-","HTTP host header ends with string"
    "hdr","string","false","\-","\-","HTTP host header matches exact string"
    "hdr_reg","string","false","\-","\-","HTTP host header matches regular expression"
    "hdr_sub","string","false","\-","\-","HTTP host header contains string"
    "path_beg","string","false","\-","\-","HTTP request URL path starts with string"
    "path_end","string","false","\-","\-","HTTP request URL path ends with string"
    "path","string","false","\-","\-","HTTP request URL path matches exact string"
    "path_reg","string","false","\-","\-","HTTP request URL path matches regular expression"
    "path_dir","string","false","\-","\-","HTTP request URL path contains directory"
    "path_sub","string","false","\-","\-","HTTP request URL path contains string"
    "ssl_c_verify_code","integer","false","\-","\-","SSL Client certificate verify error result"
    "ssl_c_ca_commonname","string","false","\-","\-","SSL Client certificate issued by CA common-name"
    "ssl_hello_type","string","false","\-","\-","SSL Hello Type"
    "src","string","false","\-","\-","Source IP matches specified IP"
    "src_port","integer","false","\-","\-","Source IP: TCP source port"
    "src_port_comparison","string","false","\-","\-","Source port comparison operator"
    "nbsrv","integer","false","\-","\-","Minimum number of usable servers in backend"
    "nbsrv_backend","string","false","\-","\-","Backend for server count check"
    "ssl_fc_sni","string","false","\-","\-","SNI TLS extension matches (locally deciphered)"
    "ssl_sni","string","false","\-","\-","SNI TLS extension matches (TCP request content inspection)"
    "ssl_sni_sub","string","false","\-","\-","SNI TLS extension contains (TCP request content inspection)"
    "ssl_sni_beg","string","false","\-","\-","SNI TLS extension starts with (TCP request content inspection)"
    "ssl_sni_end","string","false","\-","\-","SNI TLS extension ends with (TCP request content inspection)"
    "ssl_sni_reg","string","false","\-","\-","SNI TLS extension regex (TCP request content inspection)"
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
      ansibleguy.opnsense.haproxy_acl:
        name: 'acl_api_domain'
        description: 'API domain filter'
        expression: 'hdr'
        hdr: 'api.example.com'

----

.. _haproxy_action:

ansibleguy.opnsense.haproxy_action
====================================

Manages HAProxy Actions that execute when ACL conditions are met.

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "name","string","true","\-","\-","Name to identify this rule"
    "description","string","false","\-","\-","Description for this rule"
    "test_type","string","false","\-","\-","Choose how to test. By using IF it tests if the condition evaluates to true"
    "linked_acls","list","false","\-","\-","Select one or more conditions to be used for this rule"
    "operator","string","false","\-","\-","Choose a logical operator"
    "type","string","false","\-","\-","Choose a HAProxy function that should be executed if the condition evaluates to true"
    "use_backend","string","false","\-","\-","HAProxy will use this backend pool if the condition evaluates to true"
    "use_server","string","false","\-","\-","HAProxy will use this server instead of other servers that are specified in the Backend Pool"
    "custom_rule","string","false","\-","\-","Custom rule (option pass-through)"
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
    "http_request_set_var_scope","string","false","\-","\-","HTTP request set-var scope (proc/sess/txn/req/res)"
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
    "http_response_set_status_code","integer","false","\-","\-","HTTP response status code (100-999)"
    "http_response_set_status_reason","string","false","\-","\-","HTTP response status reason"
    "http_response_set_var_scope","string","false","\-","\-","HTTP response set-var scope (proc/sess/txn/req/res)"
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
      ansibleguy.opnsense.haproxy_action:
        name: 'action_allow_api'
        description: 'Allow API access'
        test_type: 'if'
        linked_acls: ['acl_api_domain']
        type: 'http-request_allow'


See also: :ref:`modules_haproxy_general` and :ref:`troubleshooting <troubleshooting>`