from ansible.module_utils.basic import AnsibleModule

from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.oxlorg.opnsense.plugins.module_utils.helper.main import \
    is_unset
from ansible_collections.oxlorg.opnsense.plugins.module_utils.helper.match import \
    get_multiple_matching
from ansible_collections.oxlorg.opnsense.plugins.module_utils.helper.trust import \
    strip_keys_and_duplicates, lifetime_days, check_immutable
from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.module import BaseModule


class BaseTrust(BaseModule):
    # NOTE: most fields of the trust-models are 'volatile' - they are not saved but parsed from the certificate
    #   only the description can be changed without re-issuing the certificate
    API_MOD = 'trust'
    FIELDS_CHANGE = ['description']
    FIELDS_IMMUTABLE = []
    INT_VALIDATIONS = {
        'lifetime': {'min': 1},
    }
    EXIST_ATTR = 'entry'
    KIND = 'entry'

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session)
        self.entry = {}

    def check(self) -> None:
        if self.p['state'] == 'present':
            self._resolve_ca()

        self._base_check()

        if self.p['state'] == 'present' and self.exists:
            check_immutable(
                module=self.m,
                existing=self.entry,
                params=self.p,
                fields=self.FIELDS_IMMUTABLE,
                kind=self.KIND,
            )

        self._check_ambiguous()

    def _check_ambiguous(self) -> None:
        if not self.exists:
            return

        matching = get_multiple_matching(
            module=self.m,
            existing_items=self.existing_entries,
            compare_item=self.p,
            match_fields=self.p['match_fields'],
            simplify_func=self.simplify_existing,
        )
        if len(matching) > 1:
            self.m.fail_json(
                f"Multiple existing {self.KIND} entries match the fields {self.p['match_fields']} - "
                'unable to decide which one to manage!'
            )

    def _resolve_ca(self) -> None:
        # the issuing CA can be provided by its description or reference-id
        if is_unset(self.p['ca']):
            self.p['ca'] = ''
            return

        cas = self.s.get(cnf={
            **self.call_cnf,
            'command': self.CMDS['ca_list'],
        })['rows']

        by_refid = [ca for ca in cas if ca['caref'] == self.p['ca']]
        if len(by_refid) == 1:
            return

        by_desc = [ca for ca in cas if ca['descr'] == self.p['ca']]
        if len(by_desc) == 0:
            self.m.fail_json(f"Provided CA '{self.p['ca']}' was not found!")

        if len(by_desc) > 1:
            self.m.fail_json(
                f"Multiple CAs with the description '{self.p['ca']}' exist - provide its reference-id instead!"
            )

        self.p['ca'] = by_desc[0]['caref']

    def search_call(self) -> list:
        # the search-response already contains all fields - no need to pull the details of every entry
        #   the private keys are removed right away - this is also used by the 'list' module
        return [
            strip_keys_and_duplicates(entry)
            for entry in self.api_search_post({
                **self.call_cnf,
                'command': self.CMDS['search'],
            })
        ]

    def simplify_existing(self, existing: dict) -> dict:
        simple = self._base_simplify_existing(existing)
        simple['lifetime'] = lifetime_days(simple)
        return simple

    def _get_detail(self) -> dict:
        return self.s.get(cnf={
            **self.call_cnf,
            'command': self.CMDS['detail'],
            'params': [self.entry[self.field_pk]],
        })[self.API_KEY_PATH]
