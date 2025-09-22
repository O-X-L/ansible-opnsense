#!/usr/bin/python

# Copyright: (C) 2025, MaximeWewer
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.handler import \
    module_dependency_error, MODULE_EXCEPTIONS

try:
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.wrapper import module_wrapper
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.defaults.main import \
        OPN_MOD_ARGS, EN_ONLY_MOD_ARG, RELOAD_MOD_ARG
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.wazuh_agent import WazuhAgent

except MODULE_EXCEPTIONS:
    module_dependency_error()

# DOCUMENTATION = 'https://opnsense.ansibleguy.net/modules/wazuh_agent.html'
# EXAMPLES = 'https://opnsense.ansibleguy.net/modules/wazuh_agent.html'


def run_module():
    module_args = dict(
        # General settings
        server_address=dict(
            type='str', required=False, aliases=['server'],
            description='Specifies the IP address or the hostname of the Wazuh manager.'
        ),
        agent_name=dict(
            type='str', required=False, default='',
            description='Specifies the hostname of this agent.'
        ),
        protocol=dict(
            type='str', required=False, default='tcp',
            choices=['tcp', 'udp'],
            description='Specifies the transport protocol to use.'
        ),
        port=dict(
            type='int', required=False, default=1514,
            description='Specifies the port to use for communicating with the Wazuh manager.'
        ),
        debug_level=dict(
            type='int', required=False, default=0,
            description='Debug level for this agents services.'
        ),
        
        # Authentication settings
        auth_password=dict(
            type='str', required=False, no_log=True,
            description='Password to use in authd.pass file.'
        ),
        auth_port=dict(
            type='int', required=False, default=1515,
            description='Specifies the port to use for communicating with the Wazuh manager during enrollment.'
        ),
        
        # Log collector settings
        remote_commands=dict(
            type='bool', required=False, default=True,
            description='Enable remote commands from the log collector'
        ),
        syslog_programs=dict(
            type='list', required=False, elements='str',
            description='Choose which applications to forward to Wazuh.'
        ),
        suricata_eve_log=dict(
            type='bool', required=False, default=True,
            description='Send events from the intrusion detection engine to Wazuh'
        ),
        
        # Module enablers
        rootcheck_enabled=dict(
            type='bool', required=False, default=True,
            description='Enable policy monitoring and anomaly detection'
        ),
        syscollector_enabled=dict(
            type='bool', required=False, default=True,
            description='Enable syscollector'
        ),
        syscheck_enabled=dict(
            type='bool', required=False, default=True,
            description='Enable file integrity monitoring'
        ),
        active_response_enabled=dict(
            type='bool', required=False, default=True,
            description='Enable Active response'
        ),
        active_response_remote_commands=dict(
            type='bool', required=False, default=True,
            description='Toggles whether Command Module should accept commands'
        ),
        active_response_fw_alias_ignore=dict(
            type='list', required=False, elements='str',
            description='Select an alias from which items should be ignored when dropping IP addresses'
        ),
        
        **RELOAD_MOD_ARG,
        **EN_ONLY_MOD_ARG,
        **OPN_MOD_ARGS,
    )

    result = dict(
        changed=False,
        diff={
            'before': {},
            'after': {},
        }
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
    )

    module_wrapper(WazuhAgent(module=module, result=result))
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()