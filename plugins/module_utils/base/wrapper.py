from typing import Callable
from inspect import stack as inspect_stack
from inspect import getfile as inspect_getfile

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.cls import BaseModule
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.multi import MultiModule
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.utils import profiler
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import diff_remove_empty


def _single_module_process(instance: BaseModule):
    instance.check()
    instance.process()
    if 'reload' in instance.m.params and instance.r['changed'] and instance.m.params['reload']:
        instance.reload()

    if hasattr(instance, 's'):
        instance.s.close()

    instance.r['diff'] = diff_remove_empty(instance.r['diff'])


def is_multi_module_call(m: AnsibleModule) -> bool:
    return len(m.params['multi']) > 0 or \
        len(m.params['multi_purge']) > 0 or \
        m.params['multi_control']['purge_all']


def module_multi_wrapper(
        module: AnsibleModule, result: dict, obj: BaseModule, kind: str, module_args: dict,
        callback_build: Callable = None, callback_get_existing: Callable = None, callback_set_existing: Callable = None,
        callback_update_existing: Callable = None, callback_purge_exclude: Callable = None,
):
    m = MultiModule(
        module=module,
        result=result,
        kind=kind,
        obj=obj,
        entry_args=module_args['multi']['options'],
        callback_build=callback_build,
        callback_get_existing=callback_get_existing,
        callback_set_existing=callback_set_existing,
        callback_update_existing=callback_update_existing,
        callback_purge_exclude=callback_purge_exclude,
    )
    if module.params['profiling'] or module.params['debug']:
        module_name = inspect_getfile(inspect_stack()[1][0]).rsplit('/', 1)[1].rsplit('.', 1)[0]
        return profiler(check=m.process, module_name=module_name, kwargs={})

    return m.process()


def module_wrapper(instance: BaseModule):
    if instance.m.params['profiling'] or instance.m.params['debug']:
        module_name = inspect_getfile(inspect_stack()[1][0]).rsplit('/', 1)[1].rsplit('.', 1)[0]
        return profiler(check=_single_module_process, module_name=module_name, kwargs={'instance': instance})

    return _single_module_process(instance)
