.. _modules_haproxy_lua:

.. include:: ../_include/head.rst

===============
HAProxy - Lua
===============

**STATE**: stable

**COMPATIBILITY**: OPNsense 24.1+

**Note**: Most functions should work on earlier OPNsense versions, but full compatibility is tested with OPNsense 24.1+. For compatibility with earlier versions, please check the configuration differences at: `HAProxy Configuration Reference <https://github.com/opnsense/plugins/blob/master/net/haproxy/src/opnsense/mvc/app/models/OPNsense/HAProxy/HAProxy.xml>`_

**TESTS**: `Playbook <https://github.com/ansibleguy/collection_opnsense/blob/latest/tests/haproxy_lua.yml>`_


Contribution
************

This module was contributed by **MaximeWewer** (@MaximeWewer).

If you encounter any issues or have suggestions for improvements, please feel free to contribute to the project.


Prerequisites
*************

You need to install and configure HAProxy on the target system.

.. include:: ../_include/haproxy.rst

Definition
**********

.. include:: ../_include/param_basic.rst

ansibleguy.opnsense.haproxy_lua
*******************************

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "name","string","true","\-","n","Name of the Lua script"
    "description","string","false","\-","desc","Description for the Lua script"
    "preload","boolean","false","true","\-","Whether to preload the Lua script"
    "filename_scheme","string","false","id","\-","Filename scheme. One of: 'id', 'name'"
    "content","string","true","\-","\-","Lua script content"

.. include:: ../_include/param_basic_en_state.rst

Examples
********

.. code-block:: yaml

    - ansibleguy.opnsense.haproxy_lua:
        name: 'custom_auth'
        description: 'Custom authentication logic'
        preload: true
        filename_scheme: 'name'
        content: |
          function authenticate(txn)
              local auth_header = txn.http:req_get_headers()["authorization"]
              if auth_header and auth_header[0] then
                  -- Custom authentication logic here
                  return true
              end
              return false
          end

    - ansibleguy.opnsense.haproxy_lua:
        name: 'request_logger'
        description: 'Log detailed request information'
        content: |
          function log_request(txn)
              local method = txn.http:req_get_method()
              local path = txn.http:req_get_path()
              local ip = txn.f:src()
              core.log(core.info, string.format("Request: %s %s from %s", method, path, ip))
          end
