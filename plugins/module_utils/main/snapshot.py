from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.cls import BaseModule


class Snapshot(BaseModule):
    FIELD_ID = 'name'
    CMDS = {
        'add': 'add',
        'del': 'del',
        'search': 'search',
        'activate': 'activate',
    }
    API_KEY_PATH = None
    API_MOD = 'core'
    API_CONT = 'snapshots'
    FIELDS_CHANGE = []
    FIELDS_ALL = ['name']
    FIELDS_TYPING = {}
    EXIST_ATTR = 'snapshot'

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session)
        self.snapshot = {}

    def check(self) -> None:
        self._base_check()

        if self.p['activate'] and 'R' not in self.snapshot['active']:
            self.activate()

    def _search_call(self) -> dict:
        return self.s.get(cnf={
            **self.call_cnf,
            'command': self.CMDS['search'],
        })['rows']

    def create(self) -> dict:
        self.r['changed'] = True

        if not self.m.check_mode:
            resp = self.s.post({
                **self.call_cnf,
                'command': self.CMDS['add'],
                'data': {'name': self.p['name']},
            })
            if resp['status'] != 'ok':
                self.m.fail_json(f"Failed creating snapshot '{self.p['name']}'")

    def update(self) -> dict:
        pass

    def activate(self) -> dict:
        self.r['changed'] = True

        if not self.m.check_mode:
            resp = self.s.post({
                **self.call_cnf,
                'command': self.CMDS['activate'],
                'params': self.snapshot['uuid'],
            })
            if resp['status'] != 'ok':
                self.m.fail_json(f"Failed activating snapshot '{self.p['name']}'")
