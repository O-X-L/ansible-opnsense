.. _modules_acmeclient:

.. include:: ../_include/head.rst

===========
ACME Client
===========

**STATE**: unstable

**TESTS**: `acme_certificate <https://github.com/ansibleguy/collection_opnsense/blob/latest/tests/acme_certificate.yml>`_

**API Docs**: `Plugins - Acmeclient <https://docs.opnsense.org/development/api/plugins/acmeclient.html>`_


Contribution
************

Thanks to `@jiuka <https://github.com/jiuka>`_ for developing this module!

Prerequisites
*************

You need to install the FRR plugin:

```
os-acme-client
```

You can also install it using the package module.

Definition
**********

.. include:: ../_include/param_basic.rst

ansibleguy.opnsense.acme_general
====================================

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "enable","boolean","false","false","\-","Enable ACME client plugin."
    "auto_renewal","boolean","false","true","\-","Enable automatic renewal for certificates to prevent expiration."
    "challenge_port","integer","false","43580","\-","When using HTTP-01 as challenge type, a local webserver is used to provide acme challenge data to the ACME CA. The local webserver is NOT directly exposed to the outside and should NOT use port 80 or any other well-known port. This setting allows you to change the local port of this webserver in case it interferes with another local service."
    "tls_challenge_port","integer","false","43581","\-","The service port when using TLS-ALPN-01 as challenge type. It works similar to the HTTP-01 challenge type."
    "restart_timeout","integer","false","600","\-","The maximum time in seconds to wait for an automation to complete. When the timeout is reached the command is forcefully aborted."
    "haproxy_integration","boolean","false","false","\-","Enable automatic integration with the OPNsense HAProxy plugin. **Requires that the OPNsense HAProxy plugin is installed.** This will automatically add the required backend, server, action and ACL for you. You just need to select your HAProxy frontend when configuring the certificate or challenge type."
    "log_level","string","false","normal","\-","Specifies the log level for acme.sh. Other log levels then 'default' add 'information' are for debug purposes, but be aware that this will break the log formatting in the GUI. Levels 'debug2' and 'debug3' log successively deeper log messages from the acme.sh including messages from DNS-01 DNSAPI scripts. One of: 'normal', 'extended', 'debug', 'debug2', 'debug3'"
    "show_intro","boolean","false","true","\-","Disable to hide all introduction pages."
    "reload","boolean","false","true","\-", .. include:: ../_include/param_reload.rst


ansibleguy.opnsense.acme_account
================================

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "name","string","true","\-","\-","Name to identify this account."
    "description","string","false","\-","desc","Description for this account."
    "email","string","false","\-","\-","E-mail address for this account."
    "ca","string","false","letsencrypt","\-","One of: 'buypass', 'buypass_test', 'google', 'google_test', 'letsencrypt', 'letsencrypt_test', 'sslcom', 'zerossl', 'custom'"
    "custom_ca","string","false","","\-","The HTTPS URL of the custom ACME CA that should be used for this account and all associated certificates. For example: 'https://ca.internal/acme/directory'"
    "eab_kid","string","false","\-","\-","An value provided by the CA when using ACME External Account Binding (EAB)."
    "eab_hmac","string","false","\-","\-","An value provided by the CA when using ACME External Account Binding (EAB)."
    "register","boolean","false","false","\-","Register the selected account with the configured ACME CA."
    "reload","boolean","false","true","\-", .. include:: ../_include/param_reload.rst


ansibleguy.opnsense.acme_validation
===================================

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "name","string","true","\-","\-","Name to identify this validation."
    "description","string","false","\-","desc","Description for this validation."
    "method","string","false","dns01","\-","Set the ACME challenge type. One of: 'http01', 'dns01', 'tlsalpn01'"
    "http_service","string","false","opnsense","\-","HTTP Service to use for 'http01' validation. One of: 'opnsense', 'haproxy'"
    "http_opn_autodiscovery","boolean","false","true","\-","The FQDN's used in your certificate must currently point to an official IP address. Choose this option to let OPNsense try to auto-discover these IP addresses. This will lead to a short downtime of the service that is normally used with this IP address."
    "http_opn_interface","string","false","\-","\-","The FQDN's used in your certificate must currently point to an official IP address. Choose the interface where this IP address is currently configured. OPNsense will automatically create a temporary port forward to allow the ACME validation to succeed. This will lead to a short downtime of the service that is normally used with this IP address."
    "http_opn_ipaddresses","list","false","\-","\-","The FQDN's used in your certificate must currently point to one or more official IP addresses. Enter the all of these IP addresses here. OPNsense will automatically create a temporary port forward to allow the ACME validation to succeed. This will lead to a short downtime of the service that is normally used with these IP addresses."
    "http_haproxy_inject","boolean","false","true","\-","Automatically inject config into the local HAProxy instance to let it serve acme challanges without service interruption. Of course, adding the configuration requires a short restart of the HAProxy service."
    "http_haproxy_frontends","list","false","\-","\-","Choose the local HAProxy frontends. They will automatically be configured to redirect acme challenges to the internal acme client. The HAProxy service will automatically be restarted if a certificate was renewed."
    "tlsalpn_acme_autodiscovery","boolean","false","true","\-","The FQDN's used in your certificate must currently point to an official IP address. Choose this option to let OPNsense try to auto-discover these IP addresses. This will lead to a short downtime of the service that is normally used with this IP address."
    "tlsalpn_acme_interface","string","false","\-","\-","The FQDN's used in your certificate must currently point to an official IP address. Choose the interface where this IP address is currently configured. OPNsense will automatically create a temporary port forward to allow the ACME validation to succeed. This will lead to a short downtime of the service that is normally used with this IP address."
    "tlsalpn_acme_ipaddresses","list","false","\-","\-","The FQDN's used in your certificate must currently point to one or more official IP addresses. Enter the all of these IP addresses here. OPNsense will automatically create a temporary port forward to allow the ACME validation to succeed. This will lead to a short downtime of the service that is normally used with these IP addresses."
    "dns_service","string","false","dns_freedns","\-","DNS Service. One of: 'dns_1984hosting', 'dns_acmedns', 'dns_acmeproxy', 'dns_active24', 'dns_ad', 'dns_ali', 'dns_kas', 'dns_arvan', 'dns_artfiles', 'dns_aurora', 'dns_autodns', 'dns_aws', 'dns_azure', 'dns_bunny', 'dns_cloudns', 'dns_cf', 'dns_cx', 'dns_cn', 'dns_conoha', 'dns_constellix', 'dns_cpanel', 'dns_cyon', 'dns_ddnss', 'dns_desec', 'dns_dgon', 'dns_da', 'dns_dnsexit', 'dns_dnshome', 'dns_dnsimple', 'dns_dnsservices', 'dns_domeneshop', 'dns_me', 'dns_dp', 'dns_doapi', 'dns_do', 'dns_dreamhost', 'dns_duckdns', 'dns_dyn', 'dns_dynu', 'dns_dynv6', 'dns_easydns', 'dns_euserv', 'dns_exoscale', 'dns_fornex', 'dns_freedns', 'dns_gandi_livedns', 'dns_gd', 'dns_gcloud', 'dns_googledomains', 'dns_gdnsdk', 'dns_hetzner', 'dns_hexonet', 'dns_hostingde', 'dns_he', 'dns_infoblox', 'dns_infomaniak', 'dns_internetbs', 'dns_inwx', 'dns_ionos', 'dns_ipv64', 'dns_ispconfig', 'dns_jd', 'dns_joker', 'dns_kinghost', 'dns_knot', 'dns_leaseweb', 'dns_lexicon', 'dns_limacity', 'dns_linode', 'dns_linode_v4', 'dns_loopia', 'dns_lua', 'dns_miab', 'dns_mydnsjp', 'dns_mythic_beasts', 'dns_namecom', 'dns_namecheap', 'dns_namesilo', 'dns_nederhost', 'dns_netcup', 'dns_nic', 'dns_njalla', 'dns_nsone', 'dns_nsupdate', 'dns_online', 'dns_opnsense', 'dns_oci', 'dns_ovh', 'dns_pdns', 'dns_pleskxml', 'dns_pointhq', 'dns_porkbun', 'dns_rackspace', 'dns_rage4', 'dns_regru', 'dns_schlundtech', 'dns_selectel', 'dns_selfhost', 'dns_servercow', 'dns_simply', 'dns_transip', 'dns_udr', 'dns_unoeuro', 'dns_variomedia', 'dns_vscale', 'dns_vultr', 'dns_world4you', 'dns_yandex', 'dns_zilore', 'dns_zone', 'dns_zonomi'"
    "dns_sleep","integer","false","0","\-","The time in seconds to wait for all the TXT records to take effect after adding them to the DNS API. Defaults to 0 seconds, which causes Acme Client to check public DNS services every 10 seconds for up to 20 minutes. If set to a non-zero value, a fixed DNS sleep time will be used and the local DNS servers will be queried instead. A DNS sleep time of 120 seconds or more is recommended for some DNS APIs."
    "dns_active24_token","string","false","\-","\-","Paramater token for dns_service 'dns_active24'"
    "dns_ad_key","string","false","\-","\-","Paramater key for dns_service 'dns_ad'"
    "dns_ali_key","string","false","\-","\-","Paramater key for dns_service 'dns_ali'"
    "dns_ali_secret","string","false","\-","\-","Paramater secret for dns_service 'dns_ali'"
    "dns_autodns_user","string","false","\-","\-","Paramater user for dns_service 'dns_autodns'"
    "dns_autodns_password","string","false","\-","\-","Paramater password for dns_service 'dns_autodns'"
    "dns_autodns_context","string","false","\-","\-","Paramater context for dns_service 'dns_autodns'"
    "dns_aws_id","string","false","\-","\-","Paramater id for dns_service 'dns_aws'"
    "dns_aws_secret","string","false","\-","\-","Paramater secret for dns_service 'dns_aws'"
    "dns_azuredns_subscriptionid","string","false","\-","\-","Paramater subscriptionid for dns_service 'dns_azuredns'"
    "dns_azuredns_tenantid","string","false","\-","\-","Paramater tenantid for dns_service 'dns_azuredns'"
    "dns_azuredns_appid","string","false","\-","\-","Paramater appid for dns_service 'dns_azuredns'"
    "dns_azuredns_clientsecret","string","false","\-","\-","Paramater clientsecret for dns_service 'dns_azuredns'"
    "dns_bunny_api_key","string","false","\-","\-","Paramater api_key for dns_service 'dns_bunny'"
    "dns_cf_email","string","false","\-","\-","Paramater email for dns_service 'dns_cf'"
    "dns_cf_key","string","false","\-","\-","Paramater key for dns_service 'dns_cf'"
    "dns_cf_token","string","false","\-","\-","Paramater token for dns_service 'dns_cf'"
    "dns_cf_account_id","string","false","\-","\-","Paramater account_id for dns_service 'dns_cf'"
    "dns_cf_zone_id","string","false","\-","\-","Paramater zone_id for dns_service 'dns_cf'"
    "dns_cloudns_auth_id","string","false","\-","\-","Paramater auth_id for dns_service 'dns_cloudns'"
    "dns_cloudns_sub_auth_id","string","false","\-","\-","Paramater sub_auth_id for dns_service 'dns_cloudns'"
    "dns_cloudns_auth_password","string","false","\-","\-","Paramater auth_password for dns_service 'dns_cloudns'"
    "dns_cx_key","string","false","\-","\-","Paramater key for dns_service 'dns_cx'"
    "dns_cx_secret","string","false","\-","\-","Paramater secret for dns_service 'dns_cx'"
    "dns_cyon_user","string","false","\-","\-","Paramater user for dns_service 'dns_cyon'"
    "dns_cyon_password","string","false","\-","\-","Paramater password for dns_service 'dns_cyon'"
    "dns_da_key","string","false","\-","\-","Paramater key for dns_service 'dns_da'"
    "dns_da_insecure","boolean","false","false","\-","Paramater insecure for dns_service 'dns_da'"
    "dns_ddnss_token","string","false","\-","\-","Paramater token for dns_service 'dns_ddnss'"
    "dns_dgon_key","string","false","\-","\-","Paramater key for dns_service 'dns_dgon'"
    "dns_dnsexit_auth_user","string","false","\-","\-","Paramater auth_user for dns_service 'dns_dnsexit'"
    "dns_dnsexit_auth_pass","string","false","\-","\-","Paramater auth_pass for dns_service 'dns_dnsexit'"
    "dns_dnsexit_api","string","false","\-","\-","Paramater api for dns_service 'dns_dnsexit'"
    "dns_dnshome_password","string","false","\-","\-","Paramater password for dns_service 'dns_dnshome'"
    "dns_dnshome_subdomain","string","false","\-","\-","Paramater subdomain for dns_service 'dns_dnshome'"
    "dns_dnsimple_token","string","false","\-","\-","Paramater token for dns_service 'dns_dnsimple'"
    "dns_dnsservices_user","string","false","\-","\-","Paramater user for dns_service 'dns_dnsservices'"
    "dns_dnsservices_password","string","false","\-","\-","Paramater password for dns_service 'dns_dnsservices'"
    "dns_doapi_token","string","false","\-","\-","Paramater token for dns_service 'dns_doapi'"
    "dns_do_pid","string","false","\-","\-","Paramater pid for dns_service 'dns_do'"
    "dns_do_password","string","false","\-","\-","Paramater password for dns_service 'dns_do'"
    "dns_domeneshop_token","string","false","\-","\-","Paramater token for dns_service 'dns_domeneshop'"
    "dns_domeneshop_secret","string","false","\-","\-","Paramater secret for dns_service 'dns_domeneshop'"
    "dns_dp_id","string","false","\-","\-","Paramater id for dns_service 'dns_dp'"
    "dns_dp_key","string","false","\-","\-","Paramater key for dns_service 'dns_dp'"
    "dns_duckdns_token","string","false","\-","\-","Paramater token for dns_service 'dns_duckdns'"
    "dns_dyn_customer","string","false","\-","\-","Paramater customer for dns_service 'dns_dyn'"
    "dns_dyn_user","string","false","\-","\-","Paramater user for dns_service 'dns_dyn'"
    "dns_dyn_password","string","false","\-","\-","Paramater password for dns_service 'dns_dyn'"
    "dns_dynu_clientid","string","false","\-","\-","Paramater clientid for dns_service 'dns_dynu'"
    "dns_dynu_secret","string","false","\-","\-","Paramater secret for dns_service 'dns_dynu'"
    "dns_freedns_user","string","false","\-","\-","Paramater user for dns_service 'dns_freedns'"
    "dns_freedns_password","string","false","\-","\-","Paramater password for dns_service 'dns_freedns'"
    "dns_fornex_api_key","string","false","\-","\-","Paramater api_key for dns_service 'dns_fornex'"
    "dns_gandi_livedns_key","string","false","\-","\-","Paramater livedns_key for dns_service 'dns_gandi'"
    "dns_gandi_livedns_token","string","false","\-","\-","Paramater livedns_token for dns_service 'dns_gandi'"
    "dns_gcloud_key","string","false","\-","\-","Paramater key for dns_service 'dns_gcloud'"
    "dns_googledomains_access_token","string","false","\-","\-","Paramater access_token for dns_service 'dns_googledomains'"
    "dns_googledomains_zone","string","false","\-","\-","Paramater zone for dns_service 'dns_googledomains'"
    "dns_gd_key","string","false","\-","\-","Paramater key for dns_service 'dns_gd'"
    "dns_gd_secret","string","false","\-","\-","Paramater secret for dns_service 'dns_gd'"
    "dns_hostingde_server","string","false","\-","\-","Paramater server for dns_service 'dns_hostingde'"
    "dns_hostingde_apiKey","string","false","\-","\-","Paramater apiKey for dns_service 'dns_hostingde'"
    "dns_he_user","string","false","\-","\-","Paramater user for dns_service 'dns_he'"
    "dns_he_password","string","false","\-","\-","Paramater password for dns_service 'dns_he'"
    "dns_infoblox_credentials","string","false","\-","\-","Paramater credentials for dns_service 'dns_infoblox'"
    "dns_infoblox_server","string","false","\-","\-","Paramater server for dns_service 'dns_infoblox'"
    "dns_inwx_user","string","false","\-","\-","Paramater user for dns_service 'dns_inwx'"
    "dns_inwx_password","string","false","\-","\-","Paramater password for dns_service 'dns_inwx'"
    "dns_inwx_shared_secret","string","false","\-","\-","Paramater shared_secret for dns_service 'dns_inwx'"
    "dns_ionos_prefix","string","false","\-","\-","Paramater prefix for dns_service 'dns_ionos'"
    "dns_ionos_secret","string","false","\-","\-","Paramater secret for dns_service 'dns_ionos'"
    "dns_ipv64_token","string","false","\-","\-","Paramater token for dns_service 'dns_ipv64'"
    "dns_ispconfig_user","string","false","\-","\-","Paramater user for dns_service 'dns_ispconfig'"
    "dns_ispconfig_password","string","false","\-","\-","Paramater password for dns_service 'dns_ispconfig'"
    "dns_ispconfig_api","string","false","\-","\-","Paramater api for dns_service 'dns_ispconfig'"
    "dns_ispconfig_insecure","boolean","false","false","\-","Paramater insecure for dns_service 'dns_ispconfig'"
    "dns_jd_id","string","false","\-","\-","Paramater id for dns_service 'dns_jd'"
    "dns_jd_region","string","false","\-","\-","Paramater region for dns_service 'dns_jd'"
    "dns_jd_secret","string","false","\-","\-","Paramater secret for dns_service 'dns_jd'"
    "dns_joker_username","string","false","\-","\-","Paramater username for dns_service 'dns_joker'"
    "dns_joker_password","string","false","\-","\-","Paramater password for dns_service 'dns_joker'"
    "dns_kinghost_username","string","false","\-","\-","Paramater username for dns_service 'dns_kinghost'"
    "dns_kinghost_password","string","false","\-","\-","Paramater password for dns_service 'dns_kinghost'"
    "dns_knot_server","string","false","\-","\-","Paramater server for dns_service 'dns_knot'"
    "dns_knot_key","string","false","\-","\-","Paramater key for dns_service 'dns_knot'"
    "dns_limacity_apikey","string","false","\-","\-","Paramater apikey for dns_service 'dns_limacity'"
    "dns_linode_v4_key","string","false","\-","\-","Paramater v4_key for dns_service 'dns_linode'"
    "dns_loopia_api","string","false","\-","\-","Paramater api for dns_service 'dns_loopia'"
    "dns_loopia_user","string","false","\-","\-","Paramater user for dns_service 'dns_loopia'"
    "dns_loopia_password","string","false","\-","\-","Paramater password for dns_service 'dns_loopia'"
    "dns_lua_email","string","false","\-","\-","Paramater email for dns_service 'dns_lua'"
    "dns_lua_key","string","false","\-","\-","Paramater key for dns_service 'dns_lua'"
    "dns_miab_user","string","false","\-","\-","Paramater user for dns_service 'dns_miab'"
    "dns_miab_password","string","false","\-","\-","Paramater password for dns_service 'dns_miab'"
    "dns_miab_server","string","false","\-","\-","Paramater server for dns_service 'dns_miab'"
    "dns_me_key","string","false","\-","\-","Paramater key for dns_service 'dns_me'"
    "dns_me_secret","string","false","\-","\-","Paramater secret for dns_service 'dns_me'"
    "dns_mydnsjp_masterid","string","false","\-","\-","Paramater masterid for dns_service 'dns_mydnsjp'"
    "dns_mydnsjp_password","string","false","\-","\-","Paramater password for dns_service 'dns_mydnsjp'"
    "dns_mythic_beasts_key","string","false","\-","\-","Paramater beasts_key for dns_service 'dns_mythic'"
    "dns_mythic_beasts_secret","string","false","\-","\-","Paramater beasts_secret for dns_service 'dns_mythic'"
    "dns_namecheap_user","string","false","\-","\-","Paramater user for dns_service 'dns_namecheap'"
    "dns_namecheap_api","string","false","\-","\-","Paramater api for dns_service 'dns_namecheap'"
    "dns_namecheap_sourceip","string","false","\-","\-","Paramater sourceip for dns_service 'dns_namecheap'"
    "dns_namecom_user","string","false","\-","\-","Paramater user for dns_service 'dns_namecom'"
    "dns_namecom_token","string","false","\-","\-","Paramater token for dns_service 'dns_namecom'"
    "dns_namesilo_key","string","false","\-","\-","Paramater key for dns_service 'dns_namesilo'"
    "dns_nederhost_key","string","false","\-","\-","Paramater key for dns_service 'dns_nederhost'"
    "dns_netcup_cid","string","false","\-","\-","Paramater cid for dns_service 'dns_netcup'"
    "dns_netcup_key","string","false","\-","\-","Paramater key for dns_service 'dns_netcup'"
    "dns_netcup_pw","string","false","\-","\-","Paramater pw for dns_service 'dns_netcup'"
    "dns_njalla_token","string","false","\-","\-","Paramater token for dns_service 'dns_njalla'"
    "dns_nsone_key","string","false","\-","\-","Paramater key for dns_service 'dns_nsone'"
    "dns_nsupdate_server","string","false","\-","\-","Paramater server for dns_service 'dns_nsupdate'"
    "dns_nsupdate_zone","string","false","\-","\-","Paramater zone for dns_service 'dns_nsupdate'"
    "dns_nsupdate_key","string","false","\-","\-","Paramater key for dns_service 'dns_nsupdate'"
    "dns_oci_cli_user","string","false","\-","\-","Paramater cli_user for dns_service 'dns_oci'"
    "dns_oci_cli_tenancy","string","false","\-","\-","Paramater cli_tenancy for dns_service 'dns_oci'"
    "dns_oci_cli_region","string","false","\-","\-","Paramater cli_region for dns_service 'dns_oci'"
    "dns_oci_cli_key","string","false","\-","\-","Paramater cli_key for dns_service 'dns_oci'"
    "dns_online_key","string","false","\-","\-","Paramater key for dns_service 'dns_online'"
    "dns_opnsense_host","string","false","localhost","\-","Paramater host for dns_service 'dns_opnsense'"
    "dns_opnsense_port","integer","false","443","\-","Paramater port for dns_service 'dns_opnsense'"
    "dns_opnsense_key","string","false","\-","\-","Paramater key for dns_service 'dns_opnsense'"
    "dns_opnsense_token","string","false","\-","\-","Paramater token for dns_service 'dns_opnsense'"
    "dns_opnsense_insecure","boolean","false","false","\-","Paramater insecure for dns_service 'dns_opnsense'"
    "dns_ovh_app_key","string","false","\-","\-","Paramater app_key for dns_service 'dns_ovh'"
    "dns_ovh_app_secret","string","false","\-","\-","Paramater app_secret for dns_service 'dns_ovh'"
    "dns_ovh_consumer_key","string","false","\-","\-","Paramater consumer_key for dns_service 'dns_ovh'"
    "dns_ovh_endpoint","string","false","\-","\-","Paramater endpoint for dns_service 'dns_ovh'"
    "dns_pleskxml_user","string","false","\-","\-","Paramater user for dns_service 'dns_pleskxml'"
    "dns_pleskxml_pass","string","false","\-","\-","Paramater pass for dns_service 'dns_pleskxml'"
    "dns_pleskxml_uri","string","false","\-","\-","Paramater uri for dns_service 'dns_pleskxml'"
    "dns_pdns_url","string","false","\-","\-","Paramater url for dns_service 'dns_pdns'"
    "dns_pdns_serverid","string","false","\-","\-","Paramater serverid for dns_service 'dns_pdns'"
    "dns_pdns_token","string","false","\-","\-","Paramater token for dns_service 'dns_pdns'"
    "dns_porkbun_key","string","false","\-","\-","Paramater key for dns_service 'dns_porkbun'"
    "dns_porkbun_secret","string","false","\-","\-","Paramater secret for dns_service 'dns_porkbun'"
    "dns_sl_key","string","false","\-","\-","Paramater key for dns_service 'dns_sl'"
    "dns_selfhost_user","string","false","\-","\-","Paramater user for dns_service 'dns_selfhost'"
    "dns_selfhost_password","string","false","\-","\-","Paramater password for dns_service 'dns_selfhost'"
    "dns_selfhost_map","string","false","\-","\-","Paramater map for dns_service 'dns_selfhost'"
    "dns_servercow_username","string","false","\-","\-","Paramater username for dns_service 'dns_servercow'"
    "dns_servercow_password","string","false","\-","\-","Paramater password for dns_service 'dns_servercow'"
    "dns_simply_api_key","string","false","\-","\-","Paramater api_key for dns_service 'dns_simply'"
    "dns_simply_account_name","string","false","\-","\-","Paramater account_name for dns_service 'dns_simply'"
    "dns_transip_username","string","false","\-","\-","Paramater username for dns_service 'dns_transip'"
    "dns_transip_key","string","false","\-","\-","Paramater key for dns_service 'dns_transip'"
    "dns_udr_user","string","false","\-","\-","Paramater user for dns_service 'dns_udr'"
    "dns_udr_password","string","false","\-","\-","Paramater password for dns_service 'dns_udr'"
    "dns_uno_key","string","false","\-","\-","Paramater key for dns_service 'dns_uno'"
    "dns_uno_user","string","false","\-","\-","Paramater user for dns_service 'dns_uno'"
    "dns_vscale_key","string","false","\-","\-","Paramater key for dns_service 'dns_vscale'"
    "dns_vultr_key","string","false","\-","\-","Paramater key for dns_service 'dns_vultr'"
    "dns_yandex_token","string","false","\-","\-","Paramater token for dns_service 'dns_yandex'"
    "dns_zilore_key","string","false","\-","\-","Paramater key for dns_service 'dns_zilore'"
    "dns_zm_key","string","false","\-","\-","Paramater key for dns_service 'dns_zm'"
    "dns_gdnsdk_user","string","false","\-","\-","Paramater user for dns_service 'dns_gdnsdk'"
    "dns_gdnsdk_password","string","false","\-","\-","Paramater password for dns_service 'dns_gdnsdk'"
    "dns_acmedns_user","string","false","\-","\-","Paramater user for dns_service 'dns_acmedns'"
    "dns_acmedns_password","string","false","\-","\-","Paramater password for dns_service 'dns_acmedns'"
    "dns_acmedns_subdomain","string","false","\-","\-","Paramater subdomain for dns_service 'dns_acmedns'"
    "dns_acmedns_updateurl","string","false","\-","\-","Paramater updateurl for dns_service 'dns_acmedns'"
    "dns_acmedns_baseurl","string","false","\-","\-","Paramater baseurl for dns_service 'dns_acmedns'"
    "dns_acmeproxy_endpoint","string","false","\-","\-","Paramater endpoint for dns_service 'dns_acmeproxy'"
    "dns_acmeproxy_username","string","false","\-","\-","Paramater username for dns_service 'dns_acmeproxy'"
    "dns_acmeproxy_password","string","false","\-","\-","Paramater password for dns_service 'dns_acmeproxy'"
    "dns_variomedia_key","string","false","\-","\-","Paramater key for dns_service 'dns_variomedia'"
    "dns_schlundtech_user","string","false","\-","\-","Paramater user for dns_service 'dns_schlundtech'"
    "dns_schlundtech_password","string","false","\-","\-","Paramater password for dns_service 'dns_schlundtech'"
    "dns_easydns_apitoken","string","false","\-","\-","Paramater apitoken for dns_service 'dns_easydns'"
    "dns_easydns_apikey","string","false","\-","\-","Paramater apikey for dns_service 'dns_easydns'"
    "dns_euserv_user","string","false","\-","\-","Paramater user for dns_service 'dns_euserv'"
    "dns_euserv_password","string","false","\-","\-","Paramater password for dns_service 'dns_euserv'"
    "dns_leaseweb_key","string","false","\-","\-","Paramater key for dns_service 'dns_leaseweb'"
    "dns_cn_user","string","false","\-","\-","Paramater user for dns_service 'dns_cn'"
    "dns_cn_password","string","false","\-","\-","Paramater password for dns_service 'dns_cn'"
    "dns_arvan_token","string","false","\-","\-","Paramater token for dns_service 'dns_arvan'"
    "dns_artfiles_username","string","false","\-","\-","Paramater username for dns_service 'dns_artfiles'"
    "dns_artfiles_password","string","false","\-","\-","Paramater password for dns_service 'dns_artfiles'"
    "dns_hetzner_token","string","false","\-","\-","Paramater token for dns_service 'dns_hetzner'"
    "dns_hexonet_login","string","false","\-","\-","Paramater login for dns_service 'dns_hexonet'"
    "dns_hexonet_password","string","false","\-","\-","Paramater password for dns_service 'dns_hexonet'"
    "dns_1984hosting_user","string","false","\-","\-","Paramater user for dns_service 'dns_1984hosting'"
    "dns_1984hosting_password","string","false","\-","\-","Paramater password for dns_service 'dns_1984hosting'"
    "dns_kas_login","string","false","\-","\-","Paramater login for dns_service 'dns_kas'"
    "dns_kas_authdata","string","false","\-","\-","Paramater authdata for dns_service 'dns_kas'"
    "dns_kas_authtype","string","false","plain","\-","Paramater authtype One of: 'plain', 'sha1' for dns_service 'dns_kas'"
    "dns_desec_token","string","false","\-","\-","Paramater token for dns_service 'dns_desec'"
    "dns_desec_name","string","false","\-","\-","Paramater name for dns_service 'dns_desec'"
    "dns_infomaniak_token","string","false","\-","\-","Paramater token for dns_service 'dns_infomaniak'"
    "dns_zone_username","string","false","\-","\-","Paramater username for dns_service 'dns_zone'"
    "dns_zone_key","string","false","\-","\-","Paramater key for dns_service 'dns_zone'"
    "dns_dynv6_token","string","false","\-","\-","Paramater token for dns_service 'dns_dynv6'"
    "dns_cpanel_user","string","false","\-","\-","Paramater user for dns_service 'dns_cpanel'"
    "dns_cpanel_token","string","false","\-","\-","Paramater token for dns_service 'dns_cpanel'"
    "dns_cpanel_hostname","string","false","\-","\-","Paramater hostname for dns_service 'dns_cpanel'"
    "dns_regru_username","string","false","\-","\-","Paramater username for dns_service 'dns_regru'"
    "dns_regru_password","string","false","\-","\-","Paramater password for dns_service 'dns_regru'"
    "dns_nic_username","string","false","\-","\-","Paramater username for dns_service 'dns_nic'"
    "dns_nic_password","string","false","\-","\-","Paramater password for dns_service 'dns_nic'"
    "dns_nic_client","string","false","\-","\-","Paramater client for dns_service 'dns_nic'"
    "dns_nic_secret","string","false","\-","\-","Paramater secret for dns_service 'dns_nic'"
    "dns_world4you_username","string","false","\-","\-","Paramater username for dns_service 'dns_world4you'"
    "dns_world4you_password","string","false","\-","\-","Paramater password for dns_service 'dns_world4you'"
    "dns_aurora_key","string","false","\-","\-","Paramater key for dns_service 'dns_aurora'"
    "dns_aurora_secret","string","false","\-","\-","Paramater secret for dns_service 'dns_aurora'"
    "dns_conoha_user","string","false","\-","\-","Paramater user for dns_service 'dns_conoha'"
    "dns_conoha_password","string","false","\-","\-","Paramater password for dns_service 'dns_conoha'"
    "dns_conoha_tenantid","string","false","\-","\-","Paramater tenantid for dns_service 'dns_conoha'"
    "dns_conoha_idapi","string","false","\-","\-","Paramater idapi for dns_service 'dns_conoha'"
    "dns_constellix_key","string","false","\-","\-","Paramater key for dns_service 'dns_constellix'"
    "dns_constellix_secret","string","false","\-","\-","Paramater secret for dns_service 'dns_constellix'"
    "dns_exoscale_key","string","false","\-","\-","Paramater key for dns_service 'dns_exoscale'"
    "dns_exoscale_secret","string","false","\-","\-","Paramater secret for dns_service 'dns_exoscale'"
    "dns_internetbs_key","string","false","\-","\-","Paramater key for dns_service 'dns_internetbs'"
    "dns_internetbs_password","string","false","\-","\-","Paramater password for dns_service 'dns_internetbs'"
    "dns_pointhq_key","string","false","\-","\-","Paramater key for dns_service 'dns_pointhq'"
    "dns_pointhq_email","string","false","\-","\-","Paramater email for dns_service 'dns_pointhq'"
    "dns_rackspace_user","string","false","\-","\-","Paramater user for dns_service 'dns_rackspace'"
    "dns_rackspace_key","string","false","\-","\-","Paramater key for dns_service 'dns_rackspace'"
    "dns_rage4_token","string","false","\-","\-","Paramater token for dns_service 'dns_rage4'"
    "dns_rage4_user","string","false","\-","\-","Paramater user for dns_service 'dns_rage4'"

ansibleguy.opnsense.acme_action
===============================

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "name","string","true","\-","\-","Name to identify this automation."
    "description","string","false","\-","desc","Description for this automation."
    "type","string","false","\-","\-","Pre-defined commands for this automation. One of: 'configd_restart_gui', 'configd_restart_haproxy', 'configd_restart_nginx', 'configd_upload_sftp', 'configd_remote_ssh', 'acme_fritzbox', 'acme_panos', 'acme_proxmoxve', 'acme_vault', 'acme_synology_dsm', 'acme_truenas', 'acme_unifi', 'configd_generic'"
    "sftp_host","string","false","\-","\-","IP address or hostname of the SFTP server. For type: 'configd_upload_sftp'"
    "sftp_host_key","string","false","\-","\-","SFTP server host key, formatted as in 'known_hosts'. Leave blank to auto accept host key on first connect (not as secure as specifying it). . For type: 'configd_upload_sftp'"
    "sftp_port","integer","false","22","\-","SFTP server port. For type: 'configd_upload_sftp'"
    "sftp_user","string","false","\-","\-","The username to login to the SFTP server. For type: 'configd_upload_sftp'"
    "sftp_identity_type","string","false","\-","\-","The type of identify to present to the SFTP server for authorization. One of: 'ecdsa', 'rsa', 'ed25519'. For type: 'configd_upload_sftp'"
    "sftp_remote_path","string","false","\-","\-","Path on the SFTP server to change to after login. The path can be absolute or relative to home and must exist. Leave blank to not change path after login. For type: 'configd_upload_sftp'"
    "sftp_chgrp","string","false","\-","\-","Unix group id to apply to all uploaded files. Leave blank to not change the group. For type: 'configd_upload_sftp'"
    "sftp_chmod","string","false","\-","\-","Unix permission to apply to uploaded public keys. Leave blank to use default '0440'. For type: 'configd_upload_sftp'"
    "sftp_chmod_key","string","false","\-","\-","Unix permission to apply to uploaded private keys. Leave blank to use default '0400'. For type: 'configd_upload_sftp'"
    "sftp_filename_cert","string","false","\-","\-","Name template for the public certificate. Placeholders '{{name}}' and '%s' are replaced by the name of the certificate being uploaded. Leave blank to use default '{{name}}/cert.pem'. For type: 'configd_upload_sftp'"
    "sftp_filename_key","string","false","\-","\-","Name template for the certificate's private key. Placeholders '{{name}}' and '%s' are replaced by the name of the certificate being uploaded. Leave blank to use default '{{name}}/key.pem'. For type: 'configd_upload_sftp'"
    "sftp_filename_ca","string","false","\-","\-","Name template for the public certificate chain file. Placeholders '{{name}}'' and '%s' are replaced by the name of the certificate being uploaded. Leave blank to use default '{{name}}/ca.pem'. For type: 'configd_upload_sftp'"
    "sftp_filename_fullchain","string","false","\-","\-","Name template for the public certificate fullchain file (cert + ca). Placeholders '{{name}}' and '%s' are replaced by the name of the certificate being uploaded. Leave blank to use default '{{name}}/fullchain.pem'. For type: 'configd_upload_sftp'"
    "remote_ssh_host","string","false","\-","\-","IP address or hostname of the SSH server. For type: 'configd_remote_ssh'"
    "remote_ssh_host_key","string","false","\-","\-","SSH server host key, formatted as in 'known_hosts'. Leave blank to auto accept host key on first connect (not as secure as specifying it). For type: 'configd_remote_ssh'"
    "remote_ssh_port","integer","false","22","\-","SSH server port. Leave blank to use default '22'. For type: 'configd_remote_ssh'"
    "remote_ssh_user","string","false","\-","\-","The username to login to the SSH server. For type: 'configd_remote_ssh'"
    "remote_ssh_identity_type","string","false","\-","\-","The type of identify to present to the SSH server for authorization.' One of: 'ecdsa', 'rsa', 'ed25519'. For type: 'configd_remote_ssh'"
    "remote_ssh_command","string","false","\-","\-","The command to execute on the SSH server. For type: 'configd_remote_ssh'"
    "configd_generic_command","string","false","\-","\-","Select a pre-defined system command which should be run. For type: 'configd_generic'"
    "acme_fritzbox_url","string","false","\-","\-","URL of the router, i.e. https://fritzbox.example.com. For type: 'acme_fritzbox'"
    "acme_fritzbox_username","string","false","\-","\-","The username to login to the router. For type: 'acme_fritzbox' For type: 'acme_fritzbox'"
    "acme_fritzbox_password","string","false","\-","\-","The password to login to the router. For type: 'acme_fritzbox'"
    "acme_panos_username","string","false","\-","\-","The username to login to the firewall. For type: 'acme_panos'"
    "acme_panos_password","string","false","\-","\-","The password to login to the firewall. For type: 'acme_panos'"
    "acme_panos_host","string","false","\-","\-","The hostname of the router. For type: 'acme_panos'"
    "acme_proxmoxve_user","string","false","root","\-","The user who owns the API key. Defaults to root. For type: 'acme_proxmoxve'"
    "acme_proxmoxve_server","string","false","\-","\-","The hostname of the proxmox ve node. For type: 'acme_proxmoxve'"
    "acme_proxmoxve_port","integer","false","8006","\-","The port number the management interface is on. Defaults to 8006. For type: 'acme_proxmoxve'"
    "acme_proxmoxve_nodename","string","false","\-","\-","The name of the node we will be connecting to. For type: 'acme_proxmoxve'"
    "acme_proxmoxve_realm","string","false","pam","\-","The authentication realm the user authenticates with. Defaults to pam. For type: 'acme_proxmoxve'"
    "acme_proxmoxve_tokenid","string","false","acme","\-","The name of the API token created for the user account. Defaults to acme. For type: 'acme_proxmoxve'"
    "acme_proxmoxve_tokenkey","string","false","\-","\-","The API token. For type: 'acme_proxmoxve'"
    "acme_vault_url","string","false","\-","\-","URL of the Vault, i.e. http://vault.example.com:8200. For type: 'acme_vault'"
    "acme_vault_prefix","string","false","acme","\-","This specifies the prefix path in Vault. If you select KV v2 you need to add .../data/... between the secret-mount-path and the path. Example: v1 prefix path: secret/acme, v2 prefix path: secret/data/acme. For type: 'acme_vault'"
    "acme_vault_token","string","false","\-","\-","This specifies the Vault token to authenticate with. For type: 'acme_vault'"
    "acme_vault_kvv2","boolean","false","true\-","\-","If checked version 2 of the kv store will be used, otherwise version 1. For type: 'acme_vault'"
    "acme_synology_dsm_hostname","string","false","\-","\-","Hostname of IP adress of the Synology DSM, i.e. synology.example.com or 192.168.0.1. For type: 'acme_synology'"
    "acme_synology_dsm_port","integer","false","5000","\-","Port that will be used when connecting to Synology DSM. For type: 'acme_synology'"
    "acme_synology_dsm_scheme","string","false","http","\-","Connection scheme that will be used when uploading certificates to Synology DSM. One of: 'http', 'https' For type: 'acme_synology'"
    "acme_synology_dsm_username","string","false","\-","\-","Username to login, must be an administrator. For type: 'acme_synology'"
    "acme_synology_dsm_password","string","false","\-","\-","Password to login with. For type: 'acme_synology'"
    "acme_synology_dsm_create","boolean","false","true","\-","This option ensures that a new certificate is created in Synology DSM if it does not exist yet. If unchecked only existing certificates will be updated. For type: 'acme_synology'"
    "acme_synology_dsm_deviceid","string","false","\-","\-","If Synology DSM has OTP enabled, then the device ID has to be provided so that no OTP is required when running the automation. For type: 'acme_synology'"
    "acme_synology_dsm_devicename","string","false","\-","\-","If Synology DSM has OTP enabled, then the device name has to be provided so that no OTP is required when running the automation. For type: 'acme_synology'"
    "acme_truenas_apikey","string","false","\-","\-","API key generated in the TrueNAS web UI. For type: 'acme_truenas'"
    "acme_truenas_hostname","string","false","\-","\-","Hostname or IP adress of TrueNAS Core Server. For type: 'acme_truenas'"
    "acme_truenas_scheme","string","false","http","\-","Connection scheme that will be used when uploading certificates to TrueNAS Core Server. One of: 'http', 'https' For type: 'acme_truenas'"
    "acme_unifi_keystore","string","false","/usr/local/share/java/unifi/data/keystore","\-","Path to the Unifi keystore file in the local filesystem, i.e. /usr/local/share/java/unifi/data/keystore. For type: 'acme_unifi'"

ansibleguy.opnsense.acme_certificate
====================================

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "name","string","false","\-","\-","Common Name (CN) and first Alt Name (subjectAltName) for this certificate."
    "description","string","true","\-","desc","Description for this certificate."
    "alt_names","list","false","\-","\-","Configure additional names that should be part of the certificate, i.e. www.example.com or mail.example.com."
    "account","string","false","\-","\-","Set the ACME CA account to use for this certificate."
    "validation","string","false","\-","\-","Set the ACME challenge type for this certificate."
    "auto_renew","boolean","false","true","\-","Enable automatic renewal for this certificate to prevent expiration. When disabled, the cron job will ignore this certificate."
    "renew_interval","integer","false","60","\-","Specifies the days to renew the cert. The max value is 5000 days."
    "key_length","string","false","key_4096","\-","Specify the domain key length: 2048, 3072, 4096, or ec-256, ec-384."
    "ocsp","boolean","false","false","\-","Generate and add OCSP Must Staple extension to the certificate."
    "restart_actions","list","false","\-","\-","Choose the automations that should be run after certificate creation and renewal."
    "aliasmode","string","false","none","\-","Configure DNS alias mode to validate the certificate. One of: 'none', 'automatic', 'domain', 'challenge'"
    "domainalias","string","false","\-","\-","When setting aliasmode to 'domain', enter the domain name that should be used for certificate validation. Please refer to the `acme.sh documentation <https://github.com/acmesh-official/acme.sh/wiki/DNS-alias-mode>`_ for further information."
    "challengealias","string","false","\-","\-","When setting aliasmode to 'challenge', enter the domain name that should be used for certificate validation. Please refer to the `acme.sh documentation <https://github.com/acmesh-official/acme.sh/wiki/DNS-alias-mode>`_ for further information."
    "reload","boolean","false","true","\-", .. include:: ../_include/param_reload.rst

.. include:: ../_include/param_basic.rst

Usage
*****

Setting up this plugin for the first time involves the following steps

 * **Enable** the plugin with the acme_general module.
 * Create an **account** with any of the supported CAs using the acme_account module.
 * Set up a **validation** / challenge type using the acme_validation module.
 * Add **actions** / automations using the acme_action module. This is optional, but recommended when using short-lived certificates. Automations allow to automatically run tasks when a certificate was created or renewed.
 * Create **certificates**: Finally create the certificates using the acme_certificate module.


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
        - name: Activate ACME Client
          ansibleguy.opnsense.acme_general:
            enable: true
            # auto_renewal: true
            # challenge_port: 43580
            # tls_challenge_port: 43581
            # restart_timeout: 600
            # haproxy_integration: false
            # log_level: normal
            # show_intro: true
            # debug: false

        - name: Adding ACME Account
          ansibleguy.opnsense.acme_account:
            name: LE opnsense
            # description:
            # email:
            # ca: letsencrypt
            # eab_kid:
            # eab_hmac:
            # register: false
            # enable: true

        - name: Adding ACME Validation
          ansibleguy.opnsense.acme_validation:
            name: HTTP
            description: Default HTTP-01 Validation
            method: http01
            # http_service: opnsense
            # http_opn_autodiscovery: true
            # http_opn_interface: wan
            # http_opn_ipaddresses: ['1.2.3.4']

        - name: Adding ACME Validation DNS
          ansibleguy.opnsense.acme_validation:
            name: DNS FreeDNS
            description: DNS Validation w/ FreeDNS
            # method: dns01
            # dns_service: dns_freedns
            dns_freedns_user: USER
            dns_freedns_password: SECRET

        - name: Adding ACME Action
          ansibleguy.opnsense.acme_action:
            name: Restart GUI
            description: Restart OPNsense GUI
            type: configd_restart_gui

        - name: Adding ACME Certificate
          ansibleguy.opnsense.acme_action:
            name: ansibleguy.net
            description: LE ansibleguy.net
            alt_names: ['ansibleguy.com']
            account: LE opnsense
            validation: HTTP
            # auto_renew: true
            # renew_interval: 60
            # key_length: key_4096
            # ocsp: false
            restart_actions: ['Restart GUI']
            # aliasmode: none

        - name: Listing jobs
          ansibleguy.opnsense.list:
            target: 'acme_certificate'
          register: existing_certificates

        - name: Printing
          ansible.builtin.debug:
            var: existing_certificates.data
