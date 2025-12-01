.. _modules_unbound_dnsbl:

.. include:: ../_include/head.rst

==========================
DNS - Unbound - Blocklists
==========================

**STATE**: stable

**TESTS**: `Playbook <https://github.com/O-X-L/ansible-opnsense/blob/latest/tests/unbound_dnsbl.yml>`_

**API Docs**: `unbound_dnsbl <https://docs.opnsense.org/development/api/core/unbound.html>`_

**Service Docs**: `Unbound DNS  - Blocklists <https://docs.opnsense.org/manual/unbound.html#blocklists>`_

Contribution
************

Thanks to `@jiuka <https://github.com/jiuka>`_ and `@Rath <https://github.com/superstes>`_ for developing this module!

----

.. warning::

    You need to run OPNsense version >= 25.7.8 to be able to have multiple DNS-blocklists.


----

Definition
**********

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "name","string","true","false","description,desc","Unique name to identify the entry"
    "providers","list of strings","false","[]","type,dnsbl,bl","Select which kind of DNSBL you want to use"
    "download_urls","list of strings","false","[]","download,lists","List of URLs/domains from where blocklist will be downloaded"
    "domains_allow","list of strings","false","[]","allowlists","List of domains to allow. You can use regular expressions. This allow list only applies to blocklist matches on items in this policy"
    "domains_block","list of strings","false","[]","blocklists","List of domains to blocklist. Only exact matches are supported"
    "wildcard_domains_block","list of strings","false","[]","wildcards_block,wildcard_domains,wildcards","List of wildcard domains to blocklist. All subdomains of the given domain will be blocked. Blocking first-level domains is not supported"
    "source_networks","list of strings","false","[]","networks,source_nets,src_nets","Source networks to apply policy on. Examples are 192.168.1.0/24 or 192.168.1.1. Leave empty to apply on everything. All specified networks should use the same protocol family and have equal sizes to avoid priority issue"
    "cache_ttl","int","false","72000","ttl","TTL-seconds for the blocklists cache. Remote blocklists don't usually update more often than once a day. Therefore, when blocklists are downloaded, they are cached locally to prevent unnecessary fetches over the internet. You can change this behavior here if you know the remote files rotate faster than this"
    "nxdomain_address","string","false","\-","address,redirect_to","Destination ip address for entries in the blocklist (leave empty to use default: 0.0.0.0). Not used when "Return NXDOMAIN" is checked"
    "nxdomain","bool","false","false","\-","Use the DNS response code NXDOMAIN instead of a destination address"

.. include:: ../_include/param_basic.rst

----

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

        oxlorg.opnsense.list:
          target: 'unbound_dnsbl'

      tasks:
        # add optional parameters commented-out
        # required ones normally
        # add their default values to get a brief overview of how the module works
        - name: Example
          oxlorg.opnsense.unbound_dnsbl:
            name: 'example DNS-BL'
            providers: ['atf']
            # download_urls: ['https://example.com/dns.blocklist']
            # domains_allow: ['opnsense.org', 'oxl.at']
            # domains_block: ['example.porn.org']
            # wildcard_domains_block: ['evil.org']
            # source_networks: ['10.0.10.0/24', '10.2.10.0/24']
            # nxdomain_address: '192.168.255.255'
            # nxdomain: false
            # enabled: false
            # state: 'absent'
            # debug: false

        - name: Adding DNS Blocklists
          oxlorg.opnsense.unbound_dnsbl:
            name: 'Provider DNS-BLs'
            providers: ['atf', 'atl']
            domains_allow: ['site-to-exclude.com']

        - name: Blocking some social media for client-networks
          oxlorg.opnsense.unbound_dnsbl:
            name: 'Social Media'
            wildcard_domains_block: ['facebook.com', 'meta.com', 'tiktok.com']
            source_networks: ['192.168.0.0/16']

        - name: Listing current config
          oxlorg.opnsense.list:
          #  target: 'unbound_dnsbl'
          register: dnsbl_config

        - name: Printing
          ansible.builtin.debug:
            var: dnsbl_config.data
