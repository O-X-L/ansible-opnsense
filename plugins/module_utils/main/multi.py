from typing import Callable

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.common.arg_spec import ModuleArgumentSpecValidator

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.handler import ModuleSoftError, exit_bug
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import diff_remove_empty
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.cls import BaseModule


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
    ):
        self.m = module
        self.p = module.params
        self.mc = self.p['multi_control']
        self.r = result
        self.o = obj
        self.k = kind
        self.mod_entry_args = entry_args
        self.validation = validation
        self.cache_existing = cache_existing
        self.callback_build = callback_build
        self.callback_validation = callback_validation
        self.callback_get_existing = callback_get_existing
        self.callback_set_existing = callback_set_existing
        self.callback_update_existing = callback_update_existing
        if self.cache_existing and (self.callback_get_existing is None or self.callback_set_existing is None):
            exit_bug('Need to supply callback-functions to get/set existing-cache!')

        if hasattr(self.o, 'FIELD_ID'):
            self.field_key = getattr(self.o, 'FIELD_ID')

        else:
            self.field_key = self.p['match_fields'][0]

        if hasattr(self.o, 'TIMEOUT'):
            self.s = Session(
                module=self.m,
                timeout=getattr(self.o, 'TIMEOUT'),
            )

        else:
            self.s = Session(module=self.m)

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
            error_func(f"Got invalid config for {self.k} '{entry[self.field_key]}': {validation.errors.msg}")

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

    # pylint: disable=R0915
    def process(self) -> None:
        _meta_entry = self.o(module=self.m, session=self.s, result={})
        existing_cache = {}
        if self.cache_existing:
            existing_cache = self.callback_get_existing(_meta_entry)

        for entry_cnf in self._build_entries():
            # process single alias like in the 'alias' module
            entry_result = dict(
                changed=False,
                diff={
                    'before': {},
                    'after': {},
                }
            )

            self.p['debug'] = entry_cnf['debug']  # per entry switch

            if self.p['debug'] or self.mc['output_info']:
                self.m.warn(f"Processing {self.k}: '{entry_cnf[self.field_key]}'")

            try:
                entry = self.o(
                    module=self.m,
                    result=entry_result,
                    cnf=entry_cnf,
                    session=self.s,
                    fail=dict(
                        verify=self.mc['fail_verify'],
                        process=self.mc['fail_process'],
                    ),
                )
                # save on requests
                if self.cache_existing:
                    self.callback_set_existing(entry, cache=existing_cache)

                entry.check()
                entry.process()

                if self.cache_existing and self.callback_update_existing is not None:
                    existing_cache = self.callback_update_existing(entry_cnf, cache=existing_cache)

                if entry_result['changed']:
                    self.r['changed'] = True
                    entry_result['diff'] = diff_remove_empty(entry_result['diff'])

                    if 'before' in entry_result['diff']:
                        self.r['diff']['before'].update(entry_result['diff']['before'])

                    if 'after' in entry_result['diff']:
                        self.r['diff']['after'].update(entry_result['diff']['after'])

            except ModuleSoftError:
                continue

        if self.r['changed'] and self.p['reload']:
            _meta_entry.reload()

        self.s.close()
