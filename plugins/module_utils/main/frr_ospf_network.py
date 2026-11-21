from ansible.module_utils.basic import AnsibleModule

from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.oxlorg.opnsense.plugins.module_utils.helper.validate import \
    is_ip_or_network, is_unset
from ansible_collections.oxlorg.opnsense.plugins.module_utils.helper.frr import \
    find_ospf_area, ospf_area_diff, ospf_area_uuid_to_id
from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.module import BaseModule


class Network(BaseModule):
    CMDS = {
        'add': 'addNetwork',
        'del': 'delNetwork',
        'set': 'setNetwork',
        'search': 'get',
        'toggle': 'toggleNetwork',
    }
    API_KEY_PATH = 'ospf.networks.network'
    API_MOD = 'quagga'
    API_CONT = 'ospfsettings'
    API_CONT_REL = 'service'
    FIELDS_CHANGE = ['ip', 'mask', 'area']
    FIELDS_ALL = ['enabled']
    FIELDS_ALL.extend(FIELDS_CHANGE)
    FIELDS_TRANSLATE = {
        'ip': 'ipaddr',
        'mask': 'netmask',
    }
    FIELDS_TYPING = {
        'bool': ['enabled'],
        'select': ['area'],
    }
    INT_VALIDATIONS = {
        'mask': {'min': 0, 'max': 32},
    }
    EXIST_ATTR = 'net'
    SEARCH_ADDITIONAL = {
        'existing_areas': 'ospf.areas.area',
    }

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None, fail: dict = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session, f=fail)
        self.net = {}
        self.existing_areas = None
        self.existing_entries = None

    def check(self) -> None:
        if self.p['state'] == 'present':
            if is_unset(self.p['area']):
                self.m.fail_json(
                    'To create a OSPF network you need to provide an area!'
                )

            if not is_ip_or_network(f"{self.p['ip']}/{self.p['mask']}", strict=True):
                self.m.fail_json(
                    'The combination of the provided ip and network mask is invalid: '
                    f"'{self.p['ip']}/{self.p['mask']}'!"
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
