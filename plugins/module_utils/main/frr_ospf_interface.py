from ansible.module_utils.basic import AnsibleModule

from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.oxlorg.opnsense.plugins.module_utils.helper.validate import \
    is_unset
from ansible_collections.oxlorg.opnsense.plugins.module_utils.helper.frr import \
    find_ospf_area, ospf_area_diff, ospf_area_uuid_to_id
from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.module import BaseModule


class Interface(BaseModule):
    CMDS = {
        'add': 'addInterface',
        'del': 'delInterface',
        'set': 'setInterface',
        'search': 'get',
        'toggle': 'toggleInterface',
    }
    API_KEY_PATH = 'ospf.interfaces.interface'
    API_MOD = 'quagga'
    API_CONT = 'ospfsettings'
    API_CONT_REL = 'service'
    FIELDS_CHANGE = [
        'interface', 'area', 'passive', 'auth_type', 'auth_key', 'auth_key_id', 'cost',
        'hello_interval', 'dead_interval', 'retransmit_interval', 'transmit_delay',
        'priority', 'network_type', 'carp_depend_on', 'cost_demoted',
    ]
    FIELDS_ALL = ['enabled']
    FIELDS_ALL.extend(FIELDS_CHANGE)
    INT_VALIDATIONS = {
        'cost': {'min': 1, 'max': 65535},
        'hello_interval': {'min': 0, 'max': 4294967295},
        'dead_interval': {'min': 0, 'max': 4294967295},
        'retransmit_interval': {'min': 0, 'max': 4294967295},
        'transmit_delay': {'min': 0, 'max': 4294967295},
        'priority': {'min': 0, 'max': 4294967295},
        'cost_demoted': {'min': 1, 'max': 65535},
        'auth_key_id': {'min': 1, 'max': 255},
    }
    FIELDS_TRANSLATE = {
        'interface': 'interfacename',
        'hello_interval': 'hellointerval',
        'dead_interval': 'deadinterval',
        'retransmit_interval': 'retransmitinterval',
        'transmit_delay': 'transmitdelay',
        'network_type': 'networktype',
        'auth_type': 'authtype',
        'auth_key': 'authkey',
        'auth_key_id': 'authkey_id',
    }
    FIELDS_TYPING = {
        'bool': ['enabled', 'passive'],
        'select': ['interface', 'area', 'carp_depend_on', 'network_type', 'auth_type'],
    }
    EXIST_ATTR = 'int'
    SEARCH_ADDITIONAL = {
        'existing_areas': 'ospf.areas.area',
    }

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None, fail: dict = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session, f=fail)
        self.int = {}
        self.existing_areas = None
        self.existing_entries = None

    def check(self) -> None:
        if self.p['state'] == 'present':
            if not is_unset(self.p['auth_type']) and is_unset(self.p['auth_key']):
                self.m.fail_json(
                    'You need to provide an authentication-key if you enable authentication!'
                )

        if self.existing_entries is None:
            self.existing_entries = self._call_search()

        find_ospf_area(self)
        self._base_check()
        ospf_area_diff(self)

    def get_existing(self) -> list:
        existing = []

        for entry in self._base_get_existing():
            entry['area'] = ospf_area_uuid_to_id(self, entry['area'])
            existing.append(entry)

        return existing
