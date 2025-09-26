from ansible_collections.ansibleguy.opnsense.plugins.module_utils.test.testdata.base_testdata import MockOPNsenseController


class Testdata_25_7_3(MockOPNsenseController):
    def __init__(self):
        super().__init__(key_path=['job', 'jobs', 'job'])
        self.state = {self._new_uuid(): self._build_entry({
            "origin": "IDS", "enabled": "0", "minutes": "0", "hours": "0", "days": "*", "months": "*",
            "weekdays": "*", "who": "root", "command": "ids update", "parameters": "",
            "description": "ids rule updates"
        })}

    def commands(self) -> dict:
        return {
            'get': self._get,
            'add_job': self._add,
            'set_job': self._set,
            'del_job': self._del,
            'toggle_job': self._toggle,
            'reconfigure': self._reconfigure,
        }

    @staticmethod
    def _build_commands(cmd: str) -> dict:
        valid_cmds = ['nginx autoblock', 'firmware auto-update', 'proxy fetchacls', 'bind dnsblcron', 'proxy downloadacls', 'firmware changelog cron', 'firmware poll', 'systemha_reconfigure_backup', 'systemreboot', 'interface routes alarm', 'interface reconfigure', 'quagga reload', 'idsreload', 'ipsec reload', 'dns reload', 'system remote backup', 'acmeclient cron-auto-renew', 'wireguard renew', 'captiveportal restart', 'cron restart', 'dhcpdrestart', 'dhcpd6 restart', 'dnsmasq restart', 'freeradius restart', 'quagga restart', 'idsrestart', 'ipsecrestart', 'kea restart', 'monit restart', 'netflowrestart', 'openssh restart', 'postfix restart', 'stunnel restart', 'syslogrestart', 'unboundrestart', 'webgui restart', 'proxy restart', 'wireguard restart', 'zabbixagentrestart', 'syslog archive', 'dhcpd start', 'dhcpd6start', 'freeradius start', 'dhcpd stop', 'dhcpd6stop', 'freeradius stop', 'filter refresh_aliases', 'ids update', 'unbound dnsbl', 'zfsscrub', 'zfs trim']
        out = {}
        for k in valid_cmds:
            selected = 1 if k == cmd else 0
            out[k] = {'value': f'Text for {k}', 'selected': selected}

        return out

    def _build_entry(self, data: dict) -> dict:
        return {
            "origin": data['origin'],
            "enabled": data['enabled'],
            "minutes": data['minutes'],
            "hours": data['hours'],
            "days": data['days'],
            "months": data['months'],
            "weekdays": data['weekdays'],
            "who": data['who'],
            "command": self._build_commands(data['command']),
            "parameters": data['parameters'],
            "description": data['description']
        }

    def _add(self, data: dict) -> dict:
        self.state[self._new_uuid()] = self._build_entry(data)
        return {'status': 'ok'}

    def _set(self, uuid: str, data: dict) -> dict:
        if uuid in self.state:
            self.state[uuid] = self._build_entry(data)
            return {'status': 'ok'}

        else:
            return {'status': 'error'}
