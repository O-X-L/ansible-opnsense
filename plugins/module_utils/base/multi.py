from abc import ABC

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.common.arg_spec import ModuleArgumentSpecValidator

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.handler import ModuleSoftError
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import diff_remove_empty
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.cls import BaseModule
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.defaults.main import \
    OPN_MOD_ARGS, RELOAD_MOD_ARG_DEF_FALSE


def build_multi_mod_args(
        mod_args: dict,
        aliases: list = None,
        description: str = None,
        not_required: list[str] = None,
) -> dict:
    """
    Function to dynamically build the module-arguments required for mass-management.

    :param mod_args: The module-specific arguments
    :param aliases: List of module-specific aliases for the 'multi' argument
    :param description: An optional description for the 'multi' argument
    :param not_required: List of module-specific arguments (only keys) that should be set to be NOT required
    :return: Module arguments required for mass-management
    """
    args_base = mod_args.copy()

    aliases_purge = ['multi_delete', 'purge', 'many_purge']
    if aliases is None:
        aliases = []

    else:
        for a in aliases:
            aliases_purge.append(f'{a}_purge')

    aliases.append('many')

    if description is None:
        description = 'Provide multiple entries to manage'

    for opn_arg in OPN_MOD_ARGS:
        if opn_arg in args_base:
            args_base.pop(opn_arg)

    if 'reload' in args_base:
        args_base.pop('reload')

    opn_args_multi = OPN_MOD_ARGS.copy()
    opn_args_multi['firewall']['required'] = False

    if not_required is None:
        not_required = []

    not_required.append('match_fields')
    for field in not_required:
        if field in args_base:
            args_base[field]['required'] = False

    entry_args_full = {**args_base, **RELOAD_MOD_ARG_DEF_FALSE, **opn_args_multi}

    return dict(
        multi=dict(
            type='list', required=False, default=[], aliases=aliases,
            description=description,
            elements='dict', options=entry_args_full,
        ),
        multi_purge=dict(
            type='list', required=False, default=[], aliases=aliases_purge,
            description='Provide multiple entries to purge (delete or disable)',
            elements='dict', options=entry_args_full,
        ),
        multi_control=dict(
            type='dict', required=False, default={}, aliases=['multi_ctrl', 'mc'],
            description=description,
            options=dict(
                # NOTE: we keep state and enabled outside overrides for convenience
                state=dict(type='str', required=False, choices=['present', 'absent'], default=None),
                enabled=dict(type='bool', required=False, default=None),
                # overrides for other parameters
                override=dict(
                    type='dict', required=False, default={}, description='Parameters to override for all entries',
                    aliases=['all', 'overrides'],
                ),
                fail_verify=dict(
                    type='bool', required=False, default=False, aliases=['fail_verification'],
                    description='Fail module if a single entry fails the verification.'
                ),
                fail_process=dict(
                    type='bool', required=False, default=True, aliases=['fail_proc', 'fail_processing'],
                    description='Fail module if a single entry fails to be processed.'
                ),
                output_info=dict(type='bool', required=False, default=False, aliases=['info']),
                purge_action=dict(
                    type='str', required=False, default='delete', choices=['disable', 'delete'],
                    description='What to do with the matched items'
                ),
                purge_filter=dict(
                    type='dict', required=False, default={}, aliases=['purge_filters'],
                    description='Field-value pairs to filter on - per example: {param1: test} '
                                "- to only purge items that have 'param1' set to 'test'"
                ),
                purge_filter_invert=dict(
                    type='bool', required=False, default=False,
                    description='If true - it will purge all but the filtered ones'
                ),
                purge_filter_partial=dict(
                    type='bool', required=False, default=False,
                    description="If true - the filter will also match if it is just a partial value-match"
                ),
                purge_all=dict(
                    type='bool', required=False, default=False,
                    description='If set to true and neither items, nor filters are provided - all items will be purged'
                ),
            ),
        ),
    )


class MultiModuleCallbacks(ABC):
    # pylint: disable=W0613
    @staticmethod
    def build(entry: dict) -> dict:
        """
        Callback to make modifications to a raw entry that was provided by the user, before it gets processed.
        This happens after the overrides were applied.

        :param entry: The entry that can be modified
        :return: The modified entry
        """
        return entry

    @staticmethod
    def validation(entry: dict) -> bool:
        """
        Callback to validate a raw entry that was provided by the use.
        This Validation extends the default Ansible-Module-Argument Validation.
        It is called after the 'build' callback.

        :param entry: The entry that should be validated
        :return: If the entry was valid
        """
        return True

    @staticmethod
    def get_existing(meta_entry: BaseModule) -> dict:
        """
        Callback to pull the 'existing_entries' that will be written to the cache.

        :param meta_entry: A dummy/meta-entry as BaseModule-instance that
                           is used to pull all existing entries from the API
        :return: Result that will be used as cache
        """
        return {'main': meta_entry.get_existing()}

    @staticmethod
    def set_existing(entry: BaseModule, cache: dict):
        """
        Callback to set the 'existing_entries' of an entry-instance that is about to be processed

        :param entry: The entry BaseModule-instance that might need 'existing_entries' to be set
        :param cache: The full cache
        :return: None
        """
        entry.existing_entries = cache['main']

    @staticmethod
    def update_existing(entry: BaseModule, cache: dict) -> dict:
        """
        Callback to update the cache after an entry was processed

        :param entry: The entry that was just processed
        :param cache: The full cache
        :return: The updated cache
        """

        # adding the config of the new entry to the cache (WITHOUT UUID!)
        if not entry.exists and entry.p.get('state', 'present') == 'present':  # was just created
            entry_cnf = entry.p.copy()
            for opn_arg in OPN_MOD_ARGS:
                entry_cnf.pop(opn_arg)

            cache['main'].append(entry_cnf)

        return cache

    @staticmethod
    def purge_exclude(entry: dict) -> bool:
        """
        Callback to check if an entry should be excluded from purge/deletion.
        This should only be used if there are built-in entries that should be protected.

        :param entry: The entry that should get purged/deleted
        :return: If the entry should be excluded from being purged
        """
        return False


# pylint: disable=R0913,R0915,R0917
class MultiModule:
    def __init__(
            self, module: AnsibleModule, result: dict, entry_args: dict, kind: str, obj: BaseModule,
            validation: bool = True, cache_existing: bool = True,
            callbacks: MultiModuleCallbacks = None,
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
        self.callbacks: MultiModuleCallbacks = callbacks
        if self.callbacks is None:
            self.callbacks = MultiModuleCallbacks()

        self.field_id = None
        if hasattr(self.o, 'FIELD_ID'):
            self.field_id = getattr(self.o, 'FIELD_ID')
            self.match_fields = [self.field_id]

        elif hasattr(self.o, 'FIELDS_MATCH'):
            self.match_fields = getattr(self.o, 'FIELDS_MATCH')

        else:
            self.match_fields = self.p['match_fields']

        if self.field_id is None:
            self.field_id = getattr(self.o, 'MULTI_DIFF_KEY', self.p['match_fields'][0])

        self._has_multi_entries = len(self.p['multi']) > 0
        self._has_multi_purge_entries = len(self.p['multi_purge']) > 0
        self._has_multi_purge_filters = len(self.mc['purge_filter']) > 0

    def _is_multi_purge(self) -> bool:
        return self._has_multi_purge_entries or self.mc['purge_all'] or self._has_multi_purge_filters

    def _is_multi_crud(self) -> bool:
        if self._is_multi_purge():
            return False

        return self._has_multi_entries

    def process(self) -> None:
        if self.cache_existing:
            self.cache = self.callbacks.get_existing(self.meta_entry)

        if self._is_multi_purge():
            self._purge()

        elif self._is_multi_crud():
            self._create_update()

        else:
            self.m.fail_json('Got invalid Mass-Management arguments!')

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
                result = self.callbacks.validation(entry)

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

            entry = self.callbacks.build(entry)

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
                try:
                    entry.check()

                except KeyError as e:
                    if str(e) == "KeyError: 'uuid'":
                        raise ModuleSoftError("Cannot modify entry that was just created!")

                entry.process()

                if self.cache_existing:
                    self.cache = self.callbacks.update_existing(entry, cache=self.cache)

                self._add_entry_result(entry, entry_result)

            except ModuleSoftError:
                continue

    # PURGE METHODS
    def _entry_matches_purge_filter(self, entry_cnf: dict) -> bool:
        # include in purge if matching & 'not inverted' - else exclude
        result = self.mc['purge_filter_invert'] is False

        for filter_key, filter_value in self.mc['purge_filter'].items():
            if self.mc['purge_filter_partial']:
                if str(entry_cnf[filter_key]).find(filter_value) != -1:
                    return result

            else:
                if entry_cnf[filter_key] == filter_value:
                    return result

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

            entry.p['debug'] = self.p['debug']
            entry.p['state'] = 'absent' if self.mc['purge_action'] == 'delete' else 'present'
            entry_cnf['match_fields'] = self.match_fields

            entry.check()
            if not entry.exists:
                return

            if self.mc['purge_action'] == 'delete':
                entry_result['changed'] = True
                if not self.m.check_mode:
                    entry.delete()

                else:
                    self.r['diff']['before'][entry_name] = entry_cnf
                    self.r['diff']['after'][entry_name] = None

            elif entry.b.is_enabled():
                entry_result['changed'] = True
                if not self.m.check_mode:
                    entry.b.disable()

                else:
                    self.r['diff']['before'][entry_name] = {'enabled': True}
                    self.r['diff']['after'][entry_name] = {'enabled': False}

            self._add_entry_result(entry, entry_result)

        except ModuleSoftError:
            pass

    def _purge(self):
        if not self.mc['purge_all'] and not self._has_multi_purge_entries and not self._has_multi_purge_filters:
            self.m.fail_json("You need to either provide entries via 'multi_purge' or 'multi_control.purge_filter'!")

        if self.mc['purge_action'] != 'delete':
            raise ValueError(self.mc['purge_filter'])

        if self._has_multi_purge_filters:
            self.m.fail_json("A purge_filter requires 'multi_control.purge_all' or items via 'multi_purge'!")

        # checking if all entries should be purged
        for entry_cnf in self.cache['main']:
            if self.callbacks.purge_exclude(entry_cnf):
                continue

            if self.mc['purge_all'] or self._entry_in_purge_list(entry_cnf):
                if not self._entry_matches_purge_filter(entry_cnf):
                    continue

                if self.p['debug']:
                    self.m.warn(f"Existing {self.k} '{self._entry_id(entry_cnf)}' will be {self.mc['purge_action']}d!")

                self._purge_entry(entry_cnf)

    # UTIL METHODS
    def _init_entry(self, entry_cnf: dict, entry_result: dict) -> BaseModule:
        entry_cnf['match_fields'] = self.match_fields
        o = self.o(
            module=self.m,
            result=entry_result,
            cnf=entry_cnf,
            session=self.s,
            fail=dict(
                verify=self.mc['fail_verify'],
                process=self.mc['fail_process'],
            ),
        )
        if self.cache_existing:
            self.callbacks.set_existing(o, cache=self.cache)

        return o

    def _add_entry_result(self, entry: BaseModule, entry_result: dict):
        if entry_result['changed']:
            self.r['changed'] = True

            entry_result['diff'] = diff_remove_empty(entry_result['diff'], to_none=True)
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
