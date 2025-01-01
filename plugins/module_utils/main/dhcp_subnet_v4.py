from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import \
    is_ip, is_network, is_unset
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.cls import BaseModule

class SubnetV4(BaseModule):
    FIELD_ID = 'subnet'
    CMDS = {
        'add': 'addSubnet',
        'del': 'delSubnet',
        'set': 'setSubnet',
        'search': 'searchSubnet',
        'detail': 'getSubnet',
    }
    API_KEY_PATH = 'subnet4'
    API_MOD = 'kea'
    API_CONT = 'dhcpv4'
    API_CONT_REL = 'service'
    FIELDS_CHANGE = [
        'subnet', 'description', 'pools'
    ]
    FIELDS_ALL = [FIELD_ID]
    FIELDS_ALL.extend(FIELDS_CHANGE)
    FIELDS_TYPING = {}
    FIELDS_TRANSLATE = {}
    EXIST_ATTR = 'subnet'

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session)
        self.subnet = {}
        self.existing_subnets = None

    def check(self) -> None:
        if self.p['state'] == 'present':
            if is_unset(self.p['subnet']):
                self.m.fail_json(
                    "You need to provide the 'subnet' you want to create. E.g. (192.168.1.0/24)!"
                )

            if is_unset(self.p['pools']):
                self.m.fail_json("You need to provide the IP 'pools' to be used in the subnet!")

        self._base_check()
