from ansible.module_utils.basic import AnsibleModule
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.validate import is_unset


class HaproxyGeneral:
    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        self.m = module
        self.r = result
        self.p = module.params
        
        self.s = Session(module=module) if session is None else session
        
        self.config = {}
        if 'diff' not in self.r:
            self.r['diff'] = {'before': {}, 'after': {}}

    def check(self) -> None:
        """Validate input parameters"""
        if not is_unset(self.p.get('hard_stop_after')):
            import re
            if not re.match(r'^[0-9]{1,8}(?:us|ms|s|m|h|d)?$', self.p['hard_stop_after']):
                self.m.fail_json(
                    f"Value of hard_stop_after '{self.p['hard_stop_after']}' is invalid. "
                    f"Should be a number between 1 and 8 characters, optionally followed by "
                    f"either 'd', 'h', 'm', 's', 'ms' or 'us'."
                )
        
        if not is_unset(self.p.get('close_spread_time')):
            import re
            if not re.match(r'^[0-9]{1,8}(?:us|ms|s|m|h|d)?$', self.p['close_spread_time']):
                self.m.fail_json(
                    f"Value of close_spread_time '{self.p['close_spread_time']}' is invalid. "
                    f"Should be a number between 1 and 8 characters, optionally followed by "
                    f"either 'd', 'h', 'm', 's', 'ms' or 'us'."
                )

    def process(self) -> None:
        """Main process method"""
        self.run()

    def get_existing(self) -> dict:
        """Get current configuration and convert to Ansible format"""
        self.config = self._search_call()
        return self._api_to_ansible(self.config)

    def _search_call(self) -> dict:
        """Get current HAProxy configuration"""
        raw = self.s.get(cnf={
            'module': 'haproxy',
            'controller': 'settings',
            'command': 'get',
        })
        
        if self.m.params.get('debug', False):
            self.m.warn(f"HAProxy General - RAW RESPONSE: {list(raw.keys()) if raw else 'None'}")
        
        return raw.get('haproxy', {}) if raw else {}

    def _api_to_ansible(self, api_config: dict) -> dict:
        """Convert API config to Ansible format for diff"""
        ansible_config = {}
        
        if self.m.params.get('debug', False):
            self.m.warn(f"Converting API config with keys: {list(api_config.keys())}")
        
        if 'general' in api_config:
            general = api_config['general']
            
            # Boolean fields
            bool_fields = {
                'enabled': 'enabled',
                'gracefulStop': 'graceful_stop',
                'seamlessReload': 'seamless_reload',
                'showIntro': 'show_intro',
            }
            
            for api_field, ansible_field in bool_fields.items():
                if api_field in general:
                    ansible_config[ansible_field] = general[api_field] == '1'
            
            # String fields
            string_fields = {
                'hardStopAfter': 'hard_stop_after',
                'closeSpreadTime': 'close_spread_time',
            }
            
            for api_field, ansible_field in string_fields.items():
                if api_field in general and general[api_field]:
                    ansible_config[ansible_field] = general[api_field]
        
        return ansible_config
    
    def _ansible_to_api(self, ansible_config: dict) -> dict:
        """Convert Ansible parameters to API format"""
        api_config = {'haproxy': {'general': {}}}
        general = api_config['haproxy']['general']
        
        field_mapping = {
            'enabled': 'enabled',
            'graceful_stop': 'gracefulStop',
            'hard_stop_after': 'hardStopAfter',
            'close_spread_time': 'closeSpreadTime',
            'seamless_reload': 'seamlessReload',
            'show_intro': 'showIntro',
        }
        
        bool_fields = ['enabled', 'graceful_stop', 'seamless_reload', 'show_intro']
        
        for ansible_field, api_field in field_mapping.items():
            if ansible_field in ansible_config and ansible_config[ansible_field] is not None:
                value = ansible_config[ansible_field]
                
                if ansible_field in bool_fields:
                    value = '1' if value else '0'
                
                general[api_field] = value
        
        return api_config
    
    def _build_request(self) -> dict:
        """Build request with correct API structure"""
        request = {}
        
        fields = ['enabled', 'graceful_stop', 'hard_stop_after', 'close_spread_time', 
                 'seamless_reload', 'show_intro']
        
        for field in fields:
            if field in self.p and self.p[field] is not None:
                request[field] = self.p[field]
        
        return self._ansible_to_api(request)
    
    def run(self) -> None:
        """Main execution method"""
        self.check()
        
        # Get existing configuration
        existing = self.get_existing()
        self.r['diff']['before'] = existing.copy()
        
        # Check if we're in check mode
        if self.m.check_mode:
            after = existing.copy()
            fields = ['enabled', 'graceful_stop', 'hard_stop_after', 'close_spread_time', 
                     'seamless_reload', 'show_intro']
            
            for field in fields:
                if field in self.p and self.p[field] is not None:
                    after[field] = self.p[field]
            
            self.r['diff']['after'] = after
            
            if existing != after:
                self.r['changed'] = True
            
            return
        
        # Build request for API
        request = self._build_request()
        
        # Send update request if there are changes
        if request.get('haproxy', {}).get('general'):
            result = self.s.post(cnf={
                'module': 'haproxy',
                'controller': 'settings',
                'command': 'set',
                'data': request,
            })
            
            if self.m.params.get('debug', False):
                self.m.warn(f"HAProxy General - SET RESPONSE: '{result}'")
            
            # Check if update was successful
            if result and result.get('result', '') == 'saved':
                self.r['changed'] = True
                
                # Reload service if requested
                if self.p.get('reload', True):
                    reload_result = self.s.post(cnf={
                        'module': 'haproxy',
                        'controller': 'service',
                        'command': 'reconfigure',
                    })
                    
                    if self.m.params.get('debug', False):
                        self.m.warn(f"HAProxy General - RELOAD RESPONSE: '{reload_result}'")
        
        # Get new configuration for diff
        new_config = self.get_existing()
        self.r['diff']['after'] = new_config