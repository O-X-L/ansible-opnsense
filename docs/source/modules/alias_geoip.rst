.. _modules_alias_geoip:

.. include:: ../_include/head.rst

============
Alias GeoIP
============

**STATE**: unstable

**TESTS**: `Playbook <https://github.com/O-X-L/ansible-opnsense/blob/latest/tests/alias_geoip.yml>`_

**API Docs**: `Core - Firewall <https://docs.opnsense.org/development/api/core/firewall.html>`_

**Service Docs**: `GeoIP <https://docs.opnsense.org/manual/how-tos/maxmind_geo_ip.html>`_

This module allows you to manage the source of the GeoIP database (*Firewall - Aliases - GeoIP settings*).

It is needed before :ref:`aliases <modules_alias>` of the type :code:`geoip` can be used.

Contribution
************

Thanks to `@zarinbal <https://github.com/zarinbal>`_ for developing this module!

----

Info
****

Credentials
===========

Most providers authenticate the download - MaxMind for example expects its account-id and license-key inside the URL: :code:`https://<ACCOUNT-ID>:<LICENSE-KEY>@download.maxmind.com/geoip/databases/GeoLite2-Country-CSV/download?suffix=zip`

Because of that:

* the :code:`url` is never shown in the diff or the module result - a change is only reported as :code:`changed`
* a URL carrying credentials (user-info or query-string) must use :code:`https` - :code:`http` is only accepted for credential-free sources like internal mirrors
* whitespace and control-characters are refused
* if the API response has an unexpected shape, the error does not include it
* the :code:`url` is **not** available through the :code:`oxlorg.opnsense.list` module
* :code:`debug: true` logs the API requests and responses **including** the URL - do not enable it where the output is persisted

Database download
=================

OPNsense only downloads the database once at least one alias of the type :code:`geoip` exists. Setting the source without such an alias will not trigger a download.

Definition
**********

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "url","string","true","\-","\-","Download-URL of the GeoIP database. Must use https if it carries credentials. Set to an empty string to remove the source. Never shown in the diff or result."
    "reload","boolean","false","true","\-", .. include:: ../_include/param_reload.rst

.. include:: ../_include/param_basic.rst

Examples
********

.. code-block:: yaml

    - hosts: localhost
      gather_facts: no
      module_defaults:
        group/oxlorg.opnsense.all:
          firewall: 'opnsense.template.opnsense.oxl.app'
          api_credential_file: '/home/guy/.secret/opn.key'

      vars:
        # keep these in a vault
        maxmind_account_id: '123456'
        maxmind_license_key: 'secret'

      tasks:
        - name: Example
          oxlorg.opnsense.alias_geoip:
            url: 'https://...'
            # reload: true
            # debug: false

        - name: Setting the MaxMind GeoLite2 source
          oxlorg.opnsense.alias_geoip:
            url: "https://{{ maxmind_account_id }}:{{ maxmind_license_key }}@download.maxmind.com/geoip/databases/GeoLite2-Country-CSV/download?suffix=zip"

        - name: Adding a GeoIP alias that uses it
          oxlorg.opnsense.alias:
            name: 'ALLOWED_COUNTRIES'
            type: 'geoip'
            content: ['CA', 'AT']

        - name: Removing the source
          oxlorg.opnsense.alias_geoip:
            url: ''
