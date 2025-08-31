from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.validate import is_ip, is_valid_domain
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import is_true, get_selected, get_selected_list, to_digit
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.cls import GeneralModule


class WazuhAgent(GeneralModule):
    CMDS = {
        'search': 'get',
        'set': 'set',
    }
    API_KEY = API_KEY_PATH = 'agent'
    API_MOD = 'wazuhagent'
    API_CONT = 'settings'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigure'
    
    # Fields that can be handled by standard translation (flat fields at root level)
    FIELDS_TRANSLATE = {
        # Future flat fields would go here
    }
    
    # Special nested fields that need manual handling
    FIELDS_TRANSLATE_SPECIAL = {
        # General section
        'enabled': 'general.enabled',
        'server_address': 'general.server_address',
        'agent_name': 'general.agent_name',
        'protocol': 'general.protocol',
        'port': 'general.port',
        'debug_level': 'general.debug_level',
        # Auth section
        'auth_password': 'auth.password',
        'auth_port': 'auth.port',
        # Logcollector section
        'remote_commands': 'logcollector.remote_commands',
        'suricata_eve_log': 'logcollector.suricata_eve_log',
        'syslog_programs': 'logcollector.syslog_programs',
        # Module sections
        'rootcheck_enabled': 'rootcheck.enabled',
        'syscollector_enabled': 'syscollector.enabled',
        'syscheck_enabled': 'syscheck.enabled',
        'active_response_enabled': 'active_response.enabled',
        'active_response_remote_commands': 'active_response.remote_commands',
        'active_response_fw_alias_ignore': 'active_response.fw_alias_ignore',
    }
    
    # Auto-generate FIELDS_CHANGE from both FIELDS_TRANSLATE and FIELDS_TRANSLATE_SPECIAL
    FIELDS_CHANGE = list(FIELDS_TRANSLATE.keys()) + list(FIELDS_TRANSLATE_SPECIAL.keys())
    FIELDS_ALL = FIELDS_CHANGE

    FIELDS_TYPING = {
        'bool': [
            'enabled', 'remote_commands', 'suricata_eve_log',
            'rootcheck_enabled', 'syscollector_enabled', 'syscheck_enabled',
            'active_response_enabled', 'active_response_remote_commands'
        ],
        'int': ['port', 'auth_port', 'debug_level'],
        'list': ['syslog_programs', 'active_response_fw_alias_ignore'],
        'select': ['protocol'],
    }
    
    TIMEOUT = 60.0

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        GeneralModule.__init__(self=self, m=module, r=result, s=session)

    def check(self) -> None:
        if 'server_address' in self.p and self.p['server_address']:
            if not is_ip(self.p['server_address']) and not is_valid_domain(self.p['server_address']):
                self.m.fail_json(f"Invalid server_address '{self.p['server_address']}'")
        self._base_check()

    def _search_call(self) -> dict:
        settings = self.s.get(cnf={
            **self.call_cnf, **{'command': self.CMDS['search']}
        })[self.API_KEY]

        if self.FIELDS_TRANSLATE:
            simple = self.b.simplify_existing(settings)
        else:
            simple = {}

        # Handle all special nested fields from FIELDS_TRANSLATE_SPECIAL
        for field, path in self.FIELDS_TRANSLATE_SPECIAL.items():
            try:
                val = settings
                for key in path.split('.'):
                    val = val[key]
                
                # Apply appropriate transformation based on field type
                if field in self.FIELDS_TYPING.get('bool', []):
                    simple[field] = is_true(val)
                elif field in self.FIELDS_TYPING.get('select', []):
                    simple[field] = get_selected(val) if isinstance(val, dict) else str(val)
                elif field in self.FIELDS_TYPING.get('list', []):
                    simple[field] = get_selected_list(val) if isinstance(val, dict) else []
                elif field in self.FIELDS_TYPING.get('int', []):
                    simple[field] = int(val) if val and str(val).isdigit() else (1515 if 'auth_port' in field else (1514 if 'port' in field else 0))
                else:
                    simple[field] = str(val) if val else ''
                    
            except (KeyError, TypeError, ValueError):
                # Set appropriate defaults
                if field in self.FIELDS_TYPING.get('bool', []):
                    simple[field] = False
                elif field in self.FIELDS_TYPING.get('int', []):
                    simple[field] = 1515 if 'auth_port' in field else (1514 if 'port' in field else 0)
                elif field in self.FIELDS_TYPING.get('list', []):
                    simple[field] = []
                else:
                    simple[field] = ''

        return simple

    def _build_request(self) -> dict:
        # Use framework's build_request, ignoring only the special nested fields
        special_fields = list(self.FIELDS_TRANSLATE_SPECIAL.keys())
        raw_request = self.b.build_request(ignore_fields=special_fields)
        
        # Start with what the framework built for flat fields
        request = raw_request.get(self.API_KEY, {}) if raw_request else {}
        
        # Build nested structure directly from FIELDS_TRANSLATE_SPECIAL
        for field, path in self.FIELDS_TRANSLATE_SPECIAL.items():
            if field in self.p and self.p[field] is not None:
                # Parse the path to get section and api_field
                section, api_field = path.split('.', 1)
                
                # Ensure section exists in request
                if section not in request:
                    request[section] = {}
                
                # Apply appropriate transformation based on field type
                if field in self.FIELDS_TYPING.get('bool', []):
                    request[section][api_field] = to_digit(self.p[field])
                elif field in self.FIELDS_TYPING.get('list', []):
                    request[section][api_field] = self.b.RESP_JOIN_CHAR.join(
                        self.p[field]
                    ) if isinstance(self.p[field], list) else ''
                elif field in self.FIELDS_TYPING.get('int', []):
                    request[section][api_field] = str(self.p[field])
                else:
                    request[section][api_field] = self.p[field]
        
        return {self.API_KEY: request} if request else {}