#!/usr/bin/python

# Copyright: (C) 2025, MaximeWewer
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

"""Module to configure HAProxy ACLs on OPNsense"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.handler import \
    module_dependency_error, MODULE_EXCEPTIONS

try:
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.wrapper import module_wrapper
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.defaults.main import \
        OPN_MOD_ARGS, EN_ONLY_MOD_ARG
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.haproxy_acl import HaproxyAcl

except MODULE_EXCEPTIONS:
    module_dependency_error()


# DOCUMENTATION = 'https://opnsense.ansibleguy.net/en/latest/modules/haproxy.html'
# EXAMPLES = 'https://opnsense.ansibleguy.net/en/latest/modules/haproxy.html'


def run_module():
    """Initiate module execution"""
    module_args = dict(
        name=dict(type='str', required=True),
        description=dict(type='str', required=False),
        expression=dict(
            type='str', required=True,
            choices=[
                'http_auth', 'hdr_beg', 'hdr_end', 'hdr', 'hdr_reg', 'hdr_sub',
                'path_beg', 'path_end', 'path', 'path_reg', 'path_dir', 'path_sub',
                'cust_hdr_beg', 'cust_hdr_end', 'cust_hdr', 'cust_hdr_reg', 'cust_hdr_sub',
                'url_param', 'ssl_c_verify', 'ssl_c_verify_code', 'ssl_c_ca_commonname',
                'ssl_hello_type', 'src', 'src_is_local', 'src_port', 'src_bytes_in_rate',
                'src_bytes_out_rate', 'src_kbytes_in', 'src_kbytes_out', 'src_conn_cnt',
                'src_conn_cur', 'src_conn_rate'
            ]
        ),
        value=dict(type='str', required=False),
        negate=dict(type='bool', required=False, default=False),
        case_sensitive=dict(type='bool', required=False, default=True),
        allowedUsers=dict(type='list', elements='str', required=False),
        allowedGroups=dict(type='list', elements='str', required=False),
        state=dict(type='str', default='present', choices=['present', 'absent']),
        **EN_ONLY_MOD_ARG,
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
    """Module entry point"""
    run_module()


if __name__ == '__main__':
    main()