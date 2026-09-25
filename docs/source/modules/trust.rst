.. _modules_trust:

Certificate authorities and certificates
============================================

**STATE**: experimental; mocked tests pass, live validation is pending.

**oxlorg.opnsense.trust_ca** creates an internal root CA.
**oxlorg.opnsense.trust_cert** creates a CA-signed server or client certificate.
Both use the Trust API: https://docs.opnsense.org/development/api/core/trust.html
The implementations are based on the OPNsense 26.7.3 controllers and models.

Safe reruns
-----------

An existing entry is matched by exact **description**, or explicitly by
**uuid**. Duplicate descriptions fail. Unknown UUIDs fail without creating
a replacement. Existing requested properties are verified; immutable differences
fail with instructions to issue a new certificate under a new description and
migrate references explicitly. Even description changes selected by UUID fail.

These modules never call set, del or reissue.
They do not renew expired certificates automatically. Validity comparison uses the
original validity duration, not the remaining time. Private keys stay on the
firewall and are excluded from results, diffs and trust API debug/error bodies.
Check mode reports prospective creation without issuing certificates.

Configuration
-------------

.. include:: ../_include/param_basic.rst

Run **ansible-doc oxlorg.opnsense.trust_ca** or
**ansible-doc oxlorg.opnsense.trust_cert** for full definitions.

For creation, provide **description**, **common_name** and **country**.
Optional subject fields are **state_or_province**, **city**, **organization**,
**organizational_unit** and **email**.
**key_type** accepts RSA sizes 2048, 3072, 4096, 7680, 8192 or the curves
prime256v1, secp384r1, secp521r1. **digest** accepts sha256, sha384, sha512;
**lifetime** is in days.

Certificate creation additionally requires an existing CA selected by **ca**
(description) or **ca_refid** (certificate reference, not UUID).
**certificate_type** accepts server, client or server_client. New certificates
default to server. **san_dns**, **san_ip**, **san_email** and **san_uri**
are lists of individual subject alternative names.

Omitted optional parameters use API creation defaults and do not enforce a value
on existing entries. In the 26.7.3 models these defaults include RSA-2048,
sha256, 825 days for CAs and 397 days for certificates.

Results return **uuid**, **refid**, and public configuration metadata under
**data**. An API record UUID and a certificate reference are different
identifiers. Use the reference when linking certificates to OpenVPN.
A check-mode creation cannot return identifiers that do not exist yet.

Example
-------

.. code-block:: yaml

    - name: Ensure the automation root CA
      oxlorg.opnsense.trust_ca:
        firewall: firewall.example.test
        api_credential_file: /secure/opnsense.key
        description: Automation CA
        common_name: Automation CA
        country: DE
        key_type: '4096'
        lifetime: 3650

    - name: Ensure a VPN server certificate
      oxlorg.opnsense.trust_cert:
        firewall: firewall.example.test
        api_credential_file: /secure/opnsense.key
        description: VPN server
        common_name: vpn.example.test
        country: DE
        ca: Automation CA
        certificate_type: server
        san_dns: [vpn.example.test]
        lifetime: 397
      register: vpn_certificate

List safe metadata using **oxlorg.opnsense.list** with target
**trust_ca** or **trust_cert**. No trust reload target is registered:
CA creation applies trust configuration in the API, and certificate consumers
must be configured and reloaded separately.

GUI certificate selection, imports, CSR workflows, key export, renewal,
intermediate CA creation and deletion are outside these modules' first scope.

Testing and recovery
--------------------

Mocked tests cover reruns, immutable drift, check mode, CA resolution and
sensitive error responses. The opt-in **tests/trust.yml** creates synthetic
test resources and cleans up only UUIDs created by that invocation. It refuses
pre-existing test descriptions. Do not add broad trust deletion to the global
cleanup playbook.

.. code-block:: console

    export TEST_FIREWALL=firewall.example.test
    export TEST_API_KEY=/secure/test-firewall.key
    ansible-playbook tests/trust.yml

Use a dedicated test firewall. The playbook exercises check mode internally.
If creation succeeds server-side but the response or read-back fails, inspect
System / Trust before retrying. Resources without a confirmed returned UUID are
not automatically removed. A timeout is not proof that creation failed.

Listing pending CSRs and externally managed certificates returns their description,
UUID, optional reference, and certificate_available/csr_available flags.
Their key and CSR payloads are never returned. Ensuring present still requires
an issued certificate with a valid reference. IP SAN comparisons normalize IPv6 notation.
