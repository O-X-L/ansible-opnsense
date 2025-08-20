from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.validate import \
    is_unset
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.cls import BaseModule


class HaproxyHealthcheck(BaseModule):
    FIELD_ID = 'name'
    CMDS = {
        'add': 'addHealthcheck',
        'del': 'delHealthcheck',
        'set': 'setHealthcheck',
        'search': 'searchHealthchecks',
        'detail': 'getHealthcheck',
        'toggle': 'toggleHealthcheck',
    }
    API_KEY_PATH = 'healthcheck'
    API_MOD = 'haproxy'
    API_CONT = 'settings'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigure'
    FIELDS_CHANGE = ['description', 'type', 'interval', 'ssl', 'ssl_sni']
    FIELDS_ALL = ['name', 'description']
    FIELDS_TRANSLATE = {
        'description': 'description', 
        'name': 'name'
    }
    FIELDS_TYPING = {
        'bool': ['enabled']
    }
    EXIST_ATTR = 'healthcheck'
    TIMEOUT = 60.0

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session)
        self.healthcheck = {}

    def check(self) -> None:
        if self.p['state'] == 'present':
            if is_unset(self.p['name']):
                self.m.fail_json('You need to provide a name to create a health check!')

            if is_unset(self.p['type']):
                self.m.fail_json('You need to provide a type to create a health check!')

            # Validate interval format
            if not is_unset(self.p['interval']):
                import re
                if not re.match(r'^[0-9]{1,8}(?:us|ms|s|m|h|d)?$', self.p['interval']):
                    self.m.fail_json(
                        f"Value of interval '{self.p['interval']}' is invalid. "
                        f"Should be a number between 1 and 8 characters, optionally followed by "
                        f"either 'd', 'h', 'm', 's', 'ms' or 'us'."
                    )

        self._base_check()

    def simplify_existing(self, existing: dict) -> dict:
        """
        Override simplify_existing to only process fields available from search API.
        Health Checks API has complex nested structures that need filtering.
        """
        simplified = {}
        available_fields = ['name', 'description', 'uuid']
        
        for field in available_fields:
            if field in existing:
                simplified[field] = existing[field]
        
        return simplified