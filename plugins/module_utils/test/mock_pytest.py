from ansible_collections.ansibleguy.opnsense.plugins.module_utils.test.mock_http_pytest import \
    pytest_mock_http_responses
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.test.mock_mod_pytest import \
    MockOPNsenseModule, MOCK_RESPONSES

ANSIBLE_RESULT = {'changed': False, 'diff': {'before': {}, 'after': {}}}


class AnsibleError(Exception):
    pass


class MockAnsibleModule:
    PARAMS = dict(
        firewall='127.0.0.1',
        api_port=51337,
        api_key='dummy',
        api_secret='secret',
        api_credential_file=None,
        ssl_verify=False,
        ssl_ca_file=None,
        debug=False,
        profiling=False,
        api_timeout=None,
        api_retries=0,

        multi={},
        multi_purge={},
        multi_control={},
    )

    def __init__(self):
        self.params = self.PARAMS.copy()

    def fail_json(self, msg: str):
        raise AnsibleError(msg)

    def warn(self, msg: str):
        print(msg)

DUMMY_MODULE = MockAnsibleModule()
DUMMY_REQ = dict(
    module='dummy',
    controller='dummy',
    command='test',
)
