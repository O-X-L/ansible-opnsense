from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.base import Base
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.validate import \
    validate_int_fields, validate_str_fields
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import \
    flatten_dict, unflatten_dict, is_true, get_selected, get_selected_list, \
    get_selected_opt_list, get_selected_opt_list_idx


class BaseShared:
    def __init__(self, m: AnsibleModule, r: dict, s: Session):
        if hasattr(self, 'TIMEOUT'):
            self.s = Session(
                module=m,
                timeout=self.TIMEOUT,
            ) if s is None else s

        else:
            self.s = Session(module=m) if s is None else s

        self.m = m
        self.p = m.params
        self.r = r
        self.b = Base(instance=self)
        self.exists = False
        self.existing_entries = None
        self.call_cnf = {
            'module': self.b.i.API_MOD,
            'controller': self.b.i.API_CONT,
        }

    def _check_validators(self):
        if 'state' in self.p and self.p['state'] != 'present':
            return

        if hasattr(self.b.i, 'STR_VALIDATIONS'):
            if hasattr(self.b.i, 'STR_LEN_VALIDATIONS'):
                validate_str_fields(
                    module=self.m,
                    data=self.p,
                    field_regex=self.b.i.STR_VALIDATIONS,
                    field_minmax_length=self.b.i.STR_LEN_VALIDATIONS
                )

            else:
                validate_str_fields(module=self.m, data=self.p, field_regex=self.b.i.STR_VALIDATIONS)

        elif hasattr(self.b.i, 'STR_LEN_VALIDATIONS'):
            validate_str_fields(module=self.m, data=self.p, field_minmax_length=self.b.i.STR_LEN_VALIDATIONS)

        if hasattr(self.b.i, 'INT_VALIDATIONS'):
            validate_int_fields(module=self.m, data=self.p, field_minmax=self.b.i.INT_VALIDATIONS)


class BaseModule(BaseShared):
    def __init__(self, m: AnsibleModule, r: dict, s: Session = None):
        super().__init__(m, r, s)

    def _base_check(self, match_fields: list = None):
        self._check_validators()

        if match_fields is None:
            if 'match_fields' in self.p:
                match_fields = self.p['match_fields']

            elif hasattr(self, 'FIELD_ID'):
                match_fields = [self.FIELD_ID]

        if match_fields is not None:
            self.b.find(match_fields=match_fields)
            if self.exists:
                self.call_cnf['params'] = [getattr(self, self.EXIST_ATTR)[self.b.field_pk]]

        if 'state' not in self.p or self.p['state'] == 'present':
            self.r['diff']['after'] = self.b.build_diff(data=self.p)

    def check(self) -> None:
        self._base_check()

    def get_existing(self) -> list:
        return self.b.get_existing()

    def process(self) -> None:
        self.b.process()

    def create(self) -> None:
        self.b.create()

    def update(self) -> None:
        self.b.update()

    def delete(self) -> None:
        self.b.delete()

    def reload(self) -> None:
        self.b.reload()


class GeneralModule(BaseShared):
    # has only a single entry; cannot be deleted or created
    EXIST_ATTR = 'settings'

    def __init__(self, m: AnsibleModule, r: dict, s: Session = None):
        super().__init__(m, r, s)
        self.settings = {}

    def _base_check(self):
        self._check_validators()
        self.settings = self._search_call()
        self._build_diff()

    def check(self) -> None:
        self._base_check()

    def _search_call(self) -> dict:
        return self.b.simplify_existing(self.b.search())

    def get_existing(self) -> dict:
        return self._search_call()

    def process(self) -> None:
        self.update()

    def update(self) -> None:
        self.b.update(enable_switch=False)

    def reload(self) -> None:
        self.b.reload()

    def _build_diff(self) -> None:
        self.r['diff']['before'] = self.b.build_diff(self.settings)
        self.r['diff']['after'] = self.b.build_diff({
            k: v for k, v in self.p.items() if k in self.settings
        })


class NestedModule(GeneralModule):
    """
    Module class for APIs with nested structure (e.g., agent.general.enabled).
    Extends GeneralModule to handle complex nested API responses and requests.
    """
    EXIST_ATTR = 'settings'

    def _search_call(self) -> dict:
        """Override to flatten nested API responses for processing"""
        nested_data = self.b.search()
        flattened = flatten_dict(nested_data)
        
        # Use custom simplify for nested structures
        translate_rcv = getattr(self, 'FIELDS_TRANSLATE_RCV', {})
        if translate_rcv:
            # Custom translation using reverse mapping
            simple = {}
            for api_key, value in flattened.items():
                if api_key in translate_rcv:
                    ansible_key = translate_rcv[api_key]
                    simple[ansible_key] = value
                else:
                    simple[api_key] = value
            
            # Apply typing and other standard processing
            simple = self._apply_typing(simple)
        else:
            simple = self.b.simplify_existing(flattened)
        
        # Ensure all FIELDS_CHANGE exist with default values
        if hasattr(self, 'FIELDS_CHANGE'):
            for field in self.FIELDS_CHANGE:
                if field not in simple:
                    simple[field] = None
        
        return simple
    
    def _apply_typing(self, simple: dict) -> dict:
        """Apply FIELDS_TYPING processing to the simple dict"""
        
        if hasattr(self, 'FIELDS_TYPING'):
            typing = self.FIELDS_TYPING
            for t, fields in typing.items():
                for f in fields:
                    if f not in simple:
                        continue
                        
                    if t == 'bool':
                        simple[f] = is_true(simple[f])
                    elif t == 'int':
                        try:
                            simple[f] = int(simple[f]) if simple[f] != '' else 0
                        except (ValueError, TypeError):
                            pass
                    elif t == 'list':
                        simple[f] = get_selected_list(data=simple[f], remove_empty=True)
                    elif t == 'select':
                        simple[f] = get_selected(simple[f])
                    elif t == 'select_opt_list':
                        simple[f] = get_selected_opt_list(simple[f])
                    elif t == 'select_opt_list_idx':
                        simple[f] = get_selected_opt_list_idx(simple[f])
        
        return simple

    def _build_request(self) -> dict:
        """Override to unflatten request data for nested API structure"""
        flat_request = self.b.build_request()
        
        # Unflatten all dict values
        for key, value in flat_request.items():
            if isinstance(value, dict):
                flat_request[key] = unflatten_dict(value)
        
        return flat_request
