from ansible_collections.ansibleguy.opnsense.plugins.module_utils.test.mock_http_pytest import \
    pytest_mock_http_responses
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.test.mock_mod_pytest import \
    MockOPNsenseModule, MOCK_MOD_ARGS

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
        self.check_mode = False
        self.diff_mode = False

    def fail_json(self, msg: str):
        raise AnsibleError(msg)

    def warn(self, msg: str):
        print(msg)


class AnsibleWarning(Exception):
    pass


class MockAnsibleModuleWarnException(MockAnsibleModule):
    def warn(self, msg: str):
        raise AnsibleWarning(msg)


DUMMY_MODULE = MockAnsibleModule()
DUMMY_REQ = dict(
    module='dummy',
    controller='dummy',
    command='test',
)
def get_ansible_module_multi_params() -> dict:
    return {
        **MockAnsibleModule.PARAMS,
        'multi': {},
        'multi_purge': {},
        'multi_control': {
            'state': None,
            'enabled': None,
            'override': {},
            'fail_verify': False,
            'fail_process': True,
            'output_info': False,
            'purge_action': 'delete',
            'purge_filter': {},
            'purge_filter_invert': False,
            'purge_filter_partial': False,
            'purge_unconfigured': False,
            'purge_all': False,
        },
    }