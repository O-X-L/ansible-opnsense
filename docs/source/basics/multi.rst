.. _modules_multi:

.. include:: ../_include/head.rst

===============
Mass Management
===============

**Tests**: `Functional <https://github.com/O-X-L/ansible-opnsense/blob/latest/tests/1_multi.yml>`_, `Unit <https://github.com/O-X-L/ansible-opnsense/tree/latest/plugins/module_utils/base>`_

This Ansible Collection has the ability to mass-manage many entries at once.

That can improve the processing speed as it can improve the amount of API calls needed.

This Multi-Handling needs to be supported by the module!

.. warning::

    Make sure to run a check-mode beforehand and manually verify the deletions!

    You can use the :code:`ansible.builtin.pause` module to wait for your review of the changes.

    We test the module behavior using `Unit-Tests <https://github.com/O-X-L/ansible-opnsense/actions/workflows/unit_test.yml>`_ AND `Functional-Tests <https://github.com/O-X-L/ansible-opnsense/tree/latest/tests>`_ - but there might be edge-case scenarios. This is especially true for newer OPNsense releases that had API-changes and were not fully tested yet.

----

Module Arguments
****************

General
=======

..  csv-table:: Definition
    :header: "Parameter","Type","Required","Default","Aliases","Comment"
    :widths: 15 10 10 10 10 45

    "multi_control.fail_verify","boolean","false","false","multi_control.fail_verification","Fail module if a single entry fails the verification"
    "multi_control.fail_process","boolean","false","true","multi_control.fail_proc, multi_control.fail_processing","Fail module if a single entry fails to be processed"
    "multi_control.output_info","boolean","false","false","multi_control.info","Increase output verbosity"

Adding & Modifying
==================

..  csv-table:: Definition
    :header: "Parameter","Type","Required","Default","Aliases","Comment"
    :widths: 15 10 10 10 10 45

    "multi","list","false","\-","multi_control.many, + module-specific aliases","List of entries to manage (add/modify/delete)"
    "multi_control.state","absent/present","false","present","\-","IP-Address or DNS hostname of the target firewall. Must be included as 'common name' or 'subject alternative name' in the firewalls web-certificate to use 'ssl_verify=true'"
    "multi_control.override","dict","false","\-","multi_control.all, multi_control.overrides","Parameters to override for all entries"

Deleting Entries
=================

..  csv-table:: Definition
    :header: "Parameter","Type","Required","Default","Aliases","Comment"
    :widths: 15 10 10 10 10 45

    "multi_purge","list","false","\-","multi_control.multi_delete, multi_control.purge, multi_control.many_purge","The list of entries to purge (delete or disable)"
    "multi_control.purge_action","disable/delete","false","delete","\-","What action to perform on the entries matched by the purge"
    "multi_control.purge_filter","dict","false","\-","multi_control.purge_filters","Field-value pairs to filter on - per example: {param1: test} - to only purge items that have 'param1' set to 'test'"
    "multi_control.purge_filter_invert","boolean","false","false","\-","If true - it will purge all but the filtered ones"
    "multi_control.purge_filter_partial","boolean","false","false","\-","If true - the filter will also match if it is just a partial value-match"
    "multi_control.purge_unconfigured","boolean","false","false","multi_control.purge_orphaned, multi_control.purge_unknown","Usable if configured entries are supplied - will delete all entries NOT matched with the configured ones"
    "multi_control.purge_all","boolean","false","false","\-","If set to true and neither items, nor filters are provided - all items will be purged"

----

Examples
********

.. code-block:: yaml

    - hosts: localhost
      gather_facts: no
      module_defaults:
        group/oxlorg.opnsense.all:
          firewall: 'opnsense.template.opnsense.oxl.app'
          api_credential_file: '/home/guy/.secret/opn.key'

        oxlorg.opnsense.rule_multi:
          match_fields: ['description']  # name == description

      tasks:
        - name: Adding & Updating multiple Aliases
          oxlorg.opnsense.alias_multi:
            aliases:
              - name: 'ANSIBLE_TEST_2_2'
                content: ['192.168.1.1', '192.168.1.3']

              - name: 'ANSIBLE_TEST_2_3'
                type: 'network'
                content: '192.168.10.0/24'

              - name: 'ANSIBLE_TEST_2_5'
                type: 'port'
                content: 81
                state: absent

              - name: 'ANSIBLE_TEST_2_7'
                type: 'url'
                content: 'http://test.template.opnsense.oxl.app'

              - name: 'ANSIBLE_TEST_2_8'
                type: 'urltable'
                content: 'https://www.spamhaus.org/drop/dropv6.txt'
                updatefreq_days: 2

              - name: 'ANSIBLE_TEST_2_9'
                type: 'geoip'
                content: 'DE'

              - name: 'ANSIBLE_TEST_2_11'
                type: 'dynipv6host'
                content:
                  - '::1000'
                  - '::f00d'
                interface: 'lan'

        - name: Removing all 'dynipv6host' aliases
          oxlorg.opnsense.alias_multi:
            multi_control:
              purge_filter:
                type: 'dynipv6host'

        - name: Adding & Updating multiple Aliases
          oxlorg.opnsense.rule_multi:
            rules:
              - name: 'ANSIBLE_TEST_2_1'
                source_net: '192.168.1.0/24'
                destination_invert: true
                destination_net: '10.1.0.0/8'
                action: 'block'

              - name: 'ANSIBLE_TEST_2_2'
                source_net: '192.168.0.0/24'
                destination_net: '192.168.10.0/24'
                destination_port: 8080
                protocol: 'TCP'
                interface: ['lan']

              - name: 'ANSIBLE_TEST_2_3'
                source_invert: true
                source_net: 'bogons'
                ip_protocol: 'inet6'
                action: 'block'

            multi_control:
              purge_unconfigured: true  # remove all existing entries not found in the provided entries (unconfigured/orphaned)


Troubleshooting
===============

To simplify troubleshooting of bad configuration there are some troubleshooting parameters available.

- info
- debug overall
- debug per rule

.. code-block:: yaml

    - name: Changing
      oxlorg.opnsense.rule_multi:
        rules: {...}

        multi_control:
          # if the module should fail if one entry has a bad config (default behaviour)
          fail_verify: true

          # if the module should fail if one entry fails to be processed
          fail_process: true

          # to output information of processed entries
          output_info: true

          # output verbose information about requests and processing
          debug: true
