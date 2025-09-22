from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.cls import GeneralModule


class GeneralStats(GeneralModule):
    CMDS = {
        'set': 'set',
        'search': 'get',
    }
    API_KEY_PATH = 'haproxy.general.stats'
    API_KEY_PATH_REQ = API_KEY_PATH
    API_MOD = 'haproxy'
    API_CONT = 'settings'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigure'

    FIELDS_TRANSLATE = {
        'port': 'port',
        'remote_enabled': 'remoteEnabled',
        'remote_bind': 'remoteBind',
        'auth_enabled': 'authEnabled',
        'users': 'users',
        'allowed_users': 'allowedUsers',
        'allowed_groups': 'allowedGroups',
        'custom_options': 'customOptions',
        'prometheus_enabled': 'prometheus_enabled',
        'prometheus_bind': 'prometheus_bind',
        'prometheus_path': 'prometheus_path',
    }

    FIELDS_CHANGE = list(FIELDS_TRANSLATE.keys()) + ['enabled']
    FIELDS_ALL = FIELDS_CHANGE

    FIELDS_TYPING = {
        'bool': ['enabled', 'remote_enabled', 'auth_enabled', 'prometheus_enabled'],
        'int': ['port'],
        'list': ['remote_bind', 'users', 'allowed_users', 'allowed_groups', 'prometheus_bind'],
    }

    INT_VALIDATIONS = {
        'port': {'min': 1024, 'max': 65535},
    }

    TIMEOUT = 60.0

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        # Resolve user and group names to UUIDs before calling parent __init__
        self._resolve_names_to_uuids(module)
        GeneralModule.__init__(self=self, m=module, r=result, s=session)

    def _resolve_names_to_uuids(self, module: AnsibleModule):
        """Resolve user and group names to UUIDs in module parameters"""
        if not any(param in module.params for param in ['allowed_users', 'allowed_groups']):
            return

        # Create temporary session to get HAProxy configuration
        temp_session = Session(
            module=module,
            timeout=self.TIMEOUT if hasattr(self, 'TIMEOUT') else 60.0
        )

        # Get current HAProxy configuration
        current_config = temp_session.get(cnf={
            'module': self.API_MOD,
            'controller': self.API_CONT,
            'command': 'get'
        })

        # Resolve user names
        if 'allowed_users' in module.params and module.params['allowed_users']:
            users_config = current_config.get('haproxy', {}).get('users', {}).get('user', {})
            resolved_users = []

            for user_name in module.params['allowed_users']:
                user_uuid = None
                for uuid, user_data in users_config.items():
                    if user_data.get('name') == user_name:
                        user_uuid = uuid
                        break

                if user_uuid:
                    resolved_users.append(user_uuid)
                else:
                    module.fail_json(msg=f"User '{user_name}' not found in HAProxy users configuration")

            module.params['allowed_users'] = resolved_users

        # Resolve group names
        if 'allowed_groups' in module.params and module.params['allowed_groups']:
            groups_config = current_config.get('haproxy', {}).get('groups', {}).get('group', {})
            resolved_groups = []

            for group_name in module.params['allowed_groups']:
                group_uuid = None
                for uuid, group_data in groups_config.items():
                    if group_data.get('name') == group_name:
                        group_uuid = uuid
                        break

                if group_uuid:
                    resolved_groups.append(group_uuid)
                else:
                    module.fail_json(msg=f"Group '{group_name}' not found in HAProxy groups configuration")

            module.params['allowed_groups'] = resolved_groups