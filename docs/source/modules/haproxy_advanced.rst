.. _modules_haproxy_advanced:

.. include:: ../_include/head.rst

=================================
HAProxy advanced & extended features
=================================

**STATE**: unstable

**COMPATIBILITY**: OPNsense 24.1+

**TESTS**:
`Lua <https://github.com/O-X-L/ansible_opnsense/blob/latest/tests/haproxy_lua.yml>`_ |
`FCGI <https://github.com/O-X-L/ansible_opnsense/blob/latest/tests/haproxy_fcgi.yml>`_ |
`ErrorFile <https://github.com/O-X-L/ansible_opnsense/blob/latest/tests/haproxy_errorfile.yml>`_

**API Docs**: `HAProxy <https://docs.opnsense.org/development/api/plugins/haproxy.html>`_

These modules manage advanced HAProxy features including Lua scripts, FastCGI applications, and custom error pages.

----

.. _haproxy_lua:

ansibleguy.opnsense.haproxy_lua
=================================

Manages HAProxy Lua scripts for custom logic and processing.

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "name","string","true","\-","\-","Name to identify this Lua script"
    "description","string","false","\-","\-","Description for this Lua script"
    "enabled","boolean","false","true","\-","Enable or disable this Lua script"
    "preload","boolean","false","false","\-","Whether HAProxy should load and execute this Lua script on startup"
    "filename_scheme","string","false","\-","\-","Filename generation strategy for Lua scripts"
    "content","string","false","\-","\-","Paste the content of your Lua script here"

Examples
--------

.. code-block:: yaml

    - name: Create authentication Lua script
      ansibleguy.opnsense.haproxy_lua:
        name: 'auth_script'
        description: 'JWT authentication script'
        enabled: true
        preload: true
        content: |
          function authenticate_jwt(txn)
            local headers = txn.http:req_get_headers()
            local auth_header = headers["authorization"]
            if auth_header and string.find(auth_header, "Bearer ") then
              return "AUTHORIZED"
            else
              return "UNAUTHORIZED"
            end
          end

----

.. _haproxy_fcgi:

ansibleguy.opnsense.haproxy_fcgi
==================================

Manages HAProxy FastCGI applications for dynamic content processing.

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "name","string","true","\-","\-","Name to identify this FastCGI application"
    "description","string","false","\-","\-","Description for this FastCGI application"
    "enabled","boolean","false","true","\-","Enable or disable this FastCGI application"
    "docroot","string","false","\-","\-","Define the document root on the remote host"
    "index","string","false","\-","\-","Define the script name that will be appended after a URI"
    "path_info","string","false","\-","\-","Define a regular expression to extract script-name and path-info"
    "log_stderr","boolean","false","false","\-","Enable logging of STDERR messages"
    "keep_conn","boolean","false","false","\-","Instruct the FastCGI application to keep connection open"
    "get_values","boolean","false","false","\-","Enable retrieval of connection management variables"
    "mpxs_conns","boolean","false","false","\-","Enable support for connection multiplexing"
    "max_reqs","integer","false","\-","\-","Define maximum number of concurrent requests (1-100000)"
    "linked_actions","list","false","\-","\-","Choose rules to be included in this FastCGI application"

Examples
--------

.. code-block:: yaml

    - name: Create PHP FastCGI application
      ansibleguy.opnsense.haproxy_fcgi:
        name: 'php_app'
        description: 'PHP application backend'
        enabled: true
        docroot: '/var/www/html'
        index: 'index.php'
        path_info: '^(/.+\.php)(/.*)?$'
        log_stderr: true
        max_reqs: 50

----

.. _haproxy_errorfile:

ansibleguy.opnsense.haproxy_errorfile
======================================

Manages HAProxy custom error pages for better user experience.

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "name","string","true","\-","\-","Name to identify this error message"
    "description","string","false","\-","\-","Description for this error message"
    "code","string","false","\-","\-","HTTP status code for error handling"
    "content","string","false","\-","\-","Paste the content of your error messages here"

Examples
--------

.. code-block:: yaml

    - name: Create custom 404 page
      ansibleguy.opnsense.haproxy_errorfile:
        name: 'custom_404'
        description: 'Custom 404 error page'
        code: 'x404'
        content: |
          HTTP/1.0 404 Not Found
          Content-Type: text/html
          Cache-Control: no-cache
          Connection: close

          <!DOCTYPE html>
          <html>
          <head><title>Page Not Found</title></head>
          <body>
            <h1>404 - Page Not Found</h1>
            <p>The requested page could not be found.</p>
          </body>
          </html>


See also: :ref:`modules_haproxy_general` and :ref:`troubleshooting <troubleshooting>`