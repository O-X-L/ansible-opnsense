.. _modules_access:

.. include:: ../_include/head.rst

========================
Access / User Management
========================

**STATE**: unstable

**TESTS**: `user <https://github.com/O-X-L/ansible_opnsense/blob/latest/tests/user.yml>`_ |
`group <https://github.com/ansibleguy/collection_opnsense/blob/latest/tests/group.yml>`_ |
`privilege <https://github.com/ansibleguy/collection_opnsense/blob/latest/tests/privilege.yml>`_

**API Docs**: `Core - Auth <https://docs.opnsense.org/development/api/core/auth.html>`_

**Service Docs**: `Access / User Management <https://docs.opnsense.org/manual/users.html>`_


Contribution
************

Thanks to `@jiuka <https://github.com/jiuka>`_ for developing this module!

----

.. warning::

    This feature is only compatible with OPNSense version >= 25.7

Definition
**********

ansibleguy.opnsense.user
===================================
..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "name","string","true","\-","n","User name"
    "expires","string","false","\-","\-","Expiration date"
    "authorized_keys","string","false","\-","\-","SSH authorized keys"
    "shell","string","false","none for all but root","sh","Login shell. One of: '/bin/csh', '/bin/sh', '/bin/tcsh'"
    "password","string","false","\-","\-","Password for the user."
    "update_password","string","false","always","\-","Update the password 'always' or only 'on_create'. One of: 'always', 'on_create'"
    "scrambled_password","boolean","false","false","\-","Generate a scrambled password to prevent local database logins for this user"
    "landing_page","string","false","\-","\-","Preferred landing page after login or authentication failure"
    "comment","string","false","\-","\-","User comment, for your own information only"
    "email","string","false","\-","\-","Users e-mail address, for your own information only"
    "language","string","false","\-","\-","Language for the user. Example: de_DE, en_US"
    "description","string","false","\-","desc, full_name","Full name of the user"
    "membership","list","false","\-","group, m, g","List of group memberships."
    "privilege","list","false","\-","priv, p","List of granted privileges."

ansibleguy.opnsense.group
=========================
..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "name","string","true","\-","n","Group name"
    "description","string","false","\-","desc","Group description for your reference"
    "member","list","false","\-","m","List of group members."
    "privilege","list","false","\-","priv, p","List of granted privileges."
    "source_net","list","false"."\-","source, src, s","List of networks which constraint the membership of this group to their location."


ansibleguy.opnsense.privilege
=============================
..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "id","string","true","\-","privilege, priv, p","Privilege ID"
    "user","list","false","\-","u","Users to manage privileges of"
    "group","list","false","\-","g","Groups to manage privileges of"
    "state","string","false","present","\-","State of the privilege. 'present' grants the privilege to this users and groups, 'absent' revokes it and 'pure' ensures only this users and groups have this privilege. One of: 'present', 'absent', 'pure'"

.. include:: ../_include/param_basic.rst

Usage
*****

This module is used to manage users and groups, assign users to groups and grant/revoke privileges.

 * The ``membership``/``member`` and ``privilege`` parameters on the ``user`` and ``group`` module are only checked/updated if the parameter is present.


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
        - name: Example User
          ansibleguy.opnsense.user:
            name: alice
            # expires:
            # authorized_keys: |
            #   ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIArgYhpejdvJADM3ZWSx7KSA0eBxJ6Y43kWIA5mX95jg alice@host1
            #   ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIDxTK7kBm3sAQMh2T4ZJdXYCBDYdDVwXMwPvSeFdgZko alice@host2
            # shell: /bin/sh
            # password:
            # update_password: always
            # scrambled_password: true
            # landing_page:
            # comment:
            # email:
            # language:
            # description:
            # membership:
            # privilege:
            # state: 'absent'
            # debug: false

        - name: Example Group
          ansibleguy.opnsense.group:
            name: aliceandbob
            # description:
            # member:
            # privilege:
            # state: 'absent'
            # source_net:
            # debug: false

        - name: Example Privilege
          ansibleguy.opnsense.group:
            id: user-config-readonly
            user: alice
            group: aliceandbob
            # state: 'absent'
            # debug: false

        - name: Adding Monitoring User
          ansibleguy.opnsense.user:
            name: alice
            update_password: on_create
            scrambled_password: true
            membership: []
            privilege:
              - user-config-readonly
              - page-status-carp

        - name: Ensure only admins have all privileges
          ansibleguy.opnsense.privilege:
            id: page-all
            user: []
            group: admin
            state: pure

        - name: Listing users
          ansibleguy.opnsense.list:
            target: 'user'
          register: existing_users

        - name: Printing users
          ansible.builtin.debug:
            var: existing_users.data
