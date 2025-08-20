from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.validate import \
    is_unset
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.cls import BaseModule


class HaproxyCpu(BaseModule):
    FIELD_ID = 'name'
    CMDS = {
        'add': 'addCpu',
        'del': 'delCpu',
        'set': 'setCpu',
        'search': 'searchCpus',
        'detail': 'getCpu',
        'toggle': 'toggleCpu',
    }
    API_KEY_PATH = 'cpu'
    API_MOD = 'haproxy'
    API_CONT = 'settings'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigure'
    FIELDS_CHANGE = ['enabled', 'thread_id', 'cpu_id']
    FIELDS_ALL = ['name']
    FIELDS_ALL.extend(FIELDS_CHANGE)
    FIELDS_TRANSLATE = {
        'enabled': 'enabled',
        'name': 'name',
        'thread_id': 'thread_id',
        'cpu_id': 'cpu_id'
    }
    FIELDS_TYPING = {
        'bool': ['enabled']
    }
    EXIST_ATTR = 'cpu'
    TIMEOUT = 60.0

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session)
        self.cpu = {}

    def check(self) -> None:
        if self.p['state'] == 'present':
            if is_unset(self.p['name']):
                self.m.fail_json('You need to provide a name to create a CPU affinity rule!')
            
            if is_unset(self.p['thread_id']):
                self.m.fail_json('You need to provide a thread_id for the CPU affinity rule!')
                
            if is_unset(self.p['cpu_id']):
                self.m.fail_json('You need to provide a cpu_id for the CPU affinity rule!')

        self._base_check()
