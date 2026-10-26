#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (C) 2026, Pascal Rath <contact+opnsense@OXL.at>
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

# see: https://docs.opnsense.org/development/api/core/trust.html

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.handler import \
    module_dependency_error, MODULE_EXCEPTIONS

try:
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.wrapper import module_wrapper
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.defaults.main import \
        OPN_MOD_ARGS, STATE_ONLY_MOD_ARG
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.helper.trust import \
        TRUST_KEY_TYPES, TRUST_DIGESTS
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.main.trust_ca import Ca

except MODULE_EXCEPTIONS:
    module_dependency_error()


# DOCUMENTATION = 'https://ansible-opnsense.oxl.app/modules/trust.html'
# EXAMPLES = 'https://ansible-opnsense.oxl.app/modules/trust.html'


def run_module():
    module_args = dict(
        description=dict(
            type='str', required=True, aliases=['desc'],
            description='Unique description of the certificate authority.',
        ),
        ca=dict(
            type='str', required=False, default='', aliases=['issuer'],
            description='Description or reference-id of an existing CA that should sign this one. '
                        'Leave empty to create a self-signed root CA.',
        ),
        key_type=dict(
            type='str', required=False, default='prime256v1', choices=TRUST_KEY_TYPES,
            description='Key size (RSA) or elliptic curve of the private key.',
        ),
        digest=dict(
            type='str', required=False, default='sha256', choices=TRUST_DIGESTS,
            description='Digest algorithm used to sign the certificate. '
                        'Note: SHA1 and SHA224 are considered weak.',
        ),
        lifetime=dict(
            type='int', required=False, default=825,
            description='Validity of the certificate in days.',
        ),
        common_name=dict(
            type='str', required=False, default='', aliases=['cn'],
            description='Common name of the CA.',
        ),
        country=dict(
            type='str', required=False,
            description='Two-letter country code. Required when the CA should be present.',
        ),
        state_or_province=dict(
            type='str', required=False, default='',
            description='State or province.',
        ),
        city=dict(
            type='str', required=False, default='',
            description='City.',
        ),
        organization=dict(
            type='str', required=False, default='',
            description='Organization.',
        ),
        organizational_unit=dict(
            type='str', required=False, default='',
            description='Organizational unit.',
        ),
        email=dict(
            type='str', required=False, default='',
            description='Email address.',
        ),
        ocsp_uri=dict(
            type='str', required=False, default='',
            description='URI of the OCSP responder for certificates signed by this CA.',
        ),
        match_fields=dict(
            type='list', required=False, elements='str',
            description='Fields that are used to match configured CAs with the running config - '
                        "if any of those fields are changed, the module will think it's a new entry",
            choices=['description', 'common_name'],
            default=['description'],
        ),
        **STATE_ONLY_MOD_ARG,
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
        required_if=[('state', 'present', ['country'])],
    )

    module_wrapper(Ca(module=module, result=result))
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
