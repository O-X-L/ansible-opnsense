from ipaddress import ip_address

from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.api import Session
from ansible_collections.oxlorg.opnsense.plugins.module_utils.helper.translate import get_selected

SUBJECT_FIELDS = {
    'common_name': 'commonname', 'country': 'country', 'state_or_province': 'state',
    'city': 'city', 'organization': 'organization', 'organizational_unit': 'organizationalunit',
    'email': 'email',
}
CERTIFICATE_TYPES = {'server': 'server_cert', 'client': 'usr_cert',
                     'server_client': 'combined_server_client'}
SAN_FIELDS = {'san_dns': 'altnames_dns', 'san_ip': 'altnames_ip',
              'san_email': 'altnames_email', 'san_uri': 'altnames_uri'}
TRUST_ARGUMENTS = {
    'description': dict(type='str'),
    'uuid': dict(type='str'),
    'state': dict(type='str', choices=['present'], default='present'),
    'key_type': dict(type='str', choices=['2048', '3072', '4096', '7680', '8192',
                                        'prime256v1', 'secp384r1', 'secp521r1']),
    'digest': dict(type='str', choices=['sha256', 'sha384', 'sha512']),
    'lifetime': dict(type='int'),
    **{field: dict(type='str') for field in SUBJECT_FIELDS},
}
CERT_ARGUMENTS = {
    'ca': dict(type='str'),
    'ca_refid': dict(type='str'),
    'certificate_type': dict(type='str', choices=list(CERTIFICATE_TYPES)),
    **{field: dict(type='list', elements='str') for field in SAN_FIELDS},
}


class Trust:
    """Create or verify trust entries without replaying certificate issuance."""

    def __init__(self, module, result, kind, session=None):
        self.m = module
        self.p = module.params
        self.r = result
        self.kind = kind
        self.s = session if session is not None else Session(module=module)
        self.cnf = {'module': 'trust', 'controller': kind, 'sensitive_response': True}

    def _rows(self):
        rows = []
        page = 1
        while True:
            response = self.s.post(cnf={
                **self.cnf, 'command': 'search', 'data': {'current': page, 'rowCount': 1000},
            })
            if not isinstance(response.get('rows'), list):
                self.m.fail_json('Trust API returned invalid search results; check API availability and privileges.')
            batch = response['rows']
            rows.extend(batch)
            if len(rows) >= int(response.get('total', len(rows))):
                return rows
            if not batch:
                self.m.fail_json('Trust API returned incomplete search results.')
            page += 1

    def _detail(self, uuid, require_certificate=True):
        response = self.s.get(cnf={**self.cnf, 'command': 'get', 'params': [uuid]})
        entry = response.get(self.kind)
        if not isinstance(entry, dict):
            self.m.fail_json('Trust API returned an invalid entry.')
        # Whitelist before any comparison, diff or returned data can see the response.
        safe = {
            'uuid': uuid, 'refid': entry.get('refid', ''), 'description': entry.get('descr', ''),
            'certificate_available': bool(entry.get('crt_payload')),
            'csr_available': bool(entry.get('csr_payload')),
        }
        if not safe['refid'] or not safe['certificate_available']:
            if require_certificate:
                self.m.fail_json('Trust entry is missing a certificate or reference; inspect it in System / Trust.')
            # Pending CSRs and externally managed certificates remain visible in lists.
            return safe
        fields = {**SUBJECT_FIELDS, 'key_type': 'key_type', 'digest': 'digest', 'ca_refid': 'caref'}
        if self.kind == 'cert':
            fields.update(SAN_FIELDS)
            fields['certificate_type'] = 'cert_type'
        for field, api_field in fields.items():
            value = get_selected(entry.get(api_field, ''))
            if field in SAN_FIELDS:
                value = self._san_values(field, value.splitlines() if value else [])
            elif field == 'certificate_type':
                value = next((name for name, api_value in CERTIFICATE_TYPES.items() if api_value == value), value)
            else:
                value = str(value)
            safe[field] = value
        try:
            safe['lifetime'] = (int(entry['valid_to']) - int(entry['valid_from'])) / 86400
        except (KeyError, TypeError, ValueError):
            self.m.fail_json('Trust API did not return valid certificate validity timestamps.')
        return safe

    def get_existing(self):
        return [self._detail(row['uuid'], require_certificate=False) for row in self._rows()]

    def _issuer(self):
        response = self.s.get(cnf={**self.cnf, 'command': 'ca_list'})
        rows = response.get('rows')
        if not isinstance(rows, list):
            self.m.fail_json('Trust API did not return a CA list.')
        refid, name = self.p.get('ca_refid'), self.p.get('ca')
        matches = [row for row in rows if row.get('caref') == refid] if refid else [
            row for row in rows if row.get('descr') == name]
        if len(matches) > 1:
            self.m.fail_json('Ambiguous CA description; provide ca_refid.')
        if not matches or not matches[0].get('caref'):
            self.m.fail_json('Requested CA does not exist; create it first or correct the CA selector.')
        return matches[0]['caref']

    def _desired(self):
        wanted = {}
        for field in [*SUBJECT_FIELDS, 'key_type', 'digest', 'lifetime', 'description']:
            if self.p.get(field) is not None:
                wanted[field] = self.p[field]
        if self.p.get('lifetime') is not None and self.p['lifetime'] <= 0:
            self.m.fail_json('lifetime must be a positive number of days.')
        if self.kind == 'ca':
            wanted['ca_refid'] = ''
        else:
            if self.p.get('ca') or self.p.get('ca_refid'):
                wanted['ca_refid'] = self._issuer()
            if self.p.get('certificate_type') is not None:
                wanted['certificate_type'] = self.p['certificate_type']
            for field in SAN_FIELDS:
                if self.p.get(field) is not None:
                    values = self.p[field]
                    if any(not value or any(char in value for char in ('\n', '\r', ',')) for value in values):
                        self.m.fail_json(
                            f'{field} must contain individual non-empty SAN values without newlines or commas.'
                        )
                    wanted[field] = self._san_values(field, values)
        return wanted

    def _san_values(self, field, values):
        if field == 'san_ip':
            try:
                values = [str(ip_address(value)) for value in values]
            except ValueError:
                self.m.fail_json('san_ip contains an invalid IP address.')
        return sorted(set(values))

    def _compare(self, existing, wanted):
        changed = []
        for field, expected in wanted.items():
            if field == 'lifetime':
                # Allow up to one minute of timestamp rounding when comparing validity duration.
                equal = abs(existing[field] - expected) <= 60 / 86400
            else:
                equal = existing.get(field) == expected
            if not equal:
                changed.append(field)
        if changed:
            self.m.fail_json(
                'Existing trust entry differs in ' + ', '.join(changed) +
                '; changing it would require replacement or reissuance. '
                'Use a new description and migrate references explicitly.'
            )

    def process(self):
        try:
            self._process()
        finally:
            self.s.close()

    def _process(self):
        uuid, description = self.p.get('uuid'), self.p.get('description')
        if not uuid and not description:
            self.m.fail_json('Provide description or UUID for the trust entry.')
        rows = self._rows()
        matches = [row for row in rows if row.get('uuid') == uuid] if uuid else [
            row for row in rows if row.get('descr') == description]
        if len(matches) > 1:
            self.m.fail_json('Ambiguous trust description; provide an explicit UUID.')
        if uuid and not matches:
            self.m.fail_json('The supplied trust UUID does not exist; refusing to create a replacement.')
        wanted = self._desired()
        if matches:
            existing = self._detail(matches[0]['uuid'])
            self._compare(existing, wanted)
            self.r.update(uuid=existing['uuid'], refid=existing['refid'], data=existing)
            return
        for field in ('description', 'common_name', 'country'):
            if not wanted.get(field):
                self.m.fail_json(f'{field} is required when creating a trust entry.')
        if self.kind == 'cert' and not wanted.get('ca_refid'):
            self.m.fail_json('ca or ca_refid is required when creating a certificate.')
        self._create(wanted)

    def _create(self, wanted):
        payload = self._creation_payload(wanted)
        self.r['changed'] = True
        self.r['diff'] = {'before': {}, 'after': wanted}
        if self.m.check_mode:
            return
        response = self.s.post(cnf={**self.cnf, 'command': 'add', 'data': {self.kind: payload}})
        if response.get('result') != 'saved' or not response.get('uuid'):
            self.m.fail_json('Trust creation did not return a saved UUID; inspect System / Trust before retrying.')
        existing = self._detail(response['uuid'])
        self._compare(existing, wanted)
        self.r.update(uuid=existing['uuid'], refid=existing['refid'], data=existing)

    def _creation_payload(self, wanted):
        payload = {'action': 'internal', 'descr': wanted['description']}
        for field, api_field in SUBJECT_FIELDS.items():
            if field in wanted:
                payload[api_field] = wanted[field]
        for field in ('key_type', 'digest', 'lifetime'):
            if field in wanted:
                payload[field] = wanted[field]
        payload['caref'] = wanted.get('ca_refid', '')
        if self.kind == 'cert':
            payload['private_key_location'] = 'firewall'
            payload['cert_type'] = CERTIFICATE_TYPES[wanted.get('certificate_type', 'server')]
            wanted.setdefault('certificate_type', 'server')
            for field, api_field in SAN_FIELDS.items():
                if field in wanted:
                    payload[api_field] = '\n'.join(wanted[field])
        return payload


class TrustCA(Trust):
    def __init__(self, module, result, session=None):
        super().__init__(module, result, 'ca', session)


class TrustCert(Trust):
    def __init__(self, module, result, session=None):
        super().__init__(module, result, 'cert', session)
