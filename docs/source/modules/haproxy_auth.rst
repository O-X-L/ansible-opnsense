.. _modules_haproxy_auth:

.. include:: ../_include/head.rst

========================================
HAProxy authentication & access control
========================================

**STATE**: unstable

**COMPATIBILITY**: OPNsense 24.1+

**TESTS**: 
`User <https://github.com/O-X-L/ansible_opnsense/blob/latest/tests/haproxy_user.yml>`_ |
`Group <https://github.com/O-X-L/ansible_opnsense/blob/latest/tests/haproxy_group.yml>`_ |

**API Docs**: `HAProxy <https://docs.opnsense.org/development/api/plugins/haproxy.html>`_

These modules manage HAProxy authentication users and groups for access control.

----

.. _haproxy_user:

ansibleguy.opnsense.haproxy_user
=================================

Manages HAProxy authentication users for access control.

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "name","string","true","\-","\-","Choose a name for this user (must be unique)"
    "description","string","false","\-","\-","You may enter a description here for your reference"
    "password","string","true","\-","\-","Password for this user (stored securely)"
    "enabled","boolean","false","true","\-","Enable this user"

Examples
--------

.. code-block:: yaml

    - name: Create HAProxy user
      ansibleguy.opnsense.haproxy_user:
        name: 'web_admin'
        description: 'Web administration user'
        password: 'secure_password123'
        enabled: true

    - name: Create multiple HAProxy users
      ansibleguy.opnsense.haproxy_user:
        name: "{{ item.name }}"
        description: "{{ item.description }}"
        password: "{{ item.password }}"
        enabled: true
      loop:
        - {name: 'admin', description: 'Administrator', password: '{{ vault_admin_pass }}'}
        - {name: 'monitor', description: 'Monitor user', password: '{{ vault_monitor_pass }}'}
        - {name: 'developer', description: 'Developer access', password: '{{ vault_dev_pass }}'}

    - name: Disable a user
      ansibleguy.opnsense.haproxy_user:
        name: 'old_user'
        password: 'dummy'
        enabled: false

----

.. _haproxy_group:

ansibleguy.opnsense.haproxy_group
==================================

Manages HAProxy authentication groups for organizing users.

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "name","string","true","\-","\-","Choose a name for this group (must be unique)"
    "description","string","false","\-","\-","You may enter a description here for your reference"
    "members","list","false","[]","\-","List of user names that are members of this group"
    "add_userlist","boolean","false","false","\-","Add this group to the userlist"
    "enabled","boolean","false","true","\-","Enable this group"

Examples
--------

.. code-block:: yaml

    - name: Create HAProxy group
      ansibleguy.opnsense.haproxy_group:
        name: 'administrators'
        description: 'Admin group for HAProxy'
        members: ['admin_user1', 'admin_user2']
        add_userlist: true
        enabled: true

    - name: Create multiple groups with members
      ansibleguy.opnsense.haproxy_group:
        name: "{{ item.name }}"
        description: "{{ item.description }}"
        members: "{{ item.members }}"
        add_userlist: true
        enabled: true
      loop:
        - {name: 'admins', description: 'Administrators', members: ['admin']}
        - {name: 'monitors', description: 'Monitoring users', members: ['monitor', 'nagios']}
        - {name: 'developers', description: 'Development team', members: ['dev1', 'dev2', 'dev3']}

    - name: Create empty group (members to be added later)
      ansibleguy.opnsense.haproxy_group:
        name: 'future_users'
        description: 'Group for future users'
        enabled: true

----

Usage scenarios
***************

Basic authentication setup
---------------------------

Set up basic authentication for HAProxy services:

.. code-block:: yaml

    - name: Setup HAProxy authentication
      hosts: opnsense
      tasks:
        - name: Create admin user
          ansibleguy.opnsense.haproxy_user:
            name: 'admin'
            description: 'Main administrator'
            password: '{{ admin_password }}'
            enabled: true

        - name: Create monitoring user
          ansibleguy.opnsense.haproxy_user:
            name: 'monitoring'
            description: 'Monitoring service account'
            password: '{{ monitoring_password }}'
            enabled: true

        - name: Create admin group
          ansibleguy.opnsense.haproxy_group:
            name: 'administrators'
            description: 'Administrative access'
            members: ['admin']
            add_userlist: true
            enabled: true

Multi-tenant authentication
----------------------------

Configure authentication for multiple tenants:

.. code-block:: yaml

    - name: Configure multi-tenant authentication
      hosts: opnsense
      vars:
        tenants:
          - name: 'tenant_a'
            users: ['user_a1', 'user_a2']
            password_prefix: 'tenantA_'
          - name: 'tenant_b'
            users: ['user_b1', 'user_b2', 'user_b3']
            password_prefix: 'tenantB_'
      tasks:
        - name: Create users for each tenant
          ansibleguy.opnsense.haproxy_user:
            name: "{{ item.1 }}"
            description: "User for {{ item.0.name }}"
            password: "{{ item.0.password_prefix }}{{ item.1 }}"
            enabled: true
          loop: "{{ tenants | subelements('users') }}"

        - name: Create groups for each tenant
          ansibleguy.opnsense.haproxy_group:
            name: "{{ item.name }}_group"
            description: "Group for {{ item.name }}"
            members: "{{ item.users }}"
            add_userlist: true
            enabled: true
          loop: "{{ tenants }}"

----

Best practices
**************

Password management
-------------------

- Always use Ansible Vault for storing passwords
- Use strong, unique passwords for each user
- Rotate passwords regularly
- Never commit plain text passwords to version control

.. code-block:: yaml

    # Create encrypted variables file
    # ansible-vault create vars/haproxy_passwords.yml

    # In your playbook
    - name: Configure HAProxy users with vault
      hosts: opnsense
      vars_files:
        - vars/haproxy_passwords.yml
      tasks:
        - name: Create users with vault passwords
          ansibleguy.opnsense.haproxy_user:
            name: "{{ item.name }}"
            password: "{{ item.password }}"
            enabled: true
          loop: "{{ haproxy_users }}"

Group organization
------------------

- Use descriptive group names
- Organize users by role or access level
- Keep groups focused and single-purpose
- Document group purposes in descriptions

User lifecycle management
-------------------------

.. code-block:: yaml

    - name: User lifecycle management
      hosts: opnsense
      tasks:
        # Onboarding new user
        - name: Create new user
          ansibleguy.opnsense.haproxy_user:
            name: 'new_employee'
            description: 'Created on {{ ansible_date_time.date }}'
            password: '{{ temp_password }}'
            enabled: true

        - name: Add to appropriate groups
          ansibleguy.opnsense.haproxy_group:
            name: 'employees'
            members: ['new_employee', 'existing_user1', 'existing_user2']
            enabled: true

        # Offboarding user
        - name: Disable departing user
          ansibleguy.opnsense.haproxy_user:
            name: 'departing_user'
            password: 'disabled'
            enabled: false

        - name: Remove from groups
          ansibleguy.opnsense.haproxy_group:
            name: 'employees'
            members: ['existing_user1', 'existing_user2']  # departing_user removed
            enabled: true

----

Integration with stats module
*****************************

The authentication users and groups can be used with the HAProxy stats module for access control:

.. code-block:: yaml

    - name: Setup authentication and stats integration
      hosts: opnsense
      tasks:
        # Create users and groups first
        - name: Create stats users
          ansibleguy.opnsense.haproxy_user:
            name: "{{ item }}"
            password: "{{ lookup('password', '/dev/null length=20') }}"
            enabled: true
          loop:
            - 'stats_admin'
            - 'stats_viewer'

        - name: Create stats groups
          ansibleguy.opnsense.haproxy_group:
            name: 'stats_access'
            members: ['stats_admin', 'stats_viewer']
            enabled: true

        # Configure stats with authentication
        - name: Configure HAProxy stats with auth
          ansibleguy.opnsense.haproxy_general_stats:
            enabled: true
            auth_enabled: true
            allowed_users: ['stats_admin', 'stats_viewer']  # Names resolved to UUIDs
            allowed_groups: ['stats_access']  # Names resolved to UUIDs

----

Troubleshooting
***************

Common issues
-------------

**User not found**

If you get "User not found" errors when referencing users in other modules:

- Verify the user exists and is enabled
- Check for typos in the username (case-sensitive)
- Ensure the user was created before being referenced

**Group membership**

- Members must exist before being added to groups
- Member names are case-sensitive
- Empty groups are allowed

**Password issues**

- Passwords cannot be empty
- Special characters may need escaping in YAML
- Use quotes around passwords with special characters

Validation
----------

.. code-block:: yaml

    - name: Validate authentication setup
      hosts: opnsense
      tasks:
        - name: List all users (for validation)
          ansibleguy.opnsense.haproxy_user:
            name: 'dummy'
            state: 'list'
          register: users_list

        - name: Display users
          debug:
            var: users_list

        - name: List all groups
          ansibleguy.opnsense.haproxy_group:
            name: 'dummy'
            state: 'list'
          register: groups_list

        - name: Display groups
          debug:
            var: groups_list

See also: :ref:`troubleshooting <troubleshooting>`