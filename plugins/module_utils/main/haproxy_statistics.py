from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.validate import \
    is_unset


class HaproxyStatistics:
    """HAProxy statistics retrieval class"""
    
    API_MOD = 'haproxy'
    API_CONT = 'statistics'
    TIMEOUT = 30.0
    
    STAT_COMMANDS = {
        'counters': 'counters',
        'info': 'info',
        'tables': 'tables',
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
        if is_unset(self.p['stat_type']):
            self.m.fail_json('You need to provide a stat_type!')
        
        if self.p['stat_type'] not in self.STAT_COMMANDS:
            self.m.fail_json(f'Invalid stat_type: {self.p["stat_type"]}')

    def process(self) -> None:
        """Retrieve the statistics"""
        stat_type = self.p['stat_type']
        command = self.STAT_COMMANDS[stat_type]
        
        # Build API call configuration
        cnf = {
            'module': self.API_MOD,
            'controller': self.API_CONT,
            'command': command,
        }
        
        # Add table name parameter if specified and stat_type is tables
        if stat_type == 'tables' and not is_unset(self.p['table_name']):
            cnf['params'] = [self.p['table_name']]
        
        try:
            response = self.s.get(cnf=cnf)
            
            if self.p.get('debug', False):
                self.m.warn(f"HAProxy Stats - {stat_type.upper()} RESPONSE: '{response}'")
            
            self.r['statistics'] = response
            self.r['changed'] = False  # Statistics retrieval doesn't change anything
                
        except Exception as e:
            self.m.fail_json(f'Statistics retrieval for {stat_type} failed: {str(e)}')
        
        finally:
            if hasattr(self, 's'):
                self.s.close()

    def reload(self) -> None:
        """Not applicable for statistics operations"""
        pass