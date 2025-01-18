# pylint: disable=C0415
import pytest

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.purge import \
    check_purge_filter


class DummyModule:
    def __init__(self, filters, invert, partial):
        self.params = dict(
            filters=filters,
            filter_invert=invert,
            filter_partial=partial,
        )


DUMMY_ITEM = dict(
    string_a='ansibleguy',
    int_a=12345,
    list_a=['ansibleguy', 'ansible'],
)

DUMMY_FILTERS = [
    # Strings
    (dict(string_a='ansible'), False, False),
    (dict(string_a='ansibleguy'), False, True),

    # Strings Partial
    (dict(string_a='chef'), True, False),
    (dict(string_a='ansible'), True, True),
    (dict(string_a='ansibleguy'), True, True),

    # Integer
    (dict(int_a=234), False, False),
    (dict(int_a=12345), False, True),
    (dict(int_a='234'), False, False),
    (dict(int_a='12345'), False, False),

    # Integer Partial
    (dict(int_a='234'), True, True),
    (dict(int_a='12345'), True, True),

    # List
    (dict(list_a='ansible'), False, False),
    (dict(list_a='ansibleguy'), False, False),
    (dict(list_a=['chef']), False, False),
    (dict(list_a=['ansible']), False, False),
    #(dict(list_a=['ansible', 'ansibleguy']), False, True),
    (dict(list_a=['ansibleguy', 'ansible']), False, True),
    (dict(string_a=['chef']), False, False),
    (dict(string_a=['ansible']), False, False),
    (dict(string_a=['ansibleguy']), False, False),

    # List Partial
    (dict(list_a='ansible'), True, True),
    (dict(list_a='ansibleguy'), True, True),
    #(dict(list_a=['chef']), True, False),
    #(dict(list_a=['chef']), True, False),
    #(dict(list_a=['ansibleguy']), True, True),
    #(dict(list_a=['ansibleguy', 'chef']), True, False),
    #(dict(list_a=['chef']), True, False),
    #(dict(list_a=['ansible']), True, True),
    #(dict(list_a=['ansibleguy']), True, True),
    #(dict(list_a=['chef', 'ansibleguy']), True, False),
    #(dict(list_a=['ansible', 'ansibleguy']), True, True),

    # Combined
    (dict(string_a='chef', int_a=789), False, False),
    (dict(string_a='ansible', int_a=234), False, False),
    (dict(string_a='ansibleguy', int_a=12345), False, True),

    # Combined Partial
    (dict(string_a='chef', int_a='789'), True, False),
    (dict(string_a='ansible', int_a='234'), True, True),
    (dict(string_a='ansibleguy', int_a='12345'), True, True),
]


@pytest.mark.parametrize('filters, partial, result', DUMMY_FILTERS, ids=str)
def test_check_purge_filter(filters, partial, result):

    module = DummyModule(filters, False, partial)
    assert check_purge_filter(module, DUMMY_ITEM) == result


@pytest.mark.parametrize('filters, partial, result', DUMMY_FILTERS, ids=str)
def test_check_purge_filter_inverse(filters, partial, result):

    module = DummyModule(filters, True, partial)
    assert check_purge_filter(module, DUMMY_ITEM) != result
