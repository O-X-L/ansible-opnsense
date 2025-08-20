from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.validate import \
    is_ip, is_valid_domain, is_unset
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.cls import BaseModule


class HaproxyFrontend(BaseModule):
    FIELD_ID = 'name'
    CMDS = {
        'add': 'addFrontend',
        'del': 'delFrontend',
        'set': 'setFrontend',
        'search': 'searchFrontends',
        'detail': 'getFrontend',
        'toggle': 'toggleFrontend',
    }
    API_KEY_PATH = 'frontend'
    API_MOD = 'haproxy'
    API_CONT = 'settings'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigure'
    FIELDS_CHANGE = ['enabled', 'description', 'bind', 'mode', 'default_backend', 
                     'linked_actions', 'linked_errorfiles', 'basic_auth_users', 'basic_auth_groups']
    FIELDS_ALL = ['name']
    FIELDS_ALL.extend(FIELDS_CHANGE)
    FIELDS_TRANSLATE = {
        'enabled': 'enabled',
        'description': 'description', 
        'name': 'name',
        'bind': 'bind',
        'mode': 'mode',
        'default_backend': 'defaultBackend',
        'linked_actions': 'linkedActions',
        'linked_errorfiles': 'linkedErrorfiles',
        'basic_auth_users': 'basicAuthUsers',
        'basic_auth_groups': 'basicAuthGroups'
    }
    FIELDS_TYPING = {
        'bool': ['enabled']
    }
    EXIST_ATTR = 'frontend'
    TIMEOUT = 60.0
    
    INT_VALIDATIONS = {
        'bind_port': {'min': 1, 'max': 65535},
        'max_connections': {'min': 1, 'max': 1000000},
    }
    
    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session)
        self.frontend = {}
        self.diff = {}

    def check(self) -> None:
        # Validate bind address
        if self.p['state'] == 'present':
            if is_unset(self.p['bind_address']):
                self.m.fail_json('You need to provide a bind_address to create a frontend!')
            
            if not is_ip(self.p['bind_address']) and \
                    not is_valid_domain(self.p['bind_address']) and \
                    self.p['bind_address'] not in ['*', '0.0.0.0', '::']:
                self.m.fail_json(
                    f"Value of bind_address '{self.p['bind_address']}' is not a valid "
                    f"IP-Address, domain-name, or wildcard!"
                )
        
        self._prepare_data()
        self._base_check()
    
    def _prepare_data(self):
        """Prepare data by combining bind_address and bind_port into bind field"""
        # Combine bind_address and bind_port into single bind field
        if not is_unset(self.p['bind_address']) and not is_unset(self.p['bind_port']):
            self.p['bind'] = f"{self.p['bind_address']}:{self.p['bind_port']}"
    
    def _build_request(self) -> dict:
        """
        Override request building to handle relationship field linking.
        """
        # Build base request
        request_data = {}
        
        # Handle basic fields
        for field in ['name', 'description', 'bind', 'mode']:
            if field in self.p and self.p[field] is not None:
                request_data[field] = self.p[field]
        
        # Handle boolean fields
        for field in ['enabled']:
            if field in self.p:
                request_data[field] = '1' if self.p[field] else '0'
        
        # Handle default backend - resolve name to UUID
        # IMPORTANT: Use 'defaultBackend' (camelCase) for frontend according to XML schema
        if 'default_backend' in self.p and self.p['default_backend']:
            backend_uuid = self._resolve_backend_name(self.p['default_backend'])
            if backend_uuid:
                request_data['defaultBackend'] = backend_uuid
        
        # Handle linked actions - resolve names to UUIDs
        # IMPORTANT: Use 'linkedActions' (camelCase) for frontend according to XML schema  
        if 'linked_actions' in self.p and self.p['linked_actions']:
            action_uuids = self._resolve_action_names(self.p['linked_actions'])
            if action_uuids:
                request_data['linkedActions'] = ','.join(action_uuids)
        
        # Handle linked errorfiles - resolve names to UUIDs
        if 'linked_errorfiles' in self.p and self.p['linked_errorfiles']:
            errorfile_uuids = self._resolve_errorfile_names(self.p['linked_errorfiles'])
            if errorfile_uuids:
                request_data['linkedErrorfiles'] = ','.join(errorfile_uuids)
        
        # Handle basic auth users - resolve names to UUIDs
        if 'basic_auth_users' in self.p and self.p['basic_auth_users']:
            user_uuids = self._resolve_user_names(self.p['basic_auth_users'])
            if user_uuids:
                request_data['basicAuthUsers'] = ','.join(user_uuids)
        
        # Handle basic auth groups - resolve names to UUIDs
        if 'basic_auth_groups' in self.p and self.p['basic_auth_groups']:
            group_uuids = self._resolve_group_names(self.p['basic_auth_groups'])
            if group_uuids:
                request_data['basicAuthGroups'] = ','.join(group_uuids)
        
        return {self.API_KEY_PATH: request_data}
    
    def _resolve_backend_name(self, backend_name: str) -> str:
        """
        Resolve backend name to UUID by fetching the backend list.
        """
        if not backend_name:
            return ''
        
        try:
            backends_response = self.s.get(cnf={
                'module': self.API_MOD,
                'controller': self.API_CONT,
                'command': 'searchBackends'
            })
            
            if 'rows' in backends_response:
                for backend in backends_response['rows']:
                    if backend.get('name') == backend_name:
                        if self.p.get('debug', False):
                            self.m.warn(f"Resolved backend '{backend_name}' to UUID: {backend.get('uuid')}")
                        return backend.get('uuid')
                
                self.m.warn(f"Backend '{backend_name}' not found")
            
        except Exception as e:
            self.m.warn(f"Failed to resolve backend name: {str(e)}")
        
        return ''
    
    def _resolve_action_names(self, action_names: list) -> list:
        """
        Resolve action names to UUIDs by fetching the action list.
        """
        if not action_names:
            return []
        
        try:
            actions_response = self.s.get(cnf={
                'module': self.API_MOD,
                'controller': self.API_CONT,
                'command': 'searchActions'
            })
            
            if 'rows' in actions_response:
                action_uuids = []
                for action_name in action_names:
                    for action in actions_response['rows']:
                        if action.get('name') == action_name:
                            action_uuids.append(action.get('uuid'))
                            break
                    else:
                        self.m.warn(f"Action '{action_name}' not found, skipping")
                
                if self.p.get('debug', False):
                    self.m.warn(f"Resolved actions: {dict(zip(action_names, action_uuids))}")
                
                return action_uuids
            
        except Exception as e:
            self.m.warn(f"Failed to resolve action names: {str(e)}")
        
        return []
    
    def _resolve_errorfile_names(self, errorfile_names: list) -> list:
        """
        Resolve errorfile names to UUIDs by fetching the errorfile list.
        """
        if not errorfile_names:
            return []
        
        try:
            errorfiles_response = self.s.get(cnf={
                'module': self.API_MOD,
                'controller': self.API_CONT,
                'command': 'searchErrorfiles'
            })
            
            if 'rows' in errorfiles_response:
                errorfile_uuids = []
                for errorfile_name in errorfile_names:
                    for errorfile in errorfiles_response['rows']:
                        if errorfile.get('name') == errorfile_name:
                            errorfile_uuids.append(errorfile.get('uuid'))
                            break
                    else:
                        self.m.warn(f"Errorfile '{errorfile_name}' not found, skipping")
                
                if self.p.get('debug', False):
                    self.m.warn(f"Resolved errorfiles: {dict(zip(errorfile_names, errorfile_uuids))}")
                
                return errorfile_uuids
            
        except Exception as e:
            self.m.warn(f"Failed to resolve errorfile names: {str(e)}")
        
        return []
    
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