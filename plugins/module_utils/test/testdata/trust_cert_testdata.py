from ansible_collections.oxlorg.opnsense.plugins.module_utils.test.testdata.trust_ca_testdata import TrustTestdata


class Testdata_26_7_3(TrustTestdata):
    KEY = 'cert'
    LIFETIME_DEFAULT = 397
    ACTION_READ = 'reissue'
    ACTIONS_REGENERATE = ['internal', 'reissue']
    EXPORT_TYPES = ['crt', 'prv', 'csr', 'pkcs12']

    def __init__(self):
        super().__init__()
        self.cas = [
            {'caref': '65f0af2ce06c7', 'descr': 'OpenVPN'},
            {'caref': '6adf83700f877', 'descr': 'TestCA'},
        ]
        uuid = self._new_uuid()
        self.state[uuid] = self._build_entry({
            'descr': 'OpenVPN Server', 'caref': '65f0af2ce06c7', 'cert_type': 'server_cert', 'lifetime': '397',
            'country': 'AT', 'commonname': 'OpenVPN Server',
            # openssl returns IPv6 SANs in their expanded form
            'altnames_ip': '192.168.1.1\n2001:DB8:0:0:0:0:0:1',
        })
        self.state[uuid]['refid'] = '65f0af2ce06c8'
        self._issue(self.state[uuid], {'descr': 'OpenVPN Server', 'lifetime': '397'})

    def _build_entry(self, data: dict) -> dict:
        return {
            'descr': data['descr'],
            'caref': data.get('caref', ''),
            'key_type': data.get('key_type', '2048'),
            'digest': data.get('digest', 'sha256'),
            'cert_type': data.get('cert_type', 'usr_cert'),
            'private_key_location': data.get('private_key_location', 'firewall'),
            'city': data.get('city', ''),
            'state': data.get('state', ''),
            'organization': data.get('organization', ''),
            'organizationalunit': data.get('organizationalunit', ''),
            'country': data.get('country', 'NL'),
            'email': data.get('email', ''),
            'commonname': data.get('commonname', ''),
            'ocsp_uri': data.get('ocsp_uri', ''),
            'altnames_dns': data.get('altnames_dns', ''),
            'altnames_ip': data.get('altnames_ip', ''),
            'altnames_uri': data.get('altnames_uri', ''),
            'altnames_email': data.get('altnames_email', ''),
            'csr_payload': '',
            'rfc3280_purpose': 'id-kp-serverAuth',
            'in_use': '0',
            'is_user': '0',
            'name': f"/C={data.get('country', 'NL')}",
        }
