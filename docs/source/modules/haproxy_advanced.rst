.. _modules_haproxy_advanced:

.. include:: ../_include/head.rst

=================================
HAProxy advanced & extended features
=================================

**STATE**: stable

**COMPATIBILITY**: OPNsense 24.1+

**TESTS**:
`Lua <https://github.com/O-X-L/ansible_opnsense/blob/latest/tests/haproxy_lua.yml>`_ |
`FCGI <https://github.com/O-X-L/ansible_opnsense/blob/latest/tests/haproxy_fcgi.yml>`_ |
`ErrorFile <https://github.com/O-X-L/ansible_opnsense/blob/latest/tests/haproxy_errorfile.yml>`_

**API Docs**: `HAProxy <https://docs.opnsense.org/development/api/plugins/haproxy.html>`_

**HAProxy Docs**: `Lua <https://www.haproxy.com/documentation/haproxy-lua-api/>`_ | `Error pages <https://www.haproxy.com/documentation/haproxy-configuration-tutorials/protocol-support/fastcgi/>`_ | `FastCGI <https://www.haproxy.com/documentation/haproxy-configuration-tutorials/alerts-and-monitoring/error-pages/>`_

These modules manage advanced HAProxy features including Lua scripts, FastCGI applications, and custom error pages.

----

.. _haproxy_lua:

ansibleguy.opnsense.haproxy_lua
=================================

Manages HAProxy Lua scripts for custom logic and processing.

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "name","string","true","\-","\-","Choose a name for this Lua script (must be unique)"
    "description","string","false","\-","\-","You may enter a description here for your reference"
    "enabled","boolean","false","true","\-","Enable or disable the Lua script"
    "preload","boolean","false","true","\-","Preload the script at HAProxy startup"
    "filename_scheme","string","false","id","\-","Filename scheme for the script file (id or name)"
    "content","string","true","\-","\-","Lua script content"

Examples
--------

.. code-block:: yaml

    - name: Create authentication Lua script
      ansibleguy.opnsense.haproxy_lua:
        name: 'auth_script'
        description: 'JWT token authentication'
        enabled: true
        preload: true
        filename_scheme: 'id'
        content: |
          function authenticate_request(txn)
            local headers = txn.http:req_get_headers()
            local auth_header = headers["authorization"]
            if not auth_header then
              core.Info("No authorization header")
              return "UNAUTHORIZED"
            end
            local token = string.match(auth_header, "Bearer%s+(.+)")
            if not token then
              core.Info("Invalid authorization format")
              return "UNAUTHORIZED"
            end
            core.Info("Valid JWT token")
            return "AUTHORIZED"
          end

    - name: Create rate limiting Lua script
      ansibleguy.opnsense.haproxy_lua:
        name: 'rate_limiter'
        description: 'Advanced rate limiting'
        enabled: true
        preload: true
        filename_scheme: 'name'
        content: |
          local rate_limits = {}
          function check_rate_limit(txn)
            local src_ip = txn.sf:src()
            local current_time = core.now()
            local window = 60
            local max_requests = 100
            if not rate_limits[src_ip] then
              rate_limits[src_ip] = {count = 1, start_time = current_time}
              return "ALLOWED"
            end
            local limit_data = rate_limits[src_ip]
            if current_time - limit_data.start_time > window then
              rate_limits[src_ip] = {count = 1, start_time = current_time}
              return "ALLOWED"
            end
            if limit_data.count >= max_requests then
              core.Info("Rate limit exceeded for " .. src_ip)
              return "RATE_LIMITED"
            end
            limit_data.count = limit_data.count + 1
            return "ALLOWED"
          end

    - name: Create request logging Lua script
      ansibleguy.opnsense.haproxy_lua:
        name: 'request_logger'
        description: 'Enhanced request logging'
        enabled: true
        preload: false
        filename_scheme: 'id'
        content: |
          function log_request(txn)
            local method = txn.sf:method()
            local path = txn.sf:path()
            local src_ip = txn.sf:src()
            local user_agent = txn.http:req_get_headers()["user-agent"] or "unknown"
            local log_entry = string.format(
              "Request: %s %s from %s (UA: %s)",
              method, path, src_ip, user_agent
            )
            core.Info(log_entry)
          end

----

.. _haproxy_fcgi:

ansibleguy.opnsense.haproxy_fcgi
=================================

Manages HAProxy FastCGI applications for dynamic content processing.

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "name","string","true","\-","\-","Choose a name for this FastCGI application (must be unique)"
    "description","string","false","\-","\-","You may enter a description here for your reference"
    "enabled","boolean","false","true","\-","Enable or disable the FastCGI application"
    "docroot","string","true","\-","\-","Document root path on the remote host"
    "index","string","false","\-","\-","Default index file name"
    "path_info","string","false","\-","\-","Regular expression to extract script-name and path-info"
    "log_stderr","boolean","false","false","\-","Enable logging of STDERR messages"
    "keep_conn","boolean","false","true","\-","Keep connection open to FastCGI application"
    "get_values","boolean","false","false","\-","Enable retrieval of connection management variables"
    "mpxs_conns","boolean","false","false","\-","Enable support for connection multiplexing"
    "max_reqs","integer","false","\-","\-","Maximum number of concurrent requests (1-100000)"
    "linked_actions","list","false","[]","\-","List of action names to include (automatically resolved to UUIDs)"

Examples
--------

.. code-block:: yaml

    - name: Create PHP-FPM FastCGI application
      ansibleguy.opnsense.haproxy_fcgi:
        name: 'php_fpm_app'
        description: 'PHP-FPM application server'
        enabled: true
        docroot: '/var/www/html'
        index: 'index.php'
        path_info: '^(/.+\.php)(/.*)?$'
        log_stderr: false
        keep_conn: true
        max_reqs: 100

    - name: Create advanced PHP application with logging
      ansibleguy.opnsense.haproxy_fcgi:
        name: 'api_php_app'
        description: 'API PHP application with logging'
        enabled: true
        docroot: '/var/www/api'
        index: 'api.php'
        path_info: '^(/.+\.php)(/.*)?$'
        log_stderr: true
        keep_conn: true
        get_values: true
        mpxs_conns: false
        max_reqs: 50

    - name: Create FastCGI with linked actions
      ansibleguy.opnsense.haproxy_fcgi:
        name: 'secure_php_app'
        description: 'Secure PHP app with rate limiting'
        enabled: true
        docroot: '/var/www/secure'
        index: 'index.php'
        linked_actions: ['rate_limit_action', 'auth_check_action']

----

.. _haproxy_errorfile:

ansibleguy.opnsense.haproxy_errorfile
======================================

Manages HAProxy custom error pages for better user experience.

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "name","string","true","\-","\-","Choose a name for this error file (must be unique)"
    "description","string","false","\-","\-","You may enter a description here for your reference"
    "code","string","true","\-","\-","HTTP error code for this error file (x200, x400, x403, x405, x408, x429, x500, x502, x503, x504)"
    "content","string","true","\-","\-","Complete HTTP response content including headers"

Examples
--------

.. code-block:: yaml

    - name: Create 503 Service Unavailable page
      ansibleguy.opnsense.haproxy_errorfile:
        name: 'custom_503'
        description: 'Maintenance mode page'
        code: 'x503'
        content: |
          HTTP/1.0 503 Service Unavailable
          Content-Type: text/html
          Cache-Control: no-cache
          Connection: close

          <!DOCTYPE html>
          <html>
          <head>
            <title>Maintenance Mode</title>
            <style>
              body { font-family: Arial, sans-serif; background: #f5f5f5; margin: 0; padding: 50px; }
              .container { max-width: 600px; margin: 0 auto; background: white; padding: 40px; border-radius: 10px; text-align: center; }
              h1 { color: #1976d2; margin-bottom: 20px; }
              p { color: #555; line-height: 1.6; }
            </style>
          </head>
          <body>
            <div class="container">
              <h1>🔧 Maintenance in Progress</h1>
              <p>We're currently performing scheduled maintenance to improve our service.</p>
              <p>We'll be back online shortly. Thank you for your patience!</p>
            </div>
          </body>
          </html>

    - name: Create 500 Internal Server Error page
      ansibleguy.opnsense.haproxy_errorfile:
        name: 'custom_500'
        description: 'Internal server error page'
        code: 'x500'
        content: |
          HTTP/1.0 500 Internal Server Error
          Content-Type: text/html
          Cache-Control: no-cache
          Connection: close

          <!DOCTYPE html>
          <html>
          <head>
            <title>Internal Server Error</title>
            <style>
              body { font-family: Arial, sans-serif; background: #f5f5f5; margin: 0; padding: 50px; }
              .error-container { max-width: 500px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; text-align: center; }
              h1 { color: #e53e3e; font-size: 24px; margin-bottom: 15px; }
              p { color: #666; margin-bottom: 20px; }
              .error-code { font-family: monospace; background: #f8f8f8; padding: 10px; border-radius: 4px; display: inline-block; }
            </style>
          </head>
          <body>
            <div class="error-container">
              <h1>Oops! Something went wrong</h1>
              <p>An internal server error has occurred. We've been notified and are working to fix this issue.</p>
              <div class="error-code">HTTP 500</div>
            </div>
          </body>
          </html>

    - name: Create 404 Not Found page
      ansibleguy.opnsense.haproxy_errorfile:
        name: 'custom_404'
        description: 'Page not found'
        code: 'x404'
        content: |
          HTTP/1.0 404 Not Found
          Content-Type: text/html
          Cache-Control: no-cache
          Connection: close

          <!DOCTYPE html>
          <html>
          <head>
            <title>Page Not Found</title>
            <style>
              body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); margin: 0; padding: 0; height: 100vh; display: flex; align-items: center; justify-content: center; }
              .container { background: rgba(255,255,255,0.9); padding: 40px; border-radius: 15px; text-align: center; box-shadow: 0 8px 32px rgba(0,0,0,0.1); }
              h1 { color: #333; font-size: 72px; margin: 0; }
              h2 { color: #555; font-size: 24px; margin: 10px 0; }
              p { color: #666; font-size: 16px; }
              a { color: #667eea; text-decoration: none; }
            </style>
          </head>
          <body>
            <div class="container">
              <h1>404</h1>
              <h2>Page Not Found</h2>
              <p>The page you're looking for doesn't exist.</p>
              <p><a href="/">Return to homepage</a></p>
            </div>
          </body>
          </html>

----

Lua scripting scenarios
************************

Authentication & authorization
-------------------------------

Implement custom authentication logic with Lua:

.. code-block:: yaml

    - name: Authentication Lua scripts
      hosts: opnsense
      tasks:
        - name: Create JWT authentication script
          ansibleguy.opnsense.haproxy_lua:
            name: 'jwt_auth'
            description: 'JWT token validation'
            enabled: true
            preload: true
            filename_scheme: 'id'
            content: |
              -- JWT authentication script
              function validate_jwt(txn)
                local headers = txn.http:req_get_headers()
                local auth_header = headers["authorization"]

                if not auth_header then
                  txn:set_var("txn.auth_status", "missing_header")
                  return "UNAUTHORIZED"
                end

                local token = string.match(auth_header, "Bearer%s+(.+)")
                if not token then
                  txn:set_var("txn.auth_status", "invalid_format")
                  return "UNAUTHORIZED"
                end

                -- Simple token validation (in practice, verify signature)
                if token == "valid-jwt-token-123" then
                  txn:set_var("txn.auth_status", "valid")
                  txn:set_var("txn.user_id", "12345")
                  return "AUTHORIZED"
                else
                  txn:set_var("txn.auth_status", "invalid_token")
                  return "UNAUTHORIZED"
                end
              end

        - name: Create API key validation script
          ansibleguy.opnsense.haproxy_lua:
            name: 'api_key_auth'
            description: 'API key validation'
            enabled: true
            preload: true
            filename_scheme: 'name'
            content: |
              -- API key authentication
              local valid_api_keys = {
                ["key-123"] = {user_id = "user1", permissions = {"read", "write"}},
                ["key-456"] = {user_id = "user2", permissions = {"read"}},
                ["key-789"] = {user_id = "admin", permissions = {"read", "write", "admin"}}
              }

              function validate_api_key(txn)
                local headers = txn.http:req_get_headers()
                local api_key = headers["x-api-key"]

                if not api_key then
                  return "NO_API_KEY"
                end

                local key_data = valid_api_keys[api_key]
                if key_data then
                  txn:set_var("txn.user_id", key_data.user_id)
                  txn:set_var("txn.permissions", table.concat(key_data.permissions, ","))
                  return "VALID_KEY"
                else
                  return "INVALID_KEY"
                end
              end

Request processing & modification
---------------------------------

Process and modify requests using Lua:

.. code-block:: yaml

    - name: Request processing Lua scripts
      hosts: opnsense
      tasks:
        - name: Create request enrichment script
          ansibleguy.opnsense.haproxy_lua:
            name: 'request_enricher'
            description: 'Add request metadata'
            enabled: true
            preload: false
            filename_scheme: 'id'
            content: |
              function enrich_request(txn)
                local headers = txn.http:req_get_headers()
                local method = txn.sf:method()
                local path = txn.sf:path()
                local src_ip = txn.sf:src()

                -- Add request ID
                local request_id = "req_" .. os.time() .. "_" .. math.random(1000, 9999)
                txn.http:req_add_header("X-Request-ID", request_id)

                -- Add geolocation info (simplified)
                local country = "US"  -- In practice, use GeoIP lookup
                txn.http:req_add_header("X-Country", country)

                -- Add processing timestamp
                txn.http:req_add_header("X-Processing-Time", os.date("%Y-%m-%d %H:%M:%S"))

                -- Log request details
                core.Info(string.format("Processing request %s: %s %s from %s",
                  request_id, method, path, src_ip))
              end

        - name: Create load balancing script
          ansibleguy.opnsense.haproxy_lua:
            name: 'smart_lb'
            description: 'Intelligent load balancing'
            enabled: true
            preload: true
            filename_scheme: 'name'
            content: |
              -- Smart load balancing based on request characteristics
              function select_backend(txn)
                local path = txn.sf:path()
                local user_agent = txn.http:req_get_headers()["user-agent"] or ""

                -- Route API requests to API backend
                if string.match(path, "^/api/") then
                  return "api_backend"
                end

                -- Route mobile traffic to mobile backend
                if string.match(user_agent, "Mobile") or string.match(user_agent, "Android") or string.match(user_agent, "iPhone") then
                  return "mobile_backend"
                end

                -- Route admin requests to admin backend
                if string.match(path, "^/admin/") then
                  return "admin_backend"
                end

                -- Default to web backend
                return "web_backend"
              end

----

FastCGI application scenarios
******************************

PHP application deployment
---------------------------

Deploy PHP applications with FastCGI:

.. code-block:: yaml

    - name: PHP FastCGI deployment
      hosts: opnsense
      tasks:
        - name: Create production PHP application
          ansibleguy.opnsense.haproxy_fcgi:
            name: 'prod_php_app'
            description: 'Production PHP application'
            enabled: true
            docroot: '/var/www/production'
            index: 'index.php'
            path_info: '^(/.+\.php)(/.*)?$'
            log_stderr: false
            keep_conn: true
            get_values: false
            mpxs_conns: true
            max_reqs: 200

        - name: Create development PHP application
          ansibleguy.opnsense.haproxy_fcgi:
            name: 'dev_php_app'
            description: 'Development PHP application'
            enabled: true
            docroot: '/var/www/development'
            index: 'index.php'
            path_info: '^(/.+\.php)(/.*)?$'
            log_stderr: true
            keep_conn: false
            get_values: true
            mpxs_conns: false
            max_reqs: 50

        - name: Create API PHP application
          ansibleguy.opnsense.haproxy_fcgi:
            name: 'api_php_app'
            description: 'REST API PHP application'
            enabled: true
            docroot: '/var/www/api'
            index: 'api.php'
            path_info: '^(/api/.+\.php)(/.*)?$'
            log_stderr: true
            keep_conn: true
            max_reqs: 100

High-performance FastCGI setup
-------------------------------

Configure FastCGI for high-performance scenarios:

.. code-block:: yaml

    - name: High-performance FastCGI configuration
      hosts: opnsense
      vars:
        php_pools:
          - {name: 'pool_1', docroot: '/var/www/app1', max_reqs: 300}
          - {name: 'pool_2', docroot: '/var/www/app2', max_reqs: 300}
          - {name: 'pool_3', docroot: '/var/www/app3', max_reqs: 300}
      tasks:
        - name: Create high-performance PHP pools
          ansibleguy.opnsense.haproxy_fcgi:
            name: "{{ item.name }}"
            description: "High-performance PHP pool {{ item.name }}"
            enabled: true
            docroot: "{{ item.docroot }}"
            index: 'index.php'
            path_info: '^(/.+\.php)(/.*)?$'
            log_stderr: false
            keep_conn: true
            get_values: false
            mpxs_conns: true
            max_reqs: "{{ item.max_reqs }}"
          loop: "{{ php_pools }}"

        - name: Create FastCGI with security actions
          ansibleguy.opnsense.haproxy_fcgi:
            name: 'secure_fcgi_app'
            description: 'Secure FastCGI with rate limiting'
            enabled: true
            docroot: '/var/www/secure'
            index: 'secure.php'
            linked_actions: ['rate_limit_check', 'auth_validation', 'security_headers']

----

Custom error page scenarios
****************************

Branded error pages
--------------------

Create branded, professional error pages:

.. code-block:: yaml

    - name: Branded error pages
      hosts: opnsense
      vars:
        brand_colors:
          primary: '#1976d2'
          secondary: '#424242'
          accent: '#ff6b35'
        error_pages:
          - {code: 'x404', title: 'Page Not Found', message: 'The requested page could not be found.'}
          - {code: 'x500', title: 'Server Error', message: 'An internal server error has occurred.'}
          - {code: 'x503', title: 'Service Unavailable', message: 'The service is temporarily unavailable.'}
      tasks:
        - name: Create branded error pages
          ansibleguy.opnsense.haproxy_errorfile:
            name: "branded_{{ item.code }}"
            description: "Branded {{ item.title }} page"
            code: "{{ item.code }}"
            content: |
              HTTP/1.0 {{ item.code | replace('x', '') }} {{ item.title }}
              Content-Type: text/html
              Cache-Control: no-cache
              Connection: close

              <!DOCTYPE html>
              <html>
              <head>
                <title>{{ item.title }} - YourBrand</title>
                <style>
                  body { font-family: 'Segoe UI', Arial, sans-serif; background: #f8f9fa; margin: 0; padding: 0; }
                  .header { background: {{ brand_colors.primary }}; color: white; padding: 20px 0; text-align: center; }
                  .logo { font-size: 24px; font-weight: bold; }
                  .container { max-width: 600px; margin: 50px auto; background: white; padding: 40px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
                  h1 { color: {{ brand_colors.accent }}; font-size: 48px; margin: 0 0 20px 0; text-align: center; }
                  h2 { color: {{ brand_colors.secondary }}; margin-bottom: 20px; }
                  p { color: #666; line-height: 1.6; margin-bottom: 20px; }
                  .footer { text-align: center; margin-top: 30px; color: #999; font-size: 14px; }
                  .btn { display: inline-block; background: {{ brand_colors.primary }}; color: white; padding: 12px 24px; text-decoration: none; border-radius: 4px; margin-top: 20px; }
                </style>
              </head>
              <body>
                <div class="header">
                  <div class="logo">YourBrand</div>
                </div>
                <div class="container">
                  <h1>{{ item.code | replace('x', '') }}</h1>
                  <h2>{{ item.title }}</h2>
                  <p>{{ item.message }}</p>
                  <p>If you continue to experience issues, please contact our support team.</p>
                  <a href="/" class="btn">Return to Home</a>
                  <div class="footer">
                    Error Code: {{ item.code | replace('x', '') }} | Generated at {{ ansible_date_time.iso8601 }}
                  </div>
                </div>
              </body>
              </html>
          loop: "{{ error_pages }}"

Maintenance mode pages
-----------------------

Create informative maintenance mode pages:

.. code-block:: yaml

    - name: Maintenance mode error pages
      hosts: opnsense
      tasks:
        - name: Create scheduled maintenance page
          ansibleguy.opnsense.haproxy_errorfile:
            name: 'maintenance_scheduled'
            description: 'Scheduled maintenance mode'
            code: 'x503'
            content: |
              HTTP/1.0 503 Service Unavailable
              Content-Type: text/html
              Cache-Control: no-cache
              Retry-After: 3600
              Connection: close

              <!DOCTYPE html>
              <html>
              <head>
                <title>Scheduled Maintenance</title>
                <meta http-equiv="refresh" content="300">
                <style>
                  body { font-family: Arial, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); margin: 0; padding: 0; min-height: 100vh; display: flex; align-items: center; justify-content: center; }
                  .maintenance-box { background: rgba(255,255,255,0.95); padding: 50px; border-radius: 15px; text-align: center; box-shadow: 0 10px 30px rgba(0,0,0,0.2); max-width: 500px; }
                  h1 { color: #333; margin-bottom: 20px; }
                  .icon { font-size: 64px; margin-bottom: 20px; }
                  p { color: #666; margin-bottom: 15px; line-height: 1.6; }
                  .countdown { background: #f0f0f0; padding: 15px; border-radius: 8px; margin: 20px 0; font-family: monospace; font-size: 18px; }
                  .progress { width: 100%; height: 6px; background: #e0e0e0; border-radius: 3px; margin-top: 20px; }
                  .progress-bar { height: 100%; background: #667eea; border-radius: 3px; width: 30%; animation: pulse 2s infinite; }
                  @keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.7; } }
                </style>
              </head>
              <body>
                <div class="maintenance-box">
                  <div class="icon">🔧</div>
                  <h1>Scheduled Maintenance</h1>
                  <p>We're currently performing scheduled maintenance to improve our services.</p>
                  <p>Expected completion time: <strong>2 hours</strong></p>
                  <div class="countdown">Page will refresh automatically in 5 minutes</div>
                  <p>Thank you for your patience. We'll be back online shortly!</p>
                  <div class="progress">
                    <div class="progress-bar"></div>
                  </div>
                </div>
              </body>
              </html>

        - name: Create emergency maintenance page
          ansibleguy.opnsense.haproxy_errorfile:
            name: 'maintenance_emergency'
            description: 'Emergency maintenance mode'
            code: 'x503'
            content: |
              HTTP/1.0 503 Service Unavailable
              Content-Type: text/html
              Cache-Control: no-cache
              Retry-After: 1800
              Connection: close

              <!DOCTYPE html>
              <html>
              <head>
                <title>Emergency Maintenance</title>
                <style>
                  body { font-family: Arial, sans-serif; background: #fff; margin: 0; padding: 50px; }
                  .alert { max-width: 600px; margin: 0 auto; padding: 30px; border: 2px solid #ff6b35; border-radius: 10px; background: #fff8f6; }
                  h1 { color: #ff6b35; font-size: 28px; margin-bottom: 20px; }
                  p { color: #333; font-size: 16px; line-height: 1.5; margin-bottom: 15px; }
                  .status { background: #f0f0f0; padding: 15px; border-radius: 5px; margin: 20px 0; }
                  .contact { background: #e8f4fd; padding: 15px; border-radius: 5px; margin-top: 20px; }
                </style>
              </head>
              <body>
                <div class="alert">
                  <h1>🚨 Emergency Maintenance</h1>
                  <p>We're currently experiencing technical difficulties and are working to resolve the issue as quickly as possible.</p>
                  <div class="status">
                    <strong>Status:</strong> Investigating and repairing
                  </div>
                  <p>We apologize for any inconvenience this may cause. Our technical team has been notified and is actively working on a solution.</p>
                  <div class="contact">
                    <strong>Need immediate assistance?</strong><br>
                    Email: support@yourcompany.com<br>
                    Phone: +1 (555) 123-4567
                  </div>
                </div>
              </body>
              </html>

----

Best practices
**************

Lua script optimization
------------------------

**Performance considerations**

- Preload frequently used scripts for better performance
- Keep scripts lightweight and focused
- Cache expensive operations where possible
- Use appropriate variable scopes (proc, sess, txn, req, res)

**Security guidelines**

- Validate all input data in Lua scripts
- Avoid exposing sensitive information in logs
- Use secure coding practices for authentication logic
- Regularly review and update scripts

.. code-block:: yaml

    - name: Optimized Lua script practices
      hosts: opnsense
      tasks:
        - name: Create optimized authentication script
          ansibleguy.opnsense.haproxy_lua:
            name: 'optimized_auth'
            description: 'Optimized authentication with caching'
            enabled: true
            preload: true  # Preload for performance
            filename_scheme: 'id'
            content: |
              -- Optimized authentication with simple caching
              local auth_cache = {}
              local cache_ttl = 300  -- 5 minutes

              function validate_with_cache(txn)
                local token = get_auth_token(txn)
                if not token then return "NO_TOKEN" end

                local current_time = core.now()
                local cached_result = auth_cache[token]

                -- Check cache first
                if cached_result and (current_time - cached_result.timestamp) < cache_ttl then
                  txn:set_var("txn.user_id", cached_result.user_id)
                  return cached_result.status
                end

                -- Perform validation (simplified)
                local is_valid = validate_token(token)
                if is_valid then
                  auth_cache[token] = {
                    status = "VALID",
                    user_id = "user123",
                    timestamp = current_time
                  }
                  txn:set_var("txn.user_id", "user123")
                  return "VALID"
                else
                  return "INVALID"
                end
              end

              function get_auth_token(txn)
                local headers = txn.http:req_get_headers()
                local auth_header = headers["authorization"]
                if auth_header then
                  return string.match(auth_header, "Bearer%s+(.+)")
                end
                return nil
              end

              function validate_token(token)
                -- Simplified validation logic
                return token == "valid-token-123"
              end

FastCGI deployment strategies
-----------------------------

**Resource management**

- Set appropriate max_reqs based on backend capacity
- Use connection multiplexing for high-traffic applications
- Monitor stderr logs for debugging
- Keep connections alive for better performance

**Action integration**

- Create actions before linking them to FCGI applications
- Use compatible action types (fcgi_pass_header, fcgi_set_param)
- Test action chains thoroughly
- Document action dependencies

.. code-block:: yaml

    - name: Production FastCGI deployment
      hosts: opnsense
      tasks:
        # Create actions first
        - name: Create FCGI security actions
          ansibleguy.opnsense.haproxy_action:
            name: "{{ item.name }}"
            description: "{{ item.description }}"
            test_type: 'if'
            type: "{{ item.type }}"
            "{{ item.param_name }}": "{{ item.param_value }}"
          loop:
            - {name: 'fcgi_security_header', description: 'Add security header', type: 'fcgi_pass_header', param_name: 'fcgi_pass_header', param_value: 'X-Security-Check: enabled'}
            - {name: 'fcgi_app_param', description: 'Set app parameter', type: 'fcgi_set_param', param_name: 'fcgi_set_param', param_value: 'APP_ENV=production'}

        # Deploy FCGI with actions
        - name: Deploy production FCGI application
          ansibleguy.opnsense.haproxy_fcgi:
            name: 'production_app'
            description: 'Production PHP application'
            enabled: true
            docroot: '/var/www/production'
            index: 'app.php'
            path_info: '^(/.+\.php)(/.*)?$'
            log_stderr: false
            keep_conn: true
            get_values: false
            mpxs_conns: true
            max_reqs: 500
            linked_actions: ['fcgi_security_header', 'fcgi_app_param']

Error page design guidelines
----------------------------

**User experience**

- Provide clear, helpful error messages
- Include contact information for support
- Use consistent branding and styling
- Offer actionable next steps

**Technical considerations**

- Include proper HTTP headers and status codes
- Set appropriate cache-control headers
- Consider retry-after headers for 503 errors
- Keep page size reasonable for fast loading

.. code-block:: yaml

    - name: User-friendly error page design
      hosts: opnsense
      tasks:
        - name: Create comprehensive 404 page
          ansibleguy.opnsense.haproxy_errorfile:
            name: 'helpful_404'
            description: 'User-friendly 404 page'
            code: 'x404'
            content: |
              HTTP/1.0 404 Not Found
              Content-Type: text/html
              Cache-Control: no-cache, no-store, must-revalidate
              Expires: 0
              Connection: close

              <!DOCTYPE html>
              <html>
              <head>
                <title>Page Not Found - YourSite</title>
                <meta name="viewport" content="width=device-width, initial-scale=1">
                <style>
                  body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #f8f9fa; margin: 0; padding: 20px; }
                  .container { max-width: 600px; margin: 50px auto; background: white; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.1); overflow: hidden; }
                  .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 40px; text-align: center; }
                  .content { padding: 40px; }
                  h1 { font-size: 48px; margin: 0; font-weight: 300; }
                  h2 { color: #333; margin: 0 0 20px 0; }
                  p { color: #666; line-height: 1.6; margin-bottom: 20px; }
                  .suggestions { background: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0; }
                  .suggestions ul { margin: 0; padding-left: 20px; }
                  .contact { background: #e8f4fd; padding: 20px; border-radius: 8px; margin-top: 20px; }
                  .btn { display: inline-block; background: #667eea; color: white; padding: 12px 24px; text-decoration: none; border-radius: 6px; margin: 10px 10px 0 0; }
                  .btn:hover { background: #5a6fd8; }
                </style>
              </head>
              <body>
                <div class="container">
                  <div class="header">
                    <h1>404</h1>
                    <h2>Page Not Found</h2>
                  </div>
                  <div class="content">
                    <p>We're sorry, but the page you're looking for doesn't exist.</p>
                    <div class="suggestions">
                      <strong>Here are some suggestions:</strong>
                      <ul>
                        <li>Check the URL for typos</li>
                        <li>Go back to the previous page</li>
                        <li>Visit our homepage</li>
                        <li>Use the search function</li>
                      </ul>
                    </div>
                    <div>
                      <a href="/" class="btn">Go Home</a>
                      <a href="/search" class="btn">Search</a>
                      <a href="/contact" class="btn">Contact Support</a>
                    </div>
                    <div class="contact">
                      <strong>Still need help?</strong><br>
                      Contact our support team at <a href="mailto:support@yoursite.com">support@yoursite.com</a>
                    </div>
                  </div>
                </div>
              </body>
              </html>

----

Troubleshooting
***************

Lua script issues
------------------

**Common problems**

- **Script syntax errors**: Validate Lua syntax before deployment
- **Runtime errors**: Check HAProxy logs for Lua error messages
- **Performance issues**: Profile script execution time
- **Variable scope problems**: Ensure correct variable scope usage

**Debugging steps**

1. Test Lua scripts in standalone Lua interpreter first
2. Use core.Info() for debugging output in scripts
3. Check HAProxy error logs for script failures
4. Validate script preload settings

FastCGI connectivity issues
---------------------------

**Connection problems**

- **Backend unreachable**: Verify FastCGI server is running
- **Path configuration**: Check docroot and index file settings
- **Permission issues**: Ensure proper file permissions
- **Resource limits**: Check max_reqs and connection settings

**Action linking problems**

The HAProxy FCGI module automatically resolves action names to UUIDs. If you encounter errors like "Related action item not found":

1. Create actions before linking them to FCGI applications
2. Ensure action names match exactly (case-sensitive)
3. Verify actions are of compatible types (fcgi_pass_header, fcgi_set_param)
4. Check action configuration is valid

Error page rendering issues
---------------------------

**HTTP response problems**

- **Invalid headers**: Ensure proper HTTP response format
- **Content-Type missing**: Always specify Content-Type header
- **Cache issues**: Set appropriate cache-control headers
- **Character encoding**: Specify charset in Content-Type

.. code-block:: yaml

    - name: Troubleshooting advanced modules
      hosts: opnsense
      tasks:
        # Test Lua script syntax
        - name: Create minimal test Lua script
          ansibleguy.opnsense.haproxy_lua:
            name: 'test_lua'
            description: 'Test Lua script'
            enabled: true
            preload: false
            filename_scheme: 'id'
            content: |
              function test_function(txn)
                core.Info("Test Lua script is working")
                return "OK"
              end

        # Test FCGI with minimal configuration
        - name: Create minimal test FCGI
          ansibleguy.opnsense.haproxy_fcgi:
            name: 'test_fcgi'
            description: 'Test FCGI application'
            enabled: true
            docroot: '/var/www/test'

        # Test error page with basic content
        - name: Create minimal test error page
          ansibleguy.opnsense.haproxy_errorfile:
            name: 'test_error'
            description: 'Test error page'
            code: 'x503'
            content: |
              HTTP/1.0 503 Service Unavailable
              Content-Type: text/html
              Connection: close

              <html><body><h1>Test Error Page</h1></body></html>

        # Clean up test objects
        - name: Remove test objects
          block:
            - name: Remove test Lua script
              ansibleguy.opnsense.haproxy_lua:
                name: 'test_lua'
                state: absent

            - name: Remove test FCGI
              ansibleguy.opnsense.haproxy_fcgi:
                name: 'test_fcgi'
                state: absent

            - name: Remove test error page
              ansibleguy.opnsense.haproxy_errorfile:
                name: 'test_error'
                state: absent

See also: :ref:`troubleshooting <troubleshooting>`