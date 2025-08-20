.. _modules_haproxy_statistics:

.. include:: ../_include/head.rst

=====================
HAProxy Statistics
=====================

**STATE**: stable

**COMPATIBILITY**: OPNsense 24.1+

**Note**: Most functions should work on earlier OPNsense versions, but full compatibility is tested with OPNsense 24.1+. For compatibility with earlier versions, please check the configuration differences at: `HAProxy Configuration Reference <https://github.com/opnsense/plugins/blob/master/net/haproxy/src/opnsense/mvc/app/models/OPNsense/HAProxy/HAProxy.xml>`_

**TESTS**: `Playbook <https://github.com/O-X-L/ansible_opnsense/blob/latest/tests/haproxy_statistics.yml>`_

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

    "stat_type","string","true","\-","\-","Type of statistics to retrieve (counters, info, tables)"
    "table_name","string","false","\-","\-","Specific table name when stat_type is 'tables'"

.. include:: ../_include/param_basic.rst

Usage
*****

This module retrieves real-time HAProxy statistics from OPNsense. It provides access to different types of operational data for monitoring and troubleshooting purposes.

Available statistics types:

- **counters**: Connection counters, session statistics, and performance metrics
- **info**: General HAProxy information including version, uptime, and global status
- **tables**: Stick tables and other HAProxy internal data structures

Key features:

- **Real-time monitoring**: Get current HAProxy operational statistics
- **Performance metrics**: Access connection counts, session data, and throughput information
- **Health monitoring**: Check service status and uptime information
- **Table inspection**: Examine HAProxy internal state and stick tables
- **Read-only operations**: Safe monitoring without configuration changes

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
        - name: Get HAProxy connection counters
          ansibleguy.opnsense.haproxy_statistics:
            stat_type: counters
          register: haproxy_counters

        - name: Display connection statistics
          ansible.builtin.debug:
            msg: |
              Total connections: {{ haproxy_counters.statistics.total_connections | default('N/A') }}
              Active sessions: {{ haproxy_counters.statistics.active_sessions | default('N/A') }}
              Current queue: {{ haproxy_counters.statistics.current_queue | default('N/A') }}

        - name: Get HAProxy system information
          ansibleguy.opnsense.haproxy_statistics:
            stat_type: info
          register: haproxy_info

        - name: Display HAProxy info
          ansible.builtin.debug:
            msg: |
              HAProxy version: {{ haproxy_info.statistics.version | default('Unknown') }}
              Uptime: {{ haproxy_info.statistics.uptime | default('Unknown') }}
              Process ID: {{ haproxy_info.statistics.pid | default('Unknown') }}
              Max connections: {{ haproxy_info.statistics.max_connections | default('Unknown') }}

        - name: Get HAProxy tables data
          ansibleguy.opnsense.haproxy_statistics:
            stat_type: tables
          register: haproxy_tables

        - name: Display available tables
          ansible.builtin.debug:
            var: haproxy_tables.statistics

        - name: Get specific table information
          ansibleguy.opnsense.haproxy_statistics:
            stat_type: tables
            table_name: "backend_sessions"
          register: backend_table
          when: haproxy_tables.statistics.tables is defined

        - name: Monitor HAProxy health
          ansibleguy.opnsense.haproxy_statistics:
            stat_type: info
          register: health_check
          failed_when: health_check.statistics.status is defined and health_check.statistics.status != 'running'

        - name: Collect performance metrics
          block:
            - name: Get counters
              ansibleguy.opnsense.haproxy_statistics:
                stat_type: counters
              register: metrics

            - name: Alert on high connection count
              ansible.builtin.debug:
                msg: "WARNING: High connection count detected"
              when: 
                - metrics.statistics.total_connections is defined
                - metrics.statistics.total_connections | int > 10000

        - name: Generate monitoring report
          ansible.builtin.template:
            src: haproxy_report.j2
            dest: /tmp/haproxy_status.html
          vars:
            counters: "{{ haproxy_counters.statistics }}"
            info: "{{ haproxy_info.statistics }}"
            tables: "{{ haproxy_tables.statistics }}"