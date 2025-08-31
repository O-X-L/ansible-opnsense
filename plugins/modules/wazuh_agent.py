#!/usr/bin/python

# Copyright: (C) 2025, MaximeWewer
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.handler import \
    module_dependency_error, MODULE_EXCEPTIONS

try:
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.wrapper import module_wrapper
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.defaults.main import \
        OPN_MOD_ARGS, RELOAD_MOD_ARG
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.wazuh_agent import WazuhAgent

except MODULE_EXCEPTIONS:
    module_dependency_error()

# DOCUMENTATION = 'https://opnsense.ansibleguy.net/modules/wazuh_agent.html'
# EXAMPLES = 'https://opnsense.ansibleguy.net/modules/wazuh_agent.html'


def run_module():
    module_args = dict(
        # General settings
        enabled=dict(
            type='bool', required=False, default=True,
            description='Enable/disable the Wazuh agent'
        ),
        server_address=dict(
            type='str', required=False, aliases=['server'],
            description='Wazuh server hostname or IP address'
        ),
        agent_name=dict(
            type='str', required=False, default='',
            description='Agent name (defaults to hostname if not specified)'
        ),
        protocol=dict(
            type='str', required=False, default='tcp',
            choices=['tcp', 'udp'],
            description='Protocol to use for communication with server'
        ),
        port=dict(
            type='int', required=False, default=1514,
            description='Server port for agent communication'
        ),
        debug_level=dict(
            type='int', required=False, default=0,
            choices=[0, 1, 2],
            description='Debug level (0=no debug, 1=basic, 2=verbose)'
        ),
        
        # Authentication settings
        auth_password=dict(
            type='str', required=False, no_log=True,
            description='Authentication password'
        ),
        auth_port=dict(
            type='int', required=False, default=1515,
            description='Authentication port'
        ),
        
        # Log collector settings
        remote_commands=dict(
            type='bool', required=False, default=True,
            description='Allow remote commands execution'
        ),
        syslog_programs=dict(
            type='list', required=False, elements='str',
            description='List of syslog programs to monitor'
        ),
        suricata_eve_log=dict(
            type='bool', required=False, default=True,
            description='Enable Suricata EVE log monitoring'
        ),
        
        # Module enablers
        rootcheck_enabled=dict(
            type='bool', required=False, default=True,
            description='Enable rootcheck module'
        ),
        syscollector_enabled=dict(
            type='bool', required=False, default=True,
            description='Enable syscollector module'
        ),
        syscheck_enabled=dict(
            type='bool', required=False, default=True,
            description='Enable syscheck module'
        ),
        active_response_enabled=dict(
            type='bool', required=False, default=True,
            description='Enable active response module'
        ),
        active_response_remote_commands=dict(
            type='bool', required=False, default=True,
            description='Allow active response remote commands'
        ),
        active_response_fw_alias_ignore=dict(
            type='list', required=False, elements='str',
            description='Firewall aliases to ignore in active response'
        ),
        
        **RELOAD_MOD_ARG,
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