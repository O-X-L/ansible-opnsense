from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.validate import \
    is_unset
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.cls import BaseModule


class HaproxyBackend(BaseModule):
    FIELD_ID = 'name'
    CMDS = {
        'add': 'addBackend',
        'del': 'delBackend', 
        'set': 'setBackend',
        'search': 'searchBackends',
        'detail': 'getBackend',
        'toggle': 'toggleBackend',
    }
    API_KEY_PATH = 'backend'
    API_MOD = 'haproxy'
    API_CONT = 'settings'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigure'
    FIELDS_CHANGE = [
        'enabled', 'description', 'mode', 'algorithm', 'source', 
        'linked_servers', 'linked_actions', 'linked_errorfiles', 'basic_auth_users', 'basic_auth_groups',
        'health_check_enabled', 'health_check_interval', 
        'health_check_timeout', 'health_check_retries', 'http_reuse'
    ]
    FIELDS_ALL = ['name', 'enabled', 'description', 'mode', 'algorithm']
    FIELDS_TRANSLATE = {
        'enabled': 'enabled',
        'description': 'description', 
        'name': 'name',
        'mode': 'mode',
        'algorithm': 'algorithm',
        'source': 'source',
        'linked_servers': 'linkedServers',
        'linked_actions': 'linkedActions',
        'linked_errorfiles': 'linkedErrorfiles', 
        'basic_auth_users': 'basicAuthUsers',
        'basic_auth_groups': 'basicAuthGroups',
        'health_check_enabled': 'healthCheckEnabled',
        'health_check_interval': 'checkInterval',
        'health_check_timeout': 'tuning_timeoutCheck',
        'health_check_retries': 'tuning_retries',
        'http_reuse': 'tuning_httpreuse'
    }
    FIELDS_TYPING = {
        'bool': ['enabled']
    }
    EXIST_ATTR = 'backend'
    TIMEOUT = 60.0
    
    INT_VALIDATIONS = {
        'health_check_retries': {'min': 1, 'max': 10},
    }
    
    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session)
        self.backend = {}

    def check(self) -> None:
        # Validate time format for intervals
        if not is_unset(self.p['health_check_interval']):
            import re
            if not re.match(r'^[0-9]{1,8}(?:us|ms|s|m|h|d)?$', self.p['health_check_interval']):
                self.m.fail_json(
                    f"Value of health_check_interval '{self.p['health_check_interval']}' is invalid."
                )
        
        if not is_unset(self.p['health_check_timeout']):
            import re
            if not re.match(r'^[0-9]{1,8}(?:us|ms|s|m|h|d)?$', self.p['health_check_timeout']):
                self.m.fail_json(
                    f"Value of health_check_timeout '{self.p['health_check_timeout']}' is invalid."
                )
        
        self._base_check()

    def _build_request(self) -> dict:
        """
        Override request building to handle server linking.
        """
        # Build base request
        request_data = {}
        
        # Handle basic fields
        for field in ['name', 'description', 'mode', 'algorithm', 'source']:
            if field in self.p and self.p[field] is not None:
                api_field = self.FIELDS_TRANSLATE.get(field, field)
                request_data[api_field] = self.p[field]
        
        # Handle boolean fields
        for field in ['enabled', 'health_check_enabled']:
            if field in self.p:
                api_field = self.FIELDS_TRANSLATE.get(field, field)
                request_data[api_field] = '1' if self.p[field] else '0'
        
        # Handle health check fields
        for field in ['health_check_interval', 'health_check_timeout', 'health_check_retries']:
            if field in self.p and self.p[field] is not None:
                api_field = self.FIELDS_TRANSLATE.get(field, field)
                request_data[api_field] = str(self.p[field])
        
        # Handle http_reuse
        if 'http_reuse' in self.p and self.p['http_reuse']:
            request_data['tuning_httpreuse'] = self.p['http_reuse']
        
        # Handle linked servers - resolve names to UUIDs
        if 'linked_servers' in self.p and self.p['linked_servers']:
            server_uuids = self._resolve_server_names(self.p['linked_servers'])
            if server_uuids:
                # Join UUIDs with comma for HAProxy API
                request_data['linkedServers'] = ','.join(server_uuids)
        
        # Handle linked actions - resolve names to UUIDs
        # IMPORTANT: Use 'linkedActions' (camelCase) for backend - different from frontend 'linked_actions'
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
    
    def _resolve_server_names(self, server_names: list) -> list:
        """
        Resolve server names to UUIDs by fetching the server list.
        """
        if not server_names:
            return []
        
        try:
            # Get all servers
            servers_response = self.s.get(cnf={
                'module': self.API_MOD,
                'controller': self.API_CONT,
                'command': 'searchServers'
            })
            
            if 'rows' in servers_response:
                server_uuids = []
                for server_name in server_names:
                    for server in servers_response['rows']:
                        if server.get('name') == server_name:
                            server_uuids.append(server.get('uuid'))
                            break
                    else:
                        self.m.warn(f"Server '{server_name}' not found, skipping")
                
                if self.p.get('debug', False):
                    self.m.warn(f"Resolved servers: {dict(zip(server_names, server_uuids))}")
                
                return server_uuids
            
        except Exception as e:
            self.m.warn(f"Failed to resolve server names: {str(e)}")
        
        return []
    
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