from typing import Callable

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.common.arg_spec import ModuleArgumentSpecValidator

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.handler import ModuleSoftError
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import diff_remove_empty
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.cls import BaseModule
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.validate import is_unset


# pylint: disable=R0913,R0917
class MultiModule:
    def __init__(
            self, module: AnsibleModule, result: dict, entry_args: dict, kind: str, obj: BaseModule,
            validation: bool = True, cache_existing: bool = True,
            callback_build: Callable[dict, dict] = None,
            callback_validation: Callable[dict, bool] = None,
            callback_get_existing: Callable[BaseModule, dict] = None,
            callback_set_existing: Callable[[BaseModule, dict], None] = None,
            callback_update_existing: Callable[[dict, dict], dict] = None,
            callback_purge_exclude: Callable[dict, bool] = None,
    ):
        self.m = module
        self.p = module.params
        self.mc = self.p['multi_control']
        self.r = result
        self.o = obj
        self.k = kind

        if hasattr(self.o, 'TIMEOUT'):
            self.s = Session(
                module=self.m,
                timeout=getattr(self.o, 'TIMEOUT'),
            )

        else:
            self.s = Session(module=self.m)

        self.meta_entry = self.o(module=self.m, session=self.s, result={})
        self.mod_entry_args = entry_args
        self.validation = validation
        self.cache = {}
        self.cache_existing = cache_existing
        self.callback_build = callback_build
        self.callback_validation = callback_validation
        self.callback_get_existing = callback_get_existing
        self.callback_set_existing = callback_set_existing
        self.callback_update_existing = callback_update_existing
        self.callback_purge_exclude = callback_purge_exclude
        if self.cache_existing:
            if self.callback_get_existing is None:
                self.callback_get_existing = self._default_callback_get_existing

            if self.callback_set_existing is None:
                self.callback_set_existing = self._default_callback_set_existing

        if hasattr(self.o, 'FIELD_ID'):
            self.field_id = getattr(self.o, 'FIELD_ID')
            self.match_fields = [self.field_id]

        elif hasattr(self.o, 'FIELDS_MATCH'):
            self.match_fields = getattr(self.o, 'FIELDS_MATCH')

        else:
            self.match_fields = self.p['match_fields']

    def process(self) -> None:
        if self.cache_existing:
            self.cache = self.callback_get_existing(self.meta_entry)

        self._create_update()

        if len(self.p['multi_purge']) > 0 or self.mc['purge_all']:
            self._purge()

        if self.r['changed'] and self.p['reload']:
            self.meta_entry.reload()

        self.s.close()

    # CREATE/UPDATE METHODS
    def _validate_entry(self, entry: dict) -> bool:
        result = False
        if self.mc['fail_verify']:
            error_func = self.m.fail_json

        else:
            error_func = self.m.warn

        validation = ModuleArgumentSpecValidator(
            self.mod_entry_args,
            self.m.mutually_exclusive,
            self.m.required_together,
            self.m.required_one_of,
            self.m.required_if,
            self.m.required_by,
         ).validate(parameters=entry)

        try:
            validation_error = validation.errors[0]

        except IndexError:
            validation_error = None

        if validation_error:
            error_func(f"Got invalid config for {self.k} '{self._entry_id(entry)}': {validation.errors.msg}")

        else:
            result = True

        if result and self.callback_validation is not None:
            try:
                result = self.callback_validation(entry)

            except ModuleSoftError as e:
                result = False
                error_func(e)

        return result

    def _build_entries(self) -> list:
        overrides = {
            'reload': False,
            'debug': self.p['debug'],
            **self.mc['override'],  # user-defined overrides
        }
        if 'match_fields' in self.p:
            overrides['match_fields'] = self.p['match_fields']

        if self.mc['state'] is not None:
            overrides['state'] = self.mc['state']

        if self.mc['enabled'] is not None:
            overrides['enabled'] = self.mc['enabled']

        # build list of valid entries or fail if invalid config is not permitted
        valid_entries = []
        for entry_cnf in self.p['multi']:
            # apply overrides
            entry = {
                **entry_cnf,
                **overrides,
            }

            if self.callback_build is not None:
                entry = self.callback_build(entry)

            if entry['debug']:
                self.m.warn(f"Validating {self.k}: '{entry}'")

            # (re-)validate the entry like ansible does on module-init
            if not self.validation or self._validate_entry(entry):
                valid_entries.append(entry)

        return valid_entries

    def _create_update(self):
        for entry_cnf in self._build_entries():
            # process single entry like in the single-module
            entry_result = dict(
                changed=False,
                diff={
                    'before': {},
                    'after': {},
                }
            )

            self.p['debug'] = entry_cnf['debug']  # per entry switch

            if self.p['debug'] or self.mc['output_info']:
                self.m.warn(f"Processing {self.k}: '{self._entry_id(entry_cnf)}'")

            try:
                entry = self._init_entry(entry_cnf, entry_result)
                if self.cache_existing:
                    self.callback_set_existing(entry, cache=self.cache)

                entry.check()
                entry.process()

                if self.cache_existing and self.callback_update_existing is not None:
                    self.cache = self.callback_update_existing(entry_cnf, cache=self.cache)

                self._add_entry_result(entry, entry_result)

            except ModuleSoftError:
                continue

    # PURGE METHODS
    def _entry_matches_purge_filter(self, entry_cnf: dict) -> bool:
        to_purge = True

        for filter_key, filter_value in self.mc['purge_filter'].items():
            if self.mc['purge_filter_invert']:
                # purge all except matches
                if self.mc['purge_filter_partial']:
                    if str(entry_cnf[filter_key]).find(filter_value) != -1:
                        to_purge = False
                        break

                else:
                    if entry_cnf[filter_key] == filter_value:
                        to_purge = False
                        break

            else:
                # purge only matches
                if self.mc['purge_filter_partial']:
                    if str(entry_cnf[filter_key]).find(filter_value) == -1:
                        to_purge = False
                        break

                else:
                    if entry_cnf[filter_key] != filter_value:
                        to_purge = False
                        break

        return to_purge

    def _entry_in_purge_list(self, entry_cnf: dict) -> bool:
        for purge_entry_cnf in self.p['multi_purge']:
            if self._entry_matches(entry_cnf, purge_entry_cnf):
                return True

        return False

    def _purge_entry(self, entry_cnf: dict) -> None:
        entry_name = self._entry_id(entry_cnf)

        try:
            entry_result = dict(
                changed=False,
                diff={
                    'before': {},
                    'after': {},
                }
            )
            entry = self._init_entry(entry_cnf, entry_result)
            if self.cache_existing:
                self.callback_set_existing(entry, cache=self.cache)

            entry.p['debug'] = self.p['debug']
            entry.p['state'] = 'absent' if self.mc['purge_action'] == 'delete' else 'present'

            entry.check()
            if not entry.exists:
                return

            if self.mc['purge_action'] == 'delete':
                if not self.m.check_mode:
                    entry.delete()

                else:
                    result['diff']['before'][entry_name] = entry_cnf
                    result['diff']['after'][entry_name] = None

            elif entry.b.is_enabled():
                if not self.m.check_mode:
                    entry.b.disable()

                else:
                    result['diff']['before'][entry_name] = {'enabled': True}
                    result['diff']['after'][entry_name] = {'enabled': False}

            self._add_entry_result(entry, entry_result)

        except ModuleSoftError:
            pass

    def _purge(self):
        if not self.mc['purge_all'] and is_unset(self.p['multi_purge']) and is_unset(self.mc['purge_filter']):
            m.fail_json("You need to either provide entries via 'multi_purge' or 'multi_control.purge_filter'!")

        # checking if all entries should be purged
        for entry_cnf in self.cache['main']:
            if self.callback_purge_exclude is not None:
                if self.callback_purge_exclude(entry_cnf):
                    continue

            if self.mc['purge_all'] or self._entry_in_purge_list(entry_cnf):
                if not self._entry_matches_purge_filter(entry_cnf):
                    continue

                if self.p['debug']:
                    self.m.warn(f"Existing {self.kind} '{self._entry_id(entry_cnf)}' will be {self.mc['purge_action']}d!")

                self._purge_entry(entry_cnf)

    # UTIL METHODS
    def _init_entry(self, entry_cnf: dict, entry_result: dict) -> BaseModule:
        return self.o(
            module=self.m,
            result=entry_result,
            cnf=entry_cnf,
            session=self.s,
            fail=dict(
                verify=self.mc['fail_verify'],
                process=self.mc['fail_process'],
            ),
        )

    def _add_entry_result(self, entry: BaseModule, entry_result: dict):
        if entry_result['changed']:
            self.r['changed'] = True
            entry_result['diff'] = diff_remove_empty(entry_result['diff'])
            entry_name = self._entry_id(entry)

            if 'before' in entry_result['diff']:
                self.r['diff']['before'][entry_name] = entry_result['diff']['before']

            if 'after' in entry_result['diff']:
                self.r['diff']['after'][entry_name] = entry_result['diff']['after']

    def _entry_matches(self, e1: dict, e2: dict) -> bool:
        matches = []
        for field in self.match_fields:
            matches.append(
                field in e1 and field in e2 and e1[field] == e2[field]
            )

        return all(matches)

    def _entry_id(self, entry: (dict, BaseModule)) -> str:
        entry_cnf = entry
        if isinstance(entry, BaseModule):
            entry_cnf = entry.p

        if self.field_id in entry_cnf:
            return entry_cnf[self.field_id]

        return 'NO-ID-FOUND'

    @staticmethod
    def _default_callback_get_existing(meta_entry: BaseModule) -> dict:
        return {'main': meta_entry.get_existing()}

    @staticmethod
    def _default_callback_set_existing(entry: BaseModule, cache: dict):
        entry.existing_entries = cache['main']
