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
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.acme_action import Action

except MODULE_EXCEPTIONS:
    module_dependency_error()


# DOCUMENTATION = 'https://opnsense.ansibleguy.net/en/latest/modules/acme_action.html'
# EXAMPLES = 'https://opnsense.ansibleguy.net/en/latest/modules/acme_action.html'


def run_module():
    module_args = dict(
        name=dict(
            type='str', required=True,
            description='Name to identify this automation.',
        ),
        description=dict(
            type='str', required=False, aliases=['desc'],
            description='Description for this automation. ',
        ),
        type=dict(
            type='str', required=False,
            choices=[
                'configd_restart_gui', 'configd_restart_haproxy', 'configd_restart_nginx','configd_upload_sftp',
                'configd_remote_ssh', 'acme_fritzbox', 'acme_panos', 'acme_proxmoxve', 'acme_vault',
                'acme_synology_dsm', 'acme_truenas', 'acme_unifi', 'configd_generic',
            ],
        ),
        sftp_host=dict(
            type='str', required=False,
            description='IP address or hostname of the SFTP server.'
        ),
        sftp_host_key=dict(
            type='str', required=False,
            description='SFTP server host key, formatted as in \'known_hosts\'. Leave blank to auto accept host key '
                        'on first connect (not as secure as specifying it).'
        ),
        sftp_port=dict(
            type='int', required=False, defalt=22,
            description='SFTP server port. Leave blank to use default "22".'
        ),
        sftp_user=dict(
            type='str', required=False,
            description='The username to login to the SFTP server.'
        ),
        sftp_identity_type=dict(
            type='str', required=False,
            choices=['ecdsa', 'rsa', 'ed25519'],
            description='The type of identify to present to the SFTP server for authorization.'
        ),
        sftp_remote_path=dict(
            type='str', required=False,
            description='Path on the SFTP server to change to after login. The path can be absolute or relative to '
                        'home and must exist. Leave blank to not change path after login.'
        ),
        sftp_chgrp=dict(
            type='str', required=False,
            description='Unix group id to apply to all uploaded files. Leave blank to not change the group.'
        ),
        sftp_chmod=dict(
            type='str', required=False,
            description='Unix permission to apply to uploaded public keys. Leave blank to use default "0440".'
        ),
        sftp_chmod_key=dict(
            type='str', required=False,
            description='Unix permission to apply to uploaded private keys. Leave blank to use default "0400".'
        ),
        sftp_filename_cert=dict(
            type='str', required=False,
            description='Name template for the public certificate. Placeholders "{{name}}" and "%s" are replaced by '
                        'the name of the certificate being uploaded. Leave blank to use default "{{name}}/cert.pem".'
        ),
        sftp_filename_key=dict(
            type='str', required=False,
            description='Name template for the certificate\'s private key. Placeholders "{{name}}" and "%s" are '
                        'replaced by the name of the certificate being uploaded. Leave blank to use default '
                        '"{{name}}/key.pem".'
        ),
        sftp_filename_ca=dict(
            type='str', required=False,
            description='Name template for the public certificate chain file. Placeholders "{{name}}" and "%s" are '
                        'replaced by the name of the certificate being uploaded. Leave blank to use default '
                        '"{{name}}/ca.pem".'
        ),
        sftp_filename_fullchain=dict(
            type='str', required=False,
            description='Name template for the public certificate fullchain file (cert + ca). Placeholders "{{name}}" '
                        'and "%s" are replaced by the name of the certificate being uploaded. Leave blank to use '
                        'default "{{name}}/fullchain.pem".'
        ),
        # Remote SSH
        remote_ssh_host=dict(
            type='str', required=False,
            description='IP address or hostname of the SSH server.'
        ),
        remote_ssh_host_key=dict(
            type='str', required=False,
            description='SSH server host key, formatted as in \'known_hosts\'. Leave blank to auto accept host key on '
                        'first connect (not as secure as specifying it).'
        ),
        remote_ssh_port=dict(
            type='int', required=False, defalt=22,
            description='SSH server port. Leave blank to use default "22".'
        ),
        remote_ssh_user=dict(
            type='str', required=False,
            description='The username to login to the SSH server.'
        ),
        remote_ssh_identity_type=dict(
            type='str', required=False,
            choices=['ecdsa', 'rsa', 'ed25519'],
            description='The type of identify to present to the SSH server for authorization.'
        ),
        remote_ssh_command=dict(
            type='str', required=False,
            description='The command to execute on the SSH server.'
        ),
        # Configd
        configd_generic_command=dict(
            type='str', required=False,
            description='Select a pre-defined system command which should be run.'
        ),
        # ACME FRITZ!Box
        acme_fritzbox_url=dict(
            type='str', required=False,
            description='URL of the router, i.e. https://fritzbox.example.com.'
        ),
        acme_fritzbox_username=dict(
            type='str', required=False,
            description='The username to login to the router.'
        ),
        acme_fritzbox_password=dict(
            type='str', required=False, no_log=True,
            description='The password to login to the router.'
        ),
        # ACME PANOS
        acme_panos_username=dict(
            type='str', required=False,
            description='The username to login to the firewall.'
        ),
        acme_panos_password=dict(
            type='str', required=False, no_log=True,
            description='The password to login to the firewall.'
        ),
        acme_panos_host=dict(
            type='str', required=False,
            description='The hostname of the router.'
        ),
        # ACME Proxmox
        acme_proxmoxve_user=dict(
            type='str', required=False, default='root',
            description='The user who owns the API key. Defaults to root.'
        ),
        acme_proxmoxve_server=dict(
            type='str', required=False,
            description='The hostname of the proxmox ve node.'
        ),
        acme_proxmoxve_port=dict(
            type='int', required=False, default=8006,
            description='The port number the management interface is on. Defaults to 8006.'
        ),
        acme_proxmoxve_nodename=dict(
            type='str', required=False,
            description='The name of the node we will be connecting to.'
        ),
        acme_proxmoxve_realm=dict(
            type='str', required=False, default='pam',
            description='The authentication realm the user authenticates with. Defaults to pam.'
        ),
        acme_proxmoxve_tokenid=dict(
            type='str', required=False, default='acme',
            description='The name of the API token created for the user account. Defaults to acme.'
        ),
        acme_proxmoxve_tokenkey=dict(
            type='str', required=False, no_log=True,
            description='The API token.'
        ),
        # ACME Vault
        acme_vault_url=dict(
            type='str', required=False,
            description='URL of the Vault, i.e. http://vault.example.com:8200.'
        ),
        acme_vault_prefix=dict(
            type='str', required=False, default='acme',
            description='This specifies the prefix path in Vault. If you select KV v2 you need to add .../data/... '
                        'between the secret-mount-path and the path. Example: v1 prefix path: secret/acme, v2 prefix '
                        'path: secret/data/acme.'
        ),
        acme_vault_token=dict(
            type='str', required=False, no_log=True,
            description='This specifies the Vault token to authenticate with.'
        ),
        acme_vault_kvv2=dict(
            type='bool', required=False, default=True,
            description='If checked version 2 of the kv store will be used, otherwise version 1.'
        ),
        # ACME Synology DSM
        acme_synology_dsm_hostname=dict(
            type='str', required=False,
            description='Hostname of IP adress of the Synology DSM, i.e. synology.example.com or 192.168.0.1.'
        ),
        acme_synology_dsm_port=dict(
            type='int', required=False, default=5000,
            description='Port that will be used when connecting to Synology DSM.'
        ),
        acme_synology_dsm_scheme=dict(
            type='str', required=False, default='http',
            choices=['http', 'https'],
            description='Connection scheme that will be used when uploading certificates to Synology DSM.'
        ),
        acme_synology_dsm_username=dict(
            type='str', required=False,
            description='Username to login, must be an administrator.'
        ),
        acme_synology_dsm_password=dict(
            type='str', required=False, no_log=True,
            description='Password to login with.'
        ),
        acme_synology_dsm_create=dict(
            type='bool', required=False, default=True,
            description='This option ensures that a new certificate is created in Synology DSM if it does not exist '
                        'yet. If unchecked only existing certificates will be updated.'
        ),
        acme_synology_dsm_deviceid=dict(
            type='str', required=False,
            description='If Synology DSM has OTP enabled, then the device ID has to be provided so that no OTP is '
                        'required when running the automation.'
        ),
        acme_synology_dsm_devicename=dict(
            type='str', required=False,
            description='If Synology DSM has OTP enabled, then the device name has to be provided so that no OTP is '
                        'required when running the automation.'
        ),
        # ACME TrueNAS
        acme_truenas_apikey=dict(
            type='str', required=False, no_log=True,
            description='API key generated in the TrueNAS web UI.'
        ),
        acme_truenas_hostname=dict(
            type='str', required=False,
            description='Hostname or IP adress of TrueNAS Core Server.'
        ),
        acme_truenas_scheme=dict(
            type='str', required=False, default='http',
            choices=['http', 'https'],
            description='Connection scheme that will be used when uploading certificates to TrueNAS Core Server.'
        ),
        # ACME unifi
        acme_unifi_keystore=dict(
            type='str', required=False, default='/usr/local/share/java/unifi/data/keystore',
            description='Path to the Unifi keystore file in the local filesystem, i.e. '
                        '/usr/local/share/java/unifi/data/keystore.'
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
    )

    module_wrapper(Action(module=module, result=result))
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
