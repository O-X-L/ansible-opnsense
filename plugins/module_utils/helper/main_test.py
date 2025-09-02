from unittest.mock import Mock
import pytest

@pytest.mark.parametrize('existing, translate, simple', [
    ({'api_name': 'value'}, {'ansible_name': 'api_name'}, {'ansible_name': 'value'}),
    ({'api': {'name': 'value'}}, {'ansible_name': ('api', 'name')}, {'ansible_name': 'value'}),
])
def test_simplify_translate_translate(existing, translate, simple):
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import simplify_translate

    assert simple == simplify_translate(existing=existing, translate=translate, ignore=['api'])
