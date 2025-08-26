from typing import Callable

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.handler import \
    exit_bug, exit_cnf


def diff_remove_empty(diff: dict) -> dict:
    d = diff.copy()
    for k in diff:
        if len(diff[k]) == 0:
            d.pop(k)

    return d


def ensure_list(data: (int, str, list, None)) -> list:
    # if user supplied a string instead of a list => convert it to match our expectations
    if isinstance(data, list):
        return data

    if data is None:
        return []

    return [data]


def get_matching(
        module: AnsibleModule, existing_items: (dict, list), compare_item: dict,
        match_fields: list, simplify_func: Callable = None,
) -> (dict, None):
    matching = None

    if len(existing_items) > 0:
        if isinstance(existing_items, dict):
            _existing_items_list = []
            for uuid, existing in existing_items.items():
                existing['uuid'] = uuid
                _existing_items_list.append(existing)

            existing_items = _existing_items_list

        for existing in existing_items:
            _matching = []

            if simplify_func is not None:
                existing = simplify_func(existing)

            try:
                for field in match_fields:
                    _matching.append(str(existing[field]) == str(compare_item[field]))

                    if module.params['debug']:
                        if existing[field] != compare_item[field]:
                            module.warn(
                                f"NOT MATCHING: "
                                f"'{existing[field]}' != '{compare_item[field]}'"
                            )

            except KeyError as error:
                exit_bug(
                    "Failed to match existing entry with provided one: "
                    f"{existing} <=> {sanitize_module_args(compare_item)}; "
                    f"Error while comparing: {error}"
                )

            if all(_matching):
                matching = existing
                break

    return matching


def get_multiple_matching(
        module: AnsibleModule, existing_items: (dict, list), compare_item: dict,
        match_fields: list, simplify_func: Callable = None,
) -> list:
    matching = []

    if len(existing_items) > 0:
        if isinstance(existing_items, dict):
            _existing_items_list = []
            for uuid, existing in existing_items.items():
                existing['uuid'] = uuid
                _existing_items_list.append(existing)

            existing_items = _existing_items_list

        for existing in existing_items:
            _simple = get_matching(
                module=module,
                existing_items=[existing],
                compare_item=compare_item,
                match_fields=match_fields,
                simplify_func=simplify_func,
            )
            if _simple is not None:
                matching.append(_simple)

    return matching


def is_true(data: (str, int, bool)) -> bool:
    return data in [1, '1', True]


def get_selected(data: dict) -> (str, None):
    if isinstance(data, dict):
        for key, values in data.items():
            if is_true(values['selected']):
                return key

        return ''  # none selected

    # if function is re-applied
    return data


def get_selected_value(data: dict) -> (str, None):
    if isinstance(data, dict):
        for values in data.values():
            if is_true(values['selected']) and 'value' in values:
                return values['value']

        return ''  # none selected

    if isinstance(data, list):
        for values in data:
            if is_true(values['selected']) and 'value' in values:
                return values['value']

        return ''  # none selected

    # if function is re-applied
    return data


def get_selected_opt_list(data: (dict, list)) -> (str, None):
    if isinstance(data, dict):
        return get_selected(data)

    return get_selected_value(data)


def get_selected_opt_list_idx(data: list) -> int:
    idx = 0
    for values in data:
        if is_true(values['selected']):
            return idx

        idx += 1

    return 0

def get_selected_list(data: dict, remove_empty: bool = False) -> list:
    if isinstance(data, list):
        # if function is re-applied
        return data

    if isinstance(data, str):
        if data.strip() == '':
            return []

        return data.split(',')

    selected = []
    if len(data) > 0:
        try:
            for key, values in data.items():
                if remove_empty and key in [None, '', ' ']:
                    continue

                if is_true(values['selected']):
                    selected.append(key)

        except AttributeError:
            exit_bug(f"Got data entry that is not a dictionary => '{data}'")

    selected.sort()
    return selected


def get_key_by_value_from_selection(selection: dict, value: str) -> (str, None):
    if isinstance(selection, dict):
        for key, values in selection.items():
            if 'value' in values and values['value'] == value:
                return key

    return None


def get_key_by_value_end_from_selection(selection: dict, value: str) -> (str, None):
    if isinstance(selection, dict):
        for key, values in selection.items():
            if 'value' in values and values['value'].endswith(value):
                return key

    return None


def get_key_by_value_beg_from_selection(selection: dict, value: str) -> (str, None):
    if isinstance(selection, dict):
        for key, values in selection.items():
            if 'value' in values and values['value'].startswith(value):
                return key

    return None


def to_digit(data: bool) -> int:
    return 1 if data else 0


def get_simple_existing(
        entries: (dict, list), add_filter: Callable = None,
        simplify_func: Callable = None
) -> list:
    simple_entries = []

    if isinstance(entries, dict):
        _entries = []
        for uuid, entry in entries.items():
            if not isinstance(entry, dict):
                exit_bug(f"The provided entry is not a dictionary => '{entry}'")

            entry['uuid'] = uuid
            _entries.append(entry)

        entries = _entries

    for entry in entries:
        if simplify_func is not None and add_filter is not None:
            simple_entries.append(add_filter(simplify_func(entry)))

        elif simplify_func is not None:
            simple_entries.append(simplify_func(entry))

        else:
            simple_entries.append(entries)

    return simple_entries


def format_int(data: (int, str)) -> (int, str):
    if isinstance(data, int):
        return data

    if data.isnumeric():
        return int(data)

    return data


def sort_param_lists(params: dict) -> None:
    for k in params:
        if isinstance(params[k], list):
            try:
                params[k].sort()

            except TypeError:
                pass

# pylint: disable=R0914,R0915
def simplify_translate(
        existing: dict, translate: dict = None, typing: dict = None,
        bool_invert: list = None, ignore: list = None, value_map: dict = None,
) -> dict:
    # pylint: disable=R0912
    simple = {}
    if translate is None:
        translate = {}

    if typing is None:
        typing = {}

    if bool_invert is None:
        bool_invert = []

    if ignore is None:
        ignore = []

    if value_map is None:
        value_map = {}

    try:
        # translate api-fields to ansible-fields
        for k, v in translate.items():
            if '.' in v:
                # Support for nested paths (e.g., 'general.enabled')
                path_parts = v.split('.')
                value = existing
                for part in path_parts:
                    if isinstance(value, dict) and part in value:
                        value = value[part]
                    else:
                        value = None
                        break
                if value is not None:
                    simple[k] = value
            elif v in existing:
                simple[k] = existing[v]

        translate_fields = translate.values()
        for k in existing:
            if k not in translate_fields and k not in ignore:
                simple[k] = existing[k]

        # correct value types to match (for diff-checks)
        for t, fields in typing.items():
            for f in fields:
                if f in ignore:
                    continue

                if t == 'bool':
                    simple[f] = is_true(simple[f])

                elif t == 'int':
                    simple[f] = format_int(simple[f])

                elif t == 'list':
                    simple[f] = get_selected_list(data=simple[f], remove_empty=True)

                elif t == 'select':
                    simple[f] = get_selected(simple[f])

                elif t == 'select_opt_list':
                    simple[f] = get_selected_opt_list(simple[f])

                elif t == 'select_opt_list_idx':
                    simple[f] = get_selected_opt_list_idx(simple[f])

        for f, vmap in value_map.items():
            try:
                for pretty_value, opn_value in vmap.items():
                    if simple[f] == opn_value:
                        simple[f] = pretty_value
                        break

            except KeyError:
                pass

        for k, v in simple.items():
            if isinstance(v, str) and v.isnumeric():
                simple[k] = int(simple[k])

            elif isinstance(v, bool) and k in bool_invert:
                simple[k] = not simple[k]

    except KeyError as err:
        exit_bug(
            f"Failed to translate API entry to Ansible entry! Maybe the API changed lately? "
            f"Failed field: {err} | "
            f"API entry: '{existing}' '{simple}'"
        )

    return simple


def is_unset(value: (str, None, list, dict)) -> bool:
    if isinstance(value, (list, dict)):
        return len(value) == 0

    if isinstance(value, str):
        value = value.strip()

    return value in ['', None]


def unset_check_error(params: dict, field: str, fail: bool) -> bool:
    if is_unset(params[field]):
        if fail:
            exit_cnf(f"Field '{field}' must be set!")

        return False

    return True

def sanitize_module_args(args: dict) -> dict:
    args.pop('api_key', None)
    args.pop('api_secret', None)
    return args


def flatten_dict(nested: dict, parent_key: str = '', sep: str = '.') -> dict:
    """
    Flatten a nested dictionary structure into a flat dictionary with dot-notation keys.
    
    Args:
        nested: The nested dictionary to flatten
        parent_key: The parent key prefix (used for recursion)
        sep: The separator to use between keys (default: '.')
    
    Returns:
        A flat dictionary with dot-notation keys
    """
    items = []
    for k, v in nested.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict) and 'selected' not in v and not any(key in ['value'] for key in v.keys() if isinstance(v.get(key), str)):
            # Only recurse if it's a nested structure, not a selection dict
            items.extend(flatten_dict(v, new_key, sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


def unflatten_dict(flat_dict: dict, sep: str = '.') -> dict:
    """
    Reconstruct a nested dictionary structure from a flat dictionary with dot-notation keys.
    
    Args:
        flat_dict: The flat dictionary with dot-notation keys
        sep: The separator used in the keys (default: '.')
    
    Returns:
        A nested dictionary structure
    """
    nested = {}
    for key, value in flat_dict.items():
        parts = key.split(sep)
        current = nested
        for part in parts[:-1]:
            if part not in current:
                current[part] = {}
            current = current[part]
        current[parts[-1]] = value
    return nested
