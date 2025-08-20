.. _modules_haproxy_exporter:

.. include:: ../_include/head.rst

===================
HAProxy Exporter
===================

**STATE**: stable

**COMPATIBILITY**: OPNsense 24.1+

**Note**: Most functions should work on earlier OPNsense versions, but full compatibility is tested with OPNsense 24.1+. For compatibility with earlier versions, please check the configuration differences at: `HAProxy Configuration Reference <https://github.com/opnsense/plugins/blob/master/net/haproxy/src/opnsense/mvc/app/models/OPNsense/HAProxy/HAProxy.xml>`_

**TESTS**: `Playbook <https://github.com/O-X-L/ansible_opnsense/blob/latest/tests/haproxy_exporter.yml>`_


Contribution
************

This module was contributed by **MaximeWewer** (@MaximeWewer).

If you encounter any issues or have suggestions for improvements, please feel free to contribute to the project.


Definition
**********

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "export_type","string","true","\-","\-","Type of export operation (config, diff, download)"
    "download_type","string","false","\-","\-","Specific download type when export_type is 'download'"

.. include:: ../_include/param_basic.rst

Usage
*****

This module exports HAProxy configuration and related data from OPNsense. It provides various export formats for configuration backup, analysis, and integration with external tools.

Available export types:

- **config**: Export the current HAProxy configuration in native format
- **diff**: Export configuration differences for change tracking
- **download**: Download specific HAProxy data files and reports

Key features:

- **Configuration backup**: Export complete HAProxy configurations
- **Change tracking**: Generate configuration diffs for auditing
- **Data extraction**: Download specific HAProxy data files
- **Integration support**: Provide data for external monitoring and management tools
- **Read-only operations**: Safe export without configuration changes
- **Multiple formats**: Support various export formats and data types

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
        - name: Export HAProxy configuration
          ansibleguy.opnsense.haproxy_exporter:
            export_type: config
          register: haproxy_config

        - name: Save configuration to file
          ansible.builtin.copy:
            content: "{{ haproxy_config.result.config }}"
            dest: "/backup/haproxy_{{ ansible_date_time.date }}.cfg"
          when: haproxy_config.result.config is defined

        - name: Export configuration differences
          ansibleguy.opnsense.haproxy_exporter:
            export_type: diff
          register: config_diff

        - name: Display configuration changes
          ansible.builtin.debug:
            var: config_diff.result
          when: config_diff.result.changes is defined

        - name: Download HAProxy data files
          ansibleguy.opnsense.haproxy_exporter:
            export_type: download
            download_type: "statistics"
          register: stats_download

        - name: Backup configuration with timestamp
          block:
            - name: Export current config
              ansibleguy.opnsense.haproxy_exporter:
                export_type: config
              register: current_config

            - name: Create backup directory
              ansible.builtin.file:
                path: "/backup/haproxy/{{ ansible_date_time.date }}"
                state: directory

            - name: Save configuration backup
              ansible.builtin.copy:
                content: "{{ current_config.result.config }}"
                dest: "/backup/haproxy/{{ ansible_date_time.date }}/haproxy.cfg"

        - name: Monitor configuration changes
          block:
            - name: Check for configuration diff
              ansibleguy.opnsense.haproxy_exporter:
                export_type: diff
              register: daily_diff

            - name: Alert on configuration changes
              ansible.builtin.mail:
                to: admin@example.com
                subject: "HAProxy Configuration Changes Detected"
                body: |
                  Configuration changes detected on {{ inventory_hostname }}:
                  {{ daily_diff.result | to_nice_json }}
              when: 
                - daily_diff.result.changes is defined
                - daily_diff.result.changes | length > 0

        - name: Generate configuration report
          block:
            - name: Export configuration
              ansibleguy.opnsense.haproxy_exporter:
                export_type: config
              register: config_export

            - name: Download additional data
              ansibleguy.opnsense.haproxy_exporter:
                export_type: download
                download_type: "{{ item }}"
              register: downloads
              loop:
                - "statistics"
                - "logs"
                - "certificates"

            - name: Generate comprehensive report
              ansible.builtin.template:
                src: haproxy_report.j2
                dest: "/reports/haproxy_{{ ansible_date_time.date }}.html"
              vars:
                config: "{{ config_export.result }}"
                downloads: "{{ downloads.results }}"

        - name: Configuration validation workflow
          block:
            - name: Export current configuration
              ansibleguy.opnsense.haproxy_exporter:
                export_type: config
              register: before_config

            - name: Apply configuration changes
              # ... make configuration changes ...

            - name: Export updated configuration
              ansibleguy.opnsense.haproxy_exporter:
                export_type: config
              register: after_config

            - name: Compare configurations
              ansible.builtin.debug:
                msg: "Configuration size changed from {{ before_config.result.config | length }} to {{ after_config.result.config | length }} characters"