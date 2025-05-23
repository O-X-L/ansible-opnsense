from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import \
    get_selected_list, simplify_translate
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.cls import BaseModule


class SubnetV4(BaseModule):
    CMDS = {
        'add': 'addSubnet',
        'del': 'delSubnet',
        'set': 'setSubnet',
        'search': 'searchSubnet',
        'detail': 'getSubnet',
    }
    API_KEY = 'subnet4'
    API_KEY_PATH = 'subnet4'
    API_MOD = 'kea'
    API_CONT = 'dhcpv4'
    API_CONT_REL = 'service'
    FIELDS_CHANGE = [
        'subnet', 'description', 'pools', 'auto_options',
    ]
    FIELDS_ALL = FIELDS_CHANGE
    FIELDS_TYPING = {
        'list': ['gateway', 'dns', 'domain_search', 'ntp_servers', 'time_servers'],  # 'pools',
        'bool': ['auto_options'],
    }
    FIELDS_TRANSLATE = {
        'auto_options': 'option_data_autocollect',
    }
    API_ATTR_OPTIONS = 'option_data'
    API_FIELDS_OPTIONS = [
        'gateway', 'routes', 'dns', 'domain', 'domain_search', 'ntp_servers', 'time_servers',
        'next_server', 'tftp_server', 'tftp_file',
    ]
    POOL_JOIN_CHAR = '\n'
    FIELDS_TRANSLATE_SPECIAL = {
        'dns': 'domain_name_servers',
        'domain': 'domain_name',
        'gateway': 'routers',
        'routes': 'static_routes',
        'tftp_server': 'tftp_server_name',
        'tftp_file': 'boot_file_name',
    }
    EXIST_ATTR = 'subnet'

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None, fail: dict = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session, f=fail)
        self.subnet = {}
        self.existing_subnets = None

    def _simplify_existing(self, entry: dict) -> dict:
        simple = simplify_translate(
            existing=entry,
            typing=self.FIELDS_TYPING,
            translate=self.FIELDS_TRANSLATE,
            ignore=self.API_FIELDS_OPTIONS,
        )

        simple['pools'] = simple['pools'].split(self.POOL_JOIN_CHAR)
        opts = entry[self.API_ATTR_OPTIONS]
        if isinstance(opts, dict):
            simple['dns'] = get_selected_list(opts[self.FIELDS_TRANSLATE_SPECIAL['dns']])
            simple['domain_search'] = get_selected_list(opts['domain_search'])
            simple['gateway'] = get_selected_list(opts[self.FIELDS_TRANSLATE_SPECIAL['gateway']])
            simple['routes'] = opts[self.FIELDS_TRANSLATE_SPECIAL['routes']]
            simple['domain'] = opts[self.FIELDS_TRANSLATE_SPECIAL['domain']]
            simple['ntp_servers'] = get_selected_list(opts['ntp_servers'])
            simple['time_servers'] = get_selected_list(opts['time_servers'])
            simple['tftp_server'] = opts[self.FIELDS_TRANSLATE_SPECIAL['tftp_server']]
            simple['tftp_file'] = opts[self.FIELDS_TRANSLATE_SPECIAL['tftp_file']]

        else:
            opt_keys = list(self.FIELDS_TRANSLATE_SPECIAL.keys())
            opt_keys.extend(['domain_search', 'ntp_servers', 'time_servers'])

            for opt in opt_keys:
                if opt in self.FIELDS_TYPING['list']:
                    simple[opt] = []

                else:
                    simple[opt] = ''

        return simple

    def _build_request(self) -> dict:
        raw_request = self.b.build_request(ignore_fields=self.API_FIELDS_OPTIONS)

        raw_request[self.API_KEY]['pools'] = self.POOL_JOIN_CHAR.join(self.p['pools'])
        raw_request[self.API_KEY][self.API_ATTR_OPTIONS] = {
            self.FIELDS_TRANSLATE_SPECIAL['dns']: self.b.RESP_JOIN_CHAR.join(self.p['dns']),
            self.FIELDS_TRANSLATE_SPECIAL['gateway']: self.b.RESP_JOIN_CHAR.join(self.p['gateway']),
            self.FIELDS_TRANSLATE_SPECIAL['routes']: self.p['routes'],
            self.FIELDS_TRANSLATE_SPECIAL['domain']: self.p['domain'],
            self.FIELDS_TRANSLATE_SPECIAL['tftp_server']: self.p['tftp_server'],
            self.FIELDS_TRANSLATE_SPECIAL['tftp_file']: self.p['tftp_file'],
            'ntp_servers': self.b.RESP_JOIN_CHAR.join(self.p['ntp_servers']),
            'time_servers': self.b.RESP_JOIN_CHAR.join(self.p['time_servers']),
            'domain_search': self.b.RESP_JOIN_CHAR.join(self.p['domain_search']),
        }

        return raw_request
