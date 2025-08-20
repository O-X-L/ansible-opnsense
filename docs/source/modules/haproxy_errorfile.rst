.. _modules_haproxy_errorfile:

.. include:: ../_include/head.rst

==================
HAProxy Error File
==================

**STATE**: stable

**COMPATIBILITY**: OPNsense 24.1+

**Note**: Most functions should work on earlier OPNsense versions, but full compatibility is tested with OPNsense 24.1+. For compatibility with earlier versions, please check the configuration differences at: `HAProxy Configuration Reference <https://github.com/opnsense/plugins/blob/master/net/haproxy/src/opnsense/mvc/app/models/OPNsense/HAProxy/HAProxy.xml>`_

**TESTS**: `Playbook <https://github.com/O-X-L/ansible_opnsense/blob/latest/tests/haproxy_errorfile.yml>`_


Contribution
************

This module was contributed by **MaximeWewer** (@MaximeWewer).

If you encounter any issues or have suggestions for improvements, please feel free to contribute to the project.


Definition
**********

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "name","string","true","\-","\-","Error file name"
    "description","string","false","\-","\-","Error file description"
    "enabled","boolean","false","true","\-","Enable or disable error file"
    "code","string","true","\-","\-","HTTP error code (200, 400, 403, 405, 408, 429, 500, 502, 503, 504)"
    "content","string","true","\-","\-","Error file content (HTML)"
    "state","string","false","present","\-","State of the error file (present, absent)"
    "reload","boolean","false","true","\-", .. include:: ../_include/param_reload.rst

.. include:: ../_include/param_basic.rst

Usage
*****

This module manages HAProxy custom error files. Error files allow you to customize the error pages that HAProxy serves when specific HTTP errors occur, improving user experience and providing consistent branding.

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
          target: 'haproxy_errorfile'

      tasks:
        - name: Create custom 404 error page
          ansibleguy.opnsense.haproxy_errorfile:
            name: 'custom_404'
            description: 'Custom 404 error page'
            enabled: true
            code: '404'
            content: |
              HTTP/1.1 404 Not Found
              Content-Type: text/html
              Cache-Control: no-cache
              Connection: close
              
              <!DOCTYPE html>
              <html>
              <head>
                  <title>Page Not Found</title>
                  <style>
                      body { font-family: Arial, sans-serif; text-align: center; margin-top: 50px; }
                      h1 { color: #e74c3c; }
                  </style>
              </head>
              <body>
                  <h1>404 - Page Not Found</h1>
                  <p>The page you are looking for could not be found.</p>
              </body>
              </html>

        - name: Create custom 503 maintenance page
          ansibleguy.opnsense.haproxy_errorfile:
            name: 'maintenance_503'
            description: 'Maintenance mode page'
            enabled: true
            code: '503'
            content: |
              HTTP/1.1 503 Service Unavailable
              Content-Type: text/html
              Cache-Control: no-cache
              Connection: close
              
              <!DOCTYPE html>
              <html>
              <head>
                  <title>Maintenance Mode</title>
              </head>
              <body>
                  <h1>Service Temporarily Unavailable</h1>
                  <p>We are currently performing maintenance. Please try again later.</p>
              </body>
              </html>

        - name: Create custom 500 error page
          ansibleguy.opnsense.haproxy_errorfile:
            name: 'custom_500'
            description: 'Internal server error page'
            enabled: true
            code: '500'
            content: |
              HTTP/1.1 500 Internal Server Error
              Content-Type: text/html
              
              <html><body><h1>Internal Server Error</h1></body></html>

        - name: Remove error file
          ansibleguy.opnsense.haproxy_errorfile:
            name: 'old_errorfile'
            state: 'absent'

        - name: List all error files
          ansibleguy.opnsense.list:
          register: haproxy_errorfiles

        - name: Show error files
          ansible.builtin.debug:
            var: haproxy_errorfiles.data