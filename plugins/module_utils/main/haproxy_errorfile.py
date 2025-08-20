from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.validate import \
    is_unset
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.cls import BaseModule


class HaproxyErrorfile(BaseModule):
    FIELD_ID = 'name'
    CMDS = {
        'add': 'addErrorfile',
        'del': 'delErrorfile',
        'set': 'setErrorfile',
        'search': 'searchErrorfiles',
        'detail': 'getErrorfile',
        'toggle': 'toggleErrorfile',
    }
    API_KEY_PATH = 'errorfile'
    API_MOD = 'haproxy'
    API_CONT = 'settings'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigure'
    FIELDS_CHANGE = ['description', 'code', 'content']
    FIELDS_ALL = ['name', 'description']
    FIELDS_TRANSLATE = {
        'description': 'description', 
        'name': 'name'
    }
    FIELDS_TYPING = {
        'select': ['code']
    }
    EXIST_ATTR = 'errorfile'
    TIMEOUT = 60.0

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session)
        self.errorfile = {}

    def check(self) -> None:
        if self.p['state'] == 'present':
            if is_unset(self.p['name']):
                self.m.fail_json('You need to provide a name to create an error file!')

            if is_unset(self.p['code']):
                self.m.fail_json('You need to provide a code to create an error file!')

            if is_unset(self.p['content']):
                self.m.fail_json('You need to provide content to create an error file!')

        self._base_check()

    def _search_call(self) -> list:
        """
        Override _search_call method which is called by Base.find().
        The search API only returns name, description, uuid but not code/content.
        """
        try:
            response = self.s.get(cnf={
                'module': self.API_MOD,
                'controller': self.API_CONT,
                'command': self.CMDS['search']
            })
            
            if 'rows' in response:
                return response['rows']
            return []
            
        except Exception as e:
            self.m.warn(f"Search API failed: {str(e)}")
            return []
    
    def simplify_existing(self, existing: dict) -> dict:
        """
        Override simplify_existing to only process fields available from search API.
        ErrorFiles search API only returns name, description, uuid - not code/content.
        """
        simplified = {}
        available_fields = ['name', 'description', 'uuid']
        
        for field in available_fields:
            if field in existing:
                simplified[field] = existing[field]
        
        return simplified

    def update(self) -> None:
        """
        Override update to handle ErrorFiles properly.
        Since API inconsistency prevents proper update detection, always recreate.
        """
        if self.exists:
            # Delete existing entry first
            self.b.delete()
        
        # Create new entry
        self.create()

    def _build_request(self) -> dict:
        """
        Override request building to include all required fields for ErrorFiles.
        """
        return {
            self.API_KEY_PATH: {
                'name': self.p['name'],
                'description': self.p.get('description', ''),
                'code': self.p['code'],
                'content': self.p['content']
            }
        }