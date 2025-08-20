from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.validate import \
    is_unset


class HaproxyExporter:
    """HAProxy export operations class"""
    
    API_MOD = 'haproxy'
    API_CONT = 'export'
    TIMEOUT = 60.0
    
    EXPORT_COMMANDS = {
        'config': 'config',
        'diff': 'diff',
        'download': 'download',
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
        if is_unset(self.p['export_type']):
            self.m.fail_json('You need to provide an export_type!')
        
        if self.p['export_type'] not in self.EXPORT_COMMANDS:
            self.m.fail_json(f'Invalid export_type: {self.p["export_type"]}')
        
        # For download type, validate download_type parameter
        if self.p['export_type'] == 'download' and is_unset(self.p.get('download_type')):
            self.m.fail_json('You need to provide a download_type when export_type is "download"!')

    def process(self) -> None:
        """Execute the export operation"""
        export_type = self.p['export_type']
        command = self.EXPORT_COMMANDS[export_type]
        
        if self.m.check_mode:
            self.r['result'] = {'status': 'check_mode', 'export_type': export_type}
            return
        
        # Build API call configuration
        cnf = {
            'module': self.API_MOD,
            'controller': self.API_CONT,
            'command': command,
        }
        
        # Add download type parameter for download operations
        if export_type == 'download' and not is_unset(self.p.get('download_type')):
            cnf['params'] = [self.p['download_type']]
        
        try:
            response = self.s.get(cnf=cnf)
            
            if self.p.get('debug', False):
                self.m.warn(f"HAProxy Exporter - {export_type.upper()} RESPONSE: '{response}'")
            
            self.r['result'] = response
            self.r['changed'] = False  # Export operations don't change anything
                
        except Exception as e:
            self.m.fail_json(f'Export operation {export_type} failed: {str(e)}')
        
        finally:
            if hasattr(self, 's'):
                self.s.close()

    def reload(self) -> None:
        """Not applicable for export operations"""
        pass