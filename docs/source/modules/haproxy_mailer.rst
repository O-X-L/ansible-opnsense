.. _modules_haproxy_mailer:

.. include:: ../_include/head.rst

==============
HAProxy Mailer
==============

**STATE**: stable

**COMPATIBILITY**: OPNsense 24.1+

**Note**: Most functions should work on earlier OPNsense versions, but full compatibility is tested with OPNsense 24.1+. For compatibility with earlier versions, please check the configuration differences at: `HAProxy Configuration Reference <https://github.com/opnsense/plugins/blob/master/net/haproxy/src/opnsense/mvc/app/models/OPNsense/HAProxy/HAProxy.xml>`_

**TESTS**: `Playbook <https://github.com/O-X-L/ansible_opnsense/blob/latest/tests/haproxy_mailer.yml>`_


Contribution
************

This module was contributed by **MaximeWewer** (@MaximeWewer).

If you encounter any issues or have suggestions for improvements, please feel free to contribute to the project.


Definition
**********

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "name","string","true","\-","\-","Mailer name"
    "description","string","false","\-","\-","Mailer description"
    "enabled","boolean","false","true","\-","Enable or disable mailer"
    "mailservers","list","true","\-","\-","List of mail servers"
    "sender","string","true","\-","\-","Sender email address"
    "recipient","string","true","\-","\-","Recipient email address"
    "state","string","false","present","\-","State of the mailer (present, absent)"
    "reload","boolean","false","true","\-", .. include:: ../_include/param_reload.rst

.. include:: ../_include/param_basic.rst

Usage
*****

This module manages HAProxy mailer configurations for email notifications.

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
        - name: Create mailer configuration
          ansibleguy.opnsense.haproxy_mailer:
            name: 'alerts'
            description: 'Alert mailer'
            enabled: true
            mailservers: ['smtp.example.com:587']
            sender: 'haproxy@example.com'
            recipient: 'admin@example.com'