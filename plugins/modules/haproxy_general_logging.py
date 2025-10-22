#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (C) 2025, AnsibleGuy <guy@ansibleguy.net>
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

# see: https://docs.opnsense.org/development/api/plugins/haproxy.html

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.handler import \
    module_dependency_error, MODULE_EXCEPTIONS

try:
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.wrapper import module_wrapper
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.defaults.main import \
        OPN_MOD_ARGS, RELOAD_MOD_ARG
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.haproxy_general_logging import HaproxyGeneralLogging

except MODULE_EXCEPTIONS:
    module_dependency_error()


# DOCUMENTATION = 'https://ansible-opnsense.oxl.app/modules/haproxy.html'
# EXAMPLES = 'https://ansible-opnsense.oxl.app/modules/haproxy.html'


def run_module():
    module_args = dict(
        host=dict(
            type='str', required=False, default='127.0.0.1',
            description='Indicates where to send the logs. Takes an IPv4 or IPv6 address optionally followed by a colon'
        ),
        facility=dict(
            type='str', required=False, default='local0',
            choices=['alert', 'audit', 'auth2', 'auth', 'cron2', 'cron', 'daemon', 'ftp', 'kern',
                     'local0', 'local1', 'local2', 'local3', 'local4', 'local5', 'local6', 'local7',
                     'lpr', 'mail', 'news', 'ntp', 'syslog', 'user', 'uucp'],
            description='Choose one of the 24 standard syslog facilities'
        ),
        level=dict(
            type='str', required=False, default='info',
            choices=['alert', 'crit', 'debug', 'emerg', 'err', 'info', 'notice', 'warning'],
            description='Can be specified to filter outgoing messages. By default, all messages are sent'
        ),
        length=dict(
            type='int', required=False, default=None,
            description='Specify an optional maximum line length in characters. Log lines larger than this value will be truncated'
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

    module_wrapper(HaproxyGeneralLogging(module=module, result=result))

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
