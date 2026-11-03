from ansible_collections.oxlorg.opnsense.plugins.module_utils.main.rule import Rule


def _rule(params: dict, base_request: dict) -> Rule:
    rule = Rule.__new__(Rule)
    rule.p = {'categories': [], **params}
    rule.r = {'diff': {'before': {}, 'after': {}}}
    rule.RESP_JOIN_CHAR = ','
    rule._base_build_request = lambda: base_request
    return rule


def test_rule_build_request_sends_icmpv6_type_numbers():
    rule = _rule(
        params={'icmpv6_type': ['echoreq', 'echorep']},
        base_request={'rule': {'icmp6type': 'echoreq,echorep'}},
    )

    assert rule.build_request() == {'rule': {'icmp6type': '128,129'}}


def test_rule_build_request_sends_empty_icmpv6_type():
    rule = _rule(
        params={'icmpv6_type': []},
        base_request={'rule': {'icmp6type': ''}},
    )

    assert rule.build_request() == {'rule': {'icmp6type': ''}}


def test_rule_build_request_without_icmpv6_type_field():
    rule = _rule(params={}, base_request={'rule': {}})

    assert rule.build_request() == {'rule': {}}


def test_rule_simplify_existing_returns_icmpv6_type_names():
    rule = Rule.__new__(Rule)
    rule._base_simplify_existing = lambda existing: {'icmpv6_type': ['128', '129']}

    assert rule.simplify_existing({})['icmpv6_type'] == ['echoreq', 'echorep']


def test_rule_simplify_existing_keeps_unknown_icmpv6_type():
    rule = Rule.__new__(Rule)
    rule._base_simplify_existing = lambda existing: {'icmpv6_type': ['999']}

    assert rule.simplify_existing({})['icmpv6_type'] == ['999']
