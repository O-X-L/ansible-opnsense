from ipaddress import ip_address

from ansible.module_utils.basic import AnsibleModule

# see: https://github.com/opnsense/core/blob/master/src/opnsense/mvc/app/models/OPNsense/Trust/Ca.xml
#      https://github.com/opnsense/core/blob/master/src/opnsense/mvc/app/models/OPNsense/Trust/Cert.xml

# the API returns the private keys in every search- and detail-response
TRUST_SECRET_FIELDS = ['prv', 'prv_payload']
# base64-encoded duplicates of the public 'crt_payload'/'csr_payload'
TRUST_DUPLICATE_FIELDS = ['crt', 'csr']

TRUST_SUBJECT_FIELDS = [
    'common_name', 'country', 'state_or_province', 'city', 'organization', 'organizational_unit', 'email',
]
TRUST_FIELDS_TRANSLATE = {
    'description': 'descr',
    'ca': 'caref',
    'common_name': 'commonname',
    'state_or_province': 'state',
    'organizational_unit': 'organizationalunit',
}
TRUST_KEY_TYPES = [
    '512', '1024', '2048', '3072', '4096', '7680', '8192', 'prime256v1', 'secp384r1', 'secp521r1',
]
TRUST_DIGESTS = ['sha1', 'sha224', 'sha256', 'sha384', 'sha512']
TRUST_SAN_FIELDS = ['san_dns', 'san_ip', 'san_email', 'san_uri']
TRUST_SAN_TRANSLATE = {
    'san_dns': 'altnames_dns',
    'san_ip': 'altnames_ip',
    'san_email': 'altnames_email',
    'san_uri': 'altnames_uri',
}

SECONDS_PER_DAY = 86400


def strip_keys_and_duplicates(entry: dict) -> dict:
    return {k: v for k, v in entry.items() if k not in TRUST_SECRET_FIELDS and k not in TRUST_DUPLICATE_FIELDS}


def lifetime_days(entry: dict) -> int:
    # 'lifetime' is a volatile field - the API always returns its default value
    #   the actual validity has to be calculated using the timestamps parsed from the certificate
    try:
        return (int(entry['valid_to']) - int(entry['valid_from'])) // SECONDS_PER_DAY

    except (KeyError, TypeError, ValueError):
        return 0


def normalize_ips(values: list) -> list:
    # openssl returns IPv6 SANs in their expanded uppercase form
    return [str(ip_address(v)) for v in values]


def split_san(value: (str, list)) -> list:
    if isinstance(value, list):
        # if function is re-applied
        return value

    return [v.strip() for v in str(value).split('\n') if v.strip() != '']


def validate_san(module: AnsibleModule, field: str, values: list) -> list:
    for v in values:
        # the API joins and splits the SAN-values using these characters
        if v.strip() == '' or any(c in v for c in [',', '\n', '\r']):
            module.fail_json(f"Invalid {field} value '{v}' - must not be empty or contain commas/newlines!")

    if field == 'san_ip':
        try:
            values = normalize_ips(values)

        except ValueError:
            module.fail_json(f"The field '{field}' contains an invalid IP address: {values}")

    return sorted(set(values))


def check_immutable(module: AnsibleModule, existing: dict, params: dict, fields: list, kind: str) -> None:
    changed = []
    for field in fields:
        if field not in params:
            continue

        wanted = params[field]
        current = existing.get(field, '')
        if isinstance(wanted, list):
            if sorted(wanted) != sorted(current if isinstance(current, list) else split_san(current)):
                changed.append(field)

        elif str('' if wanted is None else wanted) != str(current):
            changed.append(field)

    if len(changed) > 0:
        module.fail_json(
            f"The existing {kind} differs in fields that cannot be changed without re-issuing it: "
            f"{', '.join(changed)}! Create a new {kind} with a different description instead "
            f"and migrate its references."
        )
