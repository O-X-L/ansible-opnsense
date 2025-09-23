from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.cls import BaseModule


class HaproxyAcl(BaseModule):
    CMDS = {
        'add': 'addAcl',
        'del': 'delAcl',
        'set': 'setAcl',
        'search': 'get',
        'toggle': 'toggleAcl',
    }
    API_KEY_PATH = 'haproxy.acls.acl'
    API_KEY_PATH_REQ = 'acl'
    API_MOD = 'haproxy'
    API_CONT = 'settings'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigure'

    FIELDS_TRANSLATE = {
        'name': 'name',
        'description': 'description',
        'expression': 'expression',
        'negate': 'negate',
        'case_sensitive': 'caseSensitive',
        'hdr_beg': 'hdr_beg',
        'hdr_end': 'hdr_end',
        'hdr': 'hdr',
        'hdr_reg': 'hdr_reg',
        'hdr_sub': 'hdr_sub',
        'path_beg': 'path_beg',
        'path_end': 'path_end',
        'path': 'path',
        'path_reg': 'path_reg',
        'path_dir': 'path_dir',
        'path_sub': 'path_sub',
        'cust_hdr_beg_name': 'cust_hdr_beg_name',
        'cust_hdr_beg': 'cust_hdr_beg',
        'cust_hdr_end_name': 'cust_hdr_end_name',
        'cust_hdr_end': 'cust_hdr_end',
        'cust_hdr_name': 'cust_hdr_name',
        'cust_hdr': 'cust_hdr',
        'cust_hdr_reg_name': 'cust_hdr_reg_name',
        'cust_hdr_reg': 'cust_hdr_reg',
        'cust_hdr_sub_name': 'cust_hdr_sub_name',
        'cust_hdr_sub': 'cust_hdr_sub',
        'url_param': 'url_param',
        'url_param_value': 'url_param_value',
        'ssl_c_verify_code': 'ssl_c_verify_code',
        'ssl_c_ca_commonname': 'ssl_c_ca_commonname',
        'ssl_hello_type': 'ssl_hello_type',
        'src': 'src',
        'src_port': 'src_port',
        'src_port_comparison': 'src_port_comparison',
        'nbsrv': 'nbsrv',
        'nbsrv_backend': 'nbsrv_backend',
        'ssl_fc_sni': 'ssl_fc_sni',
        'ssl_sni': 'ssl_sni',
        'ssl_sni_sub': 'ssl_sni_sub',
        'ssl_sni_beg': 'ssl_sni_beg',
        'ssl_sni_end': 'ssl_sni_end',
        'ssl_sni_reg': 'ssl_sni_reg',
        'custom_acl': 'custom_acl',
        'allowed_users': 'allowedUsers',
        'allowed_groups': 'allowedGroups',
        'src_bytes_in_rate_comparison': 'src_bytes_in_rate_comparison',
        'src_bytes_in_rate': 'src_bytes_in_rate',
        'src_bytes_out_rate_comparison': 'src_bytes_out_rate_comparison',
        'src_bytes_out_rate': 'src_bytes_out_rate',
        'src_conn_cnt_comparison': 'src_conn_cnt_comparison',
        'src_conn_cnt': 'src_conn_cnt',
        'src_conn_cur_comparison': 'src_conn_cur_comparison',
        'src_conn_cur': 'src_conn_cur',
        'src_conn_rate_comparison': 'src_conn_rate_comparison',
        'src_conn_rate': 'src_conn_rate',
        'src_http_err_cnt_comparison': 'src_http_err_cnt_comparison',
        'src_http_err_cnt': 'src_http_err_cnt',
        'src_http_err_rate_comparison': 'src_http_err_rate_comparison',
        'src_http_err_rate': 'src_http_err_rate',
        'src_http_req_cnt_comparison': 'src_http_req_cnt_comparison',
        'src_http_req_cnt': 'src_http_req_cnt',
        'src_http_req_rate_comparison': 'src_http_req_rate_comparison',
        'src_http_req_rate': 'src_http_req_rate',
        'src_kbytes_in_comparison': 'src_kbytes_in_comparison',
        'src_kbytes_in': 'src_kbytes_in',
        'src_kbytes_out_comparison': 'src_kbytes_out_comparison',
        'src_kbytes_out': 'src_kbytes_out',
        'src_sess_cnt_comparison': 'src_sess_cnt_comparison',
        'src_sess_cnt': 'src_sess_cnt',
        'src_sess_rate_comparison': 'src_sess_rate_comparison',
        'src_sess_rate': 'src_sess_rate'
    }

    FIELDS_CHANGE = list(FIELDS_TRANSLATE.keys())
    FIELDS_ALL = FIELDS_CHANGE

    FIELDS_TYPING = {
        'str': ['name', 'description', 'expression', 'hdr_beg', 'hdr_end', 'hdr', 'hdr_reg', 'hdr_sub',
                'path_beg', 'path_end', 'path', 'path_reg', 'path_dir', 'path_sub',
                'cust_hdr_beg_name', 'cust_hdr_beg', 'cust_hdr_end_name', 'cust_hdr_end',
                'cust_hdr_name', 'cust_hdr', 'cust_hdr_reg_name', 'cust_hdr_reg',
                'cust_hdr_sub_name', 'cust_hdr_sub', 'url_param', 'url_param_value',
                'ssl_c_ca_commonname', 'ssl_hello_type', 'src', 'src_port_comparison',
                'ssl_fc_sni', 'ssl_sni', 'ssl_sni_sub', 'ssl_sni_beg', 'ssl_sni_end',
                'ssl_sni_reg', 'custom_acl', 'nbsrv_backend', 'src_bytes_in_rate_comparison',
                'src_bytes_out_rate_comparison', 'src_conn_cnt_comparison', 'src_conn_cur_comparison',
                'src_conn_rate_comparison', 'src_http_err_cnt_comparison', 'src_http_err_rate_comparison',
                'src_http_req_cnt_comparison', 'src_http_req_rate_comparison', 'src_kbytes_in_comparison',
                'src_kbytes_out_comparison', 'src_sess_cnt_comparison', 'src_sess_rate_comparison'],
        'bool': ['negate', 'case_sensitive'],
        'int': ['ssl_c_verify_code', 'src_port', 'nbsrv', 'src_bytes_in_rate', 'src_bytes_out_rate',
                'src_conn_cnt', 'src_conn_cur', 'src_conn_rate', 'src_http_err_cnt', 'src_http_err_rate',
                'src_http_req_cnt', 'src_http_req_rate', 'src_kbytes_in', 'src_kbytes_out',
                'src_sess_cnt', 'src_sess_rate'],
        'list': ['allowed_users', 'allowed_groups']
    }
    FIELD_ID = 'name'
    EXIST_ATTR = 'acl'
    TIMEOUT = 60.0

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        # Resolve user and group names to UUIDs before calling parent __init__
        self._resolve_names_to_uuids(module)
        BaseModule.__init__(self=self, m=module, r=result, s=session)
        self.acl = {}

    def _resolve_names_to_uuids(self, module: AnsibleModule):
        """Resolve user and group names to UUIDs in module parameters"""
        if not any(param in module.params for param in ['allowed_users', 'allowed_groups']):
            return

        # Create temporary session to get HAProxy configuration
        temp_session = Session(
            module=module,
            timeout=self.TIMEOUT if hasattr(self, 'TIMEOUT') else 60.0
        )

        # Get current HAProxy configuration
        current_config = temp_session.get(cnf={
            'module': self.API_MOD,
            'controller': self.API_CONT,
            'command': 'get'
        })

        if 'haproxy' not in current_config:
            module.fail_json(msg="No HAProxy configuration found")

        haproxy_config = current_config['haproxy']

        # Resolve allowed_users
        if 'allowed_users' in module.params and module.params['allowed_users']:
            if 'users' not in haproxy_config:
                module.fail_json(msg="No users found in HAProxy configuration")

            users_config = haproxy_config['users']
            resolved_users = []

            for user_name in module.params['allowed_users']:
                user_uuid = None
                for user_uuid_candidate, user_data in users_config.get('user', {}).items():
                    if user_data.get('name') == user_name:
                        user_uuid = user_uuid_candidate
                        break

                if not user_uuid:
                    module.fail_json(msg=f"User '{user_name}' not found")

                resolved_users.append(user_uuid)

            module.params['allowed_users'] = resolved_users

        # Resolve allowed_groups
        if 'allowed_groups' in module.params and module.params['allowed_groups']:
            if 'groups' not in haproxy_config:
                module.fail_json(msg="No groups found in HAProxy configuration")

            groups_config = haproxy_config['groups']
            resolved_groups = []

            for group_name in module.params['allowed_groups']:
                group_uuid = None
                for group_uuid_candidate, group_data in groups_config.get('group', {}).items():
                    if group_data.get('name') == group_name:
                        group_uuid = group_uuid_candidate
                        break

                if not group_uuid:
                    module.fail_json(msg=f"Group '{group_name}' not found")

                resolved_groups.append(group_uuid)

            module.params['allowed_groups'] = resolved_groups