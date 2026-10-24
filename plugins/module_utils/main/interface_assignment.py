from ansible.module_utils.basic import AnsibleModule

from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.oxlorg.opnsense.plugins.module_utils.helper.validate import \
    is_unset
from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.module import BaseModule
from ansible_collections.oxlorg.opnsense.plugins.module_utils.helper.translate import \
    get_selected

class Assignment(BaseModule):
    FIELD_ID = 'identifier'
    CMDS = {
        'add': 'add_item',
        'del': 'del_item',
        'set': 'set_item',
        'search': 'search_item',
        'detail': 'get_item',
    }
    API_KEY_PATH = 'interface'
    API_MOD = 'interfaces'
    API_CONT = 'assignment'
    # todo: implement the other ~20 fields
    FIELDS_CHANGE = ['description', 'device', 'lock']
    FIELDS_ALL = [FIELD_ID]
    FIELDS_ALL.extend(FIELDS_CHANGE)
    FIELDS_TRANSLATE = {
        'device': 'if',
        'description': 'descr',
        'disable_vlan_hw_filter': 'disablevlanhwfilter',
        'dhcp_reject_from': 'dhcprejectfrom',
        'dhcp_vlan_prio': 'dhcpvlanprio',
        'dhcpv6_vlan_prio': 'dhcp6vlanprio',
        'dhcpv6_ia_pd_len': 'dhcp6-ia-pd-len',
        'track6_interface': 'track6-interface',
        'gateway_v6': 'gatewayv6',
    }
    FIELDS_TYPING = {
        'str': ['description', 'identifier'],
        'bool': ['lock'],
        'select': [
            'device', 'media', 'disable_vlan_hw_filter', 'type4', 'type6', 'dhcp_reject_from', 'dhcp_vlan_prio',
            'dhcpv6_vlan_prio', 'dhcpv6_ia_pd_len', 'track6_interface', 'gateway', 'gateway_v6',
        ],
    }
    EXIST_ATTR = 'assignment'

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None, fail: dict = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session, f=fail)
        self.assignment = {}

    def _find_device(self) -> None:
        for assignment in self.get_existing():
            device = get_selected(assignment.get('device', {}))

            # device and id both are unique
            if device == self.p['device'] or assignment['identifier'] == self.p['identifier']:
                self.exists = True
                self.e = assignment
                self.p['identifier'] = assignment['identifier']
                return

    def check(self) -> None:
        self._find_device()

        if self.p['state'] == 'absent':
            if is_unset(self.p['identifier']):
                self.m.fail_json("You need to provide a 'identifier' to delete an interface-assignment!")

            if self.exists and self.e['lock']:
                self.m.fail_json("You need to unlock the interface before you delete an interface-assignment!")

        if self.p['state'] == 'present' and not self.exists:
            if is_unset(self.p['device']):
                self.m.fail_json("You need to provide a 'device' to create an interface-assignment!")

        self._base_check()
