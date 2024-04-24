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

ansibleguy.opnsense.nginx_upstream_server
=========================================

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "parameter name","parameter type","if is required","default value","aliases","description"
    "placeholder","string","false","\-","\-","Some description"
    "reload","boolean","false","true","\-", .. include:: ../_include/param_reload.rst



Usage
*****

Basic description of the module.

Place for additional information the user should know of.

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
        # add optional parameters commented-out
        # required ones normally
        # add their default values to get a brief overview of how the module works
        - name: Example
          ansibleguy.opnsense.nginx_upstream_server:
            description: 'test1'
            command: 'system remote backup'
            # state: 'absent'
            # debug: false

        - name: Adding something
          ansibleguy.opnsense.nginx_upstream_server:

        - name: Changing something
          ansibleguy.opnsense.nginx_upstream_server:

        - name: Listing jobs
          ansibleguy.opnsense.list:
          #  target: 'nginx_upstream_server'
          register: existing_jobs

        - name: Printing
          ansible.builtin.debug:
            var: existing_jobs.data
