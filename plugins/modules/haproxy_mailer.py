#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (C) 2025, MaximeWewer
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

# see: https://docs.opnsense.org/development/api/plugins/haproxy.html

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.handler import \
    module_dependency_error, MODULE_EXCEPTIONS

try:
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.wrapper import module_wrapper
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.defaults.main import \
        OPN_MOD_ARGS, STATE_MOD_ARG, RELOAD_MOD_ARG
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.main.haproxy_mailer import HaproxyMailer

except MODULE_EXCEPTIONS:
    module_dependency_error()


# DOCUMENTATION = 'https://ansible-opnsense.oxl.app/modules/haproxy.html'
# EXAMPLES = 'https://ansible-opnsense.oxl.app/modules/haproxy.html'


def run_module():
    module_args = dict(
        name=dict(
            type='str', required=True,
            description='Choose a name for this mailer configuration.'
        ),
        description=dict(
            type='str', required=False,
            description='Choose a optional description for this mailer configuration.'
        ),
        mailservers=dict(
            type='list', elements='str', required=False, default=[],
            description='Add mailservers to this mailer configuration, i.e. 192.168.1.1:25.'
        ),
        sender=dict(
            type='str', required=False,
            description='Declare the from email address to be used in both the envelope and header of email alerts.'
        ),
        recipient=dict(
            type='str', required=False,
            description='Recipient email address for alerts.'
        ),
        loglevel=dict(
            type='str', required=False,
            description='Declare the maximum log level of messages for which email alerts will be sent.'
        ),
        timeout=dict(
            type='str', required=False,
            description='Time in seconds to connect and send email to mail server.'
        ),
        hostname=dict(
            type='str', required=False,
            description='Declare the to hostname address to be used when communicating with mailers.'
        ),
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

    module_wrapper(HaproxyMailer(module=module, result=result))

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
