# -*- coding:utf-8 -*-


instances = {}


def Singleton(cls, *args, **kw):
    """
    实现单例模式
    """
    global instances

    def _singleton(*args, **kw):
        if cls.__name__ not in instances:
            instances[cls.__name__] = cls(*args, **kw)
        return instances[cls.__name__]

    return _singleton
