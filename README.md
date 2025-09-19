# Ansible Collection to manage OPNsense Firewalls

[![Lint](https://github.com/O-X-L/ansible_opnsense/actions/workflows/lint.yml/badge.svg)](https://github.com/O-X-L/ansible_opnsense/actions/workflows/lint.yml)
[![Unit Test Status](https://github.com/O-X-L/ansible_opnsense/actions/workflows/unit_test.yml/badge.svg)](https://github.com/O-X-L/ansible_opnsense/actions/workflows/unit_test.yml)
[![Ansible Galaxy](https://badges.ansibleguy.net/galaxy.badge.svg)](https://galaxy.ansible.com/ui/repo/published/ansibleguy/opnsense)

**Functional Tests**: 

* Status: [![Functional Test Status](https://badges.ansibleguy.net/opnsense.collection.test.svg)](https://github.com/O-X-L/ansible-opnsense/actions/workflows/functional_test_result.yml) |
[![Functional-Tests](https://github.com/O-X-L/ansible_opnsense/actions/workflows/functional_test_result.yml/badge.svg)](https://github.com/O-X-L/ansible_opnsense/actions/workflows/functional_test_result.yml)
* Logs: [API](https://ci.ansibleguy.net/api/job/ansible-test-collection-opnsense/logs?token=2b7bba30-9a37-4b57-be8a-99e23016ce70&lines=1000) |
[Daily Archive](https://github.com/O-X-L/ansible_opnsense/actions/workflows/functional_test_result.yml)

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
ansible-galaxy collection install git+https://github.com/O-X-L/ansible_opnsense.git

# stable/tested version:
ansible-galaxy collection install git+https://github.com/O-X-L/ansible_opnsense.git,1.2.15
## OR
ansible-galaxy collection install ansibleguy.opnsense
```

----

## Usage

See: [Docs](https://ansible-opnsense.oxl.app)

[![Docs Uptime](https://status.oxl.at/api/v1/endpoints/4--ansibleguy_ansible-collection---opnsense-documentation/uptimes/7d/badge.svg)](https://status.oxl.at/endpoints/4--ansibleguy_ansible-collection---opnsense-documentation)

If you DO NOT want to use Ansible - [this fork](https://github.com/O-X-L/opnsense-api-client) provides you with a raw Python3 interface.

----

## Contribute

Feel free to contribute to this project using [pull-requests](https://github.com/O-X-L/ansible_opnsense/pulls), [issues](https://github.com/O-X-L/ansible_opnsense/issues) and [discussions](https://github.com/O-X-L/ansible_opnsense/discussions)!

See also: [Contributing](https://github.com/O-X-L/ansible_opnsense/blob/latest/CONTRIBUTING.md)

<img src="https://contrib.rocks/image?repo=O-X-L/ansible_opnsense&max=7" />

----

## Version Support

We try that the `ansibleguy.opnsense` modules always support the latest version of OPNSense.

If an API changed, the current module-implementation might fail for firewalls running an older firmware.

As [this project is unfunded](https://github.com/O-X-L/ansible_opnsense/discussions/199) we do not actively check for API-changes - if you find missing functionalities you need/want to have please [report it](https://github.com/O-X-L/ansible_opnsense/issues)!

----


## Modules

**Development States**:

not implemented => development => [testing](https://github.com/O-X-L/ansible_opnsense/tree/latest/tests) => [unstable (_practical testing_)](https://github.com/O-X-L/ansible-opnsense/discussions/85) => stable

### Implemented


| Function                  | Module                                                                 | Usage                                                                                                               | State    |
|:--------------------------|:-----------------------------------------------------------------------|:--------------------------------------------------------------------------------------------------------------------|:---------|
| **Base**                  | ansibleguy.opnsense.list                                               | [Docs](https://ansible-opnsense.oxl.app/modules/2_list.html)                                                        | stable   |
| **Base**                  | ansibleguy.opnsense.reload                                             | [Docs](https://ansible-opnsense.oxl.app/modules/2_reload.html)                                                      | stable   |
| **Services**              | ansibleguy.opnsense.service                                            | [Docs](https://ansible-opnsense.oxl.app/modules/service.html)                                                       | stable   |
| **Raw**                   | ansibleguy.opnsense.raw                                                | [Docs](https://ansible-opnsense.oxl.app/modules/raw.html)                                                           | unstable |
| **Alias**                 | ansibleguy.opnsense.alias                                              | [Docs](https://ansible-opnsense.oxl.app/modules/alias.html)                                                         | stable   | 
| **Alias**                 | ansibleguy.opnsense.alias_multi                                        | [Docs](https://ansible-opnsense.oxl.app/modules/alias_multi.html)                                                   | stable   |
| **Alias**                 | ansibleguy.opnsense.alias_purge                                        | [Docs](https://ansible-opnsense.oxl.app/modules/alias_multi.html#ansibleguy-opnsense-alias-purge)                   | unstable |
| **Rules**                 | ansibleguy.opnsense.rule                                               | [Docs](https://ansible-opnsense.oxl.app/modules/rule.html)                                                          | stable   |
| **Rules**                 | ansibleguy.opnsense.rule_multi                                         | [Docs](https://ansible-opnsense.oxl.app/modules/rule_multi.html)                                                    | stable   |
| **Rules**                 | ansibleguy.opnsense.rule_purge                                         | [Docs](https://ansible-opnsense.oxl.app/modules/rule_multi.html#ansibleguy-opnsense-rule-purge)                     | unstable |
| **Rule Interface Groups** | ansibleguy.opnsense.rule_interface_group                               | [Docs](https://ansible-opnsense.oxl.app/modules/rule_interface_group.html#ansibleguy-opnsense-rule-interface-group) | stable |
| **Savepoints**            | ansibleguy.opnsense.savepoint                                          | [Docs](https://ansible-opnsense.oxl.app/modules/savepoint.html)                                                     | stable   |
| **Packages**              | ansibleguy.opnsense.package                                            | [Docs](https://ansible-opnsense.oxl.app/modules/package.html)                                                       | stable   |
| **System**                | ansibleguy.opnsense.system                                             | [Docs](https://ansible-opnsense.oxl.app/modules/system.html)                                                        | stable   |
| **Cron-Jobs**             | ansibleguy.opnsense.cron                                               | [Docs](https://ansible-opnsense.oxl.app/modules/cron.html)                                                          | stable   |
| **Routes**                | ansibleguy.opnsense.route                                              | [Docs](https://ansible-opnsense.oxl.app/modules/routing.html)                                                       | stable   |
| **Gateways**              | ansibleguy.opnsense.gateway                                            | [Docs](https://ansible-opnsense.oxl.app/modules/routing.html)                                                       | stable |
| **DNS**                   | ansibleguy.opnsense.unbound_general                                    | [Docs](https://ansible-opnsense.oxl.app/modules/unbound_general.html)                                               | stable   |
| **DNS**                   | ansibleguy.opnsense.unbound_acl                                        | [Docs](https://ansible-opnsense.oxl.app/modules/unbound_acl.html)                                                   | stable   |
| **DNS**                   | ansibleguy.opnsense.unbound_forward                                    | [Docs](https://ansible-opnsense.oxl.app/modules/unbound_forwarding.html)                                            | stable   |
| **DNS**                   | ansibleguy.opnsense.unbound_dot                                        | [Docs](https://ansible-opnsense.oxl.app/modules/unbound_dot.html)                                                   | stable   |
| **DNS**                   | ansibleguy.opnsense.unbound_host                                       | [Docs](https://ansible-opnsense.oxl.app/modules/unbound_host.html)                                                  | stable   |
| **DNS**                   | ansibleguy.opnsense.unbound_host_alias                                 | [Docs](https://ansible-opnsense.oxl.app/modules/unbound_host_alias.html)                                            | stable   |
| **DNS**                   | ansibleguy.opnsense.unbound_dnsbl                                      | [Docs](https://ansible-opnsense.oxl.app/modules/unbound_host_alias.html)                                            | stable |
| **Syslog**                | ansibleguy.opnsense.syslog                                             | [Docs](https://ansible-opnsense.oxl.app/modules/syslog.html)                                                        | stable   |
| **IPSec**                 | ansibleguy.opnsense.ipsec_connection, ansibleguy.opnsense.ipsec_tunnel | [Docs](https://ansible-opnsense.oxl.app/modules/ipsec.html)                                                         | stable   |
| **IPSec**                 | ansibleguy.opnsense.ipsec_pool, ansibleguy.opnsense.ipsec_network      | [Docs](https://ansible-opnsense.oxl.app/modules/ipsec.html)                                                         | stable   |
| **IPSec**                 | ansibleguy.opnsense.ipsec_auth_local                                   | [Docs](https://ansible-opnsense.oxl.app/modules/ipsec.html)                                                         | stable   |
| **IPSec**                 | ansibleguy.opnsense.ipsec_auth_remote                                  | [Docs](https://ansible-opnsense.oxl.app/modules/ipsec.html)                                                         | stable   |
| **IPSec**                 | ansibleguy.opnsense.ipsec_child                                        | [Docs](https://ansible-opnsense.oxl.app/modules/ipsec.html)                                                         | stable   |
| **IPSec**                 | ansibleguy.opnsense.ipsec_vti                                          | [Docs](https://ansible-opnsense.oxl.app/modules/ipsec.html)                                                         | stable   |
| **IPSec**                 | ansibleguy.opnsense.ipsec_cert                                         | [Docs](https://ansible-opnsense.oxl.app/modules/ipsec.html)                                                         | stable   |
| **IPSec**                 | ansibleguy.opnsense.ipsec_psk                                          | [Docs](https://ansible-opnsense.oxl.app/modules/ipsec.html)                                                         | stable   |
| **IPSec**                 | ansibleguy.opnsense.ipsec_manual_spd                                   | [Docs](https://ansible-opnsense.oxl.app/modules/ipsec.html)                                                         | stable   |
| **IPSec**                 | ansibleguy.opnsense.general                                            | [Docs](https://ansible-opnsense.oxl.app/modules/ipsec.html)                                                         | unstable |
| **Traffic Shaper**        | ansibleguy.opnsense.shaper_pipe                                        | [Docs](https://ansible-opnsense.oxl.app/modules/shaper.html)                                                        | stable   |
| **Traffic Shaper**        | ansibleguy.opnsense.shaper_queue                                       | [Docs](https://ansible-opnsense.oxl.app/modules/shaper.html)                                                        | stable   |
| **Traffic Shaper**        | ansibleguy.opnsense.shaper_rule                                        | [Docs](https://ansible-opnsense.oxl.app/modules/shaper.html)                                                        | stable   |
| **Monit**                 | ansibleguy.opnsense.monit_service                                      | [Docs](https://ansible-opnsense.oxl.app/modules/monit.html)                                                         | stable   |
| **Monit**                 | ansibleguy.opnsense.monit_alert                                        | [Docs](https://ansible-opnsense.oxl.app/modules/monit.html)                                                         | stable   |
| **Monit**                 | ansibleguy.opnsense.monit_test                                         | [Docs](https://ansible-opnsense.oxl.app/modules/monit.html)                                                         | stable   |
| **WireGuard**             | ansibleguy.opnsense.wireguard_server                                   | [Docs](https://ansible-opnsense.oxl.app/modules/wireguard.html)                                                     | stable   |
| **WireGuard**             | ansibleguy.opnsense.wireguard_peer                                     | [Docs](https://ansible-opnsense.oxl.app/modules/wireguard.html)                                                     | stable   |
| **WireGuard**             | ansibleguy.opnsense.wireguard_show                                     | [Docs](https://ansible-opnsense.oxl.app/modules/wireguard.html)                                                     | stable   |
| **WireGuard**             | ansibleguy.opnsense.wireguard_general                                  | [Docs](https://ansible-opnsense.oxl.app/modules/wireguard.html)                                                     | stable   |
| **Interfaces**            | ansibleguy.opnsense.interface_vlan                                     | [Docs](https://ansible-opnsense.oxl.app/modules/interface.html)                                                     | stable   |
| **Interfaces**            | ansibleguy.opnsense.interface_vxlan                                    | [Docs](https://ansible-opnsense.oxl.app/modules/interface.html)                                                     | stable   |
| **Interfaces**            | ansibleguy.opnsense.interface_vip                                      | [Docs](https://ansible-opnsense.oxl.app/modules/interface.html)                                                     | stable   |
| **Interfaces**            | ansibleguy.opnsense.interface_lagg                                     | [Docs](https://ansible-opnsense.oxl.app/modules/interface.html)                                                     | stable |
| **Interfaces**            | ansibleguy.opnsense.interface_loopback                                 | [Docs](https://ansible-opnsense.oxl.app/modules/interface.html)                                                     | stable |
| **Interfaces**            | ansibleguy.opnsense.interface_gre                                      | [Docs](https://ansible-opnsense.oxl.app/modules/interface.html)                                                     | stable   |
| **Interfaces**            | ansibleguy.opnsense.interface_bridge                                   | [Docs](https://ansible-opnsense.oxl.app/modules/interface.html)                                                     | unstable |
| **Interfaces**            | ansibleguy.opnsense.interface_gif                                      | [Docs](https://ansible-opnsense.oxl.app/modules/interface.html)                                                     | unstable |
| **NAT**                   | ansibleguy.opnsense.nat_source                                         | [Docs](https://ansible-opnsense.oxl.app/modules/source_nat.html)                                                    | stable   |
| **NAT**                   | ansibleguy.opnsense.nat_one_to_one                                     | [Docs](https://ansible-opnsense.oxl.app/modules/one_to_one.html)                                                    | stable |
| **Dynamic Routing**       | ansibleguy.opnsense.frr_diagnostic                                     | [Docs](https://ansible-opnsense.oxl.app/modules/frr_diagnostic.html)                                                | stable   |
| **Dynamic Routing**       | ansibleguy.opnsense.frr_general                                        | [Docs](https://ansible-opnsense.oxl.app/modules/frr_general.html)                                                   | stable   |
| **Dynamic Routing**       | ansibleguy.opnsense.frr_bfd_general                                    | [Docs](https://ansible-opnsense.oxl.app/modules/frr_bfd.html#ansibleguy-opnsense-frr-bfd-general)                   | stable   |
| **Dynamic Routing**       | ansibleguy.opnsense.frr_bfd_neighbor                                   | [Docs](https://ansible-opnsense.oxl.app/modules/frr_bfd.html#ansibleguy-opnsense-frr-bfd-neighbor)                  | stable   |
| **Dynamic Routing**       | ansibleguy.opnsense.frr_bgp_general                                    | [Docs](https://ansible-opnsense.oxl.app/modules/frr_bgp.html#ansibleguy-opnsense-frr-bgp-general)                   | stable   |
| **Dynamic Routing**       | ansibleguy.opnsense.frr_bgp_neighbor                                   | [Docs](https://ansible-opnsense.oxl.app/modules/frr_bgp.html#ansibleguy-opnsense-frr-bgp-neighbor)                  | stable   |
| **Dynamic Routing**       | ansibleguy.opnsense.frr_bgp_prefix_list                                | [Docs](https://ansible-opnsense.oxl.app/modules/frr_bgp.html#ansibleguy-opnsense-frr-bgp-prefix-list)               | stable   |
| **Dynamic Routing**       | ansibleguy.opnsense.frr_bgp_route_map                                  | [Docs](https://ansible-opnsense.oxl.app/modules/frr_bgp.html#ansibleguy-opnsense-frr-bgp-route-map)                 | stable   |
| **Dynamic Routing**       | ansibleguy.opnsense.frr_bgp_community_list                             | [Docs](https://ansible-opnsense.oxl.app/modules/frr_bgp.html#ansibleguy-opnsense-frr-bgp-community-list)            | stable   |
| **Dynamic Routing**       | ansibleguy.opnsense.frr_bgp_as_path                                    | [Docs](https://ansible-opnsense.oxl.app/modules/frr_bgp.html#ansibleguy-opnsense-frr-bgp-as-path)                   | stable   |
| **Dynamic Routing**       | ansibleguy.opnsense.frr_bgp_redistribution                             | [Docs](https://ansible-opnsense.oxl.app/modules/frr_bgp.html#ansibleguy-opnsense-frr-bgp-redistribution)            | stable |
| **Dynamic Routing**       | ansibleguy.opnsense.frr_bgp_peer_group                                 | [Docs](https://ansible-opnsense.oxl.app/modules/frr_bgp.html#ansibleguy-opnsense-frr-bgp-peer-group)                | stable |
| **Dynamic Routing**       | ansibleguy.opnsense.frr_ospf_general                                   | [Docs](https://ansible-opnsense.oxl.app/modules/frr_ospf.html#ansibleguy-opnsense-frr-ospf-general)                 | stable   |
| **Dynamic Routing**       | ansibleguy.opnsense.frr_ospf_prefix_list                               | [Docs](https://ansible-opnsense.oxl.app/modules/frr_ospf.html#ansibleguy-opnsense-frr-ospf-prefix-list)             | stable   |
| **Dynamic Routing**       | ansibleguy.opnsense.frr_ospf_route_map                                 | [Docs](https://ansible-opnsense.oxl.app/modules/frr_ospf.html#ansibleguy-opnsense-frr-ospf-route-map)               | stable   |
| **Dynamic Routing**       | ansibleguy.opnsense.frr_ospf_interface                                 | [Docs](https://ansible-opnsense.oxl.app/modules/frr_ospf.html#ansibleguy-opnsense-frr-ospf-interface)               | stable   |
| **Dynamic Routing**       | ansibleguy.opnsense.frr_ospf_network                                   | [Docs](https://ansible-opnsense.oxl.app/modules/frr_ospf.html#ansibleguy-opnsense-frr-ospf-network)                 | stable   |
| **Dynamic Routing**       | ansibleguy.opnsense.frr_ospf_redistribution                            | [Docs](https://ansible-opnsense.oxl.app/modules/frr_ospf.html#ansibleguy-opnsense-frr-ospf-redistribution)          | stable |
| **Dynamic Routing**       | ansibleguy.opnsense.frr_ospf3_general                                  | [Docs](https://ansible-opnsense.oxl.app/modules/frr_ospf.html#ansibleguy-opnsense-frr-ospf3-general)                | stable   |
| **Dynamic Routing**       | ansibleguy.opnsense.frr_ospf3_prefix_list                              | [Docs](https://ansible-opnsense.oxl.app/modules/frr_ospf.html#ansibleguy-opnsense-frr-ospf3-prefix-list)            | stable   |
| **Dynamic Routing**       | ansibleguy.opnsense.frr_ospf3_route_map                                | [Docs](https://ansible-opnsense.oxl.app/modules/frr_ospf.html#ansibleguy-opnsense-frr-ospf3-route-map)              | stable   |
| **Dynamic Routing**       | ansibleguy.opnsense.frr_ospf3_interface                                | [Docs](https://ansible-opnsense.oxl.app/modules/frr_ospf.html#ansibleguy-opnsense-frr-ospf3-interface)              | stable   |
| **Dynamic Routing**       | ansibleguy.opnsense.frr_ospf3_network                                  | [Docs](https://ansible-opnsense.oxl.app/modules/frr_ospf.html#ansibleguy-opnsense-frr-ospf3-network)                | stable   |
| **Dynamic Routing**       | ansibleguy.opnsense.frr_ospf3_redistribution                           | [Docs](https://ansible-opnsense.oxl.app/modules/frr_ospf.html#ansibleguy-opnsense-frr-ospf3-redistribution)         | stable |
| **Dynamic Routing**       | ansibleguy.opnsense.frr_rip                                            | [Docs](https://ansible-opnsense.oxl.app/modules/frr_rip.html)                                                       | stable   |
| **DNS**                   | ansibleguy.opnsense.bind_general                                       | [Docs](https://ansible-opnsense.oxl.app/modules/bind.html#ansibleguy-opnsense-bind-general)                         | stable   |
| **DNS**                   | ansibleguy.opnsense.bind_blocklist                                     | [Docs](https://ansible-opnsense.oxl.app/modules/bind.html#ansibleguy-opnsense-bind-blocklist)                       | stable   |
| **DNS**                   | ansibleguy.opnsense.bind_acl                                           | [Docs](https://ansible-opnsense.oxl.app/modules/bind.html#ansibleguy-opnsense-bind-acl)                             | stable   |
| **DNS**                   | ansibleguy.opnsense.bind_domain                                        | [Docs](https://ansible-opnsense.oxl.app/modules/bind.html#ansibleguy-opnsense-bind-domain)                          | stable   |
| **DNS**                   | ansibleguy.opnsense.bind_record                                        | [Docs](https://ansible-opnsense.oxl.app/modules/bind.html#ansibleguy-opnsense-bind-record)                          | stable   |
| **DNS**                   | ansibleguy.opnsense.bind_record_multi                                  | [Docs](https://ansible-opnsense.oxl.app/modules/bind.html#ansibleguy-opnsense-bind-record-multi)                    | stable   |
| **Web Proxy**             | ansibleguy.opnsense.webproxy_general                                   | [Docs](https://ansible-opnsense.oxl.app/modules/webproxy.html#id2)                                                  | stable   |
| **Web Proxy**             | ansibleguy.opnsense.webproxy_cache                                     | [Docs](https://ansible-opnsense.oxl.app/modules/webproxy.html#id3)                                                  | stable   |
| **Web Proxy**             | ansibleguy.opnsense.webproxy_parent                                    | [Docs](https://ansible-opnsense.oxl.app/modules/webproxy.html#id4)                                                  | stable   |
| **Web Proxy**             | ansibleguy.opnsense.webproxy_traffic                                   | [Docs](https://ansible-opnsense.oxl.app/modules/webproxy.html#id5)                                                  | stable   |
| **Web Proxy**             | ansibleguy.opnsense.webproxy_forward                                   | [Docs](https://ansible-opnsense.oxl.app/modules/webproxy.html#id7)                                                  | stable   |
| **Web Proxy**             | ansibleguy.opnsense.webproxy_acl                                       | [Docs](https://ansible-opnsense.oxl.app/modules/webproxy.html#id8)                                                  | stable   |
| **Web Proxy**             | ansibleguy.opnsense.webproxy_icap                                      | [Docs](https://ansible-opnsense.oxl.app/modules/webproxy.html#id9)                                                  | stable   |
| **Web Proxy**             | ansibleguy.opnsense.webproxy_auth                                      | [Docs](https://ansible-opnsense.oxl.app/modules/webproxy.html#id10)                                                 | stable   |
| **Web Proxy**             | ansibleguy.opnsense.webproxy_remote_acl                                | [Docs](https://ansible-opnsense.oxl.app/modules/webproxy.html#id12)                                                 | stable   |
| **Web Proxy**             | ansibleguy.opnsense.webproxy_pac_proxy                                 | [Docs](https://ansible-opnsense.oxl.app/modules/webproxy.html#id14)                                                 | stable   |
| **Web Proxy**             | ansibleguy.opnsense.webproxy_pac_match                                 | [Docs](https://ansible-opnsense.oxl.app/modules/webproxy.html#id15)                                                 | stable   |
| **Web Proxy**             | ansibleguy.opnsense.webproxy_pac_rule                                  | [Docs](https://ansible-opnsense.oxl.app/modules/webproxy.html#id18)                                                 | stable   |
| **IDS/IPS**               | ansibleguy.opnsense.ids_action                                         | [Docs](https://ansible-opnsense.oxl.app/modules/ids.html#id2)                                                       | stable   |
| **IDS/IPS**               | ansibleguy.opnsense.ids_general                                        | [Docs](https://ansible-opnsense.oxl.app/modules/ids.html#id3)                                                       | stable   |
| **IDS/IPS**               | ansibleguy.opnsense.ids_ruleset                                        | [Docs](https://ansible-opnsense.oxl.app/modules/ids.html#id4)                                                       | stable   |
| **IDS/IPS**               | ansibleguy.opnsense.ids_rule                                           | [Docs](https://ansible-opnsense.oxl.app/modules/ids.html#id5)                                                       | stable   |
| **IDS/IPS**               | ansibleguy.opnsense.ids_user_rule                                      | [Docs](https://ansible-opnsense.oxl.app/modules/ids.html#id6)                                                       | stable   |
| **IDS/IPS**               | ansibleguy.opnsense.ids_policy                                         | [Docs](https://ansible-opnsense.oxl.app/modules/ids.html#id7)                                                       | stable   |
| **IDS/IPS**               | ansibleguy.opnsense.ids_policy_rule                                    | [Docs](https://ansible-opnsense.oxl.app/modules/ids.html#id8)                                                       | stable   |
| **OpenVPN**               | ansibleguy.opnsense.openvpn_client                                     | [Docs](https://ansible-opnsense.oxl.app/modules/openvpn.html)                                                       | stable   |
| **OpenVPN**               | ansibleguy.opnsense.openvpn_server                                     | [Docs](https://ansible-opnsense.oxl.app/modules/openvpn.html)                                                       | stable   |
| **OpenVPN**               | ansibleguy.opnsense.openvpn_static_key                                 | [Docs](https://ansible-opnsense.oxl.app/modules/openvpn.html)                                                       | stable   |
| **OpenVPN**               | ansibleguy.opnsense.openvpn_status                                     | [Docs](https://ansible-opnsense.oxl.app/modules/openvpn.html)                                                       | stable   |
| **OpenVPN**               | ansibleguy.opnsense.openvpn_client_override                            | [Docs](https://ansible-opnsense.oxl.app/modules/openvpn.html)                                                       | stable   |
| **Nginx**                 | ansibleguy.opnsense.nginx_general                                      | [Docs](https://ansible-opnsense.oxl.app/modules/nginx.html#ansibleguy-opnsense-nginx-general)                       | stable |
| **Nginx**                 | ansibleguy.opnsense.nginx_upstream_server                              | [Docs](https://ansible-opnsense.oxl.app/modules/nginx.html#ansibleguy-opnsense-nginx-upstream-server)               | stable |
| **DHCP Relay**            | ansibleguy.opnsense.dhcrelay_relay                                     | [Docs](https://ansible-opnsense.oxl.app/modules/dhcrelay_relay.html)                                                | stable |
| **DHCP Relay**            | ansibleguy.opnsense.dhcrelay_destination                               | [Docs](https://ansible-opnsense.oxl.app/modules/dhcrelay_destination.html)                                          | stable |
| **DHCP**                  | ansibleguy.opnsense.dhcp_general                                       | [Docs](https://ansible-opnsense.oxl.app/modules/dhcp.html)                                                          | stable |
| **DHCP Subnet**           | ansibleguy.opnsense.dhcp_subnet                                        | [Docs](https://ansible-opnsense.oxl.app/modules/dhcp.html)                                                          | stable |
| **DHCP Reservation**      | ansibleguy.opnsense.dhcp_reservation                                   | [Docs](https://ansible-opnsense.oxl.app/modules/dhcp.html)                                                          | stable |
| **DHCP Controlagent**     | ansibleguy.opnsense.dhcp_controlagent                                  | [Docs](https://ansible-opnsense.oxl.app/modules/dhcp.html)                                                          | stable |
| **ACME (Certificates)**   | ansibleguy.opnsense.acme_account                                       | [Docs](https://ansible-opnsense.oxl.app/modules/acmeclient.html)                                                    | stable |
| **ACME (Certificates)**   | ansibleguy.opnsense.acme_action                                        | [Docs](https://ansible-opnsense.oxl.app/modules/acmeclient.html)                                                    | stable |
| **ACME (Certificates)**   | ansibleguy.opnsense.acme_general                                       | [Docs](https://ansible-opnsense.oxl.app/modules/acmeclient.html)                                                    | stable |
| **ACME (Certificates)**   | ansibleguy.opnsense.acme_validation                                    | [Docs](https://ansible-opnsense.oxl.app/modules/acmeclient.html)                                                    | stable |
| **ACME (Certificates)**   | ansibleguy.opnsense.acme_certificate                                   | [Docs](https://ansible-opnsense.oxl.app/modules/acmeclient.html)                                                    | stable |
| **Postfix**               | ansibleguy.opnsense.postfix_general                                    | [Docs](https://ansible-opnsense.oxl.app/modules/postfix.html)                                                       | stable |
| **Postfix**               | ansibleguy.opnsense.postfix_domain                                     | [Docs](https://ansible-opnsense.oxl.app/modules/postfix.html)                                                       | stable |
| **Postfix**               | ansibleguy.opnsense.postfix_recipient                                  | [Docs](https://ansible-opnsense.oxl.app/modules/postfix.html)                                                       | stable |
| **Postfix**               | ansibleguy.opnsense.postfix_recipientbcc                               | [Docs](https://ansible-opnsense.oxl.app/modules/postfix.html)                                                       | stable |
| **Postfix**               | ansibleguy.opnsense.postfix_sender                                     | [Docs](https://ansible-opnsense.oxl.app/modules/postfix.html)                                                       | stable |
| **Postfix**               | ansibleguy.opnsense.postfix_senderbcc                                  | [Docs](https://ansible-opnsense.oxl.app/modules/postfix.html)                                                       | stable |
| **Postfix**               | ansibleguy.opnsense.postfix_sendercanonical                            | [Docs](https://ansible-opnsense.oxl.app/modules/postfix.html)                                                       | stable |
| **Postfix**               | ansibleguy.opnsense.postfix_headercheck                                | [Docs](https://ansible-opnsense.oxl.app/modules/postfix.html)                                                       | stable |
| **Postfix**               | ansibleguy.opnsense.postfix_address                                    | [Docs](https://ansible-opnsense.oxl.app/modules/postfix.html)                                                       | stable |
| **Snapshot**              | ansibleguy.opnsense.snapshot                                           | [Docs](https://ansible-opnsense.oxl.app/modules/snapshot.html)                                                      | stable |
| **High Availability**     | ansibleguy.opnsense.hasync_general                                     | [Docs](https://ansible-opnsense.oxl.app/modules/hasync.html)                                                        | stable |
| **High Availability**     | ansibleguy.opnsense.hasync_service                                     | [Docs](https://ansible-opnsense.oxl.app/modules/hasync.html)                                                        | stable |
| **User Management**       | ansibleguy.opnsense.user                                               | [Docs](https://ansible-opnsense.oxl.app/modules/access.html)                                                        | unstable |
| **User Management**       | ansibleguy.opnsense.group                                              | [Docs](https://ansible-opnsense.oxl.app/modules/access.html)                                                        | unstable |
| **User Management**       | ansibleguy.opnsense.privilege                                          | [Docs](https://ansible-opnsense.oxl.app/modules/access.html)                                                        | unstable |
| **Neighbor**              | ansibleguy.opnsense.neighbor                                           | [Docs](https://ansible-opnsense.oxl.app/modules/neighbor.html)                                                      | unstable |
| **Dnsmasq**               | ansibleguy.opnsense.dnsmasq_general                                    | [Docs](https://ansible-opnsense.oxl.app/modules/dnsmasq.html)                                                             | unstable |

### Roadmap

See: [Feature Requests](https://github.com/O-X-L/ansible_opnsense/issues?q=is%3Aopen+is%3Aissue+label%3Aenhancement)
