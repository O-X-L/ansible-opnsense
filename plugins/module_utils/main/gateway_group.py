from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.module import BaseModule


class GatewayGroup(BaseModule):
    FIELD_ID = 'name'
    EXIST_ATTR = 'group'
    API_MOD = 'routing'
    API_CONT = 'group_settings'
    API_KEY_PATH = 'gateway_group'
    CMDS = {'search': 'search', 'detail': 'get', 'add': 'add', 'set': 'set', 'del': 'del'}
    FIELDS_CHANGE = ['name', 'description', 'trigger', 'pool_options',
                     'tier_1', 'tier_2', 'tier_3', 'tier_4', 'tier_5']
    FIELDS_ALL = FIELDS_CHANGE
    FIELDS_TRANSLATE = {
        'description': 'descr', 'pool_options': 'poolopts',
        'tier_1': 'item', 'tier_2': 'item2', 'tier_3': 'item3', 'tier_4': 'item4', 'tier_5': 'item5',
    }
    FIELDS_TYPING = {'select': ['trigger', 'pool_options'],
                     'list': ['tier_1', 'tier_2', 'tier_3', 'tier_4', 'tier_5']}

    def __init__(self, module, result, session=None):
        super().__init__(m=module, r=result, s=session)
        self.group = {}

    def _rows(self):
        rows = []
        page = 1
        while True:
            response = self._api_post({
                'module': self.API_MOD, 'controller': self.API_CONT, 'command': 'search',
                'data': {'current': page, 'rowCount': self.QUERY_MAX_ENTRIES},
            })
            if not isinstance(response.get('rows'), list):
                self.m.fail_json('Gateway group API unavailable or invalid search response; requires OPNsense 26.7.')
            batch = response['rows']
            rows.extend(batch)
            if len(rows) >= int(response.get('total', len(rows))):
                return rows
            if not batch:
                self.m.fail_json('Gateway group API returned incomplete search results.')
            page += 1

    def _detail(self, uuid=None):
        response = self._api_get({
            'module': self.API_MOD, 'controller': self.API_CONT, 'command': 'get',
            'params': [uuid] if uuid else [],
        })
        raw = response.get('gateway_group')
        if not isinstance(raw, dict) or not all(
                self.FIELDS_TRANSLATE.get(field, field) in raw for field in self.FIELDS_ALL):
            self.m.fail_json('Invalid gateway group detail response; requires the OPNsense 26.7 API.')
        return raw

    def simplify_existing(self, existing: dict) -> dict:
        # The shared translator casts numeric strings to integers, but these are text fields.
        text_fields = {'name': existing['name'], 'description': existing['descr']}
        simplified = super().simplify_existing(existing)
        simplified.update(text_fields)
        return simplified

    def get_existing(self):
        return [self.simplify_existing(dict(self._detail(row['uuid']), uuid=row['uuid']))
                for row in self._rows()]

    def check(self):
        uuid = self.p.get('uuid')
        name = self.p.get('name')
        if not uuid and not name:
            self.m.fail_json('Provide name or UUID for the gateway group.')
        rows = self._rows()
        matches = [row for row in rows if row.get('uuid') == uuid] if uuid else [
            row for row in rows if row.get('name') == name]
        if len(matches) > 1:
            self.m.fail_json('Ambiguous gateway group name; use an explicit UUID.')
        if uuid and not matches:
            self.m.fail_json('The supplied gateway group UUID does not exist.')
        self.exists = bool(matches)
        self.raw = self._detail(matches[0]['uuid'] if matches else None)
        defaults = self.simplify_existing(self.raw)
        if self.exists:
            self.group = dict(defaults, uuid=matches[0]['uuid'])
            self.call_cnf['params'] = [self.group['uuid']]
            if name and name != self.group['name']:
                self.m.fail_json('OPNsense does not allow renaming an existing gateway group.')
            self.r['uuid'] = self.group['uuid']
            self.r['diff']['before'] = self.build_diff(self.group)

        if self.p['state'] == 'absent':
            return
        # An omitted field preserves the existing value (or the API creation default).
        for field in self.FIELDS_ALL:
            if self.p.get(field) is None:
                self.p[field] = defaults[field]
        self._validate_tiers()
        self.r['diff']['after'] = self.build_diff(self.p)

    def _validate_tiers(self):
        tiers = []
        for tier in self.FIELDS_TYPING['list']:
            values = self.p[tier]
            choices = self.raw[self.FIELDS_TRANSLATE[tier]]
            for gateway in values:
                if not isinstance(choices, dict) or gateway not in choices:
                    self.m.fail_json(f"Unknown gateway '{gateway}' in {tier}.")
                if gateway in tiers:
                    self.m.fail_json(f"Gateway '{gateway}' occurs in more than one tier or twice in a tier.")
                tiers.append(gateway)
        if not tiers:
            self.m.fail_json('At least one gateway tier must be configured.')
        # 26.7.3 GatewayGroupItemField.setValue ignores empty values.
        if self.exists and self.group['tier_1'] and not self.p['tier_1']:
            self.m.fail_json('The OPNsense 26.7 API cannot safely clear tier_1; adjust it manually first.')

    def process(self):
        self._base_process()

    def create(self):
        response = self._base_create()
        if not self.m.check_mode:
            uuid = response.get('uuid')
            if response.get('result') != 'saved' or not uuid:
                self.m.fail_json('Gateway group creation did not return a saved UUID.')
            self.r['uuid'] = uuid
            self._verify(uuid)
        return response

    def update(self):
        response = self._base_update(enable_switch=False)
        if self.r['changed'] and not self.m.check_mode:
            self._verify(self.group['uuid'])
        return response

    def delete(self):
        response = self._base_delete()
        if not self.m.check_mode:
            if response.get('in_use'):
                self.m.fail_json('Gateway group is in use; remove its references before deletion.')
            if response.get('result') != 'deleted':
                self.m.fail_json('Gateway group deletion failed.')
            if any(row['uuid'] == self.group['uuid'] for row in self._rows()):
                self.m.fail_json('Gateway group deletion verification failed.')
        return response

    def reload(self):
        response = self._base_reload()
        if not self.m.check_mode and response.get('status') != 'ok':
            self.m.fail_json('Gateway group reload failed.')
        return response

    def _verify(self, uuid):
        actual = self.simplify_existing(self._detail(uuid))
        for field in self.FIELDS_ALL:
            expected = self.p[field]
            observed = actual[field]
            if isinstance(expected, list):
                expected, observed = sorted(expected), sorted(observed)
            if expected != observed:
                self.m.fail_json(
                    f"Gateway group write verification failed for {field}; inspect the saved configuration."
                )
