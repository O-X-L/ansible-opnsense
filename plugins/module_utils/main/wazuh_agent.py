from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.validate import \
    is_ip, is_valid_domain, is_unset
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.cls import BaseModule


class WazuhAgent(BaseModule):
    CMDS = {
        'search': 'get',
        'set': 'set',
    }
    API_KEY_PATH = 'agent'
    API_KEY_PATH_REQ = API_KEY_PATH
    API_MOD = 'wazuhagent'
    API_CONT = 'settings'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigure'
    
    FIELDS_CHANGE = [
        'enabled', 'server_address', 'agent_name', 'port', 'protocol', 'debug_level',
        'auth_password', 'auth_port', 'remote_commands', 'suricata_eve_log', 
        'syslog_programs', 'logcollector_enabled',
        'rootcheck_enabled', 'syscollector_enabled', 'syscheck_enabled', 
        'active_response_enabled', 'active_response_remote_commands',
        'active_response_fw_alias_ignore'
    ]
    FIELDS_ALL = FIELDS_CHANGE.copy()
    
    FIELDS_TRANSLATE = {
        'enabled': 'general.enabled',
        'server_address': 'general.server_address',
        'agent_name': 'general.agent_name', 
        'protocol': 'general.protocol',
        'port': 'general.port',
        'debug_level': 'general.debug_level',
        'auth_password': 'auth.password',
        'auth_port': 'auth.port',
        'logcollector_enabled': 'logcollector.enabled',
        'remote_commands': 'logcollector.remote_commands',
        'syslog_programs': 'logcollector.syslog_programs',
        'suricata_eve_log': 'logcollector.suricata_eve_log',
        'rootcheck_enabled': 'rootcheck.enabled',
        'syscollector_enabled': 'syscollector.enabled',
        'syscheck_enabled': 'syscheck.enabled',
        'active_response_enabled': 'active_response.enabled',
        'active_response_remote_commands': 'active_response.remote_commands',
        'active_response_fw_alias_ignore': 'active_response.fw_alias_ignore',
    }
    
    FIELDS_TYPING = {
        'bool': [
            'enabled', 'logcollector_enabled', 'remote_commands', 'suricata_eve_log',
            'rootcheck_enabled', 'syscollector_enabled', 'syscheck_enabled',
            'active_response_enabled', 'active_response_remote_commands'
        ],
        'int': ['port', 'auth_port', 'debug_level'],
        'list': ['syslog_programs', 'active_response_fw_alias_ignore'],
    }
    
    EXIST_ATTR = 'config'
    TIMEOUT = 60.0
    
    INT_VALIDATIONS = {
        'port': {'min': 1, 'max': 65535},
        'auth_port': {'min': 1, 'max': 65535},
    }

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session)
        self.config = {}
        # Initialize diff structure
        if 'diff' not in self.r:
            self.r['diff'] = {'before': {}, 'after': {}}

    def check(self) -> None:
        # Validate server address
        if not is_ip(self.p['server_address']) and \
                not is_valid_domain(self.p['server_address']):
            self.m.fail_json(
                f"Value of server_address '{self.p['server_address']}' is neither "
                f"a valid IP-Address nor a valid domain-name!"
            )

        self._base_check()


    def process(self) -> None:
        """Override the main process method"""
        self.run()

    def get_existing(self) -> dict:
        """Get current configuration and convert to Ansible format"""
        self.config = self._search_call()
        return self._api_to_ansible(self.config)

    def _search_call(self) -> dict:
        """Get current Wazuh configuration"""
        raw = self.s.get(cnf={
            'module': self.API_MOD,
            'controller': self.API_CONT,
            'command': self.CMDS['search'],
        })
        
        if self.m.params.get('debug', False):
            self.m.warn(f"Wazuh Agent - RAW RESPONSE: '{raw}'")
        
        return raw.get('agent', {}) if raw else {}


    def _get_selected_value(self, data: dict) -> str:
        """Extract selected value from OPNsense 'selected' format"""
        for key, val in data.items():
            if isinstance(val, dict) and val.get('selected') == 1:
                return key
        return ''
    
    def _get_selected_index(self, data: list) -> int:
        """Extract selected index from array of {value, selected} objects"""
        for idx, item in enumerate(data):
            if isinstance(item, dict) and item.get('selected') == 1:
                return idx
        return 0
    
    def _safe_int(self, value, default: int = 0) -> int:
        """Safely convert various formats to int"""
        if isinstance(value, (str, int)):
            return int(value)
        elif isinstance(value, list) and value:
            return int(value[0])
        return default
    
    def _get_selected_list(self, data: dict) -> list:
        """Extract list of selected keys from multi-select format"""
        return [key for key, val in data.items() 
                if isinstance(val, dict) and val.get('selected') == 1 and key]
    
    def _api_to_ansible(self, api_config: dict) -> dict:
        """Convert API config to Ansible format for diff"""
        ansible_config = {}
        
        # Debug output to understand API structure
        if self.m.params.get('debug', False):
            self.m.warn(f"API Config Structure: {api_config}")
        
        # General section
        if 'general' in api_config:
            general = api_config['general']
            # Simple fields
            for field in ['server_address', 'agent_name']:
                if field in general:
                    ansible_config[field] = general[field]
            
            # Boolean field
            if 'enabled' in general:
                ansible_config['enabled'] = general['enabled'] == '1'
            
            # Complex fields with selected format
            if 'protocol' in general:
                proto_val = general['protocol']
                ansible_config['protocol'] = proto_val if isinstance(proto_val, str) else self._get_selected_value(proto_val)
            
            if 'port' in general:
                ansible_config['port'] = self._safe_int(general['port'], 1514)
            
            if 'debug_level' in general:
                debug_val = general['debug_level']
                ansible_config['debug_level'] = int(debug_val) if isinstance(debug_val, (str, int)) else self._get_selected_index(debug_val)
                
        # Auth section  
        if 'auth' in api_config:
            auth = api_config['auth']
            if 'password' in auth:
                ansible_config['auth_password'] = auth['password']
            if 'port' in auth:
                ansible_config['auth_port'] = self._safe_int(auth['port'], 1515)
                
        # Logcollector section
        if 'logcollector' in api_config:
            logcoll = api_config['logcollector']
            # Boolean fields
            for field in ['enabled', 'remote_commands', 'suricata_eve_log']:
                if field in logcoll:
                    ansible_field = f'logcollector_{field}' if field == 'enabled' else field
                    ansible_config[ansible_field] = logcoll[field] == '1'
            
            # Multi-select field
            if 'syslog_programs' in logcoll and logcoll['syslog_programs']:
                if isinstance(logcoll['syslog_programs'], dict):
                    programs = self._get_selected_list(logcoll['syslog_programs'])
                    if programs:
                        ansible_config['syslog_programs'] = programs
                
        # Module sections
        for module_name in ['rootcheck', 'syscollector', 'syscheck', 'active_response']:
            if module_name in api_config:
                module_config = api_config[module_name]
                
                # All modules have enabled field
                if 'enabled' in module_config:
                    ansible_config[f'{module_name}_enabled'] = module_config['enabled'] == '1'
                
                # Active response specific fields
                if module_name == 'active_response':
                    if 'remote_commands' in module_config:
                        ansible_config['active_response_remote_commands'] = module_config['remote_commands'] == '1'
                    
                    if 'fw_alias_ignore' in module_config and isinstance(module_config['fw_alias_ignore'], dict):
                        aliases = self._get_selected_list(module_config['fw_alias_ignore'])
                        if aliases:
                            ansible_config['active_response_fw_alias_ignore'] = aliases
                    
        return ansible_config

    def _bool_to_str(self, value) -> str:
        """Convert boolean to API string format"""
        return '1' if value else '0'
    
    def _build_section(self, section_name: str, field_mapping: dict) -> dict:
        """Build API section from field mapping"""
        section_data = {}
        for ansible_field, (api_field, field_type, default) in field_mapping.items():
            value = self.p.get(ansible_field, default)
            if value is not None:
                if field_type == 'bool':
                    section_data[api_field] = self._bool_to_str(value)
                elif field_type == 'list':
                    section_data[api_field] = ','.join(value) if isinstance(value, list) else str(value)
                else:
                    section_data[api_field] = str(value)
        return section_data
    
    def _ansible_to_api(self) -> dict:
        """Convert Ansible parameters to API format"""
        api_data = {}
        
        # General section mapping
        general_mapping = {
            'enabled': ('enabled', 'bool', None),
            'server_address': ('server_address', 'str', None),
            'agent_name': ('agent_name', 'str', ''),
            'protocol': ('protocol', 'str', 'tcp'),
            'port': ('port', 'str', 1514),
            'debug_level': ('debug_level', 'str', 0)
        }
        
        general_data = self._build_section('general', general_mapping)
        if general_data:
            api_data['general'] = general_data
            
        # Auth section mapping
        auth_mapping = {
            'auth_password': ('password', 'str', None),
            'auth_port': ('port', 'str', None)
        }
        
        auth_data = self._build_section('auth', auth_mapping)
        if auth_data:
            api_data['auth'] = auth_data
            
        # Logcollector section mapping
        logcoll_mapping = {
            'logcollector_enabled': ('enabled', 'bool', None),
            'remote_commands': ('remote_commands', 'bool', None),
            'suricata_eve_log': ('suricata_eve_log', 'bool', None),
            'syslog_programs': ('syslog_programs', 'list', None)
        }
        
        logcoll_data = self._build_section('logcollector', logcoll_mapping)
        if logcoll_data:
            api_data['logcollector'] = logcoll_data
            
        # Module sections
        modules = ['rootcheck', 'syscollector', 'syscheck', 'active_response']
        for module_name in modules:
            mapping = {f'{module_name}_enabled': ('enabled', 'bool', None)}
            
            # Active response has extra fields
            if module_name == 'active_response':
                mapping.update({
                    'active_response_remote_commands': ('remote_commands', 'bool', None),
                    'active_response_fw_alias_ignore': ('fw_alias_ignore', 'list', None)
                })
            
            module_data = self._build_section(module_name, mapping)
            if module_data:
                api_data[module_name] = module_data
                
        return api_data

    def run(self) -> None:
        """Main execution logic"""
        self.config = self._search_call()
        
        if not self.config:
            self.m.fail_json("Unable to retrieve current Wazuh configuration")
        
        # Initialize diff with current config
        self.r['diff']['before'] = self._api_to_ansible(self.config)
            
        # Build the change request
        api_request = self._ansible_to_api()
        
        if not api_request:
            # No changes requested
            return
            
        # Calculate what would change
        if api_request:
            # Merge with existing config to see the result
            new_config = self.config.copy()
            for section, data in api_request.items():
                if section in new_config:
                    new_config[section].update(data)
                else:
                    new_config[section] = data
                    
            self.r['diff']['after'] = self._api_to_ansible(new_config)
            
            # Check if anything actually changed
            if self.r['diff']['before'] != self.r['diff']['after']:
                self.r['changed'] = True
                
                if not self.m.check_mode:
                    # Apply the changes
                    response = self.s.post(cnf={
                        'module': self.API_MOD,
                        'controller': self.API_CONT,
                        'command': self.CMDS['set'],
                        'data': {'agent': api_request}
                    })
                    
                    if self.m.params.get('debug', False):
                        self.m.warn(f"Wazuh Agent - SET RESPONSE: '{response}'")
                        
                    # Reload if requested
                    if self.p.get('reload', True):
                        self.reload()
            else:
                self.r['diff']['after'] = self.r['diff']['before']