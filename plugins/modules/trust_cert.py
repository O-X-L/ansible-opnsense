#!/usr/bin/python
# -*- coding: utf-8 -*-
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.oxlorg.opnsense.plugins.module_utils.defaults.main import OPN_MOD_ARGS
from ansible_collections.oxlorg.opnsense.plugins.module_utils.main.trust import (
    Trust, TRUST_ARGUMENTS, CERT_ARGUMENTS,
)


DOCUMENTATION = r'''
module: trust_cert
short_description: Create or verify an OPNsense CA-signed certificate
description:
- Uses the OPNsense API. Supports check mode and preserves unrelated resources.
- API behavior verified against OPNsense 26.7.3 source; live integration validation is pending.
author:
- OXL contributors
options:
  description:
    type: str
    description:
    - Description. Trust modules match this exactly and reject duplicate descriptions.
  uuid:
    type: str
    description:
    - Select an existing entry by UUID. An unknown UUID fails without creating a replacement.
  state:
    type: str
    choices:
    - present
    default: present
    description:
    - Desired state. Trust modules support present only and never delete or reissue.
  key_type:
    type: str
    choices:
    - '2048'
    - '3072'
    - '4096'
    - '7680'
    - '8192'
    - prime256v1
    - secp384r1
    - secp521r1
    description:
    - Key size or elliptic curve for creation. Existing keys are verified and never replaced.
  digest:
    type: str
    choices:
    - sha256
    - sha384
    - sha512
    description:
    - Signature digest for creation. Existing certificates are verified.
  lifetime:
    type: int
    description:
    - Certificate validity duration in days. Compared with validity timestamps on reruns, not remaining
      life.
  common_name:
    type: str
    description:
    - Certificate subject common name. Required when creating an entry.
  country:
    type: str
    description:
    - Two-letter subject country code. Required when creating an entry.
  state_or_province:
    type: str
    description:
    - Certificate subject state or province.
  city:
    type: str
    description:
    - Certificate subject locality.
  organization:
    type: str
    description:
    - Certificate subject organization.
  organizational_unit:
    type: str
    description:
    - Certificate subject organizational unit.
  email:
    type: str
    description:
    - Certificate subject email address.
  ca:
    type: str
    description:
    - Exact description of an existing issuing CA. Mutually exclusive with ca_refid.
  ca_refid:
    type: str
    description:
    - Existing issuing CA reference ID (not its UUID). Mutually exclusive with ca.
  certificate_type:
    type: str
    choices:
    - server
    - client
    - server_client
    description:
    - Certificate purpose. New certificates default to server; omitted values preserve existing purpose.
  san_dns:
    type: list
    elements: str
    description:
    - List of DNS subject alternative names. Omitted values are not compared.
  san_ip:
    type: list
    elements: str
    description:
    - List of IP subject alternative names. Omitted values are not compared.
  san_email:
    type: list
    elements: str
    description:
    - List of EMAIL subject alternative names. Omitted values are not compared.
  san_uri:
    type: list
    elements: str
    description:
    - List of URI subject alternative names. Omitted values are not compared.
  firewall:
    type: str
    required: true
    description:
    - IP-Address or DNS hostname of the target firewall. Must be included as 'common name' or 'subject
      alternative name' in the firewalls web-certificate to use 'ssl_verify=true'
  api_port:
    type: int
    required: false
    default: 443
    description:
    - Port the target firewall uses for its web-interface
  api_key:
    type: str
    required: false
    description:
    - API key used to authenticate, alternative to 'api_credential_file'
  api_secret:
    type: str
    required: false
    description:
    - API secret used to authenticate, alternative to 'api_credential_file'. Is set as 'no_log' parameter
  api_credential_file:
    type: path
    required: false
    description:
    - Path to the api-credential file as downloaded through the web-interface. Alternative to 'api_key'
      and 'api_secret'
  ssl_verify:
    type: bool
    required: false
    default: true
    description:
    - If the certificate of the target firewall should be validated. RECOMMENDED FOR PRODUCTION USAGE!
  ssl_ca_file:
    type: path
    required: false
    description:
    - If you use an internal certificate-authority to create the certificate of the target firewall, provide
      the path to its public key for validation
  debug:
    type: bool
    required: false
    default: false
    description:
    - Used to en-/disable the debug mode. All API requests and responses will be shown as Ansible warnings
      at runtime. Will be hidden if the tasks 'no_log' parameter is set to 'true'
  profiling:
    type: bool
    required: false
    default: false
    description:
    - Used to en-/disable the profiling mode. Time consumption of the module will be logged to '/tmp/oxlorg.opnsense'
  api_timeout:
    type: float
    required: false
    aliases:
    - timeout
    description:
    - Manually override the modules default API-request timeout
  api_retries:
    type: int
    required: false
    default: 0
    aliases:
    - connect_retries
    description:
    - Number of retries on API requests, in case there is an error when establishing the connection. This
      does not handle errors returned by the OPNsense system
notes:
- Omitted optional fields preserve existing values.
- Run against a dedicated test firewall before production use.
- Existing immutable differences fail; certificates and private keys are never silently replaced.
- Private keys are never returned. Trust response bodies are suppressed in debug output and API errors.
- UUID identifies the API record; refid identifies the certificate for consumers such as OpenVPN.
'''

EXAMPLES = r'''
- name: Ensure a VPN server certificate
  oxlorg.opnsense.trust_cert:
    firewall: firewall.example.test
    api_credential_file: /secure/opnsense.key
    description: VPN server
    common_name: vpn.example.test
    country: DE
    ca: Automation CA
    certificate_type: server
    san_dns: [vpn.example.test]
    lifetime: 397
  register: vpn_certificate
# Use vpn_certificate.refid when another API requires a certificate reference.
'''

RETURN = r'''
uuid:
  description: API record UUID; absent for a check-mode creation.
  type: str
  returned: when an existing or newly created record is available
refid:
  description: Certificate reference ID, distinct from UUID.
  type: str
  returned: when an existing or newly created record is available
data:
  description: Public configuration metadata only; no key or certificate payloads.
  type: dict
  returned: when an existing or newly created record is available
'''

ARGUMENT_SPEC = dict(**TRUST_ARGUMENTS, **CERT_ARGUMENTS, **OPN_MOD_ARGS)


def run_module():
    module = AnsibleModule(argument_spec=ARGUMENT_SPEC, supports_check_mode=True,
                           required_one_of=[['description', 'uuid']],
                           mutually_exclusive=[['ca', 'ca_refid']])
    result = dict(changed=False)
    Trust(module, result, 'cert').process()
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
