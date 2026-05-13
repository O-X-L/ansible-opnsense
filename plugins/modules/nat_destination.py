#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (C) 2025, Pascal Rath <contact+opnsense@OXL.at>
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

# see: https://docs.opnsense.org/development/api/plugins/firewall.html

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.handler import \
    module_dependency_error, MODULE_EXCEPTIONS

try:
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.wrapper import module_wrapper
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.defaults.rule import \
        RULE_MOD_ARGS
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.defaults.main import \
        OPN_MOD_ARGS, STATE_MOD_ARG, RELOAD_MOD_ARG
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.main.nat_destination import DNat

except MODULE_EXCEPTIONS:
    module_dependency_error()


# DOCUMENTATION = 'https://ansible-opnsense.oxl.app/modules/nat_destination.html'
# EXAMPLES = 'https://ansible-opnsense.oxl.app/modules/nat_destination.html'


def run_module():
    shared_rule_args = {
        'sequence': RULE_MOD_ARGS['sequence'],
        'ip_protocol': RULE_MOD_ARGS['ip_protocol'],
        'protocol': RULE_MOD_ARGS['protocol'],
        'source_invert': RULE_MOD_ARGS['source_invert'],
        'source_net': RULE_MOD_ARGS['source_net'],
        'source_port': RULE_MOD_ARGS['source_port'],
        'destination_invert': RULE_MOD_ARGS['destination_invert'],
        'destination_net': RULE_MOD_ARGS['destination_net'],
        'destination_port': RULE_MOD_ARGS['destination_port'],
        'log': RULE_MOD_ARGS['log'],
        'uuid': RULE_MOD_ARGS['uuid'],
        'description': RULE_MOD_ARGS['description'],
    }

    module_args = dict(

        interface=dict(type='str', required=False, default='', aliases=['int', 'i']),
        target=dict(
            type='str', required=False,
            description='NAT translation target - Packets matching this rule will be '
                        'forwarded to the IP address given here.',
        ),
        target_port=dict(type='int', required=False),
        filter_rule=dict(
            type='str', required=False, default='', choices=['', 'pass', 'rule'],
            aliases=['firewall_rule', 'rule'],
            description="Filter rule association. Empty string means no association (manual). "
                        "'rule' automatically creates a corresponding firewall pass rule. ",
        ),
        nat_reflection=dict(
            type='str', required=False, choices=['', 'purenat', 'disable'],
            description='NAT reflection setting for this rule. '
                        "Empty is for system default, 'purenat' is enable.",
        ),
        no_rdr=dict(
            type='bool', required=False, default=False,
            aliases=['no_redirect'],
            description='Enabling this option will disable NAT for traffic matching '
                        'this rule and stop processing Inbound NAT rules.',
        ),
        match_fields=dict(
            type='list', required=True, elements='str',
            description='Fields that are used to match configured rules with the running config - '
                        "if any of those fields are changed, the module will think it's a new rule",
            choices=[
                'sequence', 'interface', 'target', 'target_port', 'ip_protocol', 'protocol',
                'source_invert', 'source_net', 'source_port', 'destination_invert', 'destination_net',
                'destination_port', 'description', 'uuid',
            ]
        ),
        **shared_rule_args,
        **STATE_MOD_ARG,
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

    module_wrapper(DNat(module=module, result=result))
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
