.. _modules_haproxy_maintenance:

.. include:: ../_include/head.rst

======================
HAProxy Maintenance
======================

**STATE**: stable

**COMPATIBILITY**: OPNsense 24.1+

**Note**: Most functions should work on earlier OPNsense versions, but full compatibility is tested with OPNsense 24.1+. For compatibility with earlier versions, please check the configuration differences at: `HAProxy Configuration Reference <https://github.com/opnsense/plugins/blob/master/net/haproxy/src/opnsense/mvc/app/models/OPNsense/HAProxy/HAProxy.xml>`_

**TESTS**: `Playbook <https://github.com/O-X-L/ansible_opnsense/blob/latest/tests/haproxy_maintenance.yml>`_

**API Docs**: `HAProxy <https://docs.opnsense.org/development/api/plugins/haproxy.html>`_

**Service Docs**: `HAProxy <https://docs.opnsense.org/manual/how-tos/haproxy.html>`_


Contribution
************

This module was contributed by **MaximeWewer** (@MaximeWewer).

If you encounter any issues or have suggestions for improvements, please feel free to contribute to the project.


Definition
**********

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "action","string","true","\-","\-","Maintenance action to perform"
    "server","string","false","\-","\-","Server identifier (backend/server format)"
    "state","string","false","\-","\-","Server state for server_state operations (ready, drain, maint)"
    "weight","integer","false","\-","\-","Server weight for server_weight operations (0-256)"

.. include:: ../_include/param_basic.rst

Usage
*****

This module performs various HAProxy maintenance operations on OPNsense. It provides runtime control over server states, weights, and certificate management without requiring configuration reloads.

Available maintenance actions:

- **Server state management**: Control server operational states (ready, drain, maintenance)
- **Weight management**: Dynamically adjust server weights for load balancing
- **Certificate operations**: Manage SSL certificates and synchronization
- **Server discovery**: Search and inspect configured servers
- **Bulk operations**: Perform actions on multiple servers simultaneously

Key features:

- **Runtime operations**: Make changes without HAProxy service restarts
- **Server state control**: Enable maintenance mode or graceful drainage
- **Dynamic weight adjustment**: Balance traffic loads in real-time
- **Certificate management**: Sync and update SSL certificates
- **Bulk operations**: Efficiently manage multiple servers
- **Safe operations**: Non-destructive maintenance commands

Action Types
************

Server State Actions:
- ``server_state``: Change individual server state
- ``server_state_bulk``: Change multiple server states

Weight Management:
- ``server_weight``: Adjust individual server weight
- ``server_weight_bulk``: Adjust multiple server weights

Certificate Management:
- ``cert_sync``: Synchronize certificates
- ``cert_sync_bulk``: Bulk certificate synchronization
- ``cert_actions``: Perform certificate actions
- ``cert_diff``: Check certificate differences
- ``search_certificate_diff``: Search for certificate changes

Information Gathering:
- ``get``: Get maintenance information
- ``search_server``: Search for servers
- ``fetch_cron_integration``: Get cron integration data

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
        - name: Get current maintenance information
          ansibleguy.opnsense.haproxy_maintenance:
            action: get
          register: maintenance_info

        - name: Search for all servers
          ansibleguy.opnsense.haproxy_maintenance:
            action: search_server
          register: all_servers

        - name: Display found servers
          ansible.builtin.debug:
            var: all_servers.result

        - name: Put server into maintenance mode
          ansibleguy.opnsense.haproxy_maintenance:
            action: server_state
            server: "web_backend/web01"
            state: maint

        - name: Drain server gracefully
          ansibleguy.opnsense.haproxy_maintenance:
            action: server_state
            server: "api_backend/api01"
            state: drain

        - name: Bring server back online
          ansibleguy.opnsense.haproxy_maintenance:
            action: server_state
            server: "web_backend/web01"
            state: ready

        - name: Reduce server weight during maintenance window
          ansibleguy.opnsense.haproxy_maintenance:
            action: server_weight
            server: "web_backend/web02"
            weight: 50

        - name: Restore normal server weight
          ansibleguy.opnsense.haproxy_maintenance:
            action: server_weight
            server: "web_backend/web02"
            weight: 100

        - name: Synchronize SSL certificates
          ansibleguy.opnsense.haproxy_maintenance:
            action: cert_sync

        - name: Check for certificate differences
          ansibleguy.opnsense.haproxy_maintenance:
            action: cert_diff
          register: cert_changes

        - name: Rolling maintenance example
          block:
            - name: Get all servers in backend
              ansibleguy.opnsense.haproxy_maintenance:
                action: search_server
              register: servers

            - name: Perform rolling maintenance
              include_tasks: server_maintenance.yml
              loop: "{{ servers.result.servers | default([]) }}"
              loop_control:
                loop_var: server_item
              when: "'web_backend' in server_item"

        - name: Emergency server shutdown
          ansibleguy.opnsense.haproxy_maintenance:
            action: server_state
            server: "{{ emergency_server }}"
            state: maint
          when: emergency_shutdown | default(false)