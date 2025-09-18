# FRR Diagnostic

**STATE**: stable

**TESTS**: [frr_diagnostic](https://github.com/O-X-L/ansible_opnsense/blob/latest/tests/frr_diagnostic.yml)

**API Docs**: [Plugins - Quagga](https://docs.opnsense.org/development/api/plugins/quagga.html)

**Service Docs**: [Dynamic Routing](https://docs.opnsense.org/manual/dynamic_routing.html)

**FRR Docs**: [FRRouting](https://docs.frrouting.org/) (_make sure you are looking at the current OPNSense package version!_)

## Contribution

Thanks to [@Rath](https://github.com/superstes) for developing this module!

## Sponsoring

Thanks to [@telmich](https://github.com/telmich) for sponsoring the development of this module!

----

## Prerequisites

You need to install the FRR plugin:
```
os-frr
```

You can also install it using the [package module](https://ansible-opnsense.oxl.app/modules/package.html).

----

## Definition

For basic parameters see: [Basics](https://ansible-opnsense.oxl.app/usage/2_basic.html)

### ansibleguy.opnsense.frr_diagnostic

| Parameter   | Type            | Required | Default value         | Aliases | Comment                                                                                                                                                                                                                                                                                                                                  |
|:------------|:----------------|:---------|:----------------------|:--------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| target      | string          | true     | -                     | -       | What information to query. One of: 'bgpneighbors', 'bgproute', 'bgproute4', 'bgproute6', 'bgpsummary', 'generalroute', 'generalroute4', 'generalroute6', 'generalrunningconfig', 'ospfdatabase', 'ospfinterface', 'ospfneighbor', 'ospfoverview', 'ospfroute', 'ospfv3database', 'ospfv3interface', 'ospfv3neighbor', 'ospfv3overview', 'ospfv3route' |

----

## Examples

### ansibleguy.opnsense.frr_diagnostic

```yaml
- hosts: localhost
  gather_facts: no
  module_defaults:
    group/ansibleguy.opnsense.all:
      firewall: 'opnsense.template.ansibleguy.net'
      api_credential_file: '/home/guy/.secret/opn.key'

  tasks:
    - name: Example
      ansibleguy.opnsense.frr_diagnostic:
        target: 'generalroute'
      register: frr_info

    - name: Printing
      ansible.builtin.debug:
        var: frr_info.data
```
