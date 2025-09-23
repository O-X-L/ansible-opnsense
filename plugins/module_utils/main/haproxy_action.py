from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.cls import BaseModule


class HaproxyAction(BaseModule):
    CMDS = {
        'add': 'addAction',
        'del': 'delAction',
        'set': 'setAction',
        'search': 'get',
        'toggle': 'toggleAction',
    }
    API_KEY_PATH = 'haproxy.actions.action'
    API_KEY_PATH_REQ = 'action'
    API_MOD = 'haproxy'
    API_CONT = 'settings'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigure'

    FIELDS_TRANSLATE = {
        'name': 'name',
        'description': 'description',
        'test_type': 'testType',
        'linked_acls': 'linkedAcls',
        'operator': 'operator',
        'type': 'type',
        'use_backend': 'use_backend',
        'use_server': 'use_server',
        'fcgi_pass_header': 'fcgi_pass_header',
        'fcgi_set_param': 'fcgi_set_param',
        'http_request_auth': 'http_request_auth',
        'http_request_redirect': 'http_request_redirect',
        'http_request_lua': 'http_request_lua',
        'http_request_use_service': 'http_request_use_service',
        'http_request_add_header_name': 'http_request_add_header_name',
        'http_request_add_header_content': 'http_request_add_header_content',
        'http_request_set_header_name': 'http_request_set_header_name',
        'http_request_set_header_content': 'http_request_set_header_content',
        'http_request_del_header_name': 'http_request_del_header_name',
        'http_request_replace_header_name': 'http_request_replace_header_name',
        'http_request_replace_header_regex': 'http_request_replace_header_regex',
        'http_request_replace_value_name': 'http_request_replace_value_name',
        'http_request_replace_value_regex': 'http_request_replace_value_regex',
        'http_request_set_path': 'http_request_set_path',
        'http_request_set_var_scope': 'http_request_set_var_scope',
        'http_request_set_var_name': 'http_request_set_var_name',
        'http_request_set_var_expr': 'http_request_set_var_expr',
        'http_response_lua': 'http_response_lua',
        'http_response_add_header_name': 'http_response_add_header_name',
        'http_response_add_header_content': 'http_response_add_header_content',
        'http_response_set_header_name': 'http_response_set_header_name',
        'http_response_set_header_content': 'http_response_set_header_content',
        'http_response_del_header_name': 'http_response_del_header_name',
        'http_response_replace_header_name': 'http_response_replace_header_name',
        'http_response_replace_header_regex': 'http_response_replace_header_regex',
        'http_response_replace_value_name': 'http_response_replace_value_name',
        'http_response_replace_value_regex': 'http_response_replace_value_regex',
        'http_response_set_status_code': 'http_response_set_status_code',
        'http_response_set_status_reason': 'http_response_set_status_reason',
        'http_response_set_var_scope': 'http_response_set_var_scope',
        'http_response_set_var_name': 'http_response_set_var_name',
        'http_response_set_var_expr': 'http_response_set_var_expr',
        'monitor_fail_uri': 'monitor_fail_uri',
        'tcp_request_content_lua': 'tcp_request_content_lua',
        'tcp_request_content_use_service': 'tcp_request_content_use_service',
        'tcp_request_inspect_delay': 'tcp_request_inspect_delay',
        'tcp_response_content_lua': 'tcp_response_content_lua',
        'tcp_response_inspect_delay': 'tcp_response_inspect_delay',
        'custom_rule': 'custom',
        'map_use_backend_file': 'map_use_backend_file',
        'map_use_backend_default': 'map_use_backend_default'
    }

    FIELDS_CHANGE = list(FIELDS_TRANSLATE.keys())
    FIELDS_ALL = FIELDS_CHANGE

    FIELDS_TYPING = {
        'str': ['name', 'description', 'test_type', 'operator', 'type', 'use_backend', 'use_server',
                'fcgi_pass_header', 'fcgi_set_param', 'http_request_auth', 'http_request_redirect',
                'http_request_lua', 'http_request_use_service', 'http_request_add_header_name',
                'http_request_add_header_content', 'http_request_set_header_name', 'http_request_set_header_content',
                'http_request_del_header_name', 'http_request_replace_header_name', 'http_request_replace_header_regex',
                'http_request_replace_value_name', 'http_request_replace_value_regex', 'http_request_set_path',
                'http_request_set_var_scope', 'http_request_set_var_name', 'http_request_set_var_expr',
                'http_response_lua', 'http_response_add_header_name', 'http_response_add_header_content',
                'http_response_set_header_name', 'http_response_set_header_content', 'http_response_del_header_name',
                'http_response_replace_header_name', 'http_response_replace_header_regex', 'http_response_replace_value_name',
                'http_response_replace_value_regex', 'http_response_set_status_reason', 'http_response_set_var_scope',
                'http_response_set_var_name', 'http_response_set_var_expr', 'monitor_fail_uri',
                'tcp_request_content_lua', 'tcp_request_content_use_service', 'tcp_request_inspect_delay',
                'tcp_response_content_lua', 'tcp_response_inspect_delay', 'custom_rule',
                'map_use_backend_file', 'map_use_backend_default'],
        'int': ['http_response_set_status_code'],
        'list': ['linked_acls']
    }
    FIELD_ID = 'name'
    EXIST_ATTR = 'action'
    TIMEOUT = 60.0

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        # Resolve ACL names to UUIDs before calling parent __init__
        self._resolve_names_to_uuids(module)
        BaseModule.__init__(self=self, m=module, r=result, s=session)
        self.action = {}

    def _resolve_names_to_uuids(self, module: AnsibleModule):
        """Resolve ACL names to UUIDs in module parameters"""
        if 'linked_acls' not in module.params or not module.params['linked_acls']:
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

        if 'haproxy' not in current_config or 'acls' not in current_config['haproxy']:
            module.fail_json(msg="No ACLs found in HAProxy configuration")

        acls_config = current_config['haproxy']['acls']
        resolved_acls = []

        for acl_name in module.params['linked_acls']:
            acl_uuid = None
            # Find UUID for the given ACL name
            for acl_uuid_candidate, acl_data in acls_config.get('acl', {}).items():
                if acl_data.get('name') == acl_name:
                    acl_uuid = acl_uuid_candidate
                    break

            if not acl_uuid:
                module.fail_json(msg=f"ACL '{acl_name}' not found")

            resolved_acls.append(acl_uuid)

        # Update module params with resolved UUIDs
        module.params['linked_acls'] = resolved_acls