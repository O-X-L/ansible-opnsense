from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.validate import \
    is_ip, is_valid_domain, is_unset
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.cls import BaseModule


class HaproxyServer(BaseModule):
    FIELD_ID = 'name'
    CMDS = {
        'add': 'addServer',
        'del': 'delServer',
        'set': 'setServer',
        'search': 'searchServers',
        'detail': 'getServer',
        'toggle': 'toggleServer',
    }
    API_KEY_PATH = 'server'
    API_MOD = 'haproxy'
    API_CONT = 'settings'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigure'
    FIELDS_CHANGE = ['enabled', 'description', 'address', 'port', 'linked_resolver', 'unix_socket']
    FIELDS_ALL = ['name']
    FIELDS_ALL.extend(FIELDS_CHANGE)
    FIELDS_TRANSLATE = {
        'enabled': 'enabled',
        'description': 'description', 
        'name': 'name',
        'address': 'address',
        'port': 'port',
        'linked_resolver': 'linkedResolver',
        'unix_socket': 'unix_socket'
    }
    FIELDS_TYPING = {
        'bool': ['enabled'],
        'int': ['port']
    }
    EXIST_ATTR = 'server'
    TIMEOUT = 60.0
    
    INT_VALIDATIONS = {
        'port': {'min': 1, 'max': 65535},
        'weight': {'min': 0, 'max': 255},
    }
    
    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session)
        self.server = {}
        self.diff = {}

    def check(self) -> None:
        # Validate server address
        if self.p['state'] == 'present':
            if is_unset(self.p['address']):
                self.m.fail_json('You need to provide an address to create a server!')
            
            if not is_ip(self.p['address']) and \
                    not is_valid_domain(self.p['address']):
                self.m.fail_json(
                    f"Value of address '{self.p['address']}' is neither "
                    f"a valid IP-Address nor a valid domain-name!"
                )
        
        # Validate source address if provided
        if not is_unset(self.p['source']):
            if not is_ip(self.p['source']):
                self.m.fail_json(
                    f"Value of source '{self.p['source']}' is not a valid IP-Address!"
                )
        
        # Validate time format for intervals
        if not is_unset(self.p['check_interval']):
            import re
            if not re.match(r'^[0-9]{1,8}(?:us|ms|s|m|h|d)?$', self.p['check_interval']):
                self.m.fail_json(
                    f"Value of check_interval '{self.p['check_interval']}' is invalid."
                )
        
        if not is_unset(self.p['check_down_interval']):
            import re
            if not re.match(r'^[0-9]{1,8}(?:us|ms|s|m|h|d)?$', self.p['check_down_interval']):
                self.m.fail_json(
                    f"Value of check_down_interval '{self.p['check_down_interval']}' is invalid."
                )
        
        self._base_check()
    
    def _build_request(self) -> dict:
        """
        Override request building to handle relationship field linking.
        """
        # Build base request
        request_data = {}
        
        # Handle basic fields
        for field in ['name', 'description', 'address']:
            if field in self.p and self.p[field] is not None:
                request_data[field] = self.p[field]
        
        # Handle integer fields
        for field in ['port']:
            if field in self.p and self.p[field] is not None:
                request_data[field] = str(self.p[field])
        
        # Handle boolean fields
        for field in ['enabled']:
            if field in self.p:
                request_data[field] = '1' if self.p[field] else '0'
        
        # Handle linked resolver - resolve name to UUID
        if 'linked_resolver' in self.p and self.p['linked_resolver']:
            resolver_uuid = self._resolve_resolver_name(self.p['linked_resolver'])
            if resolver_uuid:
                request_data['linkedResolver'] = resolver_uuid
        
        # Handle unix socket - resolve frontend name to UUID
        if 'unix_socket' in self.p and self.p['unix_socket']:
            frontend_uuid = self._resolve_frontend_name(self.p['unix_socket'])
            if frontend_uuid:
                request_data['unix_socket'] = frontend_uuid
        
        return {self.API_KEY_PATH: request_data}
    
    def _resolve_resolver_name(self, resolver_name: str) -> str:
        """
        Resolve resolver name to UUID by fetching the resolver list.
        """
        if not resolver_name:
            return ''
        
        try:
            resolvers_response = self.s.get(cnf={
                'module': self.API_MOD,
                'controller': self.API_CONT,
                'command': 'searchResolvers'
            })
            
            if 'rows' in resolvers_response:
                for resolver in resolvers_response['rows']:
                    if resolver.get('name') == resolver_name:
                        if self.p.get('debug', False):
                            self.m.warn(f"Resolved resolver '{resolver_name}' to UUID: {resolver.get('uuid')}")
                        return resolver.get('uuid')
                
                self.m.warn(f"Resolver '{resolver_name}' not found")
            
        except Exception as e:
            self.m.warn(f"Failed to resolve resolver name: {str(e)}")
        
        return ''
    
    def _resolve_frontend_name(self, frontend_name: str) -> str:
        """
        Resolve frontend name to UUID by fetching the frontend list.
        """
        if not frontend_name:
            return ''
        
        try:
            frontends_response = self.s.get(cnf={
                'module': self.API_MOD,
                'controller': self.API_CONT,
                'command': 'searchFrontends'
            })
            
            if 'rows' in frontends_response:
                for frontend in frontends_response['rows']:
                    if frontend.get('name') == frontend_name:
                        if self.p.get('debug', False):
                            self.m.warn(f"Resolved frontend '{frontend_name}' to UUID: {frontend.get('uuid')}")
                        return frontend.get('uuid')
                
                self.m.warn(f"Frontend '{frontend_name}' not found")
            
        except Exception as e:
            self.m.warn(f"Failed to resolve frontend name: {str(e)}")
        
        return ''