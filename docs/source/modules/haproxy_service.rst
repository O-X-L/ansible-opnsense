.. _modules_haproxy_service:

.. include:: ../_include/head.rst

================
HAProxy Service
================

**STATE**: stable

**COMPATIBILITY**: OPNsense 24.1+

**Note**: Most functions should work on earlier OPNsense versions, but full compatibility is tested with OPNsense 24.1+. For compatibility with earlier versions, please check the configuration differences at: `HAProxy Configuration Reference <https://github.com/opnsense/plugins/blob/master/net/haproxy/src/opnsense/mvc/app/models/OPNsense/HAProxy/HAProxy.xml>`_

**TESTS**: `Playbook <https://github.com/O-X-L/ansible_opnsense/blob/latest/tests/haproxy_service.yml>`_

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

    "action","string","true","\-","\-","Service action (start, stop, restart, reload, status, configtest)"

.. include:: ../_include/param_basic.rst

Usage
*****

This module controls the HAProxy service operations. It allows you to start, stop, restart, reload the service, check its status, and test the configuration validity.

**Note**: This module does not use the standard 'reload' parameter as it manages service operations directly.

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
        - name: Check HAProxy service status
          ansibleguy.opnsense.haproxy_service:
            action: status
          register: haproxy_status

        - name: Test HAProxy configuration
          ansibleguy.opnsense.haproxy_service:
            action: configtest
          register: config_test

        - name: Start HAProxy service
          ansibleguy.opnsense.haproxy_service:
            action: start
          when: haproxy_status.result.status != 'running'

        - name: Stop HAProxy service
          ansibleguy.opnsense.haproxy_service:
            action: stop

        - name: Restart HAProxy service
          ansibleguy.opnsense.haproxy_service:
            action: restart

        - name: Reload HAProxy configuration
          ansibleguy.opnsense.haproxy_service:
            action: reload

        - name: Show service status
          ansible.builtin.debug:
            var: haproxy_status.result