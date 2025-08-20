.. _modules_haproxy_healthcheck:

.. include:: ../_include/head.rst

====================
HAProxy Health Check
====================

**STATE**: stable

**COMPATIBILITY**: OPNsense 24.1+

**Note**: Most functions should work on earlier OPNsense versions, but full compatibility is tested with OPNsense 24.1+. For compatibility with earlier versions, please check the configuration differences at: `HAProxy Configuration Reference <https://github.com/opnsense/plugins/blob/master/net/haproxy/src/opnsense/mvc/app/models/OPNsense/HAProxy/HAProxy.xml>`_

**TESTS**: `Playbook <https://github.com/O-X-L/ansible_opnsense/blob/latest/tests/haproxy_healthcheck.yml>`_


Contribution
************

This module was contributed by **MaximeWewer** (@MaximeWewer).

If you encounter any issues or have suggestions for improvements, please feel free to contribute to the project.


Definition
**********

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "name","string","true","\-","\-","Health check name"
    "description","string","false","\-","\-","Health check description"
    "enabled","boolean","false","true","\-","Enable or disable health check"
    "type","string","true","\-","\-","Health check type"
    "interval","string","false","\-","\-","Check interval (e.g. 5s, 30s)"
    "ssl","string","false","\-","\-","SSL settings"
    "ssl_sni","string","false","\-","\-","SSL SNI hostname"
    "state","string","false","present","\-","State of the health check (present, absent)"
    "reload","boolean","false","true","\-", .. include:: ../_include/param_reload.rst

.. include:: ../_include/param_basic.rst

Usage
*****

This module manages HAProxy health checks for monitoring server availability.

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
        - name: Create HTTP health check
          ansibleguy.opnsense.haproxy_healthcheck:
            name: 'web_health'
            description: 'Web server health check'
            enabled: true
            type: 'http'
            interval: '5s'