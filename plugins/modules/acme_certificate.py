#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (C) 2024, AnsibleGuy <guy@ansibleguy.net>
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.handler import \
    module_dependency_error, MODULE_EXCEPTIONS

try:
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.wrapper import module_wrapper
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.defaults.main import \
        OPN_MOD_ARGS, STATE_MOD_ARG, RELOAD_MOD_ARG
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.acme_certificate import Certificate

except MODULE_EXCEPTIONS:
    module_dependency_error()


# DOCUMENTATION = 'https://opnsense.ansibleguy.net/en/latest/modules/acmeclient.html'
# EXAMPLES = 'https://opnsense.ansibleguy.net/en/latest/modules/acmeclient.html'


def run_module():
    module_args = dict(
        name=dict(
            type='str', required=False, aliases=['cn'],
            description='Common Name (CN) and first Alt Name (subjectAltName) for this certificate.',
        ),
        description=dict(
            type='str', required=True, aliases=['desc'],
            description='Description for this certificate.',
        ),
        alt_names=dict(
            type='list', required=False, elements='str', default=[], aliases=['subject_alt_name'],
            description='Configure additional names that should be part of the certificate, i.e. www.example.com or '
                        'mail.example.com. Use TAB key to complete typing a FQDN.',
        ),
        account=dict(type='str', required=False),
        validation=dict(type='str', required=False),
        auto_renewal=dict(
            type='bool', required=False, default=True,
            description='Enable automatic renewal for this certificate to prevent expiration. When disabled, the cron '
                        'job will ignore this certificate.',
        ),
        renew_interval=dict(
            type='int', required=False, default=60,
            description='Specifies the days to renew the cert. The max value is 5000 days.',
        ),
        key_length=dict(
            type='str', required=False, default='key_4096',
            choices=['key_2048', 'key_3072', 'key_4096', 'key_ec256', 'key_ec384'],
            description='Specify the domain key length: key_2048, key_3072, key_4096, key_ec256 or key_ec384.',
        ),
        ocsp=dict(
            type='bool', required=False, default=False,
            description='Generate and add OCSP Must Staple extension to the certificate.',
        ),
        restart_actions=dict(
            type='list', required=False, elements='str', default=[],
            description='Choose the automations that should be run after certificate creation and renewal.',
        ),
        aliasmode=dict(
            type='str', required=False, default='none',
            choices=['none', 'automatic', 'domain', 'challenge'],
            description='Configure DNS alias mode to validate the certificate.',
        ),
        domainalias=dict(
            type='str', required=False,
            description='When setting DNS alias mode to "Domain Alias", enter the domain name that should be used for '
                        'certificate validation. Please refer to the acme.sh documentation for further information. ',
        ),
        challengealias=dict(
            type='str', required=False,
            description='When setting DNS alias mode to "Challenge Alias", enter the domain name that should be used '
                        'for certificate validation. Please refer to the acme.sh documentation for further '
                        'information.',
        ),
        **RELOAD_MOD_ARG,
        **STATE_MOD_ARG,
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
        required_if=[
            ('aliasmode', 'domain', ('domainalias',)),
            ('aliasmode', 'challenge', ('challengealias',)),
        ],
    )

    module_wrapper(Certificate(module=module, result=result))
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
