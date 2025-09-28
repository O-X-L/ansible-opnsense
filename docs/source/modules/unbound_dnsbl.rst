.. _modules_unbound_dnsbl:

.. include:: ../_include/head.rst

==========================
DNS - Unbound - Blocklists
==========================

**STATE**: stable

**TESTS**: `Playbook <https://github.com/O-X-L/ansible_opnsense/blob/latest/tests/unbound_dnsbl.yml>`_

**API Docs**: `unbound_dnsbl <https://docs.opnsense.org/development/api/core/unbound.html>`_

**Service Docs**: `Unbound DNS  - Blocklists <https://docs.opnsense.org/manual/unbound.html#blocklists>`_

Contribution
************

Thanks to `@jiuka <https://github.com/jiuka>`_ for developing this module!

----

Definition
**********

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "safesearch","boolean","false","false","\-","Force the usage of SafeSearch on Google, DuckDuckGo, Bing, Qwant, PixaBay and YouTube"
    "type","list of strings","false","[]","\-","Select which kind of DNSBL you want to use"
    "whitelists","list of strings","false","[]","whitelist, allowlist, allowlists","List of domains to whitelist. You can use regular expressions"
    "blocklists","list of strings","false","[]","blocklist","List of domains to blocklist. Only exact matches are supported"
    "wildcards","list of strings","false","[]","wildcard","List of wildcard domains to blocklist. All subdomains of the given domain will be blocked. Blocking first-level domains is not supported"
    "address","strings","false","\-","\-","Destination ip address for entries in the blocklist (leave empty to use default: 0.0.0.0). Not used when 'Return NXDOMAIN' is checked"

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "nxdomain","bool","false","false","\-","Use the DNS response code NXDOMAIN instead of a destination address"
    "enabled","boolean","false","true","\-","Enable the usage of DNS blocklists"
    "reload","boolean","false","true","\-", .. include:: ../_include/param_reload.rst

.. include:: ../_include/param_basic.rst

----

Usage
*****

Manage Unbound DNS blocklists and exceptions.

----

Examples
********

.. code-block:: yaml

    - hosts: localhost
      gather_facts: false
      module_defaults:
        group/oxlorg.opnsense.all:
          firewall: 'opnsense.template.opnsense.oxl.app'
          api_credential_file: '/home/guy/.secret/opn.key'

        oxlorg.opnsense.list:
          target: 'unbound_dnsbl'

      tasks:
        # add optional parameters commented-out
        # required ones normally
        # add their default values to get a brief overview of how the module works
        - name: Example
          oxlorg.opnsense.unbound_dnsbl:
            type: atl
            # safesearch: false
            # lists: ['https://example.com/dns.blocklist']
            # whitelists: ['opnsense.oxl.app']
            # blocklists: ['example.net']
            # wildcards: ['example.net']
            # address: 192.168.254.254
            # nxdomain: false
            # enable: false
            # state: 'absent'
            # debug: false

        - name: Configuring DNS Blocklists
          oxlorg.opnsense.unbound_dnsbl:
            type: atl
            enable: true

        - name: Listing current config
          oxlorg.opnsense.list:
          #  target: 'unbound_dnsbl'
          register: dnsbl_config

        - name: Printing
          ansible.builtin.debug:
            var: dnsbl_config.data
