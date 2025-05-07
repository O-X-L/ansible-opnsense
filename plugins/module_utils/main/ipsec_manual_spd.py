from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.cls import BaseModule


class ManualSPD(BaseModule):
    FIELD_ID = 'name'
    CMDS = {
        'add': 'add',
        'del': 'del',
        'set': 'set',
        'search': 'search',
        'detail': 'get',
        'toggle': 'toggle',
    }
    API_KEY_PATH = 'spd'
    API_MOD = 'ipsec'
    API_CONT = 'manual_spd'
    API_CONT_REL = 'service'
    FIELDS_CHANGE = ['request_id', 'connection_child', 'source', 'destination', 'name']
    FIELDS_ALL = ['enabled']
    FIELDS_ALL.extend(FIELDS_CHANGE)
    FIELDS_TRANSLATE = {
        'name': 'description',
        'request_id': 'reqid',
    }
    FIELDS_TYPING = {
        'bool': ['enabled'],
        'list': [],
        'select': ['connection_child'],
        'int': ['request_id'],
    }
    INT_VALIDATIONS = {
        'request_id': {'min': 1, 'max': 65535},
    }
    EXIST_ATTR = 'spd'

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session)
        self.spd = {}

    def check(self) -> None:
        self._base_check()

        if self.p['state'] == 'present':
            self.b.find_single_link(
                field='connection_child',
                existing=self._search_connection_child(),
                existing_field_id='value',
            )

    def _search_connection_child(self) -> dict:
        return self.s.get(cnf={
            **self.call_cnf, **{'command': self.CMDS['detail']}
        })['spd']['connection_child']
