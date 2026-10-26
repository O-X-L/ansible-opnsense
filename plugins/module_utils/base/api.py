from os import environ
from socket import setdefaulttimeout

try:
    import httpx
    HAS_LIB_HTTPX = True

except ImportError:
    HAS_LIB_HTTPX = False

try:
    import requests
    from requests.exceptions import RequestException as LibRequestsException, \
        Timeout as LibRequestsTimeout, ConnectionError as LibRequestsConnectionError
    HAS_LIB_REQUESTS = True

except ImportError:
    HAS_LIB_REQUESTS = False

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.oxlorg.opnsense.plugins.module_utils.helper.api import \
    check_host, check_response, get_params_path, debug_api, check_or_load_credentials, api_pretty_exception, \
    ssl_verification_lib_httpx, ssl_verification_lib_requests
from ansible_collections.oxlorg.opnsense.plugins.module_utils.helper.validate import is_ip6

DEFAULT_TIMEOUT = 20.0

REQUEST_EXCEPTIONS = tuple()
REQUEST_EXCEPTIONS += (ConnectionError,)
if HAS_LIB_HTTPX:
    REQUEST_EXCEPTIONS += (
        httpx.ConnectTimeout, httpx.ConnectError, httpx.ReadTimeout,
        httpx.WriteTimeout, httpx.TimeoutException, httpx.PoolTimeout,
        httpx.RemoteProtocolError,
    )

if HAS_LIB_REQUESTS:
    REQUEST_EXCEPTIONS += (LibRequestsException, LibRequestsTimeout, LibRequestsConnectionError)


class Session:
    HTTP_CLIENT_BACKEND_HTTPX = 'httpx'
    HTTP_CLIENT_BACKEND_REQUESTS = 'requests'

    def __init__(self, module: AnsibleModule, timeout: float = DEFAULT_TIMEOUT):
        self.m = module
        if not HAS_LIB_HTTPX and not HAS_LIB_REQUESTS:
            self.m.fail_json(msg="Either 'httpx' or 'requests' must be installed on the target host.")

        self._init_http_client()
        self.s = self._start(timeout)

    def _init_http_client(self):
        http_client_prio = environ.get('HTTP_CLIENT', 'httpx')
        if http_client_prio not in ['httpx', 'requests']:
            http_client_prio = 'httpx'

        self._http_client_lib = self.HTTP_CLIENT_BACKEND_HTTPX
        if http_client_prio == self.HTTP_CLIENT_BACKEND_HTTPX:
            if HAS_LIB_HTTPX:
                self._http_client_lib = self.HTTP_CLIENT_BACKEND_HTTPX

            else:
                self._http_client_lib = self.HTTP_CLIENT_BACKEND_REQUESTS

        elif http_client_prio == self.HTTP_CLIENT_BACKEND_REQUESTS:
            if HAS_LIB_REQUESTS:
                self._http_client_lib = self.HTTP_CLIENT_BACKEND_REQUESTS

            else:
                self._http_client_lib = self.HTTP_CLIENT_BACKEND_HTTPX

    def _start(self, timeout: float) -> (httpx.Client, requests.Session):
        check_host(module=self.m)
        api_key, api_secret = check_or_load_credentials(module=self.m)
        if api_secret is None:
            api_key = self.m.params['api_key']
            api_secret = self.m.params['api_secret']

        if 'api_timeout' in self.m.params and self.m.params['api_timeout'] is not None:
            timeout = self.m.params['api_timeout']

        setdefaulttimeout(timeout)

        fw = self.m.params['firewall']
        if is_ip6(fw, strip_enclosure=False):
            fw = f"[{fw}]"

        base_url = f"https://{fw}:{self.m.params['api_port']}/api"

        proxy = environ.get('HTTPS_PROXY', None)
        if proxy is not None and not proxy.startswith('http') and not proxy.startswith('sock'):
            proxy = None

        if self._http_client_lib == self.HTTP_CLIENT_BACKEND_HTTPX:
            return self._start_session_lib_httpx(
                base_url=base_url,
                api_key=api_key,
                api_secret=api_secret,
                timeout=timeout,
                proxy=proxy,
            )

        return self._start_session_lib_requests(
            base_url=base_url,
            api_key=api_key,
            api_secret=api_secret,
            timeout=timeout,
            proxy=proxy,
        )

    def _start_session_lib_httpx(
            self, base_url: str, api_key: str, api_secret: str, timeout: float, proxy: (None, str),
    ) -> httpx.Client:
        return httpx.Client(
            base_url=base_url,
            auth=(api_key, api_secret),
            timeout=httpx.Timeout(timeout=timeout, connect=2.0),
            transport=httpx.HTTPTransport(
                verify=ssl_verification_lib_httpx(module=self.m),
                retries=self.m.params['api_retries'],
                proxy=proxy,
            ),
            headers={'User-Agent': 'Ansible'}
        )

    def _start_session_lib_requests(
            self, base_url: str, api_key: str, api_secret: str, timeout: float, proxy: (None, str),
    ) -> requests.Session:
        session = requests.Session()
        session.auth = (api_key, api_secret)
        session.headers.update({'User-Agent': 'Ansible'})
        session.base_url = base_url
        session.default_timeout = timeout
        session.verify = ssl_verification_lib_requests(self.m)
        if proxy is not None:
            session.proxies.update({'https': proxy})

        return session

    def get(self, cnf: dict) -> dict:
        params_path = get_params_path(cnf=cnf)
        call_url = f"{cnf['module']}/{cnf['controller']}/{cnf['command']}{params_path}"

        debug_api(
            module=self.m,
            method='GET',
            url=f'{self.s.base_url}{call_url}',
            http_client_lib=self._http_client_lib,
        )

        try:
            if self._http_client_lib == self.HTTP_CLIENT_BACKEND_HTTPX:
                raw_response = self.s.get(url=call_url)

            else:
                # HTTP_CLIENT_BACKEND_REQUESTS
                raw_response = self.s.get(
                    url=f"{self.s.base_url}/{call_url}",
                    timeout=self.s.default_timeout,
                )

            response = check_response(
                module=self.m,
                cnf=cnf,
                http_client_lib=self._http_client_lib,
                response=raw_response
            )

        except REQUEST_EXCEPTIONS as error:
            api_pretty_exception(
                m=self.m, method='GET', error=error,
                url=f'{self.s.base_url}{call_url}',
            )
            raise

        return response

    def post(self, cnf: dict, headers: dict = None) -> dict:
        if headers is None:
            headers = {}

        data = None

        if 'data' in cnf and cnf['data'] is not None and len(cnf['data']) > 0:
            headers['Content-Type'] = 'application/json'
            data = cnf['data']

        params_path = get_params_path(cnf=cnf)
        call_url = f"{cnf['module']}/{cnf['controller']}/{cnf['command']}{params_path}"

        debug_api(
            module=self.m,
            method='POST',
            url=f'{self.s.base_url}{call_url}',
            data=data,
            headers=headers,
            http_client_lib=self._http_client_lib,
        )

        try:
            if self._http_client_lib == self.HTTP_CLIENT_BACKEND_HTTPX:
                raw_response = self.s.post(
                    url=call_url, json=data, headers=headers
                )

            else:
                # HTTP_CLIENT_BACKEND_REQUESTS
                raw_response = self.s.post(
                    url=f"{self.s.base_url}/{call_url}",
                    json=data,
                    headers=headers,
                    timeout=self.s.default_timeout,
                )

            response = check_response(
                module=self.m,
                cnf=cnf,
                http_client_lib=self._http_client_lib,
                response=raw_response
            )

        except REQUEST_EXCEPTIONS as error:
            api_pretty_exception(
                m=self.m, method='POST', error=error,
                url=f'{self.s.base_url}{call_url}',
            )
            raise

        return response

    def close(self) -> None:
        self.s.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


def single_get(module: AnsibleModule, cnf: dict, timeout: float = DEFAULT_TIMEOUT) -> dict:
    with Session(module=module, timeout=timeout) as s:
        response = s.get(cnf=cnf)

    return response


def single_post(module: AnsibleModule, cnf: dict, timeout: float = DEFAULT_TIMEOUT, headers: dict = None) -> dict:
    with Session(module=module, timeout=timeout) as s:
        response = s.post(cnf=cnf, headers=headers)

    return response
