from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.cls import BaseModule


class HaproxyFcgi(BaseModule):
    CMDS = {
        'add': 'addFcgi',
        'del': 'delFcgi',
        'set': 'setFcgi',
        'search': 'get',
        'toggle': 'toggleFcgi',
    }
    API_KEY_PATH = 'haproxy.fcgis.fcgi'
    API_KEY_PATH_REQ = 'fcgi'
    API_MOD = 'haproxy'
    API_CONT = 'settings'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigure'

    FIELDS_TRANSLATE = {
        'enabled': 'enabled',
        'name': 'name',
        'description': 'description',
        'docroot': 'docroot',
        'index': 'index',
        'path_info': 'path_info',
        'log_stderr': 'log_stderr',
        'keep_conn': 'keep_conn',
        'get_values': 'get_values',
        'mpxs_conns': 'mpxs_conns',
        'max_reqs': 'max_reqs',
        'linked_actions': 'linkedActions'
    }

    FIELDS_CHANGE = list(FIELDS_TRANSLATE.keys())
    FIELDS_ALL = FIELDS_CHANGE

    FIELDS_TYPING = {
        'bool': ['enabled', 'log_stderr', 'keep_conn', 'get_values', 'mpxs_conns'],
        'str': ['name', 'description', 'docroot', 'index', 'path_info'],
        'int': ['max_reqs'],
        'list': ['linked_actions']
    }
    FIELD_ID = 'name'
    EXIST_ATTR = 'fcgi'
    TIMEOUT = 60.0

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        # Resolve action names to UUIDs before calling parent __init__
        self._resolve_names_to_uuids(module)
        BaseModule.__init__(self=self, m=module, r=result, s=session)
        self.fcgi = {}

    def _resolve_names_to_uuids(self, module: AnsibleModule):
        """Resolve action names to UUIDs in module parameters"""
        if 'linked_actions' not in module.params or not module.params['linked_actions']:
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

        if 'haproxy' not in current_config or 'actions' not in current_config['haproxy']:
            module.fail_json(msg="No actions found in HAProxy configuration")

        actions_config = current_config['haproxy']['actions']
        resolved_actions = []

        for action_name in module.params['linked_actions']:
            action_uuid = None
            # Find UUID for the given action name
            for action_uuid_candidate, action_data in actions_config.get('action', {}).items():
                if action_data.get('name') == action_name:
                    action_uuid = action_uuid_candidate
                    break

            if not action_uuid:
                module.fail_json(msg=f"Action '{action_name}' not found")

            resolved_actions.append(action_uuid)

        # Update module params with resolved UUIDs
        module.params['linked_actions'] = resolved_actions