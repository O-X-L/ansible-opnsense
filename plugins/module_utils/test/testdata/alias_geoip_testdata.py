from copy import deepcopy

from ansible_collections.oxlorg.opnsense.plugins.module_utils.test.testdata.base_testdata import MockOPNsenseController

# used to verify that the provider-credentials inside the url never reach the module-result
SECRET = 'GEOIP-LICENSE-KEY-MUST-NOT-ESCAPE'
SECRET_OLD = 'OLD-GEOIP-LICENSE-KEY-MUST-NOT-ESCAPE'
URL = f'https://123456:{SECRET}@download.maxmind.com/geoip/databases/GeoLite2-Country-CSV/download?suffix=zip'
URL_OLD = f'https://123456:{SECRET_OLD}@download.maxmind.com/geoip/databases/GeoLite2-Country-CSV/download?suffix=zip'


class Testdata_26_1_11(MockOPNsenseController):
    """
    Emulates the OPNsense alias-API behavior for the GeoIP settings (see: OPNsense/Firewall/Api/AliasController.php)
    * 'get' returns the whole alias-model - the GeoIP source next to all aliases
    * 'set' merges the posted (partial) model - posting only the GeoIP node leaves the aliases untouched
    """

    def __init__(self, url: str = ''):
        super().__init__()
        self.state = {
            'geoip': {'url': url},
            'aliases': {'alias': {
                'a1b2c3d4-0000-0000-0000-000000000001': {
                    'enabled': '1', 'name': 'ANSIBLE_TEST_GEOIP', 'type': {'geoip': {'value': 'GeoIP', 'selected': 1}},
                    'content': {'CA': {'value': 'Canada', 'selected': 1}}, 'description': '',
                },
            }},
        }
        self.calls = []

    def commands(self) -> dict:
        return {
            'get': self._get,
            'set': self._set,
            'reconfigure': self._reconfigure,
        }

    def route_kwargs(self, method) -> list:
        return {
            self._get: [],
            self._set: ['data'],
            self._reconfigure: [],
        }[method]

    def _get(self) -> dict:
        self.calls.append(('get', None))
        return {'alias': deepcopy(self.state)}

    def _set(self, data: dict) -> dict:
        self.calls.append(('set', deepcopy(data)))
        for k, v in data['alias'].items():
            self.state[k] = {**self.state[k], **v}

        return {'result': 'saved'}

    def _reconfigure(self) -> dict:
        self.calls.append(('reconfigure', None))
        return {'status': 'ok'}

    def mutations(self) -> list:
        return [call for call in self.calls if call[0] in ['set', 'reconfigure']]
