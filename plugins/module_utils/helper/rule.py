from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import \
    get_matching
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.defaults.rule import \
     RULE_DEFAULTS


def validate_values(error_func, module: AnsibleModule, cnf: dict, kind: str = 'filter') -> None:
    # error = "Value '%s' is invalid for the field '%s'!"

    # can't validate as aliases are supported
    # for field in ['source_net', 'destination_net']:
    #     if cnf[field] not in [None, '', 'any']:
    #         try:
    #             ip_network(cnf[field])
    #
    #         except ValueError:
    #             try:
    #                 ip_address(cnf[field])
    #
    #             except ValueError:
    #                 error_func(error % (cnf[field], field))

    if kind == 'filter':
        required_together=[
            ('max_src_conn_rate', 'max_src_conn_rates', 'overload'),
            ('adaptive_start', 'adaptive_end'),
            ('tcp_flags', 'tcp_flags_clear'),
        ]
        for opts in required_together:
            if any((cnf[opts[0]] is None) != (cnf[o] is None) for o in opts[1:]):
                error_func(f"parameters are required together: {', '.join(opts)}")
            if any((cnf[opts[0]] == []) != (cnf[o] == []) for o in opts[1:]):
                error_func(f"parameters are required together: {', '.join(opts)}")

    # some recommendations - maybe the user overlooked something
    if 'action' in cnf and cnf['action'] == 'pass' and cnf['protocol'] in ['TCP', 'UDP', 'TCP/UDP']:
        if cnf['source_net'] == 'any' and cnf['destination_net'] == 'any':
            module.warn(
                "Configuring allow-rules with 'any' source and "
                "'any' destination is bad practice!"
            )

        elif cnf['destination_net'] == 'any' and cnf['destination_port'] == 'any':
            module.warn(
                "Configuring allow-rules to 'any' destination "
                "using 'all' ports is bad practice!"
            )
