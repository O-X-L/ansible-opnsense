from copy import deepcopy

from ansible_collections.oxlorg.opnsense.plugins.module_utils.test.testdata.base_testdata import MockOPNsenseController

# used to verify that private keys never reach the module-result
SECRET = 'PRIVATE-KEY-MUST-NOT-ESCAPE'
SECONDS_PER_DAY = 86400
VALID_FROM = 1793033072


class TrustTestdata(MockOPNsenseController):
    """
    Emulates the OPNsense trust-API behavior (see: OPNsense/Trust/Api/CaController.php & CertController.php)
    * most fields are volatile - they are parsed from the certificate on every read
    * 'lifetime' is not parsed - the API always returns its default
    * 'action' is reset on every read
    """
    KEY = None
    LIFETIME_DEFAULT = None
    ACTION_READ = None
    ACTIONS_REGENERATE = []
    EXPORT_TYPES = []

    def __init__(self):
        super().__init__()
        self.state = {}
        self.cas = []
        self.calls = []
        self.regenerated = []
        self._refid = 0

    def commands(self) -> dict:
        return {
            'search': self._search,
            'get': self._detail,
            'add': self._add,
            'set': self._set,
            'del': self._del,
            'ca_list': self._ca_list,
            'generate_file': self._generate_file,
        }

    def route_kwargs(self, method) -> list:
        return {
            self._search: [],
            self._detail: ['uuid'],
            self._add: ['data'],
            self._set: ['uuid', 'data'],
            self._del: ['uuid'],
            self._ca_list: [],
            self._generate_file: ['params', 'data'],
        }[method]

    def _new_refid(self) -> str:
        # format of PHP 'uniqid()'
        self._refid += 1
        return f'6adf8{self._refid:08x}'

    def _issue(self, entry: dict, data: dict) -> None:
        entry['crt_payload'] = f"-----BEGIN CERTIFICATE-----\n{data['descr']}\n-----END CERTIFICATE-----\n"
        entry['crt'] = 'BASE64-CRT'
        entry['prv_payload'] = f'-----BEGIN PRIVATE KEY-----\n{SECRET}\n-----END PRIVATE KEY-----\n'
        entry['prv'] = SECRET
        entry['valid_from'] = str(VALID_FROM + len(self.regenerated))
        entry['valid_to'] = str(int(entry['valid_from']) + int(data['lifetime']) * SECONDS_PER_DAY)

    def _build_entry(self, data: dict) -> dict:
        raise NotImplementedError

    def _row(self, uuid: str) -> dict:
        row = deepcopy(self.state[uuid])
        row['uuid'] = uuid
        row['action'] = self.ACTION_READ
        row['lifetime'] = str(self.LIFETIME_DEFAULT)
        return row

    def _search(self) -> dict:
        self.calls.append(('search', None))
        rows = [self._row(uuid) for uuid in self.state]
        return {'rows': rows, 'rowCount': len(rows), 'total': len(rows), 'current': 1}

    def _detail(self, uuid: str) -> dict:
        self.calls.append(('get', uuid))
        row = self._row(uuid)
        row.pop('uuid')
        return {self.KEY: row}

    def _add(self, data: dict) -> dict:
        data = data[self.KEY]
        self.calls.append(('add', data))
        uuid = self._new_uuid()
        entry = self._build_entry(data)
        entry['refid'] = self._new_refid()
        self._issue(entry, data)
        self.state[uuid] = entry
        return {'result': 'saved', 'uuid': uuid}

    def _set(self, uuid: str, data: dict) -> dict:
        data = data[self.KEY]
        self.calls.append(('set', data))
        if uuid not in self.state:
            return {'result': 'failed'}

        entry = self.state[uuid]
        entry['descr'] = data['descr']
        if data['action'] in self.ACTIONS_REGENERATE:
            self.regenerated.append(uuid)
            self._issue(entry, data)

        return {'result': 'saved'}

    def _del(self, uuid: str) -> dict:
        self.calls.append(('del', uuid))
        if uuid not in self.state:
            return {'result': 'failed'}

        self.state.pop(uuid)
        return {'result': 'deleted'}

    def _ca_list(self) -> dict:
        return {'rows': self.cas, 'count': len(self.cas)}

    def _generate_file(self, params: list, data: dict = None) -> dict:
        uuid, file_type = params[0], params[1] if len(params) > 1 else 'crt'
        self.calls.append(('generate_file', file_type))
        if uuid not in self.state:
            return {'status': 'failed', 'descr': '', 'error': 'Missing certificate'}

        entry = self.state[uuid]
        result = {'status': 'ok', 'descr': entry['descr']}
        if file_type not in self.EXPORT_TYPES:
            # the API silently ignores unsupported types
            return {'status': 'failed', 'descr': entry['descr']}

        if file_type == 'pkcs12':
            password = '' if data is None else data.get('password', '')
            result['payload_b64'] = f"PKCS12({entry['crt_payload']}|{entry['prv_payload']}|{password})"

        else:
            result['payload'] = entry[f'{file_type}_payload']

        return result

    def mutations(self) -> list:
        return [call for call in self.calls if call[0] in ['add', 'set', 'del']]


class Testdata_26_7_3(TrustTestdata):
    KEY = 'ca'
    LIFETIME_DEFAULT = 825
    ACTION_READ = 'existing'
    ACTIONS_REGENERATE = ['internal', 'ocsp']
    EXPORT_TYPES = ['crt', 'prv']

    def __init__(self):
        super().__init__()
        # other mocks (p.e. certificates) whose entries reference CAs
        self.referrers = []
        # references by services (p.e. OpenVPN) - not modelled by the mock
        self.service_refs = {'65f0af2ce06c7': 2}
        uuid = self._new_uuid()
        self.state[uuid] = self._build_entry({
            'descr': 'OpenVPN', 'caref': '', 'key_type': '2048', 'digest': 'sha256', 'lifetime': '825',
            'country': 'AT', 'commonname': 'openvpn',
        })
        self.state[uuid]['refid'] = '65f0af2ce06c7'
        self._issue(self.state[uuid], {'descr': 'OpenVPN', 'lifetime': '825'})

    def _build_entry(self, data: dict) -> dict:
        return {
            'descr': data['descr'],
            'serial': '',
            'caref': data.get('caref', ''),
            'key_type': data.get('key_type', '2048'),
            'digest': data.get('digest', 'sha256'),
            'city': data.get('city', ''),
            'state': data.get('state', ''),
            'organization': data.get('organization', ''),
            'organizationalunit': data.get('organizationalunit', ''),
            'country': data.get('country', 'NL'),
            'email': data.get('email', ''),
            'commonname': data.get('commonname', ''),
            'ocsp_uri': data.get('ocsp_uri', ''),
            'name': f"/C={data.get('country', 'NL')}/CN={data.get('commonname', '')}",
        }

    def _row(self, uuid: str) -> dict:
        # the API counts all references to the refid inside the config
        row = super()._row(uuid)
        refid = row['refid']
        refcount = self.service_refs.get(refid, 0)
        for mock in [self, *self.referrers]:
            refcount += len([e for e in mock.state.values() if e['caref'] == refid])

        row['refcount'] = str(refcount)
        return row

    def _ca_list(self) -> dict:
        rows = [{'caref': e['refid'], 'descr': e['descr']} for e in self.state.values()]
        return {'rows': rows, 'count': len(rows)}

    def _set(self, uuid: str, data: dict) -> dict:
        if data[self.KEY]['action'] == 'existing' and \
                (data[self.KEY].get('crt_payload', '') == '' or data[self.KEY].get('prv_payload', '') == ''):
            # the import-action requires the certificate & key to be passed
            return {'result': 'failed', 'validations': {'ca.crt_payload': 'Only a single certificate is allowed'}}

        return super()._set(uuid, data)
