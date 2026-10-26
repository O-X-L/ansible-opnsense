from ansible_collections.oxlorg.opnsense.plugins.module_utils.helper.trust import \
    TRUST_SUBJECT_FIELDS, TRUST_FIELDS_TRANSLATE, TRUST_SAN_FIELDS, TRUST_SAN_TRANSLATE, split_san, \
    normalize_ips, validate_san
from ansible_collections.oxlorg.opnsense.plugins.module_utils.main.trust import BaseTrust


class Cert(BaseTrust):
    CMDS = {
        'add': 'add',
        'del': 'del',
        'set': 'set',
        'search': 'search',
        'detail': 'get',
        'ca_list': 'ca_list',
    }
    API_KEY_PATH = 'cert'
    API_CONT = 'cert'
    FIELDS_IMMUTABLE = [
        'ca', 'cert_type', 'key_type', 'digest', 'lifetime', 'ocsp_uri', *TRUST_SUBJECT_FIELDS, *TRUST_SAN_FIELDS,
    ]
    FIELDS_ALL = [*BaseTrust.FIELDS_CHANGE, *FIELDS_IMMUTABLE]
    FIELDS_TRANSLATE = {
        **TRUST_FIELDS_TRANSLATE,
        **TRUST_SAN_TRANSLATE,
    }
    FIELDS_TYPING = {
        'select': ['ca', 'cert_type', 'key_type', 'digest', 'country'],
    }
    FIELDS_VALUE_MAPPING = {
        'cert_type': {
            'client': 'usr_cert',
            'server': 'server_cert',
            'server_client': 'combined_server_client',
        },
    }
    JOIN_CHAR = '\n'  # SAN-values
    KIND = 'certificate'

    def check(self) -> None:
        if self.p['state'] == 'present':
            for field in TRUST_SAN_FIELDS:
                self.p[field] = validate_san(module=self.m, field=field, values=self.p[field])

        super().check()

    def simplify_existing(self, existing: dict) -> dict:
        simple = super().simplify_existing(existing)
        for field in TRUST_SAN_FIELDS:
            values = split_san(simple[field])
            if field == 'san_ip':
                values = normalize_ips(values)

            simple[field] = sorted(values)

        return simple

    def build_request(self) -> dict:
        request = self._base_build_request()

        if not self.exists:
            request[self.API_KEY_PATH]['action'] = 'internal'
            # the 'local' option only returns the key once - it would not be manageable
            request[self.API_KEY_PATH]['private_key_location'] = 'firewall'
            return request

        # the API defaults to the 'reissue' action for existing certificates
        #   'manual' keeps the existing certificate and key
        request[self.API_KEY_PATH]['action'] = 'manual'
        return request
