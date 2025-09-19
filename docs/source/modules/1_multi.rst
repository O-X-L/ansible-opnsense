.. _modules_multi:

.. include:: ../_include/head.rst

===================
1 - Mass Management
===================

**Tests**: `Playbook <https://github.com/O-X-L/ansible_opnsense/blob/latest/tests/1_multi.yml>`_

This Ansible Collection has the ability to mass-manage many entries at once.

That can improve the processing speed as it can improve the amount of API calls needed.

This Multi-Handling needs to be supported by the module!

----

Module Arguments
****************

General
=======

..  csv-table:: Definition
    :header: "Parameter","Type","Required","Default","Aliases","Comment"
    :widths: 15 10 10 10 10 45

    "multi_control.fail_verify","boolean","false","false","multi_control.fail_verification","Fail module if a single entry fails the verification"
    "multi_control.fail_process","boolean","false","false","multi_control.fail_proc, multi_control.fail_processing","Fail module if a single entry fails to be processed. By default you will see a warning"
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

    "multi_purge","list","false","\-","multi_control.multi_delete, multi_control.purge, multi_control.many_purge","The list of entries to delete"
    "multi_control.purge_action","disable/delete","false","delete","\-","What to do with the matched items"
    "multi_control.purge_filter","dict","false","\-","multi_control.purge_filters","Field-value pairs to filter on - per example: {param1: test} - to only purge items that have 'param1' set to 'test'"
    "multi_control.purge_filter_invert","boolean","false","false","\-","If true - it will purge all but the filtered ones"
    "multi_control.purge_filter_partial","boolean","false","false","\-","If true - the filter will also match if it is just a partial value-match"
    "multi_control.purge_all","boolean","false","false","\-","If set to true and neither items, nor filters are provided - all items will be purged"

----

Examples
********

.. code-block:: yaml

    - hosts: localhost
      gather_facts: no
      module_defaults:
        group/ansibleguy.opnsense.all:
          firewall: 'opnsense.template.opnsense.oxl.app'
          api_credential_file: '/home/guy/.secret/opn.key'

      tasks:
        - name: Adding & Updating multiple Aliases
          ansibleguy.opnsense.alias:
            aliases:
              - name: 'ANSIBLE_TEST_2_2'
                content: ['192.168.1.1', '192.168.1.3']
              - name: 'ANSIBLE_TEST_2_3'
                type: 'network'
                content: '192.168.10.0/24'
              - name: 'ANSIBLE_TEST_2_5'
                type: 'port'
                content: 81
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
            reload: false  # geoip and urltable take LONG time

        - name: Removing all 'dynipv6host' aliases
          ansibleguy.opnsense.alias:
            multi_control:
              purge_all: true
              purge_filter:
                type: 'dynipv6host'

Troubleshooting
===============

To simplify troubleshooting of bad configuration there are some troubleshooting parameters available.

- info
- debug overall
- debug per rule

.. code-block:: yaml

    - name: Changing
      ansibleguy.opnsense.rule:
        rules: {...}

        multi_control:
          # if the module should fail if one rule has a bad config (default behaviour)
          fail_verify: true

          # to output information of processed rules
          output_info: true

          # output verbose information about requests and processing
          debug: true
