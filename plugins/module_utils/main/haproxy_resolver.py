from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.validate import \
    is_unset
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.cls import BaseModule


class HaproxyResolver(BaseModule):
    FIELD_ID = 'name'
    CMDS = {
        'add': 'addResolver',
        'del': 'delResolver',
        'set': 'setResolver',
        'search': 'searchresolvers',
        'detail': 'getResolver',
        'toggle': 'toggleResolver',
    }
    API_KEY_PATH = 'resolver'
    API_MOD = 'haproxy'
    API_CONT = 'settings'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigure'
    FIELDS_CHANGE = ['enabled', 'description']
    FIELDS_ALL = ['name']
    FIELDS_ALL.extend(FIELDS_CHANGE)
    FIELDS_TRANSLATE = {
        'enabled': 'enabled',
        'description': 'description', 
        'name': 'name'
    }
    FIELDS_TYPING = {
        'bool': ['enabled']
    }
    EXIST_ATTR = 'resolver'
    TIMEOUT = 60.0
    
    INT_VALIDATIONS = {
        'resolve_retries': {'min': 0, 'max': 100000},
    }

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session)
        self.resolver = {}

    def check(self) -> None:
        if self.p['state'] == 'present':
            if is_unset(self.p['name']):
                self.m.fail_json('You need to provide a name to create a resolver!')

            # Validate timeout format
            if not is_unset(self.p['timeout_resolve']):
                import re
                if not re.match(r'^[0-9]{1,8}(?:us|ms|s|m|h|d)?$', self.p['timeout_resolve']):
                    self.m.fail_json(
                        f"Value of timeout_resolve '{self.p['timeout_resolve']}' is invalid. "
                        f"Should be a number between 1 and 8 characters, optionally followed by "
                        f"either 'd', 'h', 'm', 's', 'ms' or 'us'."
                    )

            # Validate that nameservers are provided if not parsing resolv.conf
            if not self.p['parse_resolv_conf'] and is_unset(self.p['nameservers']):
                self.m.fail_json('You need to provide nameservers or enable parse_resolv_conf!')

        self._base_check()