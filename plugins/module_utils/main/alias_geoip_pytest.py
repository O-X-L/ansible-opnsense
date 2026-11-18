from copy import deepcopy

import pytest

from ansible_collections.oxlorg.opnsense.plugins.module_utils.test.mock_pytest import \
    pytest_mock_http_responses, MockAnsibleModule, AnsibleError
from ansible_collections.oxlorg.opnsense.plugins.module_utils.test.testdata.alias_geoip_testdata import \
    Testdata_26_1_11 as GeoIPTestdata, SECRET, SECRET_OLD, URL, URL_OLD

PARAMS = dict(url=URL, reload=True)


def _mock(mocker, url: str = '') -> GeoIPTestdata:
    testdata = GeoIPTestdata(url=url)
    pytest_mock_http_responses(mocker=mocker, handler=testdata)
    return testdata


def _run(params: dict, check_mode: bool = False) -> dict:
    # pylint: disable=C0415
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.wrapper import module_wrapper
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.main.alias_geoip import GeoIP

    module = MockAnsibleModule()
    module.params.update(params)
    module.check_mode = check_mode
    result = {'changed': False, 'diff': {'before': {}, 'after': {}}}
    module_wrapper(GeoIP(module=module, result=result))
    assert SECRET not in str(result)
    assert SECRET_OLD not in str(result)
    return result


def test_alias_geoip_set_and_rerun(mocker):
    testdata = _mock(mocker)
    aliases = deepcopy(testdata.state['aliases'])

    result = _run(PARAMS)
    assert result['changed']
    assert testdata.mutations() == [
        # only the geoip-node is posted - the aliases must not be re-sent
        ('set', {'alias': {'geoip': {'url': URL}}}),
        ('reconfigure', None),
    ]
    assert testdata.state['geoip']['url'] == URL
    assert testdata.state['aliases'] == aliases

    result = _run(PARAMS)
    assert not result['changed']
    assert len(testdata.mutations()) == 2


def test_alias_geoip_check_mode(mocker):
    testdata = _mock(mocker)
    result = _run(PARAMS, check_mode=True)
    assert result['changed']
    assert len(testdata.mutations()) == 0
    assert testdata.state['geoip']['url'] == ''


def test_alias_geoip_rotate(mocker):
    testdata = _mock(mocker, url=URL_OLD)
    result = _run(PARAMS)
    assert result['changed']
    assert testdata.state['geoip']['url'] == URL
    # the diff hides both the old and the new value
    assert result['diff']['before']['url'] == result['diff']['after']['url']


def test_alias_geoip_clear(mocker):
    testdata = _mock(mocker, url=URL_OLD)
    result = _run({**PARAMS, 'url': ''})
    assert result['changed']
    assert testdata.mutations()[0] == ('set', {'alias': {'geoip': {'url': ''}}})
    assert testdata.state['geoip']['url'] == ''

    result = _run({**PARAMS, 'url': ''})
    assert not result['changed']


def test_alias_geoip_no_reload(mocker):
    testdata = _mock(mocker)
    result = _run({**PARAMS, 'reload': False})
    assert result['changed']
    assert [call[0] for call in testdata.mutations()] == ['set']


def test_alias_geoip_http_without_credentials(mocker):
    testdata = _mock(mocker)
    url = 'http://mirror.example.internal/geoip/GeoLite2-Country-CSV.zip'
    result = _run({**PARAMS, 'url': url})
    assert result['changed']
    assert testdata.state['geoip']['url'] == url


@pytest.mark.parametrize('url', [
    # credentials in cleartext
    URL.replace('https://', 'http://'),
    URL.replace('https://', 'HTTP://'),
    f'http://download.maxmind.com/app/geoip_download?license_key={SECRET}',
    URL.replace('https://', 'ftp://'),
    f'123456:{SECRET}@download.maxmind.com/geoip',
    f'https://123456:{SECRET}@/geoip',
    # urlsplit would strip these - the raw value must be validated
    f' {URL}',
    f'{URL}\n',
    URL.replace('https://', 'ht\ttps://'),
    f'\x01{URL}',
])
def test_alias_geoip_invalid_url(mocker, url: str):
    testdata = _mock(mocker, url=URL_OLD)

    with pytest.raises(AnsibleError) as error:
        _run({**PARAMS, 'url': url})

    assert SECRET not in str(error.value)
    # validation happens before any api-call
    assert len(testdata.calls) == 0
    assert testdata.state['geoip']['url'] == URL_OLD


def test_alias_geoip_unexpected_response(mocker):
    # p.e. another OPNsense version or a proxy changing the response-shape
    testdata = _mock(mocker, url=URL_OLD)
    testdata._get = lambda: {'geoip': {'url': URL_OLD}}

    with pytest.raises(AnsibleError) as error:
        _run(PARAMS)

    assert SECRET_OLD not in str(error.value)
    assert len(testdata.mutations()) == 0
