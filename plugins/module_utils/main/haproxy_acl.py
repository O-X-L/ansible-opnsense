from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.validate import \
    is_unset
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.cls import BaseModule


class HaproxyAcl(BaseModule):
    FIELD_ID = 'name'
    CMDS = {
        'add': 'addAcl',
        'del': 'delAcl',
        'set': 'setAcl',
        'search': 'searchAcls',
        'detail': 'getAcl',
        'toggle': 'toggleAcl',
    }
    API_KEY_PATH = 'acl'
    API_MOD = 'haproxy'
    API_CONT = 'settings'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigure'
    FIELDS_CHANGE = ['description', 'expression', 'negate', 'caseSensitive', 
                     'hdr_beg', 'hdr_end', 'hdr', 'hdr_reg', 'hdr_sub',
                     'path_beg', 'path_end', 'path', 'path_reg', 'path_dir', 'path_sub',
                     'cust_hdr_beg', 'cust_hdr_end', 'cust_hdr', 'cust_hdr_reg', 'cust_hdr_sub',
                     'url_param', 'ssl_c_verify_code', 'ssl_c_ca_commonname', 'ssl_hello_type',
                     'src', 'src_port', 'allowedUsers', 'allowedGroups']
    FIELDS_ALL = ['name', 'description', 'expression', 'negate']
    FIELDS_TRANSLATE = {
        'description': 'description', 
        'name': 'name',
        'expression': 'expression',
        'negate': 'negate'
    }
    FIELDS_TYPING = {}
    EXIST_ATTR = 'acl'
    TIMEOUT = 60.0

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session)
        self.acl = {}
        self.diff = {}

    def check(self) -> None:
        if self.p['state'] == 'present':
            if is_unset(self.p['name']):
                self.m.fail_json('You need to provide a name to create an ACL!')

            if is_unset(self.p['expression']):
                self.m.fail_json('You need to provide an expression to create an ACL!')

            # Validate that value is provided for expressions that require it
            if self.p['expression'] not in ['ssl_c_verify', 'src_is_local'] and is_unset(self.p['value']):
                if self.p['expression'] != 'http_auth':
                    self.m.fail_json(f'Expression "{self.p["expression"]}" requires a value!')

            # Validate auth-specific fields
            if self.p['expression'] == 'http_auth':
                if is_unset(self.p['allowedUsers']) and is_unset(self.p['allowedGroups']):
                    self.m.fail_json('HTTP auth expression requires allowedUsers or allowedGroups!')

        self._base_check()

    def _build_request(self) -> dict:
        """
        Override request building to map value to the correct expression-specific field.
        """
        # Map expression types to their corresponding API field names
        expression_field_map = {
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
            'src': 'src',
            'src_port': 'src_port',
            'url_param': 'url_param',
            'ssl_c_verify_code': 'ssl_c_verify_code',
            'ssl_c_ca_commonname': 'ssl_c_ca_commonname',
            'ssl_hello_type': 'ssl_hello_type'
        }
        
        # Build base request data
        request_data = {
            'name': self.p['name'],
            'description': self.p.get('description', ''),
            'expression': self.p['expression'],
            'negate': '1' if self.p.get('negate', False) else '0',
            'caseSensitive': '1' if self.p.get('case_sensitive', False) else '0'
        }
        
        # Map value to the correct field based on expression type
        expression = self.p['expression']
        if expression in expression_field_map and 'value' in self.p and self.p['value']:
            api_field = expression_field_map[expression]
            request_data[api_field] = self.p['value']
        
        # Handle special cases for custom headers
        if expression.startswith('cust_hdr') and 'value' in self.p and self.p['value']:
            # For custom headers, we need to split the value into header name and value
            if ' ' in self.p['value']:
                header_name, header_value = self.p['value'].split(' ', 1)
                request_data[f'{expression}_name'] = header_name
                request_data[expression] = header_value
            else:
                request_data[f'{expression}_name'] = self.p['value']
        
        # Handle authentication fields with UUID resolution
        if expression == 'http_auth':
            if 'allowedUsers' in self.p and self.p['allowedUsers']:
                user_uuids = self._resolve_user_names(self.p['allowedUsers'])
                if user_uuids:
                    request_data['allowedUsers'] = ','.join(user_uuids)
            if 'allowedGroups' in self.p and self.p['allowedGroups']:
                group_uuids = self._resolve_group_names(self.p['allowedGroups'])
                if group_uuids:
                    request_data['allowedGroups'] = ','.join(group_uuids)
        
        return {self.API_KEY_PATH: request_data}
    
    def _resolve_user_names(self, user_names: list) -> list:
        """
        Resolve user names to UUIDs by fetching the user list.
        """
        if not user_names:
            return []
        
        try:
            users_response = self.s.get(cnf={
                'module': self.API_MOD,
                'controller': self.API_CONT,
                'command': 'searchUsers'
            })
            
            if 'rows' in users_response:
                user_uuids = []
                for user_name in user_names:
                    for user in users_response['rows']:
                        if user.get('name') == user_name:
                            user_uuids.append(user.get('uuid'))
                            break
                    else:
                        self.m.warn(f"User '{user_name}' not found, skipping")
                
                if self.p.get('debug', False):
                    self.m.warn(f"Resolved users: {dict(zip(user_names, user_uuids))}")
                
                return user_uuids
            
        except Exception as e:
            self.m.warn(f"Failed to resolve user names: {str(e)}")
        
        return []
    
    def _resolve_group_names(self, group_names: list) -> list:
        """
        Resolve group names to UUIDs by fetching the group list.
        """
        if not group_names:
            return []
        
        try:
            groups_response = self.s.get(cnf={
                'module': self.API_MOD,
                'controller': self.API_CONT,
                'command': 'searchGroups'
            })
            
            if 'rows' in groups_response:
                group_uuids = []
                for group_name in group_names:
                    for group in groups_response['rows']:
                        if group.get('name') == group_name:
                            group_uuids.append(group.get('uuid'))
                            break
                    else:
                        self.m.warn(f"Group '{group_name}' not found, skipping")
                
                if self.p.get('debug', False):
                    self.m.warn(f"Resolved groups: {dict(zip(group_names, group_uuids))}")
                
                return group_uuids
            
        except Exception as e:
            self.m.warn(f"Failed to resolve group names: {str(e)}")
        
        return []