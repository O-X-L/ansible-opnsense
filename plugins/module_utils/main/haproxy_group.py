from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.validate import \
    is_unset
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.cls import BaseModule


class HaproxyGroup(BaseModule):
    FIELD_ID = 'name'
    CMDS = {
        'add': 'addGroup',
        'del': 'delGroup',
        'set': 'setGroup',
        'search': 'searchGroups',
        'detail': 'getGroup',
        'toggle': 'toggleGroup',
    }
    API_KEY_PATH = 'group'
    API_MOD = 'haproxy'
    API_CONT = 'settings'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigure'
    FIELDS_CHANGE = ['enabled', 'description', 'members', 'add_userlist']
    FIELDS_ALL = ['name']
    FIELDS_ALL.extend(FIELDS_CHANGE)
    FIELDS_TRANSLATE = {
        'enabled': 'enabled',
        'description': 'description', 
        'name': 'name',
        'members': 'members',
        'add_userlist': 'add_userlist'
    }
    FIELDS_TYPING = {
        'bool': ['enabled']
    }
    EXIST_ATTR = 'group'
    TIMEOUT = 60.0

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session)
        self.group = {}

    def check(self) -> None:
        if self.p['state'] == 'present':
            if is_unset(self.p['name']):
                self.m.fail_json('You need to provide a name to create a group!')

        self._base_check()

    def _build_request(self) -> dict:
        """
        Override request building to handle user linking.
        """
        # Build base request
        request_data = {}
        
        # Handle basic fields
        for field in ['name', 'description']:
            if field in self.p and self.p[field] is not None:
                request_data[field] = self.p[field]
        
        # Handle boolean fields
        for field in ['enabled', 'add_userlist']:
            if field in self.p:
                request_data[field] = '1' if self.p[field] else '0'
        
        # Handle members - resolve user names to UUIDs
        # IMPORTANT: Use 'members' (underscore) for UI compatibility, not camelCase
        if 'members' in self.p and self.p['members']:
            user_uuids = self._resolve_user_names(self.p['members'])
            if user_uuids:
                # Join UUIDs with comma for HAProxy API (same pattern as linkedServers)
                request_data['members'] = ','.join(user_uuids)
        
        return {self.API_KEY_PATH: request_data}
    
    def _resolve_user_names(self, user_names: list) -> list:
        """
        Resolve user names to UUIDs by fetching the user list.
        """
        if not user_names:
            return []
        
        try:
            # Get all users
            users_response = self.s.get(cnf={
                'module': self.API_MOD,
                'controller': self.API_CONT,
                'command': 'searchUsers'
            })
            
            if 'rows' in users_response:
                user_uuids = []
                for user_name in user_names:
                    for user in users_response['rows']:
                        if user.get('name') == user_name:
                            user_uuids.append(user.get('uuid'))
                            break
                    else:
                        self.m.warn(f"User '{user_name}' not found, skipping")
                
                if self.p.get('debug', False):
                    self.m.warn(f"Resolved users: {dict(zip(user_names, user_uuids))}")
                
                return user_uuids
            
        except Exception as e:
            self.m.warn(f"Failed to resolve user names: {str(e)}")
        
        return []