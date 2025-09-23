#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (C) 2025, AnsibleGuy <guy@ansibleguy.net>
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

# see: https://docs.opnsense.org/development/api/plugins/haproxy.html

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.handler import \
    module_dependency_error, MODULE_EXCEPTIONS

try:
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.wrapper import module_wrapper
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.defaults.main import \
        OPN_MOD_ARGS, STATE_MOD_ARG, RELOAD_MOD_ARG
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.haproxy_acl import HaproxyAcl

except MODULE_EXCEPTIONS:
    module_dependency_error()


# DOCUMENTATION = 'https://ansible-opnsense.oxl.app/modules/haproxy.html'
# EXAMPLES = 'https://ansible-opnsense.oxl.app/modules/haproxy.html'


def run_module():
    module_args = dict(
        name=dict(
            type='str', required=True,
            description='Name to identify this condition'
        ),
        description=dict(
            type='str', required=False, default=None,
            description='Description for this condition'
        ),
        expression=dict(
            type='str', required=False, default=None,
            description='Select condition type'
        ),
        negate=dict(
            type='bool', required=False, default=False,
            description='Use this to invert the meaning of the expression'
        ),
        case_sensitive=dict(
            type='bool', required=False, default=False,
            description='Enable to make the condition case-sensitive'
        ),
        custom_acl=dict(
            type='str', required=False, default=None,
            description='Specify a HAProxy condition/ACL not supported by the GUI'
        ),
        # Host-related fields
        hdr_beg=dict(
            type='str', required=False, default=None,
            description='HTTP host header starts with string'
        ),
        hdr_end=dict(
            type='str', required=False, default=None,
            description='HTTP host header ends with string'
        ),
        hdr=dict(
            type='str', required=False, default=None,
            description='HTTP host header matches exact string'
        ),
        hdr_reg=dict(
            type='str', required=False, default=None,
            description='HTTP host header matches regular expression'
        ),
        hdr_sub=dict(
            type='str', required=False, default=None,
            description='HTTP host header contains string'
        ),
        # Path-related fields
        path_beg=dict(
            type='str', required=False, default=None,
            description='HTTP request URL path starts with string'
        ),
        path_end=dict(
            type='str', required=False, default=None,
            description='HTTP request URL path ends with string'
        ),
        path=dict(
            type='str', required=False, default=None,
            description='HTTP request URL path matches exact string'
        ),
        path_reg=dict(
            type='str', required=False, default=None,
            description='HTTP request URL path matches regular expression'
        ),
        path_dir=dict(
            type='str', required=False, default=None,
            description='HTTP request URL path contains directory'
        ),
        path_sub=dict(
            type='str', required=False, default=None,
            description='HTTP request URL path contains string'
        ),
        # SSL-related fields
        ssl_c_verify_code=dict(
            type='int', required=False, default=None,
            description='SSL Client certificate verify error result'
        ),
        ssl_c_ca_commonname=dict(
            type='str', required=False, default=None,
            description='SSL Client certificate issued by CA common-name'
        ),
        ssl_hello_type=dict(
            type='str', required=False, default=None,
            description='SSL Hello Type'
        ),
        # Source IP fields
        src=dict(
            type='str', required=False, default=None,
            description='Source IP matches specified IP'
        ),
        src_port=dict(
            type='int', required=False, default=None,
            description='Source IP: TCP source port'
        ),
        src_port_comparison=dict(
            type='str', required=False, default=None,
            description='Source port comparison operator'
        ),
        # Backend-related fields
        nbsrv=dict(
            type='int', required=False, default=None,
            description='Minimum number of usable servers in backend'
        ),
        nbsrv_backend=dict(
            type='str', required=False, default=None,
            description='Backend for server count check'
        ),
        # SNI fields
        ssl_fc_sni=dict(
            type='str', required=False, default=None,
            description='SNI TLS extension matches (locally deciphered)'
        ),
        ssl_sni=dict(
            type='str', required=False, default=None,
            description='SNI TLS extension matches (TCP request content inspection)'
        ),
        ssl_sni_sub=dict(
            type='str', required=False, default=None,
            description='SNI TLS extension contains (TCP request content inspection)'
        ),
        ssl_sni_beg=dict(
            type='str', required=False, default=None,
            description='SNI TLS extension starts with (TCP request content inspection)'
        ),
        ssl_sni_end=dict(
            type='str', required=False, default=None,
            description='SNI TLS extension ends with (TCP request content inspection)'
        ),
        ssl_sni_reg=dict(
            type='str', required=False, default=None,
            description='SNI TLS extension regex (TCP request content inspection)'
        ),
        # Custom header fields
        cust_hdr_beg_name=dict(
            type='str', required=False, default=None,
            description='Custom HTTP header name for starts with condition'
        ),
        cust_hdr_beg=dict(
            type='str', required=False, default=None,
            description='HTTP Header starts with string'
        ),
        cust_hdr_end_name=dict(
            type='str', required=False, default=None,
            description='Custom HTTP header name for ends with condition'
        ),
        cust_hdr_end=dict(
            type='str', required=False, default=None,
            description='HTTP Header ends with string'
        ),
        cust_hdr_name=dict(
            type='str', required=False, default=None,
            description='Custom HTTP header name for exact match condition'
        ),
        cust_hdr=dict(
            type='str', required=False, default=None,
            description='HTTP Header matches exact string'
        ),
        cust_hdr_reg_name=dict(
            type='str', required=False, default=None,
            description='Custom HTTP header name for regex condition'
        ),
        cust_hdr_reg=dict(
            type='str', required=False, default=None,
            description='HTTP Header matches regular expression'
        ),
        cust_hdr_sub_name=dict(
            type='str', required=False, default=None,
            description='Custom HTTP header name for contains condition'
        ),
        cust_hdr_sub=dict(
            type='str', required=False, default=None,
            description='HTTP Header contains string'
        ),
        # URL parameter fields
        url_param=dict(
            type='str', required=False, default=None,
            description='URL parameter name'
        ),
        url_param_value=dict(
            type='str', required=False, default=None,
            description='URL parameter value'
        ),
        # Auth fields
        allowed_users=dict(
            type='list', required=False, default=None,
            description='Select one or more users for HTTP Basic Auth'
        ),
        allowed_groups=dict(
            type='list', required=False, default=None,
            description='Select one or more groups for HTTP Basic Auth'
        ),
        # Source IP metrics with comparisons
        src_bytes_in_rate_comparison=dict(
            type='str', required=False, default=None,
            description='Source IP incoming bytes rate comparison operator (gt/ge/eq/lt/le)'
        ),
        src_bytes_in_rate=dict(
            type='int', required=False, default=None,
            description='Source IP incoming bytes rate threshold'
        ),
        src_bytes_out_rate_comparison=dict(
            type='str', required=False, default=None,
            description='Source IP outgoing bytes rate comparison operator (gt/ge/eq/lt/le)'
        ),
        src_bytes_out_rate=dict(
            type='int', required=False, default=None,
            description='Source IP outgoing bytes rate threshold'
        ),
        src_conn_cnt_comparison=dict(
            type='str', required=False, default=None,
            description='Source IP connection count comparison operator (gt/ge/eq/lt/le)'
        ),
        src_conn_cnt=dict(
            type='int', required=False, default=None,
            description='Source IP cumulative number of connections threshold'
        ),
        src_conn_cur_comparison=dict(
            type='str', required=False, default=None,
            description='Source IP current connections comparison operator (gt/ge/eq/lt/le)'
        ),
        src_conn_cur=dict(
            type='int', required=False, default=None,
            description='Source IP concurrent connections threshold'
        ),
        src_conn_rate_comparison=dict(
            type='str', required=False, default=None,
            description='Source IP connection rate comparison operator (gt/ge/eq/lt/le)'
        ),
        src_conn_rate=dict(
            type='int', required=False, default=None,
            description='Source IP connection rate threshold'
        ),
        src_http_err_cnt_comparison=dict(
            type='str', required=False, default=None,
            description='Source IP HTTP error count comparison operator (gt/ge/eq/lt/le)'
        ),
        src_http_err_cnt=dict(
            type='int', required=False, default=None,
            description='Source IP cumulative number of HTTP errors threshold'
        ),
        src_http_err_rate_comparison=dict(
            type='str', required=False, default=None,
            description='Source IP HTTP error rate comparison operator (gt/ge/eq/lt/le)'
        ),
        src_http_err_rate=dict(
            type='int', required=False, default=None,
            description='Source IP rate of HTTP errors threshold'
        ),
        src_http_req_cnt_comparison=dict(
            type='str', required=False, default=None,
            description='Source IP HTTP request count comparison operator (gt/ge/eq/lt/le)'
        ),
        src_http_req_cnt=dict(
            type='int', required=False, default=None,
            description='Source IP number of HTTP requests threshold'
        ),
        src_http_req_rate_comparison=dict(
            type='str', required=False, default=None,
            description='Source IP HTTP request rate comparison operator (gt/ge/eq/lt/le)'
        ),
        src_http_req_rate=dict(
            type='int', required=False, default=None,
            description='Source IP rate of HTTP requests threshold'
        ),
        src_kbytes_in_comparison=dict(
            type='str', required=False, default=None,
            description='Source IP kilobytes in comparison operator (gt/ge/eq/lt/le)'
        ),
        src_kbytes_in=dict(
            type='int', required=False, default=None,
            description='Source IP amount of data received in kilobytes threshold'
        ),
        src_kbytes_out_comparison=dict(
            type='str', required=False, default=None,
            description='Source IP kilobytes out comparison operator (gt/ge/eq/lt/le)'
        ),
        src_kbytes_out=dict(
            type='int', required=False, default=None,
            description='Source IP amount of data sent in kilobytes threshold'
        ),
        src_sess_cnt_comparison=dict(
            type='str', required=False, default=None,
            description='Source IP session count comparison operator (gt/ge/eq/lt/le)'
        ),
        src_sess_cnt=dict(
            type='int', required=False, default=None,
            description='Source IP cumulative number of sessions threshold'
        ),
        src_sess_rate_comparison=dict(
            type='str', required=False, default=None,
            description='Source IP session rate comparison operator (gt/ge/eq/lt/le)'
        ),
        src_sess_rate=dict(
            type='int', required=False, default=None,
            description='Source IP session rate threshold'
        ),
        **STATE_MOD_ARG,
        **RELOAD_MOD_ARG,
        **OPN_MOD_ARGS,
    )

    result = dict(
        changed=False,
        diff={
            'before': {},
            'after': {},
        }
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
    )

    module_wrapper(HaproxyAcl(module=module, result=result))

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()