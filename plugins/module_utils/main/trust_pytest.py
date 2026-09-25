from copy import deepcopy
import importlib

import httpx
import pytest

from ansible_collections.oxlorg.opnsense.plugins.module_utils.test.mock_pytest import (
    MockAnsibleModule, AnsibleError,
)
from ansible_collections.oxlorg.opnsense.plugins.module_utils.helper.api import check_response

PREFIX = 'ansible_collections.oxlorg.opnsense.plugins'
UUID = '11111111-1111-4111-8111-111111111111'
CA_REF = '123456789abcd'
SECRET = 'PRIVATE-KEY-MUST-NOT-ESCAPE'


def record(description='test-ca', **values):
    return dict(
        descr=description, refid=CA_REF, caref='',
        commonname='Test CA', country={'DE': {'selected': 1}},
        key_type={'2048': {'selected': 1}}, digest={'sha256': {'selected': 1}},
        lifetime='825', valid_from='1700000000', valid_to=str(1700000000 + 30 * 86400),
        city='', state='', organization='', organizationalunit='', email='',
        crt_payload='PUBLIC-CERTIFICATE', prv_payload=SECRET, prv=SECRET,
        **values,
    )


class TrustAPI:
    def __init__(self, records=None, cas=None):
        self.records = deepcopy(records or {})
        self.cas = cas or [{'descr': 'issuer', 'caref': CA_REF}]
        self.calls = []

    def get(self, cnf):
        self.calls.append(('GET', deepcopy(cnf)))
        assert cnf['sensitive_response']
        if cnf['command'] == 'ca_list':
            return {'rows': self.cas}
        assert cnf['command'] == 'get'
        return {cnf['controller']: deepcopy(self.records[cnf['params'][0]])}

    def post(self, cnf, **kwargs):
        self.calls.append(('POST', deepcopy(cnf)))
        assert cnf['sensitive_response']
        if cnf['command'] == 'search':
            return {'rows': [dict(uuid=uuid, descr=data['descr']) for uuid, data in self.records.items()],
                    'total': len(self.records)}
        assert cnf['command'] == 'add', 'Trust must never call set, del or reissue'
        data = cnf['data'][cnf['controller']]
        entry = record()
        entry.update(data)
        entry['valid_to'] = str(1700000000 + int(data.get('lifetime', 825)) * 86400)
        if cnf['controller'] == 'cert':
            entry.setdefault('cert_type', 'server_cert')
            for name in ('dns', 'ip', 'email', 'uri'):
                entry.setdefault('altnames_' + name, '')
        self.records[UUID] = entry
        return {'result': 'saved', 'uuid': UUID, 'private_key': SECRET}

    def close(self):
        pass

    @property
    def mutations(self):
        return [cnf for method, cnf in self.calls if method == 'POST' and cnf['command'] != 'search']


def run(api, kind='ca', check=False, **params):
    entry = importlib.import_module(PREFIX + '.modules.trust_' + kind)
    impl = importlib.import_module(PREFIX + '.module_utils.main.trust')
    module = MockAnsibleModule()
    module.params.update({key: value.get('default') for key, value in entry.ARGUMENT_SPEC.items()
                          if key not in module.params})
    module.params.update(description='test-ca')
    module.params.update(params)
    module.check_mode = check
    result = {'changed': False}
    impl.Trust(module, result, kind, session=api).process()
    assert SECRET not in repr(result)
    return result


def test_create_and_repeat_preserve_key():
    api = TrustAPI()
    params = dict(common_name='Test CA', country='DE', lifetime=30)
    first = run(api, **params)
    assert first['changed'] and first['uuid'] == UUID and first['refid'] == CA_REF
    api.calls.clear()
    assert not run(api, **params)['changed']
    assert not api.mutations


def test_check_mode_creates_nothing():
    api = TrustAPI()
    assert run(api, check=True, common_name='Test CA', country='DE')['changed']
    assert not api.mutations


def test_lookup_returns_only_safe_metadata():
    result = run(TrustAPI({UUID: record()}))
    assert not result['changed']
    assert result['refid'] == CA_REF


@pytest.mark.parametrize('params', [
    {'common_name': 'Different'}, {'country': 'US'}, {'lifetime': 60},
    {'key_type': '4096'}, {'digest': 'sha512'}, {'organization': 'Another'},
])
def test_immutable_drift_fails_without_mutation(params):
    api = TrustAPI({UUID: record()})
    with pytest.raises(AnsibleError, match='reissu'):
        run(api, **params)
    assert not api.mutations


def test_lifetime_uses_validity_not_volatile_default():
    api = TrustAPI({UUID: record()})
    assert not run(api, lifetime=30)['changed']


def test_ambiguous_description_fails():
    api = TrustAPI({UUID: record(), 'second': record()})
    with pytest.raises(AnsibleError, match='[Aa]mbiguous'):
        run(api)
    assert not api.mutations


def test_unknown_uuid_does_not_create():
    api = TrustAPI()
    with pytest.raises(AnsibleError, match='UUID'):
        run(api, uuid=UUID, common_name='Test CA', country='DE')
    assert not api.mutations


def test_certificate_resolves_ca_and_newline_sans():
    api = TrustAPI()
    params = dict(kind='cert', common_name='vpn.example.test', country='DE',
                  ca='issuer', certificate_type='server', san_dns=['vpn.example.test', 'fw.example.test'])
    assert run(api, **params)['changed']
    payload = api.mutations[0]['data']['cert']
    assert payload['caref'] == CA_REF
    assert payload['private_key_location'] == 'firewall'
    assert payload['altnames_dns'] == 'fw.example.test\nvpn.example.test'
    api.calls.clear()
    assert not run(api, **params)['changed']
    assert not api.mutations


def test_unknown_ca_fails_before_mutation():
    api = TrustAPI()
    with pytest.raises(AnsibleError, match='CA'):
        run(api, kind='cert', common_name='vpn.example.test', country='DE', ca='missing')
    assert not api.mutations


def test_duplicate_ca_description_fails():
    api = TrustAPI(cas=[{'descr': 'issuer', 'caref': CA_REF}, {'descr': 'issuer', 'caref': 'bbbbbbbbbbbbb'}])
    with pytest.raises(AnsibleError, match='[Aa]mbiguous'):
        run(api, kind='cert', common_name='vpn.example.test', country='DE', ca='issuer')
    assert not api.mutations


@pytest.mark.parametrize('status,payload', [
    (400, {'private_key': SECRET, 'result': 'failed'}),
    (200, {'validations': {'prv': SECRET}, 'result': 'failed'}),
    (404, {'message': 'Controller not found', 'prv': SECRET}),
])
def test_sensitive_api_errors_never_expose_body(status, payload, capsys):
    module = MockAnsibleModule()
    module.params['debug'] = True
    response = httpx.Response(status, json=payload)
    with pytest.raises(AnsibleError) as error:
        check_response(module, {'sensitive_response': True, 'module': 'trust',
                                'controller': 'ca', 'command': 'get'}, response)
    assert SECRET not in str(error.value)
    assert SECRET not in capsys.readouterr().out


def test_sensitive_success_is_not_debug_logged(capsys):
    module = MockAnsibleModule()
    module.params['debug'] = True
    response = httpx.Response(200, json={'ca': {'prv_payload': SECRET}})
    assert check_response(module, {'sensitive_response': True}, response)['ca']['prv_payload'] == SECRET
    assert SECRET not in capsys.readouterr().out


def test_ipv6_san_compares_addresses_not_openssl_format():
    entry = record()
    entry.update(caref=CA_REF, cert_type='server_cert',
                 altnames_ip='2001:DB8:0:0:0:0:0:1',
                 altnames_dns='', altnames_email='', altnames_uri='')
    api = TrustAPI({UUID: entry})
    assert not run(api, kind='cert', san_ip=['2001:db8::1'])['changed']
    assert not api.mutations


def test_list_includes_pending_csrs_without_exposing_payloads():
    impl = importlib.import_module(PREFIX + '.module_utils.main.trust')
    pending = record('pending')
    pending.update(crt_payload='', csr_payload='PUBLIC-CSR')
    api = TrustAPI({UUID: record(), 'pending-uuid': pending})
    result = impl.Trust(MockAnsibleModule(), {}, 'cert', session=api).get_existing()
    assert len(result) == 2
    assert result[1]['description'] == 'pending'
    assert result[1]['certificate_available'] is False
    assert result[1]['csr_available'] is True
    assert SECRET not in repr(result)


def test_list_includes_external_certificate_without_reference():
    impl = importlib.import_module(PREFIX + '.module_utils.main.trust')
    external = record('external')
    external['refid'] = ''
    result = impl.Trust(MockAnsibleModule(), {}, 'cert',
                        session=TrustAPI({'external': external})).get_existing()
    assert result[0]['description'] == 'external'
    assert result[0]['certificate_available'] is True
    assert not result[0]['refid']
