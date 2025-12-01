.. _modules_wazuh_agent:

.. include:: ../_include/head.rst

===========
Wazuh Agent
===========

**State:** Unstable

**Tests:** `wazuh_agent.yml <https://github.com/O-X-L/ansible_opnsense/blob/latest/tests/wazuh_agent.yml>`_

**API Docs**: `Plugins - Wazuh Agent <https://docs.opnsense.org/development/api/plugins/wazuhagent.html>`_

**Service Docs**: `OPNsense Wazuh Agent <https://docs.opnsense.org/manual/wazuh-agent.html>`_


Contribution
************

Thanks to `@MaximeWewer <https://github.com/MaximeWewer>`_ for developing this module!

If you encounter any issues or have suggestions for improvements, please feel free to contribute to the project.

----

Prerequisites
*************

You need to install the Wazuh agent plugin:

```
os-wazuh-agent
```

You can also install it using the :ref:`oxlorg.opnsense.package <modules_package>` module.

----

Function
********

This module allows you to configure the Wazuh agent on your OPNsense firewall.

Wazuh is a comprehensive security platform that provides unified XDR and SIEM protection for endpoints and cloud workloads.

The agent collects security-relevant data and sends it to the Wazuh server for analysis.

Parameters
##########

.. csv-table:: Definition
   :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
   :widths: 15 10 10 10 10 45

   "enabled","boolean","false","true","\-","Enable/disable Wazuh Agent"
   "server_address","string","true","\-","server","Specifies the IP address or the hostname of the Wazuh manager."
   "agent_name","string","false","\-","\-","Specifies the hostname of this agent."
   "protocol","choice","false","tcp","\-","Specifies the transport protocol to use. One of: 'tcp', 'udp'"
   "port","integer","false","1514","\-","Specifies the port to use for communicating with the Wazuh manager."
   "debug_level","choice","false","0","\-","Debug level for this agents services. One of: 0, 1, 2"
   "auth_password","string","false","\-","\-","Password to use in authd.pass file."
   "auth_port","integer","false","1515","\-","Specifies the port to use for communicating with the Wazuh manager during enrollment."
   "remote_commands","boolean","false","true","\-","Enable remote commands from the log collector"
   "syslog_programs","list","false","\-","\-","Choose which applications to forward to Wazuh."
   "suricata_eve_log","boolean","false","true","\-","Send events from the intrusion detection engine to Wazuh"
   "rootcheck_enabled","boolean","false","true","\-","Enable policy monitoring and anomaly detection"
   "syscollector_enabled","boolean","false","true","\-","Enable syscollector"
   "syscheck_enabled","boolean","false","true","\-","Enable file integrity monitoring"
   "active_response_enabled","boolean","false","true","\-","Enable Active response"
   "active_response_remote_commands","boolean","false","true","\-","Toggles whether Command Module should accept commands"
   "active_response_fw_alias_ignore","list","false","\-","\-","Select an alias from which items should be ignored when dropping IP addresses"

.. include:: ../_include/param_basic.rst

.. include:: ../_include/param_reload.rst

----

Usage
*****

This module configures general Wazuh agent settings.

After configuration changes, the agent service will be reloaded automatically.

.. warning::

   Make sure to properly configure your Wazuh server before enabling the agent.

----

Examples
********

.. code-block:: yaml

    - hosts: firewalls
      connection: local
      gather_facts: false
      module_defaults:
        group/oxlorg.opnsense.all:
          firewall: 'opnsense.template.oxlorg.net'
          api_credential_file: '/home/guy/.secret/opn.key'

      tasks:
        - name: Example
          oxlorg.opnsense.wazuh_agent:
            server_address: '192.168.1.100'
            # agent_name: ''
            # protocol: 'tcp'
            # port: 1514
            # debug_level: 0
            # auth_password: ''
            # auth_port: 1515
            # remote_commands: true
            # syslog_programs: []
            # suricata_eve_log: true
            # rootcheck_enabled: true
            # syscollector_enabled: true
            # syscheck_enabled: true
            # active_response_enabled: true
            # active_response_remote_commands: true
            # active_response_fw_alias_ignore: []
            # reload: true
            # enabled: true

        - name: Configure basic Wazuh agent
          oxlorg.opnsense.wazuh_agent:
            server_address: '192.168.1.100'
            agent_name: 'opnsense-fw'

        - name: Configure Wazuh agent with authentication
          oxlorg.opnsense.wazuh_agent:
            server_address: 'wazuh.example.com'
            agent_name: 'firewall-01'
            protocol: 'tcp'
            port: 1514
            auth_password: 'your-auth-password'
            auth_port: 1515

        - name: Configure Wazuh agent with custom logging
          oxlorg.opnsense.wazuh_agent:
            server_address: '10.0.0.100'
            remote_commands: true
            syslog_programs:
              - 'filterlog'
              - 'suricata'
              - 'unbound'
            suricata_eve_log: true

        - name: Disable Wazuh agent modules selectively
          oxlorg.opnsense.wazuh_agent:
            server_address: '192.168.1.100'
            rootcheck_enabled: false
            syscheck_enabled: false
            active_response_enabled: false

        - name: Configure with debug output
          oxlorg.opnsense.wazuh_agent:
            server_address: '192.168.1.100'
            debug_level: 2
            debug: true

----

Troubleshooting
***************

Make sure your Wazuh server is reachable from the OPNsense firewall and that the specified ports are open in your firewall rules.

Check the Wazuh agent logs on the firewall for connection issues:

.. code-block:: bash

    # Check agent status
    /usr/local/ossec/bin/agent_control -l
    
    # View agent logs
    tail -f /var/ossec/logs/ossec.log