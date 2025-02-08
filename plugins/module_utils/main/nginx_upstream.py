from ansible.module_utils.basic import AnsibleModule
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.cls import BaseModule
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import is_unset, validate_int_fields

class Upstream(BaseModule):
    FIELD_ID = 'description'
    CMDS = {
        'add': 'addupstream',
        'del': 'delupstream',
        'detail': 'getupstream',
        'search': 'searchupstream',
        'set': 'setupstream',
    }
    API_KEY_PATH = 'upstream'
    API_MOD = 'nginx'
    API_CONT = 'settings'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigure'
    FIELDS_CHANGE = [
        'description', 'serverentries', 'load_balancing_algorithm', 'keepalive',
        'keepalive_requests', 'keepalive_timeout', 'host_port',
        'x_forwarded_host_verbatim', 'proxy_protocol', 'store', 'tls_enable',
        'tls_client_certificate', 'tls_name_override', 'tls_protocol_versions',
        'tls_session_reuse', 'tls_trusted_certificate', 'tls_verify',
        'tls_verify_depth'
    ]
    FIELDS_ALL = FIELDS_CHANGE
    FIELDS_TYPING = {
        'bool': ['x_forwarded_host_verbatim', 'proxy_protocol', 'store',
                'tls_enable', 'tls_session_reuse', 'tls_verify'],
        'list': ['serverentries', 'tls_protocol_versions', 'tls_trusted_certificate'],
        'int': ['keepalive', 'keepalive_requests', 'keepalive_timeout',
                'host_port', 'tls_verify_depth'],
        'select': ['load_balancing_algorithm'],
    }
    INT_VALIDATIONS = {
         'keepalive': {'min': 0, 'max': 1000000000},
         'keepalive_requests': {'min': 1, 'max': 1000000000},
         'keepalive_timeout': {'min': 1, 'max': 1000000000},
         'host_port': {'min': 1, 'max': 65535},
         'tls_verify_depth': {'min': 1, 'max': 1000000000},
    }
    FIELDS_IGNORE = []
    FIELDS_REQUIRED = ['description', 'serverentries']
    FIELDS_DEFAULTS = {
        'x_forwarded_host_verbatim': False,
        'keepalive_requests': 1000,
        'keepalive_timeout': 75,
        'proxy_protocol': False,
        'store': False,
        'tls_enable': False,
        'tls_session_reuse': True,
        'tls_verify': True,
        'tls_verify_depth': 1,
    }
    EXIST_ATTR = 'upstream'
    
    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session)
        self.upstream = {}
        self.existing_upstream_servers = None
        self.existing_tls_client_certificates = None
        self.existing_tls_trusted_certificates = None

    def check(self):
        if self.p['state'] == 'present':
            if is_unset(self.p['description']) or is_unset(self.p['serverentries']):
                self.m.fail_json("You need to provide a 'description' and 'serverentries' to create an upstream!")

            validate_int_fields(module=self.m, data=self.p, field_minmax=self.INT_VALIDATIONS)

            if 'tls_protocol_versions' in self.p and self.p['tls_protocol_versions']:
                valid_versions = ['TLSv1', 'TLSv1.1', 'TLSv1.2', 'TLSv1.3']
                for version in self.p['tls_protocol_versions']:
                    if version not in valid_versions:
                        self.m.fail_json(
                            f"Invalid TLS protocol version: '{version}'. "
                            f"Valid versions are: {', '.join(valid_versions)}"
                        )

            if 'load_balancing_algorithm' in self.p and self.p['load_balancing_algorithm']:
                if self.p['load_balancing_algorithm'] not in ['ip_hash']:
                    self.m.fail_json(
                        f"Invalid load balancing algorithm: '{self.p['load_balancing_algorithm']}'. "
                        "Valid algorithms are: 'ip_hash'"
                    )

            self._base_check()

        if self.p['state'] == 'present':
            self._resolve_relations()

    def _search_uppstream_servers(self) -> None:
        self.existing_upstream_servers = self.s.get(cnf={
            **self.call_cnf, **{'command': 'searchupstreamserver', 'controller': 'settings'}
        })['rows']

    def _search_tls_client_certificates(self) -> None:
        self.existing_tls_client_certificates = self.s.get(cnf={
            **{'module': 'trust', 'command': 'search', 'controller': 'cert'}
        })['rows']

    def _search_tls_trusted_certificates(self) -> None:
        self.existing_tls_trusted_certificates = self.s.get(cnf={
            **{'module': 'trust', 'command': 'search', 'controller': 'ca'}
        })['rows']
    
    def _resolve_relations(self) -> None:
        if not is_unset(self.p['serverentries']):
            self._search_uppstream_servers()
            mapping = {
                server['description']: server['uuid']
                for server in self.existing_upstream_servers
            }

            missing = [
                entry
                for entry in self.p['serverentries']
                if entry not in mapping
            ]
            if any(missing):
                self.m.fail_json(f"Server entries {missing.join(',')} do not exist!")

            self.p['serverentries'] = [
                mapping[entry]
                for entry in self.p['serverentries']
            ]
        
        if not is_unset(self.p['tls_client_certificate']):
            self._search_tls_client_certificates()
            mapping = {
                certificate['descr']: certificate['refid']
                for certificate in self.existing_tls_client_certificates
            }
            
            tls_client_certificate = self.p['tls_client_certificate']
            if tls_client_certificate not in mapping:
                self.m.fail_json(f"TLS client certificate {tls_client_certificate} does not exist!")

            self.p['tls_client_certificate'] = mapping[tls_client_certificate]

        if not is_unset(self.p['tls_trusted_certificate']):
            self._search_tls_trusted_certificates()
            mapping = {
                ca['descr']: ca['refid']
                for ca in self.existing_tls_trusted_certificates
            }

            missing = [
                entry
                for entry in self.p['tls_trusted_certificate']
                if entry not in mapping
            ]
            if any(missing):
                self.m.fail_json(f"TLS trusted certificates {missing.join(',')} do not exist!")

            self.p['tls_trusted_certificate'] = [
                mapping[entry]
                for entry in self.p['tls_trusted_certificate']
            ]


    def update(self) -> None:
        self.b.update(enable_switch=False)
    