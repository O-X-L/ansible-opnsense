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
            callback_build: Callable[[dict], dict] = None,
            callback_validation: Callable[[dict], bool] = None,
            callback_get_existing: Callable[[BaseModule], dict] = None,
            callback_set_existing: Callable[[BaseModule, dict], None] = None,
            callback_update_existing: Callable[[dict, dict], dict] = None,
            callback_purge_exclude: Callable[[dict], bool] = None,
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
        if self.callback_build is None:
            self.callback_build = self._default_callback_build

        if self.callback_validation is None:
            self.callback_validation = self._default_callback_validation

        if self.cache_existing:
            if self.callback_get_existing is None:
                self.callback_get_existing = self._default_callback_get_existing

            if self.callback_set_existing is None:
                self.callback_set_existing = self._default_callback_set_existing

            if self.callback_update_existing is None:
                self.callback_update_existing = self._default_callback_update_existing

        if self.callback_purge_exclude is None:
            self.callback_purge_exclude = self._default_callback_purge_exclude

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

        validation = ModuleArgumentSpecValidator(self.mod_entry_args).validate(parameters=entry)

        try:
            validation_error = validation.errors[0]

        except IndexError:
            validation_error = None

        if validation_error:
            error_func(f"Got invalid config for {self.k} '{self._entry_id(entry)}': {validation.errors.msg}")

        else:
            result = True

        if result:
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

                if self.cache_existing:
                    self.cache = self.callback_update_existing(entry_cnf, cache=self.cache)

                self._add_entry_result(entry, entry_result)

            except ModuleSoftError:
                continue

    # PURGE METHODS
    def _entry_matches_purge_filter(self, entry_cnf: dict) -> bool:
        for filter_key, filter_value in self.mc['purge_filter'].items():
            if self.mc['purge_filter_invert']:
                # purge all except matches
                if self.mc['purge_filter_partial']:
                    if str(entry_cnf[filter_key]).find(filter_value) != -1:
                        return False

                else:
                    if entry_cnf[filter_key] == filter_value:
                        return False

            else:
                # purge only matches
                if self.mc['purge_filter_partial']:
                    if str(entry_cnf[filter_key]).find(filter_value) == -1:
                        return False

                else:
                    if entry_cnf[filter_key] != filter_value:
                        return False

        return True

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
                    self.r['diff']['before'][entry_name] = entry_cnf
                    self.r['diff']['after'][entry_name] = None

            elif entry.b.is_enabled():
                if not self.m.check_mode:
                    entry.b.disable()

                else:
                    self.r['diff']['before'][entry_name] = {'enabled': True}
                    self.r['diff']['after'][entry_name] = {'enabled': False}

            self._add_entry_result(entry, entry_result)

        except ModuleSoftError:
            pass

    def _purge(self):
        if not self.mc['purge_all'] and is_unset(self.p['multi_purge']) and is_unset(self.mc['purge_filter']):
            self.m.fail_json("You need to either provide entries via 'multi_purge' or 'multi_control.purge_filter'!")

        # checking if all entries should be purged
        for entry_cnf in self.cache['main']:
            if self.callback_purge_exclude(entry_cnf):
                continue

            if self.mc['purge_all'] or self._entry_in_purge_list(entry_cnf):
                if not self._entry_matches_purge_filter(entry_cnf):
                    continue

                if self.p['debug']:
                    self.m.warn(f"Existing {self.k} '{self._entry_id(entry_cnf)}' will be {self.mc['purge_action']}d!")

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
    def _default_callback_build(entry: dict) -> dict:
        """
        Callback to make modifications to a raw entry that was provided by the user, before it gets processed.
        This happens after the overrides were applied.

        :param entry: The entry that can be modified
        :return: The modified entry
        """
        return entry

    @staticmethod
    def _default_callback_validation(entry: dict) -> bool:
        """
        Callback to validate a raw entry that was provided by the use.
        This Validation extends the default Ansible-Module-Argument Validation.
        It is called after the 'build' callback.

        :param entry: The entry that should be validated
        :return: If the entry was valid
        """
        return True

    @staticmethod
    def _default_callback_get_existing(meta_entry: BaseModule) -> dict:
        """
        Callback to pull the 'existing_entries' that will be written to the cache.

        :param meta_entry: A dummy/meta-entry as BaseModule-instance that is used to pull all existing entries from the API
        :return: Result that will be used as cache
        """
        return {'main': meta_entry.get_existing()}

    @staticmethod
    def _default_callback_set_existing(entry: BaseModule, cache: dict):
        """
        Callback to set the 'existing_entries' of an entry-instance that is about to be processed

        :param entry: The entry BaseModule-instance that might need 'existing_entries' to be set
        :param cache: The full cache
        :return: None
        """
        entry.existing_entries = cache['main']

    @staticmethod
    def _default_callback_update_existing(entry: dict, cache: dict) -> dict:
        """
        Callback to update the cache after an entry was processed

        :param entry: The entry that was just processed
        :param cache: The full cache
        :return: The updated cache
        """
        return cache

    @staticmethod
    def _default_callback_purge_exclude(entry: dict) -> bool:
        """
        Callback to check if an entry should be excluded from purge/deletion.
        This should only be used if there are built-in entries that should be protected.

        :param entry: The entry that should get purged/deleted
        :return: If the entry should be excluded from being purged
        """
        return False
