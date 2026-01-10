.. _modules_nut:

.. include:: ../_include/head.rst

=======================
NUT - Network UPS Tools
=======================

**State:** Unstable

**Tests:** `nut.yml <https://github.com/O-X-L/ansible_opnsense/blob/latest/tests/nut.yml>`_

**API Docs**: `Plugins - NUT <https://docs.opnsense.org/development/api/plugins/nut.html>`_

**Service Docs**: `NUT - Network UPS Tools <https://docs.opnsense.org/manual/how-tos/nut.html>`_

Contribution
************

Author: `@wmatusiak <https://github.com/wmatusiak>`_

If you encounter any issues or have suggestions for improvements, please feel free to contribute to the project.

----

Prerequisites
*************

You need to install the NUT plugin:

```
os-nut
```
You can also install it using the :ref:`oxlorg.opnsense.package <modules_package>` module.

----

Functions
*********

This module allows you to configure the Network UPS Tools on your OPNsense firewall.

NUT is a service that monitors UPS device and shutdown your firewall if the battery level is low.

Parameters
##########

.. csv-table:: Definition
   :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
   :widths: 15 10 10 10 10 45

   "enabled","boolean","false","true","\-","Enable/disable NUT service"
   "mode","choice","false","standalone","\-","Service mode. One of: 'standalone','netclient'."
   "name","string","false","UPSName","\-","Name for your UPS."
   "listen","list","false","['127.0.0.1','::1']","\-","Addresses this service listen on."
   "admin_password","string","false","Password","\-","Password for admin user 'admin'."
   "monitor_password","string","false","Password","\-","Password for monitoring user 'monuser'."
   "usbhid_enable","boolean","false","false","\-","Enable the USBHID driver."
   "usbhid_args","list","false","['port=auto']","\-","Extra arguments for USBHID driver, e.g. 'port=auto'."
   "apcsmart_enable","boolean","false","false","\-","Enable the APCSMART driver."
   "apcsmart_args","list","false","['port=auto']","\-","Extra arguments for APCSMART driver, e.g. 'port=auto'."
   "apcupsd_enable","boolean","false","false","\-","Enable the APCUPSD controlled devices driver."
   "apcupsd_host","string","false","localhost","\-","Hostname or ip of the remote apcupsd server."
   "apcupsd_port","int","false","\-","\-","Port of the remote apcupsd server (optional)."
   "bcmxcpusb_enable","boolean","false","false","\-","Enable the PowerWare BCMXCPUSB driver."
   "bcmxcpusb_args","list","false","['port=auto']","\-","Extra arguments for WoerWare BCMXCPUSB driver, e.g. 'port=auto'."
   "blazerusb_enable","boolean","false","false","\-","Enable the BlazerUSB driver."
   "blazerusb_args","list","false","['port=auto']","\-","Extra arguments for BlazerUSB driver, e.g. 'port=auto'."
   "blazerser_enable","boolean","false","false","\-","Enable the BlazerSerial driver. Please be aware that this driver needs to run nut-tools as root."
   "blazerser_args","list","false","['port=auto']","\-","Extra arguments for BlazerSerial driver, e.g. 'port=auto'."
   "netclient_enable","boolean","false","false","\-","Enable the Netclient driver"
   "netclient_address","string","false","\-","\-","IP address of the remote NUT server."
   "netclient_port","int","false","3493","\-","TCP port of the remote NUT server."
   "netclient_user","string","false","\-","\-","Usernname of the remote NUT server."
   "netclient_password","string","false","\-","\-","Password of the remote NUT server."
   "qx_enable","boolean","false","false","\-","Enable the OX driver."
   "qx_args","list","false","['port=auto']","\-","Extra arguments for QX driver, e.g. 'port=auto'."
   "riello_enable","boolean","false","false","\-","Enable the Riello driver."
   "riello_args","list","false","['port=auto']","\-","Extra arguments for Riello driver, e.g. 'port=auto'."
   "snmp_enable","boolean","false","false","\-","Enable the SNMP driver."
   "snmp_args","list","false","['community=public']","\-","Extra arguments for SNMP driver, e.g. 'community=public'."

.. include:: ../_include/param_basic.rst

.. include:: ../_include/param_reload.rst

----

Usages
******

This module configures all NUT service settings.

After configuration changes, the service will be reloaded automatically.

----

Examples
********

.. code-block:: yaml

   - hosts: firewalls
     connection: local
     gather_facts: false
     module_defaults:
        group/oxlorg.opnsense.all:
            firewall: 'opnsense.template.oxlorg.net'
            api_credential_file: '/home/guy/.secret/opn.key'
        oxlorg.opnsense.nut:
            # repalce defaults password 'Password' with something random
            admin_password: some random password here
            monitor_password: some random password here

    tasks:
        - name: Configure NUT service with USBHID driver
          oxlorg.opnsense.nut:
            enabled: True
            mode: standalone
            usbhid_enable: True

        - name: Configure NUT service with SNMP driver
          oxlorg.opnsense.nut:
            enabled: True
            mode: standalone
            snmp_enable: True
            snmp_args:
              - community=public
              - port=192.168.1.200
              - snmp_version=v2c

        - name: Configure NUT service in Netclient mode
          oxlorg.opnsense.nut:
            enabled: Ture
            mode: netclient
            netclient_enable: True
            netclient_address: 192.168.1.100
            netclient_user: remotemon
            netclient_password: password for remotemon user on 192.168.1.100 NUT server

----

Troubleshooting
***************

Check Service -> Nut -> Diagnostics view to check UPS status.

You can use :ref:`oxlorg.opnsense.nut_diagnostics <modules_nut>` to acces status from ansible.
