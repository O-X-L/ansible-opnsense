# pylint: disable=C0415
import pytest


DUMMY_CATEGORIES = {"category": {"categories": {"category": {
    "c355696d-f464-43ff-950c-d55ed87559e6": {"name": "ANSIBLE_TEST_1_1"},
    "006849af-893d-4c62-9a0d-b1858071238f": {"name": "ANSIBLE_TEST_1_2"},
}}}}


class DummySession:
    @staticmethod
    def get(**_kw):
        return DUMMY_CATEGORIES


class DummyModule:
    def __init__(self, **params):
        self.p = params
        self.s = DummySession


@pytest.mark.parametrize('categories, result', [
    ('ANSIBLE_TEST_1_1', ['c355696d-f464-43ff-950c-d55ed87559e6']),
    (['ANSIBLE_TEST_1_1'], ['c355696d-f464-43ff-950c-d55ed87559e6']),
    (
        ['ANSIBLE_TEST_1_2', 'ANSIBLE_TEST_1_1'],
        ['006849af-893d-4c62-9a0d-b1858071238f', 'c355696d-f464-43ff-950c-d55ed87559e6']
    ),
    (['uuid-3', 'ANSIBLE_TEST_1_1'], ['uuid-3', 'c355696d-f464-43ff-950c-d55ed87559e6']),
], ids=str)
def test_resolve_categories(categories, result):
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.category import resolve_categories

    m = DummyModule(categories=categories)
    resolve_categories(m, m.p)

    assert m.p['categories'] == result
