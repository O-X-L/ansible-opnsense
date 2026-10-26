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
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.defaults.main import OPN_MOD_ARGS
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.main.trust_export import Export

except MODULE_EXCEPTIONS:
    module_dependency_error()


# DOCUMENTATION = 'https://ansible-opnsense.oxl.app/modules/trust.html'
# EXAMPLES = 'https://ansible-opnsense.oxl.app/modules/trust.html'


def run_module():
    module_args = dict(
        description=dict(
            type='str', required=True, aliases=['desc'],
            description='Description of the CA or certificate to export.',
        ),
        target=dict(
            type='str', required=False, default='cert', choices=['ca', 'cert'],
            description='If a CA or certificate should be exported.',
        ),
        format=dict(
            type='str', required=False, default='crt', choices=['crt', 'prv', 'csr', 'pkcs12'],
            description="What to export: 'crt' = certificate, 'prv' = private key, "
                        "'csr' = certificate signing request, 'pkcs12' = base64-encoded PKCS#12 bundle "
                        "(certificate, key and CA). 'csr' and 'pkcs12' are only available for certificates. "
                        "Exporting private keys ('prv', 'pkcs12') requires the task to set 'no_log: true'.",
        ),
        password=dict(
            type='str', required=False, default='', no_log=True,
            description="Optional password to protect the 'pkcs12' bundle.",
        ),
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

    module_wrapper(Export(module=module, result=result))
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
