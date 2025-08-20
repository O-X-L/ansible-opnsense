.. _modules_haproxy_user:

.. include:: ../_include/head.rst

=============
HAProxy User
=============

**STATE**: stable

**COMPATIBILITY**: OPNsense 24.1+

**Note**: Most functions should work on earlier OPNsense versions, but full compatibility is tested with OPNsense 24.1+. For compatibility with earlier versions, please check the configuration differences at: `HAProxy Configuration Reference <https://github.com/opnsense/plugins/blob/master/net/haproxy/src/opnsense/mvc/app/models/OPNsense/HAProxy/HAProxy.xml>`_

**TESTS**: `Playbook <https://github.com/O-X-L/ansible_opnsense/blob/latest/tests/haproxy_user.yml>`_

**API Docs**: `HAProxy <https://docs.opnsense.org/development/api/plugins/haproxy.html>`_

**Service Docs**: `HAProxy <https://docs.opnsense.org/manual/how-tos/haproxy.html>`_


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

    "name","string","true","\-","\-","User name (unique identifier)"
    "description","string","false","\-","\-","User description"
    "enabled","boolean","false","true","\-","Enable or disable user"
    "password","string","true","\-","\-","User password for authentication"

Usage
*****

This module manages HAProxy users on OPNsense for authentication and authorization purposes. Users are used in conjunction with groups and ACLs to control access to HAProxy services.

Key features:

- **User authentication**: Create users for HTTP authentication in HAProxy
- **Group integration**: Users can be assigned to groups for organized access control
- **Password management**: Secure password configuration for user authentication
- **ACL compatibility**: Users work seamlessly with HAProxy ACLs for access control
- **UI integration**: Users appear correctly in the OPNsense web interface
- **Userlist management**: Users are automatically added to HAProxy userlists when needed

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
          target: 'haproxy_user'

      tasks:
        - name: Create admin user
          ansibleguy.opnsense.haproxy_user:
            name: 'admin'
            description: 'Administrator user'
            enabled: true
            password: 'secure_password_123'

        - name: Create operator user
          ansibleguy.opnsense.haproxy_user:
            name: 'operator'
            description: 'System operator'
            enabled: true
            password: 'operator_secure_pass'

        - name: Create readonly user
          ansibleguy.opnsense.haproxy_user:
            name: 'readonly'
            description: 'Read-only user'
            enabled: true
            password: 'readonly_pass'

        - name: Create API user
          ansibleguy.opnsense.haproxy_user:
            name: 'api_user'
            description: 'User for API access'
            enabled: true
            password: 'api_strong_password'

        - name: Create security auditor
          ansibleguy.opnsense.haproxy_user:
            name: 'security_admin'
            description: 'Security team member'
            enabled: true
            password: 'security_complex_pass'

        - name: Create development team users
          ansibleguy.opnsense.haproxy_user:
            name: "{{ item.name }}"
            description: "{{ item.desc }}"
            enabled: true
            password: "{{ item.password }}"
          loop:
            - { name: 'alice', desc: 'Developer Alice', password: 'alice_dev_pass' }
            - { name: 'bob', desc: 'Developer Bob', password: 'bob_dev_pass' }
            - { name: 'charlie', desc: 'Developer Charlie', password: 'charlie_dev_pass' }

        - name: Create guest user (disabled by default)
          ansibleguy.opnsense.haproxy_user:
            name: 'guest'
            description: 'Guest user for temporary access'
            enabled: false
            password: 'guest_temp_pass'

        - name: Update user password
          ansibleguy.opnsense.haproxy_user:
            name: 'admin'
            password: 'new_secure_password_456'

        - name: Disable user temporarily
          ansibleguy.opnsense.haproxy_user:
            name: 'readonly'
            enabled: false

        - name: Remove old user
          ansibleguy.opnsense.haproxy_user:
            name: 'deprecated_user'
            state: absent

        - name: List all users
          ansibleguy.opnsense.list:
          register: haproxy_users

        - name: Show users
          ansible.builtin.debug:
            var: haproxy_users.data