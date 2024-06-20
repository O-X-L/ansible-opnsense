.. _modules_nginx:

.. include:: ../_include/head.rst

=====
Nginx
=====

**STATE**: unstable

**TESTS**: `nginx_upstream_server <https://github.com/ansibleguy/collection_opnsense/blob/latest/tests/nginx_upstream_server.yml>`_

**API Docs**: `Plugins - Nginx <https://docs.opnsense.org/development/api/plugins/nginx.html>`_

**Service Docs**: `Nginx <https://docs.opnsense.org/manual/how-tos/nginx.html>`_

Contribution
************

Thanks to `@atammy-narmi <https://github.com/atammy-narmi>`_ for developing these modules!

Prerequisites
*************

You need to install the following plugin:

.. code-block:: bash

    os-nginx

You can also install it using the :ref:`ansibleguy.opnsense.package <modules_package>` module.


Definition
**********

.. include:: ../_include/param_basic.rst

ansibleguy.opnsense.nginx_general
=========================================

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "enabled","boolean","false","true","\-","Enable configured services."
    "ban_ttl","integer","false","0","\-","Set autoblock lifetime in minutes. Set to 0 for infinite."


ansibleguy.opnsense.nginx_upstream_server
=========================================

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "description","string","true","\-","name","\-"
    "server","string","true","\-","\-","\-"
    "port","integer","true","\-","\-","\-"
    "priority","integer","true","\-","\-","\-"
    "max_conns","integer","false","\-","\-","\-"
    "max_fails","integer","false","\-","\-","\-"
    "fail_timeout","integer","false","\-","\-","\-"
    "no_use","string","false","\-","\-","Choice of empty, 'down' or 'backup'."
    "state","string","false","present","\-","Choice of 'present' or 'absent'."
    "reload","boolean","false","true","\-", .. include:: ../_include/param_reload.rst


Usage
*****

Enabling the nginx configured services.

Examples
********

ansibleguy.opnsense.nginx_upstream_server
=========================================

.. code-block:: yaml

    - hosts: localhost
      gather_facts: false
      module_defaults:
        group/ansibleguy.opnsense.all:
          firewall: 'opnsense.template.ansibleguy.net'
          api_credential_file: '/home/guy/.secret/opn.key'

        ansibleguy.opnsense.list:
          target: 'nginx_upstream_server'

      tasks:
        - name: Add an upstream server
          ansibleguy.opnsense.nginx_upstream_server:
            name: 'upstream1'
            server: '192.168.1.1'
            port: 80
            priority: 1
            max_conns: 100
            max_fails: 50
            fail_timeout: 10
            no_use: 'down'
            # state: 'present'
            # reload: true

        - name: Changing the server
          ansibleguy.opnsense.nginx_upstream_server:
            name: 'upstream1'
            server: '192.168.1.100'

        - name: Listing upstream servers
          ansibleguy.opnsense.list:
          #  target: 'nginx_upstream_server'
          register: existing_servers

        - name: Printing
          ansible.builtin.debug:
            var: existing_servers.data
