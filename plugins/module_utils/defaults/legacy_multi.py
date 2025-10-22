PURGE_MOD_ARGS = dict(
    action=dict(
        type='str', required=False, default='delete', choices=['disable', 'delete'],
        description='What to do with the matched items'
    ),
    filters=dict(
        type='dict', required=False, default={},
        description='Field-value pairs to filter on - per example: {param1: test} '
                    "- to only purge items that have 'param1' set to 'test'"
    ),
    filter_invert=dict(
        type='bool', required=False, default=False,
        description='If true - it will purge all but the filtered ones'
    ),
    filter_partial=dict(
        type='bool', required=False, default=False,
        description="If true - the filter will also match if it is just a partial value-match"
    ),
    force_all=dict(
        type='bool', required=False, default=False,
        description='If set to true and neither items, nor filters are provided - all items will be purged'
    ),
)

STATE_MOD_ARG_MULTI = dict(
    state=dict(type='str', required=False, choices=['present', 'absent']),
    enabled=dict(type='bool', required=False, default=None),  # override only if set
)

FAIL_MOD_ARG_MULTI = dict(
    fail_verification=dict(
        type='bool', required=False, default=False, aliases=['fail_verify'],
        description='Fail module if a single entry fails the verification.'
    ),
    fail_processing=dict(
        type='bool', required=False, default=True, aliases=['fail_proc'],
        description='Fail module if a single entry fails to be processed.'
    ),
)

INFO_MOD_ARG = dict(
    output_info=dict(type='bool', required=False, default=False, aliases=['info']),
)

RULE_MOD_ARG_KEY_FIELD = dict(
    key_field=dict(
        type='str', required=True, choices=['sequence', 'description', 'uuid'], aliases=['key'],
        description='What field is used as key of the provided dictionary'
    )
)
