from ansible_collections.oxlorg.opnsense.plugins.module_utils.defaults.main import \
    STATE_MOD_ARG


BIND_REC_MATCH_FIELDS = dict(
    match_fields=dict(
        type='list', elements='str',
        description='Fields that are used to match configured records with the running config - '
                    "if any of those fields are changed, the module will think it's a new entry",
        choices=['name', 'domain', 'type', 'value'],
        default=['name', 'domain', 'type'],  # required=False
    )
)
BIND_REC_MOD_ARGS = dict(
    domain=dict(type='str', required=True, aliases=['domain_name']),
    name=dict(type='str', required=True, aliases=['record']),
    type=dict(
        type='str', required=False, default='A',
        choices=[
            'A', 'AAAA', 'CAA', 'CNAME', 'DNSKEY', 'DS', 'MX', 'NS', 'PTR',
            'RRSIG', 'SRV', 'TLSA', 'TXT',
        ]
    ),
    value=dict(type='str', required=False),
    round_robin=dict(
        type='bool', required=False, default=False,
        description='If multiple records with the same domain/name/type combination exist - '
                    "the module will only execute 'state=absent' if set to 'false'. "
                    "To create multiple ones set this to 'true'. "
                    "Records will only be created, NOT UPDATED! (no matching is done)"
    ),
    **BIND_REC_MATCH_FIELDS,
    **STATE_MOD_ARG,
)
