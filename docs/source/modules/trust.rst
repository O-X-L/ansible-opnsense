.. _modules_trust:

.. include:: ../_include/head.rst

=====
Trust
=====

**STATE**: unstable

**TESTS**: `trust_ca <https://github.com/O-X-L/ansible-opnsense/blob/latest/tests/trust_ca.yml>`_ |
`trust_cert <https://github.com/O-X-L/ansible-opnsense/blob/latest/tests/trust_cert.yml>`_

**API Docs**: `Core - Trust <https://docs.opnsense.org/development/api/core/trust.html>`_

**Service Docs**: `Trust <https://docs.opnsense.org/manual/certificates.html>`_

Contribution
************

Thanks to `@Rath <https://github.com/superstes>`_ and `@unclesam87 <https://github.com/unclesam87>`_ for developing this module!

----

Definition
**********

oxlorg.opnsense.trust_ca
========================

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "description","string","true","\-","desc","Unique description of the certificate authority"
    "ca","string","false","\-","issuer","Description or reference-id of an existing CA that should sign this one. Leave empty to create a self-signed root CA"
    "key_type","string","false","prime256v1","\-","Key size (RSA) or elliptic curve of the private key. One of: '512', '1024', '2048', '3072', '4096', '7680', '8192', 'prime256v1', 'secp384r1', 'secp521r1'"
    "digest","string","false","sha256","\-","Digest algorithm used to sign the certificate. One of: 'sha1', 'sha224', 'sha256', 'sha384', 'sha512'"
    "lifetime","integer","false","825","\-","Validity of the certificate in days"
    "common_name","string","false","\-","cn","Common name of the CA"
    "country","string","true (if state=present)","\-","\-","Two-letter country code"
    "state_or_province","string","false","\-","\-","State or province"
    "city","string","false","\-","\-","City"
    "organization","string","false","\-","\-","Organization"
    "organizational_unit","string","false","\-","\-","Organizational unit"
    "email","string","false","\-","\-","Email address"
    "ocsp_uri","string","false","\-","\-","URI of the OCSP responder for certificates signed by this CA"
    "match_fields","list","false","['description']","\-","Fields that are used to match configured CAs with the running config - if any of those fields are changed, the module will think it's a new entry. One or multiple of: 'description', 'common_name'"

oxlorg.opnsense.trust_cert
==========================

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "description","string","true","\-","desc","Unique description of the certificate"
    "ca","string","false","\-","issuer","Description or reference-id of the CA that should sign the certificate. Leave empty to create a self-signed certificate"
    "cert_type","string","false","server","type","Purpose of the certificate. One of: 'client', 'server', 'server_client'"
    "key_type","string","false","prime256v1","\-","Key size (RSA) or elliptic curve of the private key. One of: '512', '1024', '2048', '3072', '4096', '7680', '8192', 'prime256v1', 'secp384r1', 'secp521r1'"
    "digest","string","false","sha256","\-","Digest algorithm used to sign the certificate. One of: 'sha1', 'sha224', 'sha256', 'sha384', 'sha512'"
    "lifetime","integer","false","397","\-","Validity of the certificate in days"
    "common_name","string","false","\-","cn","Common name of the certificate"
    "country","string","true (if state=present)","\-","\-","Two-letter country code"
    "state_or_province","string","false","\-","\-","State or province"
    "city","string","false","\-","\-","City"
    "organization","string","false","\-","\-","Organization"
    "organizational_unit","string","false","\-","\-","Organizational unit"
    "email","string","false","\-","\-","Email address"
    "ocsp_uri","string","false","\-","\-","URI of the OCSP responder"
    "san_dns","list","false","\-","\-","DNS subject alternative names"
    "san_ip","list","false","\-","\-","IP address subject alternative names"
    "san_email","list","false","\-","\-","Email subject alternative names"
    "san_uri","list","false","\-","\-","URI subject alternative names"
    "match_fields","list","false","['description']","\-","Fields that are used to match configured certificates with the running config - if any of those fields are changed, the module will think it's a new entry. One or multiple of: 'description', 'common_name'"

oxlorg.opnsense.trust_export
============================

.. warning::

    You should always set :code:`no_log: true` when exporting private-keys with this module to ensure the secrets are not logged by Ansible.

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "description","string","true","\-","desc","Description of the CA or certificate to export"
    "target","string","false","cert","\-","If a CA or certificate should be exported. One of: 'ca', 'cert'"
    "format","string","false","crt","\-","What to export. One of: 'crt' (certificate), 'prv' (private key), 'csr' (certificate signing request - certificates only), 'pkcs12' (base64-encoded PKCS#12 bundle with certificate, key and CA - certificates only). You should set 'no_log: true' when exporting private keys ('prv', 'pkcs12')"
    "password","string","false","\-","\-","Optional password to protect the 'pkcs12' bundle"

.. include:: ../_include/param_basic.rst


Usage
*****

These modules create internal certificate authorities and certificates signed by them (or self-signed ones).

**Only the description can be changed** without re-issuing the certificate.
All other fields (*subject, key, digest, lifetime, issuer, purpose and SANs*) are part of the issued certificate.
If they differ from an existing entry the module fails - create a new entry with another description and migrate its references.

To rename an entry, match it by another field: :code:`match_fields: ['common_name']`

Notes:

* The **private keys are never returned** by :code:`trust_ca`, :code:`trust_cert` or the :code:`oxlorg.opnsense.list` output.
  The public certificate is available as :code:`crt_payload` in the :code:`oxlorg.opnsense.list` output.
* To use certificates in other services, export them using :code:`trust_export`. Its result contains :code:`uuid` and :code:`payload`.

  Ansible cannot hide single result-values from its output. Therefore exporting a private key (*format 'prv' or 'pkcs12'*) is refused unless the task sets :code:`no_log: true`.

  Make sure to also protect the exported key wherever you store it (*file permissions, vault, ..*). Do not enable :code:`debug` for these tasks, as it logs the raw API responses.
* Private keys are always saved on the firewall.
* A CA that is still referenced (*by certificates, other CAs or services*) cannot be removed.
  A certificate that is still in use is refused by the API.
* The lifetime is compared to the validity period of the issued certificate - not to its remaining validity. Expired certificates are **not** renewed automatically.
* Other services (*like OpenVPN*) reference CAs and certificates by their description.
* No reload is needed. CA changes are applied by the API, certificate consumers need to be reloaded separately.

Not supported (*yet*): importing existing CAs/certificates, certificate signing requests, OCSP signing certificates, re-issuing certificates.


Examples
********

.. code-block:: yaml

    - hosts: firewalls
      connection: local
      gather_facts: false
      module_defaults:
        group/oxlorg.opnsense.all:
          firewall: 'opnsense.template.opnsense.oxl.app'
          api_credential_file: '/home/guy/.secret/opn.key'

      tasks:
        - name: Example CA
          oxlorg.opnsense.trust_ca:
            description: 'Internal CA'
            country: 'AT'
            # ca: ''
            # key_type: 'prime256v1'
            # digest: 'sha256'
            # lifetime: 825
            # common_name: ''
            # state_or_province: ''
            # city: ''
            # organization: ''
            # organizational_unit: ''
            # email: ''
            # ocsp_uri: ''
            # match_fields: ['description']
            # state: 'present'
            # debug: false

        - name: Example certificate
          oxlorg.opnsense.trust_cert:
            description: 'VPN Server'
            country: 'AT'
            # ca: ''
            # cert_type: 'server'
            # key_type: 'prime256v1'
            # digest: 'sha256'
            # lifetime: 397
            # common_name: ''
            # san_dns: []
            # san_ip: []
            # san_email: []
            # san_uri: []
            # match_fields: ['description']
            # state: 'present'
            # debug: false

        - name: Adding a root CA
          oxlorg.opnsense.trust_ca:
            description: 'Internal Root CA'
            common_name: 'Internal Root CA'
            country: 'AT'
            organization: 'Example Ltd'
            key_type: 'secp384r1'
            digest: 'sha384'
            lifetime: 7300

        - name: Adding an intermediate CA
          oxlorg.opnsense.trust_ca:
            description: 'Internal VPN CA'
            common_name: 'Internal VPN CA'
            country: 'AT'
            ca: 'Internal Root CA'
            lifetime: 3650

        - name: Adding a server certificate
          oxlorg.opnsense.trust_cert:
            description: 'VPN Server'
            common_name: 'vpn.example.com'
            country: 'AT'
            ca: 'Internal VPN CA'
            cert_type: 'server'
            san_dns: ['vpn.example.com']
            san_ip: ['192.0.2.1']

        - name: Renaming the certificate
          oxlorg.opnsense.trust_cert:
            description: 'VPN Server 2026'
            common_name: 'vpn.example.com'
            country: 'AT'
            ca: 'Internal VPN CA'
            cert_type: 'server'
            san_dns: ['vpn.example.com']
            san_ip: ['192.0.2.1']
            match_fields: ['common_name']

        - name: Exporting the certificate
          oxlorg.opnsense.trust_export:
            description: 'VPN Server 2026'
            # target: 'cert'
            # format: 'crt'
          register: vpn_cert

        - name: Exporting the private key
          oxlorg.opnsense.trust_export:
            description: 'VPN Server 2026'
            format: 'prv'
          register: vpn_key
          no_log: true  # ensure ansible does not log secrets

        - name: Saving the key for another service
          ansible.builtin.copy:
            content: "{{ vpn_key.payload }}"
            dest: '/etc/ssl/private/vpn.key'
            mode: 0600
          no_log: true  # ensure ansible does not log secrets

        # Note: the payload is base64-encoded as PKCS#12 is binary
        - name: Exporting a password-protected PKCS#12 bundle
          oxlorg.opnsense.trust_export:
            description: 'VPN Server 2026'
            format: 'pkcs12'
            password: !vault |
              ...
          register: vpn_p12
          no_log: true  # ensure ansible does not log secrets

        - name: Exporting the CA certificate
          oxlorg.opnsense.trust_export:
            description: 'Internal VPN CA'
            target: 'ca'
          register: vpn_ca

        - name: Removing the certificate
          oxlorg.opnsense.trust_cert:
            description: 'VPN Server 2026'
            state: 'absent'

        - name: Listing certificates
          oxlorg.opnsense.list:
            target: 'trust_cert'
          register: existing_certs

        - name: Printing
          ansible.builtin.debug:
            var: existing_certs.data
