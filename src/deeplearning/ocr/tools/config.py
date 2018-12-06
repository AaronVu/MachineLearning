# -*- coding:utf-8 -*-
from configparser import RawConfigParser


class ConfigLoader(RawConfigParser):

    def __init__(self, path):
        super(ConfigLoader, self).__init__()
        self.path = path
        self.read(self.path)
        self._section = 'configure'
        cfgs = self.items(self._section)
        self._conf = {cfg[0]: cfg[1] for cfg in cfgs}

    def __call__(self, key):
        return self._conf.get(key)

    def __getitem__(self, item):
        return self._conf.get(item)

    def __setitem__(self, key, value):
        self.set_value(key, value)

    def __delitem__(self, key):
        self.del_conf(key)

    def __len__(self):
        return len(self._conf)

    def __iter__(self):
        return zip(self._conf.keys(), self._conf.values())

    def _save(self):
        fd = open(self.path, 'w')
        super(ConfigLoader, self).write(fd)
        fd.close()

    def get_value(self, key):
        return self._conf.get(key)

    def set_value(self, key, val):
        super(ConfigLoader, self).set(self._section, key, val)
        self._save()
        self._conf[key] = val

    def del_conf(self, key):
        super(ConfigLoader, self).remove_option(self._section, key)
        self._save()
        del self._conf[key]
