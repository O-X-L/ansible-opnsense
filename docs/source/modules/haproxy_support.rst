.. _modules_haproxy_support:

.. include:: ../_include/head.rst

========================================
HAProxy infrastructure & support modules
========================================

**STATE**: unstable

**COMPATIBILITY**: OPNsense 24.1+

**TESTS**:
`Mailer <https://github.com/O-X-L/ansible_opnsense/blob/latest/tests/haproxy_mailer.yml>`_ |
`MapFile <https://github.com/O-X-L/ansible_opnsense/blob/latest/tests/haproxy_mapfile.yml>`_ |
`Resolver <https://github.com/O-X-L/ansible_opnsense/blob/latest/tests/haproxy_resolver.yml>`_

**API Docs**: `HAProxy <https://docs.opnsense.org/development/api/plugins/haproxy.html>`_

These modules manage HAProxy supporting infrastructure including email notifications, map files for dynamic configuration, and DNS resolvers.

----

.. _haproxy_mailer:

oxlorg.opnsense.haproxy_mailer
==============================

Manages HAProxy email notifications for alerts and monitoring.

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "name","string","true","\-","\-","Name to identify this mailer configuration"
    "description","string","false","\-","\-","Description for this mailer configuration"
    "enabled","boolean","false","true","\-","Enable or disable this mailer configuration"
    "mailservers","list","false","[]","\-","Mail servers for this configuration. Add mailservers to this mailer configuration, i.e. 192.168.1.1:25"
    "sender","string","false","\-","\-","Mail sender address. Declare the from email address to be used in both the envelope and header of email alerts"
    "recipient","string","false","\-","\-","Mail recipient address. Declare both the recipient address in the envelope and to address in the header of email alerts"
    "loglevel","string","false","\-","\-","Alert log level. Declare the maximum log level of messages for which email alerts will be sent. Options: emerg, alert, crit, err, warning, notice, info, debug"
    "timeout","integer","false","\-","\-","Timeout in seconds. Defines the time (in seconds) available for a mail/connection to be made and send to the mail server (4-10000)"
    "hostname","string","false","\-","\-","Hostname address. Declare the to hostname address to be used when communicating with mailers"

Examples
--------

.. code-block:: yaml

    - name: Create basic email notification
      oxlorg.opnsense.haproxy_mailer:
        name: 'admin_alerts'
        description: 'Administrator alerts'
        enabled: true
        mailservers:
          - '192.168.1.100:25'
          - '192.168.1.101:25'
        sender: 'haproxy@example.com'
        recipient: 'admin@example.com'
        loglevel: 'warning'
        timeout: 30

    - name: Create SMTP authentication mailer
      oxlorg.opnsense.haproxy_mailer:
        name: 'monitoring_alerts'
        description: 'Monitoring system alerts'
        mailservers:
          - 'smtp.example.com:587'
        sender: 'alerts@example.com'
        recipient: 'monitoring@example.com'
        loglevel: 'info'
        timeout: 60
        hostname: 'haproxy.example.com'

----

.. _haproxy_mapfile:

oxlorg.opnsense.haproxy_mapfile
===============================

Manages HAProxy map files for dynamic configuration and content routing.

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "name","string","true","\-","\-","Name to identify this map file"
    "description","string","false","\-","\-","Description for this map file"
    "content","string","true","\-","\-","Map file content. Paste the content of your map file here"

Examples
--------

.. code-block:: yaml

    - name: Create domain routing map
      oxlorg.opnsense.haproxy_mapfile:
        name: 'domain_routing'
        description: 'Map for domain-based routing'
        content: |
          www.example.com backend_web
          api.example.com backend_api
          admin.example.com backend_admin
          static.example.com backend_static

    - name: Create path-based routing map
      oxlorg.opnsense.haproxy_mapfile:
        name: 'path_routing'
        description: 'Map for path-based routing'
        content: |
          /api/ backend_api
          /admin/ backend_admin
          /static/ backend_static
          /uploads/ backend_files

    - name: Create SSL certificate map
      oxlorg.opnsense.haproxy_mapfile:
        name: 'ssl_certificates'
        description: 'SSL certificate mapping'
        content: |
          www.example.com /usr/local/etc/haproxy/ssl/www.example.com.pem
          api.example.com /usr/local/etc/haproxy/ssl/api.example.com.pem
          admin.example.com /usr/local/etc/haproxy/ssl/admin.example.com.pem

----

.. _haproxy_resolver:

oxlorg.opnsense.haproxy_resolver
================================

Manages HAProxy DNS resolvers for dynamic server resolution and health checking.

**Field Validation Patterns:**

* **name**: 1-255 characters, cannot contain tabs, commas, semicolons, dots, or brackets
* **description**: 1-255 characters if provided
* **nameservers**: Format [protocol@]address:port[-port_range] (e.g. 127.0.0.1:53, tcp@192.168.1.1:53)
* **timeout fields** (timeout_resolve, timeout_retry, hold_*): 1-8 digit number + optional time unit (us, ms, s, m, h, d)
* **resolve_retries**: Integer between 0-100000
* **accepted_payload_size**: Integer between 0-65535

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "name","string","true","\-","\-","Name to identify this resolver configuration"
    "description","string","false","\-","\-","Description for this resolver configuration"
    "enabled","boolean","false","true","\-","Enable or disable this resolver configuration"
    "nameservers","list","false","[]","\-","DNS nameservers. Add nameservers to this resolver configuration. They may be prefixed with either tcp@ or udp@ to use the TCP or UDP protocol respectively"
    "parse_resolv_conf","boolean","false","false","\-","Use resolv.conf. Add all nameservers found in /etc/resolv.conf to this resolver configuration"
    "resolve_retries","integer","false","\-","\-","Resolve retries. This configures the number of queries to send to resolve a server name before giving up (0-100000)"
    "timeout_resolve","string","false","\-","\-","Resolve timeout. This configures the default time to trigger name resolutions when no other time applied. Enter a number followed by one of the supported suffixes \"d\" (days), \"h\" (hour), \"m\" (minute), \"s\" (seconds), \"ms\" (milliseconds)"
    "timeout_retry","string","false","\-","\-","Retry timeout. This configures the default time between two DNS queries, when no valid response has been received. Enter a number followed by one of the supported suffixes \"d\" (days), \"h\" (hour), \"m\" (minute), \"s\" (seconds), \"ms\" (milliseconds)"
    "accepted_payload_size","integer","false","\-","\-","Max DNS answer size. Defines the maximum payload size accepted by HAProxy and announced to all the name servers configured in this resolvers section. The default is 512 bytes, the maximum allowed is 8192 for UDP and 65535 for TCP (0-65535)"
    "hold_valid","string","false","\-","\-","Valid hold time. When haproxy receives a valid NS response it will not query DNS until valid time expires. Default is \"10s\""
    "hold_obsolete","string","false","\-","\-","Obsolete hold time. As a DNS server may not answer all the IPs in one DNS request, haproxy keeps a cache of previous answers. An answer will be considered obsolete after [hold obsolete] seconds without the IP returned. Default is \"30s\""
    "hold_refused","string","false","\-","\-","Refused hold time. When the DNS server refuses the resolve request haproxy will not retry until [hold refused] elapses. Default \"30s\""
    "hold_nx","string","false","\-","\-","NX hold time. When haproxy receives a NXDOMAIN error message (domain does not exist) from the resolver it will not retry until [hold nx] elapses. Default \"30s\""
    "hold_timeout","string","false","\-","\-","Timeout hold time. When a DNS resolve request times out haproxy will not retry until [hold timeout] elapses. Default \"30s\""
    "hold_other","string","false","\-","\-","Other hold time. Sets the \"hold other\" timeout value for the resolver. Default \"30s\""

Examples
--------

.. code-block:: yaml

    - name: Create basic DNS resolver
      oxlorg.opnsense.haproxy_resolver:
        name: 'basic_dns'
        description: 'Basic DNS resolver for backend resolution'
        enabled: true
        nameservers:
          - '8.8.8.8:53'
          - '8.8.4.4:53'
        resolve_retries: 3
        timeout_resolve: '1s'
        timeout_retry: '1s'

    - name: Create advanced DNS resolver
      oxlorg.opnsense.haproxy_resolver:
        name: 'advanced_dns'
        description: 'Advanced DNS resolver with custom settings'
        nameservers:
          - 'tcp@192.168.1.1:53'
          - 'udp@192.168.1.2:53'
        parse_resolv_conf: true
        resolve_retries: 5
        timeout_resolve: '2s'
        timeout_retry: '3s'
        accepted_payload_size: 1024
        hold_valid: '10s'
        hold_obsolete: '30s'
        hold_refused: '30s'
        hold_nx: '30s'
        hold_timeout: '30s'
        hold_other: '30s'

    - name: Create resolver with system DNS
      oxlorg.opnsense.haproxy_resolver:
        name: 'system_dns'
        description: 'Resolver using system DNS settings'
        parse_resolv_conf: true
        nameservers:
          - '1.1.1.1:53'
        resolve_retries: 2
        timeout_resolve: '3s'
        hold_valid: '15s'


See also: :ref:`modules_haproxy` and :ref:`troubleshooting <modules_haproxy_troubleshooting>`
