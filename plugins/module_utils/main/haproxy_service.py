from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.validate import \
    is_unset


class HaproxyService:
    """HAProxy service management class"""
    
    API_MOD = 'haproxy'
    API_CONT = 'service'
    TIMEOUT = 60.0
    
    SERVICE_COMMANDS = {
        'start': 'start',
        'stop': 'stop',
        'restart': 'restart',
        'reload': 'reconfigure',
        'status': 'status',
        'configtest': 'configtest',
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
        
        if self.p['action'] not in self.SERVICE_COMMANDS:
            self.m.fail_json(f'Invalid action: {self.p["action"]}')

    def process(self) -> None:
        """Execute the service operation"""
        action = self.p['action']
        command = self.SERVICE_COMMANDS[action]
        
        if self.m.check_mode:
            self.r['result'] = {'status': 'check_mode', 'action': action}
            return
        
        # Perform the service operation
        try:
            response = self.s.post(cnf={
                'module': self.API_MOD,
                'controller': self.API_CONT,
                'command': command,
            })
            
            if self.p.get('debug', False):
                self.m.warn(f"HAProxy Service - {action.upper()} RESPONSE: '{response}'")
            
            # Handle different response types
            if action == 'status':
                self.r['result'] = response
            elif action == 'configtest':
                self.r['result'] = response
                # Configuration test doesn't change the service state
                self.r['changed'] = False
            else:
                # start, stop, restart, reload operations
                self.r['result'] = response
                self.r['changed'] = True
                
        except Exception as e:
            self.m.fail_json(f'Service operation {action} failed: {str(e)}')
        
        finally:
            if hasattr(self, 's'):
                self.s.close()

    def reload(self) -> None:
        """Not applicable for service operations"""
        pass