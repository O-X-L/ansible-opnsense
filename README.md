# Ansible Collection - ansibleguy.opnsense

[![Lint](https://github.com/ansibleguy/collection_opnsense/actions/workflows/lint.yml/badge.svg)](https://github.com/ansibleguy/collection_opnsense/actions/workflows/lint.yml)
[![Unit Test Status](https://github.com/ansibleguy/collection_opnsense/actions/workflows/unit_test.yml/badge.svg)](https://github.com/ansibleguy/collection_opnsense/actions/workflows/unit_test.yml)
[![Ansible Galaxy](https://badges.ansibleguy.net/galaxy.badge.svg)](https://galaxy.ansible.com/ui/repo/published/ansibleguy/opnsense)

**Functional Tests**: 

* Status: [![Functional Test Status](https://badges.ansibleguy.net/opnsense.collection.test.svg)](https://github.com/ansibleguy/collection_opnsense/blob/latest/scripts/test.sh) |
[![Functional-Tests](https://github.com/ansibleguy/collection_opnsense/actions/workflows/functional_test_result.yml/badge.svg)](https://github.com/ansibleguy/collection_opnsense/actions/workflows/functional_test_result.yml)
* Logs: [API](https://ci.ansibleguy.net/api/job/ansible-test-collection-opnsense/logs?token=2b7bba30-9a37-4b57-be8a-99e23016ce70&lines=1000) |
[Daily Archive](https://github.com/ansibleguy/collection_opnsense/actions/workflows/functional_test_result.yml) |
[Short](https://badges.ansibleguy.net/log/collection_opnsense_test_short.log) | [Full](https://badges.ansibleguy.net/log/collection_opnsense_test.log)

Internal CI: [Tester Role](https://github.com/ansibleguy/_meta_cicd) | [Jobs API](https://github.com/O-X-L/github-self-hosted-jobs-systemd)

----

## Requirements

The [httpx python module](https://www.python-httpx.org/) is used for API communications!

```bash
python3 -m pip install --upgrade httpx
```

Then - install the collection itself:

```bash
# latest version:
ansible-galaxy collection install git+https://github.com/ansibleguy/collection_opnsense.git

# stable/tested version:
ansible-galaxy collection install git+https://github.com/ansibleguy/collection_opnsense.git,1.2.13
## OR
ansible-galaxy collection install ansibleguy.opnsense
```

----

## Usage

See: [Docs](https://opnsense.ansibleguy.net)

[![Docs Uptime](https://status.oxl.at/api/v1/endpoints/4--ansibleguy_ansible-collection---opnsense-documentation/uptimes/7d/badge.svg)](https://status.oxl.at/endpoints/4--ansibleguy_ansible-collection---opnsense-documentation)

[Alternative Link](https://opnsense-ansible.readthedocs.io/)

If you DO NOT want to use Ansible - [this fork](https://github.com/O-X-L/opnsense-api-client) provides you with a raw Python3 interface.

----

## Contribute

Feel free to contribute to this project using [pull-requests](https://github.com/ansibleguy/collection_opnsense/pulls), [issues](https://github.com/ansibleguy/collection_opnsense/issues) and [discussions](https://github.com/ansibleguy/collection_opnsense/discussions)!

See also: [Contributing](https://github.com/ansibleguy/collection_opnsense/blob/latest/CONTRIBUTING.md)

<img src="https://contrib.rocks/image?repo=ansibleguy/collection_opnsense&max=7" />

----

## Version Support

The `ansibleguy.opnsense` modules always support the latest version of OPNSense.

If an API changed, the current module-implementation might fail for firewalls running an older firmware.

----


## Modules

**Development States**:

not implemented => development => [testing](https://github.com/ansibleguy/collection_opnsense/tree/latest/tests) => unstable (_practical testing_) => stable

### Implemented


| Function                  | Module                                                                 | Usage                                                                                                              | State    |
|:--------------------------|:-----------------------------------------------------------------------|:-------------------------------------------------------------------------------------------------------------------|:---------|
| **Base**                  | ansibleguy.opnsense.list                                               | [Docs](https://opnsense.ansibleguy.net/modules/2_list.html)                                                        | stable   |
| **Base**                  | ansibleguy.opnsense.reload                                             | [Docs](https://opnsense.ansibleguy.net/modules/2_reload.html)                                                      | stable   |
| **Services**              | ansibleguy.opnsense.service                                            | [Docs](https://opnsense.ansibleguy.net/modules/service.html)                                                       | stable   |
| **Alias**                 | ansibleguy.opnsense.alias                                              | [Docs](https://opnsense.ansibleguy.net/modules/alias.html)                                                         | stable   | 
| **Alias**                 | ansibleguy.opnsense.alias_multi                                        | [Docs](https://opnsense.ansibleguy.net/modules/alias_multi.html)                                                   | stable   |
| **Alias**                 | ansibleguy.opnsense.alias_purge                                        | [Docs](https://opnsense.ansibleguy.net/modules/alias_multi.html#ansibleguy-opnsense-alias-purge)                   | unstable |
| **Rules**                 | ansibleguy.opnsense.rule                                               | [Docs](https://opnsense.ansibleguy.net/modules/rule.html)                                                          | stable   |
| **Rules**                 | ansibleguy.opnsense.rule_multi                                         | [Docs](https://opnsense.ansibleguy.net/modules/rule_multi.html)                                                    | stable   |
| **Rules**                 | ansibleguy.opnsense.rule_purge                                         | [Docs](https://opnsense.ansibleguy.net/modules/rule_multi.html#ansibleguy-opnsense-rule-purge)                     | unstable |
| **Rule Interface Groups** | ansibleguy.opnsense.rule_interface_group                               | [Docs](https://opnsense.ansibleguy.net/modules/rule_interface_group.html#ansibleguy-opnsense-rule-interface-group) | unstable |
| **Savepoints**            | ansibleguy.opnsense.savepoint                                          | [Docs](https://opnsense.ansibleguy.net/modules/savepoint.html)                                                     | stable   |
| **Packages**              | ansibleguy.opnsense.package                                            | [Docs](https://opnsense.ansibleguy.net/modules/package.html)                                                       | stable   |
| **System**                | ansibleguy.opnsense.system                                             | [Docs](https://opnsense.ansibleguy.net/modules/system.html)                                                        | stable   |
| **Cron-Jobs**             | ansibleguy.opnsense.cron                                               | [Docs](https://opnsense.ansibleguy.net/modules/cron.html)                                                          | stable   |
| **Routes**                | ansibleguy.opnsense.route                                              | [Docs](https://opnsense.ansibleguy.net/modules/routing.html)                                                       | stable   |
| **Gateways**              | ansibleguy.opnsense.gateway                                            | [Docs](https://opnsense.ansibleguy.net/modules/routing.html)                                                       | unstable |
| **DNS**                   | ansibleguy.opnsense.unbound_general                                    | [Docs](https://opnsense.ansibleguy.net/modules/unbound_general.html)                                               | stable   |
| **DNS**                   | ansibleguy.opnsense.unbound_acl                                        | [Docs](https://opnsense.ansibleguy.net/modules/unbound_acl.html)                                                   | stable   |
| **DNS**                   | ansibleguy.opnsense.unbound_forward                                    | [Docs](https://opnsense.ansibleguy.net/modules/unbound_forwarding.html)                                            | stable   |
| **DNS**                   | ansibleguy.opnsense.unbound_dot                                        | [Docs](https://opnsense.ansibleguy.net/modules/unbound_dot.html)                                                   | stable   |
| **DNS**                   | ansibleguy.opnsense.unbound_host                                       | [Docs](https://opnsense.ansibleguy.net/modules/unbound_host.html)                                                  | stable   |
| **DNS**                   | ansibleguy.opnsense.unbound_host_alias                                 | [Docs](https://opnsense.ansibleguy.net/modules/unbound_host_alias.html)                                            | stable   |
| **DNS**                   | ansibleguy.opnsense.unbound_dnsbl                                      | [Docs](https://opnsense.ansibleguy.net/modules/unbound_host_alias.html)                                            | unstable |
| **Syslog**                | ansibleguy.opnsense.syslog                                             | [Docs](https://opnsense.ansibleguy.net/modules/syslog.html)                                                        | stable   |
| **IPSec**                 | ansibleguy.opnsense.ipsec_connection, ansibleguy.opnsense.ipsec_tunnel | [Docs](https://opnsense.ansibleguy.net/modules/ipsec.html)                                                         | stable   |
| **IPSec**                 | ansibleguy.opnsense.ipsec_pool, ansibleguy.opnsense.ipsec_network      | [Docs](https://opnsense.ansibleguy.net/modules/ipsec.html)                                                         | stable   |
| **IPSec**                 | ansibleguy.opnsense.ipsec_auth_local                                   | [Docs](https://opnsense.ansibleguy.net/modules/ipsec.html)                                                         | stable   |
| **IPSec**                 | ansibleguy.opnsense.ipsec_auth_remote                                  | [Docs](https://opnsense.ansibleguy.net/modules/ipsec.html)                                                         | stable   |
| **IPSec**                 | ansibleguy.opnsense.ipsec_child                                        | [Docs](https://opnsense.ansibleguy.net/modules/ipsec.html)                                                         | stable   |
| **IPSec**                 | ansibleguy.opnsense.ipsec_vti                                          | [Docs](https://opnsense.ansibleguy.net/modules/ipsec.html)                                                         | stable   |
| **IPSec**                 | ansibleguy.opnsense.ipsec_cert                                         | [Docs](https://opnsense.ansibleguy.net/modules/ipsec.html)                                                         | stable   |
| **IPSec**                 | ansibleguy.opnsense.ipsec_psk                                          | [Docs](https://opnsense.ansibleguy.net/modules/ipsec.html)                                                         | stable   |
| **IPSec**                 | ansibleguy.opnsense.ipsec_manual_spd                                   | [Docs](https://opnsense.ansibleguy.net/modules/ipsec.html)                                                         | stable   |
| **Traffic Shaper**        | ansibleguy.opnsense.shaper_pipe                                        | [Docs](https://opnsense.ansibleguy.net/modules/shaper.html)                                                        | stable   |
| **Traffic Shaper**        | ansibleguy.opnsense.shaper_queue                                       | [Docs](https://opnsense.ansibleguy.net/modules/shaper.html)                                                        | stable   |
| **Traffic Shaper**        | ansibleguy.opnsense.shaper_rule                                        | [Docs](https://opnsense.ansibleguy.net/modules/shaper.html)                                                        | stable   |
| **Monit**                 | ansibleguy.opnsense.monit_service                                      | [Docs](https://opnsense.ansibleguy.net/modules/monit.html)                                                         | stable   |
| **Monit**                 | ansibleguy.opnsense.monit_alert                                        | [Docs](https://opnsense.ansibleguy.net/modules/monit.html)                                                         | stable   |
| **Monit**                 | ansibleguy.opnsense.monit_test                                         | [Docs](https://opnsense.ansibleguy.net/modules/monit.html)                                                         | stable   |
| **WireGuard**             | ansibleguy.opnsense.wireguard_server                                   | [Docs](https://opnsense.ansibleguy.net/modules/wireguard.html)                                                     | stable   |
| **WireGuard**             | ansibleguy.opnsense.wireguard_peer                                     | [Docs](https://opnsense.ansibleguy.net/modules/wireguard.html)                                                     | stable   |
| **WireGuard**             | ansibleguy.opnsense.wireguard_show                                     | [Docs](https://opnsense.ansibleguy.net/modules/wireguard.html)                                                     | stable   |
| **WireGuard**             | ansibleguy.opnsense.wireguard_general                                  | [Docs](https://opnsense.ansibleguy.net/modules/wireguard.html)                                                     | stable   |
| **Interfaces**            | ansibleguy.opnsense.interface_vlan                                     | [Docs](https://opnsense.ansibleguy.net/modules/interface.html)                                                     | stable   |
| **Interfaces**            | ansibleguy.opnsense.interface_vxlan                                    | [Docs](https://opnsense.ansibleguy.net/modules/interface.html)                                                     | stable   |
| **Interfaces**            | ansibleguy.opnsense.interface_vip                                      | [Docs](https://opnsense.ansibleguy.net/modules/interface.html)                                                     | stable   |
| **Interfaces**            | ansibleguy.opnsense.interface_lagg                                     | [Docs](https://opnsense.ansibleguy.net/modules/interface.html)                                                     | unstable |
| **Interfaces**            | ansibleguy.opnsense.interface_loopback                                 | [Docs](https://opnsense.ansibleguy.net/modules/interface.html)                                                     | unstable |
| **NAT**                   | ansibleguy.opnsense.nat_source                                         | [Docs](https://opnsense.ansibleguy.net/modules/source_nat.html)                                                    | stable   |
| **NAT**                   | ansibleguy.opnsense.nat_one_to_one                                     | [Docs](https://opnsense.ansibleguy.net/modules/one_to_one.html)                                                    | unstable |
| **Dynamic Routing**       | ansibleguy.opnsense.frr_diagnostic                                     | [Docs](https://opnsense.ansibleguy.net/modules/frr_diagnostic.html)                                                | stable   |
| **Dynamic Routing**       | ansibleguy.opnsense.frr_general                                        | [Docs](https://opnsense.ansibleguy.net/modules/frr_general.html)                                                   | stable   |
| **Dynamic Routing**       | ansibleguy.opnsense.frr_bfd_general                                    | [Docs](https://opnsense.ansibleguy.net/modules/frr_bfd.html#ansibleguy-opnsense-frr-bfd-general)                   | stable   |
| **Dynamic Routing**       | ansibleguy.opnsense.frr_bfd_neighbor                                   | [Docs](https://opnsense.ansibleguy.net/modules/frr_bfd.html#ansibleguy-opnsense-frr-bfd-neighbor)                  | stable   |
| **Dynamic Routing**       | ansibleguy.opnsense.frr_bgp_general                                    | [Docs](https://opnsense.ansibleguy.net/modules/frr_bgp.html#ansibleguy-opnsense-frr-bgp-general)                   | stable   |
| **Dynamic Routing**       | ansibleguy.opnsense.frr_bgp_neighbor                                   | [Docs](https://opnsense.ansibleguy.net/modules/frr_bgp.html#ansibleguy-opnsense-frr-bgp-neighbor)                  | stable   |
| **Dynamic Routing**       | ansibleguy.opnsense.frr_bgp_prefix_list                                | [Docs](https://opnsense.ansibleguy.net/modules/frr_bgp.html#ansibleguy-opnsense-frr-bgp-prefix-list)               | stable   |
| **Dynamic Routing**       | ansibleguy.opnsense.frr_bgp_route_map                                  | [Docs](https://opnsense.ansibleguy.net/modules/frr_bgp.html#ansibleguy-opnsense-frr-bgp-route-map)                 | stable   |
| **Dynamic Routing**       | ansibleguy.opnsense.frr_bgp_community_list                             | [Docs](https://opnsense.ansibleguy.net/modules/frr_bgp.html#ansibleguy-opnsense-frr-bgp-community-list)            | stable   |
| **Dynamic Routing**       | ansibleguy.opnsense.frr_bgp_as_path                                    | [Docs](https://opnsense.ansibleguy.net/modules/frr_bgp.html#ansibleguy-opnsense-frr-bgp-as-path)                   | stable   |
| **Dynamic Routing**       | ansibleguy.opnsense.frr_ospf_general                                   | [Docs](https://opnsense.ansibleguy.net/modules/frr_ospf.html#ansibleguy-opnsense-frr-ospf-general)                 | stable   |
| **Dynamic Routing**       | ansibleguy.opnsense.frr_ospf_prefix_list                               | [Docs](https://opnsense.ansibleguy.net/modules/frr_ospf.html#ansibleguy-opnsense-frr-ospf-prefix-list)             | stable   |
| **Dynamic Routing**       | ansibleguy.opnsense.frr_ospf_interface                                 | [Docs](https://opnsense.ansibleguy.net/modules/frr_ospf.html#ansibleguy-opnsense-frr-ospf-interface)               | stable   |
| **Dynamic Routing**       | ansibleguy.opnsense.frr_ospf_network                                   | [Docs](https://opnsense.ansibleguy.net/modules/frr_ospf.html#ansibleguy-opnsense-frr-ospf-network)                 | stable   |
| **Dynamic Routing**       | ansibleguy.opnsense.frr_ospf3_general                                  | [Docs](https://opnsense.ansibleguy.net/modules/frr_ospf.html#ansibleguy-opnsense-frr-ospf3-general)                | stable   |
| **Dynamic Routing**       | ansibleguy.opnsense.frr_ospf3_interface                                | [Docs](https://opnsense.ansibleguy.net/modules/frr_ospf.html#ansibleguy-opnsense-frr-ospf3-interface)              | stable   |
| **Dynamic Routing**       | ansibleguy.opnsense.frr_rip                                            | [Docs](https://opnsense.ansibleguy.net/modules/frr_rip.html)                                                       | stable   |
| **DNS**                   | ansibleguy.opnsense.bind_general                                       | [Docs](https://opnsense.ansibleguy.net/modules/bind.html#ansibleguy-opnsense-bind-general)                         | stable   |
| **DNS**                   | ansibleguy.opnsense.bind_blocklist                                     | [Docs](https://opnsense.ansibleguy.net/modules/bind.html#ansibleguy-opnsense-bind-blocklist)                       | stable   |
| **DNS**                   | ansibleguy.opnsense.bind_acl                                           | [Docs](https://opnsense.ansibleguy.net/modules/bind.html#ansibleguy-opnsense-bind-acl)                             | stable   |
| **DNS**                   | ansibleguy.opnsense.bind_domain                                        | [Docs](https://opnsense.ansibleguy.net/modules/bind.html#ansibleguy-opnsense-bind-domain)                          | stable   |
| **DNS**                   | ansibleguy.opnsense.bind_record                                        | [Docs](https://opnsense.ansibleguy.net/modules/bind.html#ansibleguy-opnsense-bind-record)                          | stable   |
| **DNS**                   | ansibleguy.opnsense.bind_record_multi                                  | [Docs](https://opnsense.ansibleguy.net/modules/bind.html#ansibleguy-opnsense-bind-record-multi)                    | stable   |
| **Web Proxy**             | ansibleguy.opnsense.webproxy_general                                   | [Docs](https://opnsense.ansibleguy.net/modules/webproxy.html#id2)                                                  | stable   |
| **Web Proxy**             | ansibleguy.opnsense.webproxy_cache                                     | [Docs](https://opnsense.ansibleguy.net/modules/webproxy.html#id3)                                                  | stable   |
| **Web Proxy**             | ansibleguy.opnsense.webproxy_parent                                    | [Docs](https://opnsense.ansibleguy.net/modules/webproxy.html#id4)                                                  | stable   |
| **Web Proxy**             | ansibleguy.opnsense.webproxy_traffic                                   | [Docs](https://opnsense.ansibleguy.net/modules/webproxy.html#id5)                                                  | stable   |
| **Web Proxy**             | ansibleguy.opnsense.webproxy_forward                                   | [Docs](https://opnsense.ansibleguy.net/modules/webproxy.html#id7)                                                  | stable   |
| **Web Proxy**             | ansibleguy.opnsense.webproxy_acl                                       | [Docs](https://opnsense.ansibleguy.net/modules/webproxy.html#id8)                                                  | stable   |
| **Web Proxy**             | ansibleguy.opnsense.webproxy_icap                                      | [Docs](https://opnsense.ansibleguy.net/modules/webproxy.html#id9)                                                  | stable   |
| **Web Proxy**             | ansibleguy.opnsense.webproxy_auth                                      | [Docs](https://opnsense.ansibleguy.net/modules/webproxy.html#id10)                                                 | stable   |
| **Web Proxy**             | ansibleguy.opnsense.webproxy_remote_acl                                | [Docs](https://opnsense.ansibleguy.net/modules/webproxy.html#id12)                                                 | stable   |
| **Web Proxy**             | ansibleguy.opnsense.webproxy_pac_proxy                                 | [Docs](https://opnsense.ansibleguy.net/modules/webproxy.html#id14)                                                 | stable   |
| **Web Proxy**             | ansibleguy.opnsense.webproxy_pac_match                                 | [Docs](https://opnsense.ansibleguy.net/modules/webproxy.html#id15)                                                 | stable   |
| **Web Proxy**             | ansibleguy.opnsense.webproxy_pac_rule                                  | [Docs](https://opnsense.ansibleguy.net/modules/webproxy.html#id18)                                                 | stable   |
| **IDS/IPS**               | ansibleguy.opnsense.ids_action                                         | [Docs](https://opnsense.ansibleguy.net/modules/ids.html#id2)                                                       | stable   |
| **IDS/IPS**               | ansibleguy.opnsense.ids_general                                        | [Docs](https://opnsense.ansibleguy.net/modules/ids.html#id3)                                                       | stable   |
| **IDS/IPS**               | ansibleguy.opnsense.ids_ruleset                                        | [Docs](https://opnsense.ansibleguy.net/modules/ids.html#id4)                                                       | stable   |
| **IDS/IPS**               | ansibleguy.opnsense.ids_rule                                           | [Docs](https://opnsense.ansibleguy.net/modules/ids.html#id5)                                                       | stable   |
| **IDS/IPS**               | ansibleguy.opnsense.ids_user_rule                                      | [Docs](https://opnsense.ansibleguy.net/modules/ids.html#id6)                                                       | stable   |
| **IDS/IPS**               | ansibleguy.opnsense.ids_policy                                         | [Docs](https://opnsense.ansibleguy.net/modules/ids.html#id7)                                                       | stable   |
| **IDS/IPS**               | ansibleguy.opnsense.ids_policy_rule                                    | [Docs](https://opnsense.ansibleguy.net/modules/ids.html#id8)                                                       | stable   |
| **OpenVPN**               | ansibleguy.opnsense.openvpn_client                                     | [Docs](https://opnsense.ansibleguy.net/modules/openvpn.html)                                                       | stable   |
| **OpenVPN**               | ansibleguy.opnsense.openvpn_server                                     | [Docs](https://opnsense.ansibleguy.net/modules/openvpn.html)                                                       | stable   |
| **OpenVPN**               | ansibleguy.opnsense.openvpn_static_key                                 | [Docs](https://opnsense.ansibleguy.net/modules/openvpn.html)                                                       | stable   |
| **OpenVPN**               | ansibleguy.opnsense.openvpn_status                                     | [Docs](https://opnsense.ansibleguy.net/modules/openvpn.html)                                                       | stable   |
| **OpenVPN**               | ansibleguy.opnsense.openvpn_client_override                            | [Docs](https://opnsense.ansibleguy.net/modules/openvpn.html)                                                       | stable   |
| **Nginx**                 | ansibleguy.opnsense.nginx_general                                      | [Docs](https://opnsense.ansibleguy.net/modules/nginx.html#ansibleguy-opnsense-nginx-general)                       | unstable |
| **Nginx**                 | ansibleguy.opnsense.nginx_upstream_server                              | [Docs](https://opnsense.ansibleguy.net/modules/nginx.html#ansibleguy-opnsense-nginx-upstream-server)               | unstable |
| **DHCP Relay**            | ansibleguy.opnsense.dhcrelay                                           | [Docs](https://opnsense.ansibleguy.net/modules/dhcrelay_relay.html)                                                | unstable |
| **DHCP Relay**            | ansibleguy.opnsense.dhcrelay_destination                               | [Docs](https://opnsense.ansibleguy.net/modules/dhcrelay_destination.html)                                          | unstable |
| **DHCP**                  | ansibleguy.opnsense.dhcp_general                                       | [Docs](https://opnsense.ansibleguy.net/modules/dhcp.html)                                                          | unstable |
| **DHCP Subnet**           | ansibleguy.opnsense.dhcp_subnet                                        | [Docs](https://opnsense.ansibleguy.net/modules/dhcp.html)                                                          | unstable |
| **DHCP Reservation**      | ansibleguy.opnsense.dhcp_reservation                                   | [Docs](https://opnsense.ansibleguy.net/modules/dhcp.html)                                                          | unstable |
| **DHCP Controlagent**     | ansibleguy.opnsense.dhcp_controlagent                                  | [Docs](https://opnsense.ansibleguy.net/modules/dhcp.html)                                                          | unstable |
| **ACME (Certificates)**   | ansibleguy.opnsense.acme_account                                       | [Docs](https://opnsense.ansibleguy.net/modules/acmeclient.html)                                                    | unstable |
| **ACME (Certificates)**   | ansibleguy.opnsense.acme_action                                        | [Docs](https://opnsense.ansibleguy.net/modules/acmeclient.html)                                                    | unstable |
| **ACME (Certificates)**   | ansibleguy.opnsense.acme_general                                       | [Docs](https://opnsense.ansibleguy.net/modules/acmeclient.html)                                                    | unstable |
| **ACME (Certificates)**   | ansibleguy.opnsense.acme_validation                                    | [Docs](https://opnsense.ansibleguy.net/modules/acmeclient.html)                                                    | unstable |
| **ACME (Certificates)**   | ansibleguy.opnsense.acme_certificate                                   | [Docs](https://opnsense.ansibleguy.net/modules/acmeclient.html)                                                    | unstable |
| **Postfix**               | ansibleguy.opnsense.postfix_general                                    | [Docs](https://opnsense.ansibleguy.net/modules/postfix.html)                                                    | unstable |
| **Postfix**               | ansibleguy.opnsense.postfix_domain                                     | [Docs](https://opnsense.ansibleguy.net/modules/postfix.html)                                                    | unstable |
| **Postfix**               | ansibleguy.opnsense.postfix_recipient                                  | [Docs](https://opnsense.ansibleguy.net/modules/postfix.html)                                                    | unstable |
| **Postfix**               | ansibleguy.opnsense.postfix_recipientbcc                               | [Docs](https://opnsense.ansibleguy.net/modules/postfix.html)                                                    | unstable |
| **Postfix**               | ansibleguy.opnsense.postfix_sender                                     | [Docs](https://opnsense.ansibleguy.net/modules/postfix.html)                                                    | unstable |
| **Postfix**               | ansibleguy.opnsense.postfix_senderbcc                                  | [Docs](https://opnsense.ansibleguy.net/modules/postfix.html)                                                    | unstable |
| **Postfix**               | ansibleguy.opnsense.postfix_sendercanonical                            | [Docs](https://opnsense.ansibleguy.net/modules/postfix.html)                                                    | unstable |
| **Postfix**               | ansibleguy.opnsense.postfix_headercheck                                | [Docs](https://opnsense.ansibleguy.net/modules/postfix.html)                                                    | unstable |
| **Postfix**               | ansibleguy.opnsense.postfix_address                                    | [Docs](https://opnsense.ansibleguy.net/modules/postfix.html)                                                    | unstable |
| **High Availability**     | ansibleguy.opnsense.hasync_general                                     | [Docs](https://opnsense.ansibleguy.net/modules/hasync.html)                                                    | unstable |
| **High Availability**     | ansibleguy.opnsense.hasync_service                                     | [Docs](https://opnsense.ansibleguy.net/modules/hasync.html)                                                    | unstable |

### Roadmap

See: [Feature Requests](https://github.com/ansibleguy/collection_opnsense/issues?q=is%3Aopen+is%3Aissue+label%3Aenhancement)
