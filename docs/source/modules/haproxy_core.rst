.. _modules_haproxy_core:

.. include:: ../_include/head.rst

===================================
HAProxy core load balancing modules
===================================

**STATE**: unstable

**COMPATIBILITY**: OPNsense 24.1+

**TESTS**:
`Backend <https://github.com/O-X-L/ansible_opnsense/blob/latest/tests/haproxy_backend.yml>`_ |
`Frontend <https://github.com/O-X-L/ansible_opnsense/blob/latest/tests/haproxy_frontend.yml>`_ |
`Server <https://github.com/O-X-L/ansible_opnsense/blob/latest/tests/haproxy_server.yml>`_ |
`Healthcheck <https://github.com/O-X-L/ansible_opnsense/blob/latest/tests/haproxy_healthcheck.yml>`_

**API Docs**: `HAProxy <https://docs.opnsense.org/development/api/plugins/haproxy.html>`_

These modules manage the core HAProxy load balancing functionality including backends, frontends, servers, and health checks.

----

.. _haproxy_backend:

oxlorg.opnsense.haproxy_backend
===============================

Manages HAProxy backend pools with servers, load balancing algorithms, health checks, persistence, and advanced settings.

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "name","string","true","\-","\-","Name to identify this Backend Pool"
    "description","string","false","\-","\-","Description for this Backend Pool"
    "enabled","boolean","false","true","\-","Enable or disable this backend"
    "mode","string","false","http","\-","Set the running mode or protocol. Options: http, tcp"
    "algorithm","string","false","source","\-","Load balancing algorithm. Options: source, roundrobin, static-rr, leastconn, uri, random"
    "random_draws","integer","false","2","\-","Number of draws for random algorithm (2-1000)"
    "proxy_protocol","string","false","\-","\-","PROXY protocol version. Options: v1, v2"
    "linked_servers","list","false","[]","\-","Add servers to this backend"
    "linked_fcgi","string","false","\-","\-","FastCGI application for all servers in this backend"
    "linked_resolver","string","false","\-","\-","Custom resolver configuration for all servers"
    "resolver_opts","list","false","[]","\-","Resolver options. Options: allow-dup-ip, ignore-weight, prevent-dup-ip"
    "resolve_prefer","string","false","\-","\-","Prefer IP family for DNS resolution. Options: ipv4, ipv6"
    "source","string","false","\-","\-","Source address when connecting to servers"
    "health_check_enabled","boolean","false","true","\-","Enable or disable health checking"
    "health_check","string","false","\-","\-","Health monitor for servers in this backend"
    "health_check_log_status","boolean","false","false","\-","Log health check status updates"
    "check_interval","string","false","\-","\-","Interval for running health checks"
    "check_down_interval","string","false","\-","\-","Interval for health checks when server is DOWN"
    "health_check_fall","integer","false","\-","\-","Consecutive unsuccessful checks before server unavailable (1-100)"
    "health_check_rise","integer","false","\-","\-","Consecutive successful checks before server available (1-100)"
    "linked_mailer","string","false","\-","\-","E-mail alert configuration"
    "http2_enabled","boolean","false","true","\-","Enable end-to-end HTTP/2 communication"
    "http2_enabled_nontls","boolean","false","false","\-","Enable HTTP/2 even if TLS is not enabled"
    "ba_advertised_protocols","list","false","['h2', 'http11']","\-","Protocols advertised via ALPN. Options: h2, http11, http10"
    "forwarded_header","boolean","false","false","\-","Enable RFC7239 forwarded header insertion"
    "forwarded_header_parameters","list","false","[]","\-","Parameters for forwarded header. Options: proto, host, for, by"
    "forward_for","boolean","false","false","\-","Enable X-Forwarded-For header insertion"
    "persistence","string","false","\-","\-","User-to-server mapping tracking. Options: sticktable, cookie"
    "persistence_cookiemode","string","false","piggyback","\-","Cookie handling mode. Options: piggyback, new"
    "persistence_cookiename","string","false","\-","\-","Cookie name for persistence"
    "persistence_stripquotes","boolean","false","false","\-","Strip quotes from cookie value"
    "stickiness_pattern","string","false","\-","\-","Request pattern to associate user to server"
    "stickiness_data_types","list","false","[]","\-","Additional information for stick-table"
    "stickiness_expire","string","false","30m","\-","Maximum duration of stick-table entry"
    "stickiness_size","string","false","50k","\-","Maximum number of stick-table entries"
    "stickiness_cookiename","string","false","\-","\-","Cookie name for stick table"
    "stickiness_cookielength","integer","false","\-","\-","Maximum characters stored in stick table"
    "stickiness_conn_rate_period","string","false","10s","\-","Rate period for connection rate tracking"
    "stickiness_sess_rate_period","string","false","10s","\-","Rate period for session rate tracking"
    "stickiness_http_req_rate_period","string","false","10s","\-","Rate period for HTTP request rate tracking"
    "stickiness_http_err_rate_period","string","false","10s","\-","Rate period for HTTP error rate tracking"
    "stickiness_bytes_in_rate_period","string","false","1m","\-","Rate period for bytes in rate tracking"
    "stickiness_bytes_out_rate_period","string","false","1m","\-","Rate period for bytes out rate tracking"
    "basic_auth_enabled","boolean","false","false","\-","Enable HTTP Basic Authentication"
    "basic_auth_users","list","false","[]","\-","Allowed users for Basic Authentication"
    "basic_auth_groups","list","false","[]","\-","Allowed groups for Basic Authentication"
    "tuning_timeout_connect","string","false","\-","\-","Maximum time to wait for connection to server"
    "tuning_timeout_check","string","false","\-","\-","Additional read timeout for health checks"
    "tuning_timeout_server","string","false","\-","\-","Maximum inactivity time on server side"
    "tuning_retries","integer","false","\-","\-","Number of retries after connection failure (0-100)"
    "tuning_defaultserver","string","false","\-","\-","Default option for all server entries"
    "tuning_noport","boolean","false","false","\-","Do not use port on server, use frontend port"
    "tuning_httpreuse","string","false","\-","\-","HTTP connection reuse. Options: never, safe, aggressive, always"
    "tuning_caching","boolean","false","false","\-","Enable caching of responses from this backend"
    "custom_options","string","false","\-","\-","Additional HAProxy backend configuration lines"
    "linked_actions","list","false","[]","\-","Rules to include in this Backend Pool"
    "linked_errorfiles","list","false","[]","\-","Error messages to include in this Backend Pool"

Examples
--------

.. code-block:: yaml

    - name: Create web backend pool
      oxlorg.opnsense.haproxy_backend:
        name: 'web_backend'
        description: 'Web servers backend pool'
        mode: 'http'
        algorithm: 'roundrobin'
        health_check_enabled: true
        http2_enabled: true
        forwarded_header: true
        forwarded_header_parameters: ['proto', 'host', 'for']
        linked_servers: ['web1', 'web2', 'web3']
        persistence: 'sticktable'
        stickiness_pattern: 'sourceipv4'
        tuning_timeout_connect: '5s'
        tuning_timeout_server: '30s'
        tuning_retries: 3

    - name: Create TCP backend with advanced settings
      oxlorg.opnsense.haproxy_backend:
        name: 'tcp_backend'
        description: 'TCP services backend'
        mode: 'tcp'
        algorithm: 'leastconn'
        proxy_protocol: 'v2'
        health_check_enabled: true
        health_check_fall: 3
        health_check_rise: 2
        check_interval: '10s'
        basic_auth_enabled: true
        basic_auth_users: ['admin']
        tuning_httpreuse: 'safe'
        tuning_caching: true

----

.. _haproxy_frontend:

oxlorg.opnsense.haproxy_frontend
================================

Manages HAProxy frontend services with SSL offloading, logging, traffic routing, and advanced features.

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "name","string","true","\-","\-","Name to identify this Public Service"
    "description","string","false","\-","\-","Description for this Public Service"
    "enabled","boolean","false","true","\-","Enable or disable this frontend"
    "bind","list","true","\-","\-","Listen addresses, e.g. 127.0.0.1:8080 or www.example.com:443"
    "bind_options","string","false","\-","\-","Parameters appended to every Listen Address line"
    "mode","string","false","http","\-","Running mode or protocol. Options: http, ssl, tcp"
    "default_backend","string","false","\-","\-","Default Backend Pool for this Public Service"
    "ssl_enabled","boolean","false","false","\-","Enable SSL offloading"
    "ssl_certificates","list","false","[]","\-","Certificates for SSL offloading"
    "ssl_default_certificate","string","false","\-","\-","Certificate presented if no SNI provided"
    "ssl_custom_options","string","false","\-","\-","Additional SSL parameters for HAProxy configuration"
    "ssl_advanced_enabled","boolean","false","false","\-","Enable advanced SSL settings"
    "ssl_bind_options","list","false","['prefer-client-ciphers']","\-","SSL bind options. Options: no-sslv3, no-tlsv10, no-tlsv11, no-tlsv12, no-tlsv13, no-tls-tickets, force-sslv3, force-tlsv10, force-tlsv11, force-tlsv12, force-tlsv13, prefer-client-ciphers, strict-sni"
    "ssl_min_version","string","false","\-","\-","Minimum SSL/TLS version. Options: TLSv1.0, TLSv1.1, TLSv1.2, TLSv1.3"
    "ssl_max_version","string","false","\-","\-","Maximum SSL/TLS version. Options: TLSv1.0, TLSv1.1, TLSv1.2, TLSv1.3"
    "ssl_cipher_list","string","false","\-","\-","SSL cipher suites for SSLv3/TLSv1.0/TLSv1.1/TLSv1.2"
    "ssl_cipher_suites","string","false","\-","\-","SSL cipher suites for TLSv1.3"
    "ssl_hsts_enabled","boolean","false","false","\-","Enable HTTP Strict Transport Security"
    "ssl_hsts_include_sub_domains","boolean","false","false","\-","Include all subdomains in HSTS"
    "ssl_hsts_preload","boolean","false","false","\-","Enable HSTS preload"
    "ssl_hsts_max_age","integer","false","15768000","\-","HSTS max-age in seconds (1-1000000000)"
    "ssl_client_auth_enabled","boolean","false","false","\-","Enable SSL client certificate authentication"
    "ssl_client_auth_verify","string","false","required","\-","Client certificate verification. Options: none, optional, required"
    "ssl_client_auth_cas","list","false","[]","\-","Certificate Authorities for client verification"
    "ssl_client_auth_crls","list","false","[]","\-","Certificate Revocation Lists for client verification"
    "http2_enabled","boolean","false","true","\-","Enable HTTP/2 support"
    "http2_enabled_nontls","boolean","false","false","\-","Enable HTTP/2 even without TLS"
    "advertised_protocols","list","false","['h2', 'http/1.1']","\-","Protocols advertised via ALPN. Options: h2, http/1.1, http/1.0"
    "forwarded_header","boolean","false","false","\-","Enable RFC7239 forwarded header insertion"
    "forward_for","boolean","false","false","\-","Enable X-Forwarded-For header insertion"
    "basic_auth_enabled","boolean","false","false","\-","Enable HTTP Basic Authentication"
    "basic_auth_users","list","false","[]","\-","Allowed users for Basic Authentication"
    "basic_auth_groups","list","false","[]","\-","Allowed groups for Basic Authentication"
    "tuning_max_connections","integer","false","\-","\-","Maximum connections for this frontend (0-10000000)"
    "tuning_timeout_client","string","false","\-","\-","Maximum inactivity time on client side"
    "tuning_timeout_http_req","string","false","\-","\-","Maximum time to wait for complete HTTP request"
    "tuning_timeout_http_keep_alive","string","false","\-","\-","HTTP keep-alive timeout"
    "linked_cpu_affinity_rules","list","false","[]","\-","CPU affinity rules for this frontend"
    "tuning_shards","integer","false","\-","\-","Number of shards for this frontend (2-1000)"
    "logging_dont_log_null","boolean","false","false","\-","Do not log connections with no data"
    "logging_dont_log_normal","boolean","false","false","\-","Do not log normal connections"
    "logging_log_separate_errors","boolean","false","false","\-","Log errors on separate facility"
    "logging_detailed_log","boolean","false","false","\-","Enable detailed logging"
    "logging_socket_stats","boolean","false","false","\-","Enable socket statistics in logs"
    "stickiness_pattern","string","false","\-","\-","Pattern for stick table. Options: ipv4, ipv6, integer, string, binary"
    "stickiness_data_types","list","false","[]","\-","Data types to store in stick table"
    "stickiness_expire","string","false","30m","\-","Maximum duration of stick table entry"
    "stickiness_size","string","false","50k","\-","Maximum number of stick table entries"
    "stickiness_counter","boolean","false","true","\-","Enable stick table counters"
    "stickiness_counter_key","string","false","src","\-","Key for stick table counter"
    "stickiness_length","integer","false","\-","\-","Maximum length of strings in stick table (1-16384)"
    "stickiness_conn_rate_period","string","false","10s","\-","Period for connection rate tracking"
    "stickiness_sess_rate_period","string","false","10s","\-","Period for session rate tracking"
    "stickiness_http_req_rate_period","string","false","10s","\-","Period for HTTP request rate tracking"
    "stickiness_http_err_rate_period","string","false","10s","\-","Period for HTTP error rate tracking"
    "stickiness_bytes_in_rate_period","string","false","1m","\-","Period for bytes in rate tracking"
    "stickiness_bytes_out_rate_period","string","false","1m","\-","Period for bytes out rate tracking"
    "prometheus_enabled","boolean","false","false","\-","Enable Prometheus metrics endpoint"
    "prometheus_path","string","false","/metrics","\-","Path for Prometheus metrics endpoint"
    "connection_behaviour","string","false","http-keep-alive","\-","HTTP connection behavior. Options: http-keep-alive, httpclose, http-server-close"
    "custom_options","string","false","\-","\-","Additional HAProxy frontend configuration lines"
    "linked_actions","list","false","[]","\-","Rules to include in this Public Service"
    "linked_errorfiles","list","false","[]","\-","Error messages to include in this Public Service"

Examples
--------

.. code-block:: yaml

    - name: Create HTTPS frontend with SSL offloading
      oxlorg.opnsense.haproxy_frontend:
        name: 'https_frontend'
        description: 'HTTPS frontend with SSL offloading'
        bind: ['0.0.0.0:443']
        mode: 'http'
        ssl_enabled: true
        ssl_certificates: ['example.com']
        ssl_advanced_enabled: true
        ssl_min_version: 'TLSv1.2'
        ssl_hsts_enabled: true
        ssl_hsts_include_sub_domains: true
        ssl_hsts_max_age: 31536000
        http2_enabled: true
        default_backend: 'web_backend'
        forwarded_header: true
        logging_detailed_log: true

    - name: Create TCP frontend with client auth
      oxlorg.opnsense.haproxy_frontend:
        name: 'secure_tcp_frontend'
        description: 'Secure TCP frontend with client certificates'
        bind: ['0.0.0.0:8443']
        mode: 'ssl'
        ssl_enabled: true
        ssl_certificates: ['internal.com']
        ssl_client_auth_enabled: true
        ssl_client_auth_verify: 'required'
        ssl_client_auth_cas: ['internal-ca']
        tuning_max_connections: 1000
        tuning_timeout_client: '60s'
        basic_auth_enabled: true
        basic_auth_groups: ['admins']
        prometheus_enabled: true

----

.. _haproxy_server:

oxlorg.opnsense.haproxy_server
==============================

Manages HAProxy backend servers with SSL, health checks, connection settings, and advanced configurations.

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "name","string","true","\-","\-","Name to identify this Server"
    "description","string","false","\-","\-","Description for this Server"
    "enabled","boolean","false","true","\-","Enable or disable this server"
    "address","string","false","\-","\-","Servername or IP address of the server"
    "port","integer","false","\-","\-","Port number of the server (1-65535)"
    "checkport","integer","false","\-","\-","Port number for health checks (1-65535)"
    "mode","string","false","active","\-","Server mode. Options: active, backup, disabled"
    "multiplexer_protocol","string","false","unspecified","\-","Protocol for multiplexing. Options: unspecified, fcgi, h2, h1"
    "type","string","false","static","\-","Server type. Options: static, template, unix"
    "service_name","string","false","\-","\-","Service name for DNS SRV record discovery"
    "number","string","false","\-","\-","Server number or range for template servers"
    "linked_resolver","string","false","\-","\-","Resolver configuration for this server"
    "resolver_opts","list","false","[]","\-","Resolver options. Options: allow-dup-ip, ignore-weight, prevent-dup-ip"
    "resolve_prefer","string","false","\-","\-","Prefer IP family for DNS resolution. Options: ipv4, ipv6"
    "ssl_enabled","boolean","false","false","\-","Enable SSL for this server"
    "ssl_verify","boolean","false","true","\-","Enable SSL certificate verification"
    "ssl_ca","list","false","[]","\-","Certificate Authorities for SSL verification"
    "ssl_crl","string","false","\-","\-","Certificate Revocation List for SSL verification"
    "ssl_client_certificate","string","false","\-","\-","Client certificate for SSL authentication"
    "ssl_sni","string","false","\-","\-","SNI hostname for SSL connections"
    "max_connections","integer","false","\-","\-","Maximum connections to this server (0-10000000)"
    "weight","integer","false","\-","\-","Weight for load balancing (0-256)"
    "check_interval","string","false","\-","\-","Interval between health checks"
    "check_down_interval","string","false","\-","\-","Interval between health checks when server is down"
    "source","string","false","\-","\-","Source address when connecting to this server"
    "advanced","string","false","\-","\-","Advanced server options"
    "unix_socket","string","false","\-","\-","Unix socket frontend for this server"

Examples
--------

.. code-block:: yaml

    - name: Create web server with SSL backend
      oxlorg.opnsense.haproxy_server:
        name: 'web1'
        description: 'Web server 1 with SSL backend'
        address: '192.168.1.10'
        port: 443
        mode: 'active'
        ssl_enabled: true
        ssl_verify: true
        ssl_ca: ['internal-ca']
        max_connections: 500
        weight: 100
        check_interval: '10s'
        check_down_interval: '5s'

    - name: Create backup server with health check
      oxlorg.opnsense.haproxy_server:
        name: 'web2_backup'
        description: 'Backup web server'
        address: '192.168.1.11'
        port: 80
        checkport: 8080
        mode: 'backup'
        type: 'static'
        weight: 50
        linked_resolver: 'internal_dns'
        resolve_prefer: 'ipv4'

----

.. _haproxy_healthcheck:

oxlorg.opnsense.haproxy_healthcheck
===================================

Manages HAProxy health monitoring for servers with various check types including HTTP, TCP, and specialized protocols.

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "name","string","true","\-","\-","Name for this health monitor"
    "description","string","false","\-","\-","Optional description for this health monitor"
    "enabled","boolean","false","true","\-","Enable or disable this health check"
    "type","string","false","http","\-","Type of health check. Options: tcp, http, agent, ldap, mysql, pgsql, redis, smtp, esmtp, ssl"
    "interval","string","false","2s","\-","Interval between health checks. Format: 1-8 digits optionally followed by time unit"
    "ssl","string","false","nopref","\-","Force or disable SSL for health checks. Options: nopref, ssl, sslsni, nossl"
    "ssl_sni","string","false","\-","\-","SNI hostname for SSL health checks"
    "checkport","integer","false","\-","\-","Port for health checks, overrides server port (1-65535)"
    "http_method","string","false","options","\-","HTTP method for health check. Options: options, head, get, put, post, delete, trace"
    "http_uri","string","false","\-","\-","URI requested for HTTP health checks"
    "http_version","string","false","http10","\-","HTTP version for health check. Options: http10, http11, http2"
    "http_host","string","false","localhost","\-","Host header value for HTTP health checks"
    "http_expression_enabled","boolean","false","false","\-","Enable HTTP expression matching"
    "http_expression","string","false","\-","\-","Type of HTTP expression matching. Options: status, rstatus, string, rstring"
    "http_negate","boolean","false","false","\-","Negate the HTTP expression result"
    "http_value","string","false","\-","\-","Value to match for HTTP expression"
    "tcp_enabled","boolean","false","false","\-","Enable TCP send/expect functionality"
    "tcp_send_value","string","false","\-","\-","Exact string sent for binary/text based health checks"
    "tcp_match_type","string","false","string","\-","Type of TCP response matching. Options: string, rstring, binary"
    "tcp_negate","boolean","false","false","\-","Negate the TCP match result"
    "tcp_match_value","string","false","\-","\-","Value to match in TCP response"
    "agent_port","integer","false","\-","\-","TCP port for agent checks (1-65535)"
    "mysql_user","string","false","\-","\-","MySQL username for health checks"
    "mysql_post41","boolean","false","false","\-","Use MySQL post-4.1 authentication"
    "pgsql_user","string","false","\-","\-","PostgreSQL username for health checks"
    "smtp_domain","string","false","\-","\-","SMTP domain for health checks"
    "esmtp_domain","string","false","\-","\-","ESMTP domain for health checks"

Examples
--------

.. code-block:: yaml

    - name: Create HTTP health check with custom URI
      oxlorg.opnsense.haproxy_healthcheck:
        name: 'web_health_check'
        description: 'Health check for web servers'
        type: 'http'
        interval: '5s'
        http_method: 'get'
        http_uri: '/health'
        http_host: 'api.example.com'
        http_expression_enabled: true
        http_expression: 'status'
        http_value: '200'

    - name: Create TCP health check with SSL
      oxlorg.opnsense.haproxy_healthcheck:
        name: 'tcp_ssl_check'
        description: 'TCP health check with SSL'
        type: 'tcp'
        ssl: 'ssl'
        ssl_sni: 'secure.example.com'
        checkport: 8443
        tcp_enabled: true
        tcp_send_value: 'PING'
        tcp_match_type: 'string'
        tcp_match_value: 'PONG'

    - name: Create MySQL health check
      oxlorg.opnsense.haproxy_healthcheck:
        name: 'mysql_check'
        description: 'MySQL database health check'
        type: 'mysql'
        mysql_user: 'healthcheck'
        mysql_post41: true
        interval: '10s'

See also: :ref:`modules_haproxy` and :ref:`troubleshooting <modules_haproxy_troubleshooting>`