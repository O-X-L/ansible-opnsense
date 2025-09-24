from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import \
    is_unset
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.cls import BaseModule


MOCK_RESPONSES = {
    'get-test/settings/get': {'test': {'tests': {'test': {}}}},
}


class MockOPNsenseModule(BaseModule):
    FIELD_ID = 'description'
    CMDS = {
        'add': 'add_job',
        'del': 'del_job',
        'set': 'set_job',
        'search': 'get',
        'toggle': 'toggle_job',
    }
    API_KEY_PATH = 'test.tests.test'
    API_MOD = 'test'
    API_CONT = 'settings'
    API_CONT_REL = 'service'
    FIELDS_CHANGE = [
        'minutes', 'hours', 'days', 'months',
        'weekdays', 'command', 'who', 'parameters'
    ]
    FIELDS_TYPING = {
        'bool': ['enabled'],
        'select': ['command'],
        'int': ['minutes', 'hours', 'days', 'months', 'weekdays'],
    }
    FIELDS_ALL = ['description', 'enabled']
    FIELDS_ALL.extend(FIELDS_CHANGE)
    EXIST_ATTR = 'existing'

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None, fail: dict = None, multi: dict = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session, f=fail, multi=multi)
        self.existing = {}
        self.available_commands = []

    def check(self) -> None:
        self._base_check()
