from urllib.parse import urlsplit

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.oxlorg.opnsense.plugins.module_utils.helper.validate import \
    is_unset
from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.module import GeneralModule


class GeoIP(GeneralModule):
    CMDS = {
        'set': 'set',
        'search': 'get',
    }
    API_KEY_PATH = 'alias.geoip'
    API_KEY_PATH_REQ = 'alias.geoip'
    API_MOD = 'firewall'
    API_CONT = 'alias'
    FIELDS_CHANGE = ['url']
    FIELDS_ALL = ['url']
    FIELDS_TYPING = {}
    # the url commonly holds the credentials of the GeoIP provider (p.e. MaxMind account-id + license-key)
    FIELDS_DIFF_NO_LOG = ['url']

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        GeneralModule.__init__(self=self, m=module, r=result, s=session)

    def check(self) -> None:
        # the error-messages must never contain the url itself as it may hold credentials
        if not is_unset(self.p['url']):
            self._validate_url(self.p['url'])

        self._base_check()

    def _validate_url(self, url: str) -> None:
        # urlsplit strips whitespace/control-characters - validate the raw value that is sent to the API
        if any(c.isspace() or not c.isprintable() for c in url):
            self.m.fail_json("The provided GeoIP 'url' must not contain whitespace or control-characters!")

        scheme = url.split(':', 1)[0].lower()
        if scheme not in ['https', 'http'] or not url.lower().startswith(f'{scheme}://'):
            self.m.fail_json("The provided GeoIP 'url' must start with 'https://' (or 'http://')!")

        try:
            parts = urlsplit(url)

        except ValueError:
            self.m.fail_json("The provided GeoIP 'url' could not be parsed!")
            return

        if parts.hostname is None or parts.hostname == '':
            self.m.fail_json("The provided GeoIP 'url' has no hostname!")

        if scheme == 'http' and (parts.username is not None or parts.query != ''):
            self.m.fail_json(
                "The provided GeoIP 'url' carries credentials (user-info or query-string) and must use 'https' - "
                "they would otherwise be transferred in cleartext!"
            )

    def _search_path_handling(self, data: dict, ak_path: str = None) -> dict:
        # the base-implementation includes the whole response in its error - which contains the current url
        try:
            return data['alias']['geoip']

        except (KeyError, TypeError):
            self.m.fail_json(
                "Got an unexpected response from 'firewall/alias/get' - no 'alias.geoip' node found "
                "(response not shown as it may contain credentials)"
            )
            return {}
