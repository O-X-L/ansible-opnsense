from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.validate import \
    is_ip, is_valid_domain
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.cls import NestedModule


class WazuhAgent(NestedModule):
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
        'syslog_programs',
        'rootcheck_enabled', 'syscollector_enabled', 'syscheck_enabled', 
        'active_response_enabled', 'active_response_remote_commands',
        'active_response_fw_alias_ignore'
    ]
    FIELDS_ALL = FIELDS_CHANGE
    
    # Standard mapping for build_request (Ansible -> API flat paths)
    FIELDS_TRANSLATE = {
        'enabled': 'general.enabled',
        'server_address': 'general.server_address',
        'agent_name': 'general.agent_name', 
        'protocol': 'general.protocol',
        'port': 'general.port',
        'debug_level': 'general.debug_level',
        'auth_password': 'auth.password',
        'auth_port': 'auth.port',
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
    
    # Reverse mapping for simplify_existing (API flat paths -> Ansible)
    FIELDS_TRANSLATE_RCV = {v: k for k, v in FIELDS_TRANSLATE.items()}
    
    FIELDS_TYPING = {
        'bool': [
            'enabled', 'remote_commands', 'suricata_eve_log',
            'rootcheck_enabled', 'syscollector_enabled', 'syscheck_enabled',
            'active_response_enabled', 'active_response_remote_commands'
        ],
        'int': ['port', 'auth_port'],
        'list': ['syslog_programs', 'active_response_fw_alias_ignore'],
        'select': ['protocol'],  # For {tcp: {selected: 1}} format
        'select_opt_list_idx': ['debug_level'],  # For index selection from array
    }
    TIMEOUT = 60.0
    
    INT_VALIDATIONS = {
        'port': {'min': 1, 'max': 65535},
        'auth_port': {'min': 1, 'max': 65535},
        'debug_level': {'min': 0, 'max': 2},
    }

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        NestedModule.__init__(self=self, m=module, r=result, s=session)
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

        # Call parent check method which handles everything else
        super().check()

    def process(self) -> None:
        """Process the module execution"""
        self.update()
        
        # Reload if requested
        if self.p.get('reload', True) and self.r['changed']:
            self.reload()