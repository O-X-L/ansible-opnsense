.. _modules_haproxy_group:

.. include:: ../_include/head.rst

=============
HAProxy Group
=============

**STATE**: stable

**COMPATIBILITY**: OPNsense 24.1+

**Note**: Most functions should work on earlier OPNsense versions, but full compatibility is tested with OPNsense 24.1+. For compatibility with earlier versions, please check the configuration differences at: `HAProxy Configuration Reference <https://github.com/opnsense/plugins/blob/master/net/haproxy/src/opnsense/mvc/app/models/OPNsense/HAProxy/HAProxy.xml>`_

**TESTS**: `Playbook <https://github.com/O-X-L/ansible_opnsense/blob/latest/tests/haproxy_group.yml>`_


Contribution
************

This module was contributed by **MaximeWewer** (@MaximeWewer).

If you encounter any issues or have suggestions for improvements, please feel free to contribute to the project.


Definition
**********

.. include:: ../_include/param_basic.rst

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "name","string","true","\-","\-","Group name (unique identifier)"
    "description","string","false","\-","\-","Group description"
    "enabled","boolean","false","true","\-","Enable or disable group"
    "members","list","false","\-","\-","**NEW**: List of user names as group members - supports automatic UUID resolution"
    "add_userlist","boolean","false","false","\-","Add to userlist for authentication purposes"

Usage
*****

This module manages HAProxy user groups on OPNsense for authentication and authorization purposes. Groups organize users into logical collections that can be referenced in ACLs and authentication rules.

Key features:

- **Automatic UUID Resolution**: All relationship fields accept names and automatically resolve to UUIDs
- **Name-based Linking**: Users can specify user names instead of UUIDs for group membership
- **UI Compatibility**: All selections appear correctly in the OPNsense web interface
- **Multi-select Support**: Lists support multiple users with proper comma-separated format
- **Authentication integration**: Groups can be used in HTTP authentication ACLs
- **Userlist management**: Control whether groups appear in HAProxy userlists

Examples
********

.. code-block:: yaml

    - hosts: localhost
      gather_facts: false
      module_defaults:
        group/ansibleguy.opnsense.all:
          firewall: 'opnsense.template.ansibleguy.net'
          api_credential_file: '/home/guy/.secret/opn.key'

        ansibleguy.opnsense.list:
          target: 'haproxy_group'

      tasks:
        - name: Create admin group with name-based user linking
          ansibleguy.opnsense.haproxy_group:
            name: 'administrators'
            description: 'System administrators group'
            enabled: true
            members: ['admin', 'root', 'sysadmin']  # Uses user names, not UUIDs
            add_userlist: true

        - name: Create development team group
          ansibleguy.opnsense.haproxy_group:
            name: 'developers'
            description: 'Development team members'
            enabled: true
            members: ['alice', 'bob', 'charlie', 'diana']
            add_userlist: true

        - name: Create security team group
          ansibleguy.opnsense.haproxy_group:
            name: 'security_team'
            description: 'Security and compliance team'
            enabled: true
            members: ['security_admin', 'auditor']
            add_userlist: true

        - name: Create read-only group
          ansibleguy.opnsense.haproxy_group:
            name: 'readonly_users'
            description: 'Users with read-only access'
            enabled: true
            members: ['viewer1', 'viewer2', 'guest']
            add_userlist: false  # Not added to userlist for auth

        - name: Create empty group for future use
          ansibleguy.opnsense.haproxy_group:
            name: 'future_group'
            description: 'Group reserved for future users'
            enabled: false
            members: []

        - name: Update existing group membership
          ansibleguy.opnsense.haproxy_group:
            name: 'administrators'
            members: ['admin', 'root', 'sysadmin', 'new_admin']  # Add new member

        - name: Disable group temporarily
          ansibleguy.opnsense.haproxy_group:
            name: 'maintenance_group'
            enabled: false

        - name: Remove old group
          ansibleguy.opnsense.haproxy_group:
            name: 'deprecated_group'
            state: absent

        - name: List all groups
          ansibleguy.opnsense.list:
          register: haproxy_groups

        - name: Show groups
          ansible.builtin.debug:
            var: haproxy_groups.data