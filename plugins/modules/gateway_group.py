#!/usr/bin/python
# -*- coding: utf-8 -*-
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.wrapper import module_wrapper
from ansible_collections.oxlorg.opnsense.plugins.module_utils.defaults.main import (
    OPN_MOD_ARGS, STATE_ONLY_MOD_ARG, RELOAD_MOD_ARG,
)
from ansible_collections.oxlorg.opnsense.plugins.module_utils.main.gateway_group import GatewayGroup


DOCUMENTATION = r'''
module: gateway_group
short_description: Manage OPNsense gateway groups
description:
- Uses the OPNsense API. Supports check mode and preserves unrelated resources.
- API behavior verified against OPNsense 26.7.3 source; live integration validation is pending.
author:
- OXL contributors
options:
  name:
    type: str
    description:
    - Unique gateway-group name. Required for creation; existing names cannot be changed.
  uuid:
    type: str
    description:
    - Select an existing entry by UUID. An unknown UUID fails without creating a replacement.
  description:
    type: str
    description:
    - Gateway group description. Omitted values preserve the existing description.
  tier_1:
    type: list
    elements: str
    description:
    - Gateway names in tier 1. Lower numbered tiers have priority. Omitted values preserve the existing
      tier.
  tier_2:
    type: list
    elements: str
    description:
    - Gateway names in tier 2. Lower numbered tiers have priority. Omitted values preserve the existing
      tier.
  tier_3:
    type: list
    elements: str
    description:
    - Gateway names in tier 3. Lower numbered tiers have priority. Omitted values preserve the existing
      tier.
  tier_4:
    type: list
    elements: str
    description:
    - Gateway names in tier 4. Lower numbered tiers have priority. Omitted values preserve the existing
      tier.
  tier_5:
    type: list
    elements: str
    description:
    - Gateway names in tier 5. Lower numbered tiers have priority. Omitted values preserve the existing
      tier.
  trigger:
    type: str
    choices:
    - down
    - downloss
    - downlatency
    - downlosslatency
    description:
    - Failover trigger. Omitted values preserve existing configuration; creation uses the API default.
  pool_options:
    type: str
    choices:
    - ''
    - round-robin
    - round-robin sticky-address
    description:
    - Load-balancing pool options. Empty string selects the default.
  state:
    type: str
    required: false
    choices:
    - present
    - absent
    default: present
    description:
    - Whether the gateway group should exist. Deletion must be requested explicitly.
  reload:
    type: bool
    required: false
    default: false
    aliases:
    - apply
    description:
    - If the running config should be reloaded/applied on change - will take some time
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
'''

EXAMPLES = r'''
- name: Configure WAN failover
  oxlorg.opnsense.gateway_group:
    firewall: firewall.example.test
    api_credential_file: /secure/opnsense.key
    name: WAN_FAILOVER
    tier_1: [WAN_PRIMARY]
    tier_2: [WAN_BACKUP]
    trigger: down
    reload: true
'''

RETURN = r'''
uuid:
  description: API record UUID; absent for a check-mode creation.
  type: str
  returned: when an existing or newly created record is available
'''

ARGUMENT_SPEC = dict(
    name=dict(type='str'),
    uuid=dict(type='str'),
    description=dict(type='str'),
    tier_1=dict(type='list', elements='str'),
    tier_2=dict(type='list', elements='str'),
    tier_3=dict(type='list', elements='str'),
    tier_4=dict(type='list', elements='str'),
    tier_5=dict(type='list', elements='str'),
    trigger=dict(type='str', choices=['down', 'downloss', 'downlatency', 'downlosslatency']),
    pool_options=dict(type='str', choices=['', 'round-robin', 'round-robin sticky-address']),
    **STATE_ONLY_MOD_ARG, **RELOAD_MOD_ARG, **OPN_MOD_ARGS,
)


def run_module():
    module = AnsibleModule(argument_spec=ARGUMENT_SPEC, supports_check_mode=True,
                           required_one_of=[['name', 'uuid']])
    result = dict(changed=False, diff={'before': {}, 'after': {}})
    module_wrapper(GatewayGroup(module, result))
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
