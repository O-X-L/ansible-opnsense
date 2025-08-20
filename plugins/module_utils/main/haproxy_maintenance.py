from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.validate import \
    is_unset


class HaproxyMaintenance:
    """HAProxy maintenance operations class"""
    
    API_MOD = 'haproxy'
    API_CONT = 'maintenance'
    TIMEOUT = 60.0
    
    MAINTENANCE_COMMANDS = {
        'cert_actions': 'cert_actions',
        'cert_diff': 'cert_diff', 
        'cert_sync': 'cert_sync',
        'cert_sync_bulk': 'cert_sync_bulk',
        'get': 'get',
        'search_certificate_diff': 'search_certificate_diff',
        'search_server': 'search_server',
        'server_state': 'server_state',
        'server_state_bulk': 'server_state_bulk',
        'server_weight': 'server_weight',
        'server_weight_bulk': 'server_weight_bulk',
        'fetch_cron_integration': 'fetch_cron_integration',
        'set': 'set',
    }
    
    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        self.m = module
        self.r = result
        self.p = module.params
        self.s = Session(module=module, timeout=self.TIMEOUT) if session is None else session
        
        if 'diff' not in self.r:
            self.r['diff'] = {'before': {}, 'after': {}}

    def check(self) -> None:
        """Validate parameters"""
        if is_unset(self.p['action']):
            self.m.fail_json('You need to provide an action!')
        
        if self.p['action'] not in self.MAINTENANCE_COMMANDS:
            self.m.fail_json(f'Invalid action: {self.p["action"]}')

    def process(self) -> None:
        """Execute the maintenance operation"""
        action = self.p['action']
        command = self.MAINTENANCE_COMMANDS[action]
        
        if self.m.check_mode:
            self.r['result'] = {'status': 'check_mode', 'action': action}
            return
        
        # Build API call configuration
        cnf = {
            'module': self.API_MOD,
            'controller': self.API_CONT,
            'command': command,
        }
        
        # Add server parameter for server-specific operations
        if action in ['search_server', 'server_state', 'server_weight'] and not is_unset(self.p.get('server')):
            cnf['params'] = [self.p['server']]
        
        # Add server state parameter for server state operations
        if action == 'server_state' and not is_unset(self.p.get('state')):
            cnf['params'] = cnf.get('params', []) + [self.p['state']]
        
        # Add server weight parameter for server weight operations
        if action == 'server_weight' and not is_unset(self.p.get('weight')):
            cnf['params'] = cnf.get('params', []) + [str(self.p['weight'])]
        
        try:
            # Use POST for write operations, GET for read operations
            if action in ['fetch_cron_integration', 'set']:
                response = self.s.post(cnf=cnf)
                self.r['changed'] = True
            else:
                response = self.s.get(cnf=cnf)
                self.r['changed'] = False
            
            if self.p.get('debug', False):
                self.m.warn(f"HAProxy Maintenance - {action.upper()} RESPONSE: '{response}'")
            
            self.r['result'] = response
                
        except Exception as e:
            self.m.fail_json(f'Maintenance operation {action} failed: {str(e)}')
        
        finally:
            if hasattr(self, 's'):
                self.s.close()

    def reload(self) -> None:
        """Not applicable for maintenance operations"""
        pass