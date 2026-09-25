.. _modules_service:

.. include:: ../_include/head.rst

=======
Service
=======

**STATE**: stable

**TESTS**: `Playbook <https://github.com/oxlorg/collection_opnsense/blob/latest/tests/service.yml>`_

Contribution
************

Thanks to `@Rath <https://github.com/superstes>`_ for developing this module!

----

Info
****

This module can interact with a specified service running on the OPNsense system.

Definition
**********

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "name","string","true","\-","service, target, svc, n","Pretty name of the service to interact with. One of: 'acme_client', 'apcupsd', 'bind', 'captive_portal', 'chrony', 'cicap', 'clamav', 'collectd', 'cron', 'crowdsec', 'dns_crypt_proxy', 'dyndns', 'fetchmail', 'freeradius', 'frr', 'ftp_proxy', 'haproxy', 'hwprobe', 'ids', 'iperf', 'ipsec', 'ipsec_legacy', 'lldpd', 'maltrail', 'mdns_repeater', 'monit', 'munin_node', 'netdata', 'netsnmp', 'nginx', 'node_exporter', 'nrpe', 'ntopng', 'nut', 'openconnect', 'openssh', 'openvpn', 'postfix', 'proxy', 'proxysso', 'puppet_agent', 'qemu_guest_agent', 'radsec_proxy', 'redis', 'relayd', 'rspamd', 'shadowsocks', 'shaper', 'siproxd', 'softether', 'sslh', 'stunnel', 'syslog', 'tayga', 'telegraf', 'tftp', 'tinc', 'tor', 'udp_broadcast_relay', 'unbound', 'vnstat', 'wireguard', 'zabbix_agent', 'zabbix_proxy', 'kea' (dhcp)"
    "action","string","true","\-","do, a","What action to execute. Some services may not support all of these actions (*the module will inform you in that case*). One of: 'status', 'start', 'reload', 'restart', 'stop'"

.. include:: ../_include/param_basic.rst

----

Examples
********

.. code-block:: yaml

    - hosts: firewalls
      connection: local
      gather_facts: false
      module_defaults:
        group/oxlorg.opnsense.all:
          firewall: 'opnsense.template.opnsense.oxl.app'
          api_credential_file: '/home/guy/.secret/opn.key'

      tasks:
        - name: Restarting IPSec service
          oxlorg.opnsense.service:
            name: 'ipsec'
            action: 'restart'

        - name: Get status of FRR service
          oxlorg.opnsense.service:
            name: 'frr'
            action: 'status'
          register: frr_svc

        - name: Printing FRR service status
          ansible.builtin.debug:
            var: frr_svc.data

        - name: Stopping Tor service
          oxlorg.opnsense.service:
            name: 'tor'
            action: 'stop'

SSH runtime control
*******************

On OPNsense 26.7, use :code:`name: openssh` for :code:`status`, :code:`start`,
:code:`stop` or :code:`restart`. The module reads :code:`core/service/search`
and addresses actions as :code:`core/service/<action>/openssh`.

Start and stop are unchanged when the service already has the requested state.
Restart always reports a change. Check mode reads status without changing the
service. A missing service registration fails clearly; enable/configure SSH in
the OPNsense GUI first. The module verifies the reported state after a mutation.

Stopping the process does not persistently disable SSH at boot. Persistent
enablement is outside this API. Reload is unsupported.

.. code-block:: yaml

    - name: Stop SSH after API provisioning
      oxlorg.opnsense.service:
        name: openssh
        action: stop

The opt-in :code:`tests/service_openssh.yml` playbook checks status only.
Tests for start/stop/restart use mocked API responses; live SSH lifecycle testing
must be done on a dedicated test firewall with alternative access available.
