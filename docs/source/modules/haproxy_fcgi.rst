.. _modules_haproxy_fcgi:

.. include:: ../_include/head.rst

================
HAProxy - FCGI
================

**STATE**: stable

**COMPATIBILITY**: OPNsense 24.1+

**Note**: Most functions should work on earlier OPNsense versions, but full compatibility is tested with OPNsense 24.1+. For compatibility with earlier versions, please check the configuration differences at: `HAProxy Configuration Reference <https://github.com/opnsense/plugins/blob/master/net/haproxy/src/opnsense/mvc/app/models/OPNsense/HAProxy/HAProxy.xml>`_

**TESTS**: `Playbook <https://github.com/ansibleguy/collection_opnsense/blob/latest/tests/haproxy_fcgi.yml>`_


Contribution
************

This module was contributed by **MaximeWewer** (@MaximeWewer).

If you encounter any issues or have suggestions for improvements, please feel free to contribute to the project.


Prerequisites
************

You need to install and configure HAProxy on the target system.

.. include:: ../_include/haproxy.rst

Definition
**********

.. include:: ../_include/param_basic.rst

ansibleguy.opnsense.haproxy_fcgi
********************************

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "name","string","true","\-","n","Name of the FCGI app"
    "description","string","false","\-","desc","Description for the FCGI app"
    "docroot","string","false","\-","\-","Document root path for the FCGI application"
    "index","string","false","index.php","\-","Default index file"
    "linked_actions","list","false","\-","actions","List of action names to link to this FCGI app"

.. include:: ../_include/param_basic_en_state.rst

Examples
********

.. code-block:: yaml

    - ansibleguy.opnsense.haproxy_fcgi:
        name: 'php_app'
        description: 'PHP FastCGI application'
        docroot: '/var/www/html'
        index: 'index.php'

    - ansibleguy.opnsense.haproxy_fcgi:
        name: 'wordpress'
        description: 'WordPress FCGI configuration'
        docroot: '/var/www/wordpress'
        index: 'index.php'
        linked_actions: ['wordpress_actions']
