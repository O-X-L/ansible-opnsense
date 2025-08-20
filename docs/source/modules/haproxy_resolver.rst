.. _modules_haproxy_resolver:

.. include:: ../_include/head.rst

=================
HAProxy Resolver
=================

**STATE**: stable

**COMPATIBILITY**: OPNsense 24.1+

**Note**: Most functions should work on earlier OPNsense versions, but full compatibility is tested with OPNsense 24.1+. For compatibility with earlier versions, please check the configuration differences at: `HAProxy Configuration Reference <https://github.com/opnsense/plugins/blob/master/net/haproxy/src/opnsense/mvc/app/models/OPNsense/HAProxy/HAProxy.xml>`_

**TESTS**: `Playbook <https://github.com/O-X-L/ansible_opnsense/blob/latest/tests/haproxy_resolver.yml>`_


Contribution
************

This module was contributed by **MaximeWewer** (@MaximeWewer).

If you encounter any issues or have suggestions for improvements, please feel free to contribute to the project.


Definition
**********

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "name","string","true","\-","\-","Resolver name"
    "description","string","false","\-","\-","Resolver description"
    "enabled","boolean","false","true","\-","Enable or disable resolver"
    "nameservers","list","false","\-","\-","List of nameservers"
    "parse_resolv_conf","boolean","false","false","\-","Parse /etc/resolv.conf"
    "resolve_retries","integer","false","\-","\-","Number of resolve retries"
    "timeout_resolve","string","false","\-","\-","Resolve timeout (e.g. 5s)"
    "state","string","false","present","\-","State of the resolver (present, absent)"
    "reload","boolean","false","true","\-", .. include:: ../_include/param_reload.rst

.. include:: ../_include/param_basic.rst

Usage
*****

This module manages HAProxy DNS resolvers for dynamic server resolution.

Examples
********

.. code-block:: yaml

    - hosts: localhost
      gather_facts: false
      module_defaults:
        group/ansibleguy.opnsense.all:
          firewall: 'opnsense.template.ansibleguy.net'
          api_credential_file: '/home/guy/.secret/opn.key'

      tasks:
        - name: Create DNS resolver
          ansibleguy.opnsense.haproxy_resolver:
            name: 'internal_dns'
            description: 'Internal DNS resolver'
            enabled: true
            nameservers: ['192.168.1.1:53', '192.168.1.2:53']
            resolve_retries: 3
            timeout_resolve: '5s'