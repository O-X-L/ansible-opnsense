from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.validate import \
    is_unset
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.cls import BaseModule


class HaproxyAction(BaseModule):
    FIELD_ID = 'name'
    CMDS = {
        'add': 'addAction',
        'del': 'delAction',
        'set': 'setAction',
        'search': 'searchActions',
        'detail': 'getAction',
        'toggle': 'toggleAction',
    }
    API_KEY_PATH = 'action'
    API_MOD = 'haproxy'
    API_CONT = 'settings'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigure'
    FIELDS_CHANGE = [
        'description', 'action_type', 'test_type', 'linked_acls', 'operator',
        'use_backend', 'use_server', 'http_request_auth', 'http_request_redirect',
        'http_request_lua', 'custom_lua', 'map_use_backend_file', 'map_use_backend_default'
    ]
    FIELDS_ALL = ['name']
    FIELDS_ALL.extend(FIELDS_CHANGE)
    FIELDS_TRANSLATE = {
        'name': 'name',
        'description': 'description',
        'action_type': 'type',
        'test_type': 'testType',
        'linked_acls': 'linkedAcls',
        'operator': 'operator',
        'use_backend': 'useBackend',
        'use_server': 'useServer',
        'http_request_auth': 'http_request_auth',
        'http_request_redirect': 'http_request_redirect',
        'http_request_lua': 'http_request_lua',
        'custom_lua': 'custom',
        'map_use_backend_file': 'map_use_backend_file',
        'map_use_backend_default': 'map_use_backend_default'
    }
    FIELDS_TYPING = {}
    EXIST_ATTR = 'action'
    TIMEOUT = 60.0

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session)
        self.action = {}

    def check(self) -> None:
        if self.p['state'] == 'present':
            if is_unset(self.p['name']):
                self.m.fail_json('You need to provide a name to create an action!')
            
            if is_unset(self.p['action_type']):
                self.m.fail_json('You need to provide an action_type!')

        self._base_check()

    def _build_request(self) -> dict:
        """
        Override request building to handle backend and server linking.
        """
        # Build base request
        request_data = {}
        
        # Handle basic fields
        for field in ['name', 'description', 'test_type', 'operator', 'action_type']:
            if field in self.p and self.p[field] is not None:
                api_field = self.FIELDS_TRANSLATE.get(field, field)
                request_data[api_field] = self.p[field]
        
        # Handle string fields for actions
        for field in ['http_request_auth', 'http_request_redirect', 'http_request_lua', 'custom_lua']:
            if field in self.p and self.p[field] is not None:
                api_field = self.FIELDS_TRANSLATE.get(field, field)
                request_data[api_field] = self.p[field]
        
        # Handle linked ACLs - resolve names to UUIDs
        if 'linked_acls' in self.p and self.p['linked_acls']:
            acl_uuids = self._resolve_acl_names(self.p['linked_acls'])
            if acl_uuids:
                request_data['linkedAcls'] = ','.join(acl_uuids)
        
        # Handle use_backend - resolve backend name to UUID
        # IMPORTANT: OPNsense UI uses 'use_backend' (underscore) NOT 'useBackend' (camelCase)
        if 'use_backend' in self.p and self.p['use_backend']:
            backend_uuid = self._resolve_backend_name(self.p['use_backend'])
            if backend_uuid:
                # Use underscore version for UI compatibility
                request_data['use_backend'] = backend_uuid
        
        # Handle use_server - resolve server names to UUIDs
        if 'use_server' in self.p and self.p['use_server']:
            server_uuids = self._resolve_server_names(self.p['use_server'])
            if server_uuids:
                request_data['useServer'] = ','.join(server_uuids)
        
        # Handle map backend fields - resolve backend names to UUIDs
        if 'map_use_backend_default' in self.p and self.p['map_use_backend_default']:
            backend_uuid = self._resolve_backend_name(self.p['map_use_backend_default'])
            if backend_uuid:
                request_data['map_use_backend_default'] = backend_uuid
        
        return {self.API_KEY_PATH: request_data}
    
    def _resolve_backend_name(self, backend_name: str) -> str:
        """
        Resolve backend name to UUID by fetching the backend list.
        """
        if not backend_name:
            return ''
        
        try:
            # Get all backends
            backends_response = self.s.get(cnf={
                'module': self.API_MOD,
                'controller': self.API_CONT,
                'command': 'searchBackends'
            })
            
            if 'rows' in backends_response:
                for backend in backends_response['rows']:
                    if backend.get('name') == backend_name:
                        return backend.get('uuid', '')
                
                self.m.warn(f"Backend '{backend_name}' not found")
            
        except Exception as e:
            self.m.warn(f"Failed to resolve backend name: {str(e)}")
        
        return ''
    
    def _resolve_acl_names(self, acl_names: list) -> list:
        """
        Resolve ACL names to UUIDs by fetching the ACL list.
        """
        if not acl_names:
            return []
        
        try:
            # Get all ACLs
            acls_response = self.s.get(cnf={
                'module': self.API_MOD,
                'controller': self.API_CONT,
                'command': 'searchAcls'
            })
            
            if 'rows' in acls_response:
                acl_uuids = []
                for acl_name in acl_names:
                    for acl in acls_response['rows']:
                        if acl.get('name') == acl_name:
                            acl_uuids.append(acl.get('uuid'))
                            break
                    else:
                        self.m.warn(f"ACL '{acl_name}' not found, skipping")
                
                return acl_uuids
            
        except Exception as e:
            self.m.warn(f"Failed to resolve ACL names: {str(e)}")
        
        return []
    
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
                
                return server_uuids
            
        except Exception as e:
            self.m.warn(f"Failed to resolve server names: {str(e)}")
        
        return []
