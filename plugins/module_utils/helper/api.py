import ssl
from pathlib import Path
from json import JSONDecodeError
from json import dumps as json_dumps
from datetime import datetime

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.oxlorg.opnsense.plugins.module_utils.defaults.main import \
    DEBUG_CONFIG
from ansible_collections.oxlorg.opnsense.plugins.module_utils.helper.main import \
    ensure_list
from ansible_collections.oxlorg.opnsense.plugins.module_utils.helper.validate import \
    is_valid_domain, is_ip


def _load_credential_file(module: AnsibleModule) -> tuple[(str, None), (str, None)]:
    """Parses credential files, checking for security and format compliance."""
    cred_file_info = Path(module.params['api_credential_file'])

    if cred_file_info.is_file():
        cred_file_mode = oct(cred_file_info.stat().st_mode)[-3:]

        if int(cred_file_mode[2]) != 0:
            module.warn(
                f"Provided 'api_credential_file' at path "
                f"'{module.params['api_credential_file']}' is world-readable "
                f"(mode {cred_file_mode})!"
            )

        with open(module.params['api_credential_file'], 'r', encoding='utf-8') as file:
            config = {}
            vaulted = False

            for line in file.readlines():
                try:
                    key, value = line.split('=', 1)
                    config[key] = value.strip()

                except ValueError:
                    if line.startswith('$ANSIBLE_VAULT'):
                        vaulted = True
                        break

            if vaulted:
                module.fail_json(
                    f"Credential file '{module.params['api_credential_file']}' "
                    'is ansible-vault encrypted! This is not yet supported.'
                )

            if 'key' not in config or 'secret' not in config:
                module.fail_json(
                    f"Credential file '{module.params['api_credential_file']}' "
                    'could not be parsed!'
                )

            return config['key'], config['secret']

    else:
        module.fail_json(
            f"Provided 'api_credential_file' at path "
            f"'{module.params['api_credential_file']}' does not exist!"
        )

    return None, None


def check_or_load_credentials(module: AnsibleModule) -> tuple[(str, None), (str, None)]:
    if module.params['api_credential_file'] is not None:
        return _load_credential_file(module)

    if module.params['api_key'] is None and module.params['api_secret'] is None:
        module.fail_json("Neither 'api_key' & 'api_secret' nor 'api_credential_file' were provided!")

    return None, None


def check_host(module: AnsibleModule) -> None:
    if not is_ip(module.params['firewall']):
        fw_dns = module.params['firewall']

        if fw_dns.find('.') == -1:
            # TLD-only will fail the domain validation
            fw_dns = f'dummy.{fw_dns}'

        if not is_valid_domain(fw_dns):
            module.fail_json(f"Host '{module.params['firewall']}' is neither a valid IP nor Domain-Name!")


def ssl_verification_lib_httpx(module: AnsibleModule) -> (ssl.SSLContext, bool):
    context = ssl.create_default_context()

    if not module.params['ssl_verify']:
        return False

    if module.params['ssl_ca_file'] is not None:
        if not Path(module.params['ssl_ca_file']).is_file():
            module.fail_json(f"The provided 'ssl_ca_file' at path '{module.params['ssl_ca_file']}' does not exist!")

        context.load_verify_locations(cafile=module.params['ssl_ca_file'])

    return context


def ssl_verification_lib_requests(module: AnsibleModule) -> (bool, str):
    if not module.params['ssl_verify']:
        return False

    if module.params['ssl_ca_file'] is not None:
        if not Path(module.params['ssl_ca_file']).is_file():
            module.fail_json(f"The provided 'ssl_ca_file' at path '{module.params['ssl_ca_file']}' does not exist!")

        return module.params['ssl_ca_file']

    return True


def get_params_path(cnf: dict) -> str:
    params_path = ''

    if 'params' in cnf and cnf['params'] is not None:
        for param in ensure_list(cnf['params']):
            params_path += f"/{param}"

    return params_path


def _sanitize_response_for_logging_lib_httpx(response_raw: dict) -> dict:
    sanitized = response_raw.copy()
    sanitized['http_client'] = 'httpx'

    for field in [
        'headers', 'next_request', '_decoder', 'stream', 'extensions', 'history', 'is_closed',
        'is_stream_consumed', 'default_encoding',
    ]:
        if field in sanitized:
            sanitized.pop(field)

    if '_request' in sanitized:
        raw_request = sanitized.pop('_request')
        sanitized['url'] = str(raw_request.url)  # httpx.URL
        sanitized['method'] = raw_request.method

    if '_num_bytes_downloaded' in sanitized:
        sanitized['bytes_downloaded'] = sanitized.pop('_num_bytes_downloaded')

    if '_elapsed' in sanitized:
        sanitized['elapsed_ms'] = sanitized.pop('_elapsed').microseconds

    if '_content' in sanitized:
        sanitized['body'] = sanitized.pop('_content')

    return sanitized


def _sanitize_response_for_logging_lib_requests(response_raw: dict) -> dict:
    sanitized = response_raw.copy()
    sanitized['http_client'] = 'requests'

    for field in [
        '_content_consumed', '_next', 'headers', 'raw', 'encoding', 'history', 'cookies', 'connection',
    ]:
        if field in sanitized:
            sanitized.pop(field)

    if 'request' in sanitized:
        raw_request = sanitized.pop('request')
        sanitized['method'] = raw_request.method

    if '_content' in sanitized:
        sanitized['body'] = sanitized.pop('_content')

    if 'elapsed' in sanitized:
        sanitized['elapsed_ms'] = sanitized.pop('elapsed').microseconds

    return sanitized


def _sanitize_response_for_logging(http_client_lib: str, response_raw: dict) -> dict:
    # the full response contains the full request including plaintext secrets

    if http_client_lib == 'httpx':
        return _sanitize_response_for_logging_lib_httpx(response_raw)

    return _sanitize_response_for_logging_lib_requests(response_raw)


def debug_api(
        module: AnsibleModule, http_client_lib: str, method: str = None, url: str = None,
        data: dict = None, headers: dict = None, response: dict = None,
) -> None:
    if 'debug' not in module.params or not module.params['debug']:
        return

    if response is not None:
        # NOTE: we do not sanitize the response here because the user chose to enable debug-output
        msg = f"CLI-LIB: {http_client_lib} | RESPONSE: '{response.__dict__}'"

    else:
        msg = f"CLI-LIB: {http_client_lib} | REQUEST: {method} | URL: {url}"

        if headers is not None:
            msg += f" | HEADERS: '{headers}'"

        if data is not None:
            msg += f" | DATA: '{json_dumps(data)}'"

        log_path = Path(DEBUG_CONFIG['path_log'])
        if not log_path.exists():
            log_path.mkdir()

        with open(
                f"{log_path}/{DEBUG_CONFIG['log_api_calls']}",
                'a+', encoding='utf-8'
        ) as log:
            log.write(f"\n{datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')} | {method} => {url}\n")

    module.warn(msg)


def check_response(module: AnsibleModule, cnf: dict, http_client_lib: str, response) -> dict:
    debug_api(module=module, http_client_lib=http_client_lib, response=response)

    if 'allowed_http_stati' not in cnf:
        cnf['allowed_http_stati'] = [200]

    try:
        json = response.json()

    except JSONDecodeError:
        json = {}

    sanitized_response = _sanitize_response_for_logging(
        http_client_lib=http_client_lib,
        response_raw=response.__dict__,
    )
    debug_info = " (set 'debug: true' for more info)"
    if 'debug' in module.params and module.params['debug']:
        debug_info = ''

    if 'validations' in json and json['validations'] is not None and len(json['validations']) > 0:
        # OPNsense sometimes reports a positive response-status even if the action failed :'(
        module.fail_json(
            f"API call failed | Error: {json['validations']} | "
            f"Info: {sanitized_response}{debug_info}"
        )

    if response.status_code not in cnf['allowed_http_stati'] or \
            ('result' in json and json['result'] == 'failed'):
        # sometimes an error 'hides' behind a 200-code
        if f"{sanitized_response}".find('Controller not found') != -1:
            module.fail_json(
                f"API call failed | Needed plugin not installed! | "
                f"Info: {sanitized_response}{debug_info}"
            )

        else:
            module.fail_json(f"API call failed | Info: {sanitized_response}{debug_info}")

    return json


def api_pretty_exception(m: AnsibleModule, method: str, url: str, error):
    call = f'{method} => {url}'
    msg = f"Unable to connect '{call}'"

    if str(error).find('timed out') != -1:
        msg = f"Got timeout calling '{call}'"

    if str(error).find('CERTIFICATE_VERIFY_FAILED') != -1 or str(error).find('certificate verify failed') != -1:
        msg = f"SSL verification failed '{url}'! Make sure to follow the the documentation: "\
              "https://ansible-opnsense.oxl.app/usage/2_basic.html#ssl-certificate"

    m.fail_json(f"{msg} ({error})")
