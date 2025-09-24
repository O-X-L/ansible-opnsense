.. _modules_haproxy_auth:

.. include:: ../_include/head.rst

============================
HAProxy authentication modules
============================

**STATE**: unstable

**COMPATIBILITY**: OPNsense 24.1+

**TESTS**:
`User <https://github.com/O-X-L/ansible_opnsense/blob/latest/tests/haproxy_user.yml>`_ |
`Group <https://github.com/O-X-L/ansible_opnsense/blob/latest/tests/haproxy_group.yml>`_

**API Docs**: `HAProxy <https://docs.opnsense.org/development/api/plugins/haproxy.html>`_

These modules manage HAProxy authentication users and groups for access control.

----

.. _haproxy_user:

ansibleguy.opnsense.haproxy_user
=================================

Manages HAProxy authentication users.

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "name","string","true","\-","\-","Name to identify this user"
    "description","string","false","\-","\-","Description for this user"
    "enabled","boolean","false","true","\-","Enable or disable this user"
    "password","string","false","\-","\-","Both encrypted and unencrypted passwords can be used. Most systems support MD5, SHA-256, SHA-512, and, of course, the classic DES-based method of encrypting passwords"

Examples
--------

.. code-block:: yaml

    - name: Create HAProxy admin user
      ansibleguy.opnsense.haproxy_user:
        name: 'admin'
        description: 'Administrator user'
        password: '{{ vault_admin_password }}'
        enabled: true

----

.. _haproxy_group:

ansibleguy.opnsense.haproxy_group
===================================

Manages HAProxy authentication groups.

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "name","string","true","\-","\-","Name to identify this group"
    "description","string","false","\-","\-","Description for this group"
    "enabled","boolean","false","true","\-","Enable or disable this group"
    "members","list","false","[]","\-","Type username or choose from list. List of user names that are members of this group"
    "add_userlist","boolean","false","false","\-","Usually HAproxy userlists are created automatically in a context sensitive way. This option adds this group as userlist"

Examples
--------

.. code-block:: yaml

    - name: Create HAProxy admin group
      ansibleguy.opnsense.haproxy_group:
        name: 'admins'
        description: 'Administrator group'
        members: ['admin', 'operator']
        enabled: true


See also: :ref:`modules_haproxy` and :ref:`troubleshooting <troubleshooting>`