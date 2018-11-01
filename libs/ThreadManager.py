# -*- encoding:UTF-8 -*-
import threading
import types
from random import choice

__thread_pool = dict()


def append_work(target, allow_dupl=False, **kwargs):
    if not isinstance(target, types.FunctionType) and not isinstance(target, types.MethodType):
        return False
    if allow_dupl:
        return __append_thread_duplicate(target=target, **kwargs)
    else:
        return __append_thread(target=target, **kwargs)


def is_alive(name):
    _thread = __thread_pool.get(name)
    if _thread and _thread.isAlive():
        return True
    return False


def __append_thread_duplicate(target, **kwargs):
    def add_suffix(name):
        name += ':'
        for x in range(20):
            name += choice('0123456789ABCDEF')
        return name

    name = kwargs.get('thread_name', target.__name__)
    name = add_suffix(name)
    kwargs['thread_name'] = name
    return __start_thread(target=target, **kwargs)


def __append_thread(target, **kwargs):
    thread_name = kwargs.get('thread_name', target.__name__)
    kwargs['thread_name'] = thread_name
    _thread = __thread_pool.get(thread_name)
    if _thread and _thread.isAlive():
        return False
    return __start_thread(target=target, **kwargs)


def __start_thread(target, thread_name, **kwargs):
    t = threading.Thread(target=target, kwargs=kwargs)
    t.setDaemon(True)
    __thread_pool[thread_name] = t
    t.start()
    return True


if __name__ == '__main__':
    pass
