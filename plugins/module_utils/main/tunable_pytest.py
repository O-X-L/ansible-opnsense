import pytest

from ansible_collections.oxlorg.opnsense.plugins.module_utils.main.tunable import Tunable


def _tunable(entry: dict) -> Tunable:
    t = Tunable.__new__(Tunable)
    t.entry = entry
    return t


def test_tunable_fields():
    assert Tunable.FIELD_ID == 'tunable'
    assert Tunable.FIELDS_TRANSLATE['description'] == 'descr'
    assert set(Tunable.FIELDS_CHANGE) == {'value', 'description'}


@pytest.mark.parametrize('key, configured', [
    ('a4c2ce3e-0c4f-4e2a-9a3b-2f6f1e8b7d10', True),
    ('9b1f3c1b6a1e4f5e8c9d0a1b2c3d4e5f', False),
    ('', False),
])
def test_tunable_is_configured(key: str, configured: bool):
    assert _tunable({'uuid': key})._is_configured() is configured
