.. _modules_haproxy_mapfile:

.. include:: ../_include/head.rst

================
HAProxy Map File
================

**STATE**: stable

**COMPATIBILITY**: OPNsense 24.1+

**Note**: Most functions should work on earlier OPNsense versions, but full compatibility is tested with OPNsense 24.1+. For compatibility with earlier versions, please check the configuration differences at: `HAProxy Configuration Reference <https://github.com/opnsense/plugins/blob/master/net/haproxy/src/opnsense/mvc/app/models/OPNsense/HAProxy/HAProxy.xml>`_

**TESTS**: `Playbook <https://github.com/O-X-L/ansible_opnsense/blob/latest/tests/haproxy_mapfile.yml>`_


Contribution
************

This module was contributed by **MaximeWewer** (@MaximeWewer).

If you encounter any issues or have suggestions for improvements, please feel free to contribute to the project.


Definition
**********

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "name","string","true","\-","\-","Map file name"
    "description","string","false","\-","\-","Map file description"
    "enabled","boolean","false","true","\-","Enable or disable map file"
    "content","string","true","\-","\-","Map file content"
    "state","string","false","present","\-","State of the map file (present, absent)"
    "reload","boolean","false","true","\-", .. include:: ../_include/param_reload.rst

.. include:: ../_include/param_basic.rst

Usage
*****

This module manages HAProxy map files for dynamic URL rewriting and routing.

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
        - name: Create URL rewrite map
          ansibleguy.opnsense.haproxy_mapfile:
            name: 'url_rewrites'
            description: 'URL rewrite mappings'
            enabled: true
            content: |
              /old-path /new-path
              /legacy /modern
              /api/v1 /api/v2