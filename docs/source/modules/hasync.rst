.. _modules_hasync:

.. include:: ../_include/head.rst

=================
High Availability
=================

**STATE**: unstable

**TESTS**: `ansibleguy.opnsense.hasync_general <https://github.com/ansibleguy/collection_opnsense/blob/latest/tests/hasync_general.yml>`_ |
`ansibleguy.opnsense.hasync_service <https://github.com/ansibleguy/collection_opnsense/blob/latest/tests/hasync_service.yml>`_

**API Docs**: `Core - HASync <https://docs.opnsense.org/development/api/core/core.html>`_

**Service Docs**: `High Availability <https://docs.opnsense.org/manual/hacarp.html>`_

.. warning::

    This feature is only available in OPNSense version >= 25.1

Definition
**********

.. include:: ../_include/param_basic.rst

ansibleguy.opnsense.hasync_general
===================================

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "preempt","boolean","false","true","\-","When this device is configured as CARP master it will try to switch to master when powering up, this option will keep this one slave if there already is a master on the network."
    "disconnect_ppps","boolean","false","true","\-","When this device is configured as CARP backup it will disconnect all PPP type interfaces and try to reconnect them when becoming master again."
    "pfsync_interface","string","false","\-","'interface', 'i', 'int'","Enable state insertion, update, and deletion messages between firewalls by utilizing the selected interface for communication. Best choose a dedicated interface for this type of communication to prevent manipulation of states causing security issues."
    "pfsync_peer_ip","string","false","\-","'peer'","Force pfsync to synchronize its state table to this IP address."
    "pfsync_version","string","false","1400","\-","Newer versions of OPNsense offer additional attributes in the state synchronization, for compatibility reasons you can optionally choose an older version here. Always make sure both nodes use the same version to avoid inconsistent state tables."
    "synchronize_to_ip","string","false","\-","\-","IP address of the firewall to which the selected configuration sections should be synchronized. This should be empty on the backup machine. When an IP address is offered, both web GUI configurations should be equal (port and protocol)."
    "verify_peer","boolean","false","false","\-","In most cases the target host will be a directly attached neighbor in which case TLS verification can be ignored."
    "username","string","false","\-","\-","Web GUI username of the system entered for synchronizing your configuration."
    "password","string","false","\-","\-","Web GUI password of the system entered for synchronizing your configuration."
    "update_password","string","false","always","\-","Update the password `always` or only `on_create`."
    "syncitems","list of string","false","\-","\-","Services that should be send to the other host."
    "reload","boolean","false","true","\-", .. include:: ../_include/param_reload.rst

ansibleguy.opnsense.hasync_service
===================================

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "name","string","false","all","service, target, svc, n","Pretty name of the service to interact with, or 'all'"
    "action","string","false","restart","do, a","What action to execute. Some services may not support all of these actions (*the module will inform you in that case*). One of: 'start', 'restart', 'stop'"
    "ignore_version_mismatch","boolean","false","false","\-","Ignore or fail on version mismatch."

Usage
*****

Use the :code:`ansibleguy.opnsense.hasync_general` module to configure the synchronisation of states and configuration.
If configuration synchronization is set up the :code:`ansibleguy.opnsense.hasync_service` module can be used to trigger the sync and restart of a specific or all services.


Examples
********

ansibleguy.opnsense.hasync_general
==================================

.. code-block:: yaml

    - hosts: localhost
      gather_facts: false
      module_defaults:
        group/ansibleguy.opnsense.all:
          firewall: 'opnsense.template.ansibleguy.net'
          api_credential_file: '/home/guy/.secret/opn.key'

        ansibleguy.opnsense.list:
          target: 'hasync_general'

      tasks:
        # add optional parameters commented-out
        # required ones normally
        # add their default values to get a brief overview of how the module works
        - name: Example
          ansibleguy.opnsense.hasync_general:
            # preempt: false
            # disconnect_ppps: false
            # pfsync_interface: 
            # pfsync_peer_ip:
            # pfsync_version: 1400
            # synchronize_to_ip:
            # verify_peer: false
            # username:
            # password:
            # update_password: always
            # syncitems:
            # debug: false

        - name: Setup pfsync
          ansibleguy.opnsense.hasync_general:
            preempt: false
            disconnect_ppps: false
            pfsync_interface: pfSync
            pfsync_peer_ip: 224.0.0.240
            pfsync_version: 1400

        - name: Setup Config Sync
          ansibleguy.opnsense.hasync_general:
            synchronize_to_ip: 192.168.1.2
            username: opnsync
            password: secret
            syncitems:
              - aliases
              - rules

        - name: Listing config
          ansibleguy.opnsense.list:
          #  target: 'hasync_general'
          register: hasync_config

        - name: Printing
          ansible.builtin.debug:
            var: hasync_config.data

ansibleguy.opnsense.hasync_service
==================================

.. code-block:: yaml

    - hosts: localhost
      gather_facts: false
      module_defaults:
        group/ansibleguy.opnsense.all:
          firewall: 'opnsense.template.ansibleguy.net'
          api_credential_file: '/home/guy/.secret/opn.key'


      tasks:
        - name: Synchronize and restart cron
          ansibleguy.opnsense.hasync_service:
            name: cron
            action: restart

        - name: Synchronize and restart all services
          ansibleguy.opnsense.hasync_service:
            #name: all
            action: restart

        - name: Stop ntpd
          ansibleguy.opnsense.hasync_service:
            name: ntpd
            action: stop

        - name: Start ntpd
          ansibleguy.opnsense.hasync_service:
            name: ntpd
            action: start
