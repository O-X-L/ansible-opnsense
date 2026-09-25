.. _modules_gateway_group:

Gateway groups
==============

**STATE**: experimental; mocked tests pass, live validation is pending.

The **oxlorg.opnsense.gateway_group** module manages the gateway groups API
introduced in OPNsense 26.7. It uses **routing/group_settings**.
Individual gateways must already exist; use **oxlorg.opnsense.gateway**
to manage them.

Parameters
----------

.. include:: ../_include/param_basic.rst

Use **ansible-doc oxlorg.opnsense.gateway_group** for the full parameter list.

* **name** identifies the group, or **uuid** selects an existing group.
  Unknown UUIDs and ambiguous names fail. OPNsense forbids renaming a group.
* **tier_1** through **tier_5** are lists of existing gateway names.
  Lower tiers have priority. At least one gateway is required; a gateway must
  occur in only one tier. Omitted tiers preserve existing values.
* **trigger** accepts down, downloss, downlatency, or downlosslatency.
* **pool_options** accepts an empty string, round-robin, or
  round-robin sticky-address.
* **description** updates the description.
* **state** defaults to present; explicit absent deletes only the selected
  group. Referenced groups cannot be deleted.
* **reload** defaults to false. Set it to true to apply a change, or use
  **oxlorg.opnsense.reload** with target **gateway_group** later.

Omitted fields preserve existing values; new objects use API defaults.
Check mode reads and compares without modifying or reloading.
Writes are read back and verified before a successful result is returned.

The 26.7.3 gateway model ignores attempts to empty an existing tier 1. The module
rejects this change before writing. Adjust tier 1 manually first if required;
the module never deletes and recreates a group as a workaround.

Example
-------

.. code-block:: yaml

    - name: Configure WAN failover
      oxlorg.opnsense.gateway_group:
        firewall: firewall.example.test
        api_credential_file: /secure/opnsense.key
        name: WAN_FAILOVER
        tier_1: [WAN_PRIMARY]
        tier_2: [WAN_BACKUP]
        trigger: down
        reload: true

    - name: Inspect configured gateway groups
      oxlorg.opnsense.list:
        firewall: firewall.example.test
        api_credential_file: /secure/opnsense.key
        target: gateway_group

Testing
-------

Mocked tests are in **plugins/module_utils/main/gateway_group_pytest.py**.
The opt-in **tests/gateway_group.yml** needs two existing gateway names in
**TEST_GATEWAY_PRIMARY** and **TEST_GATEWAY_BACKUP**.
It refuses a pre-existing test group and cleans up only the UUID it created.
It is not enabled in the global runner until live validation.

.. code-block:: console

    export TEST_FIREWALL=firewall.example.test
    export TEST_API_KEY=/secure/test-firewall.key
    export TEST_GATEWAY_PRIMARY=WAN_PRIMARY
    export TEST_GATEWAY_BACKUP=WAN_BACKUP
    ansible-playbook tests/gateway_group.yml

API evidence
------------

The controller and XML model are in opnsense/core at tag 26.7.3:
src/opnsense/mvc/app/controllers/OPNsense/Routing/Api/GroupSettingsController.php
and src/opnsense/mvc/app/models/OPNsense/Routing/GatewayGroups.xml.
