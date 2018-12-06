# -*- coding:utf-8 -*-
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex
from Crypto.Random.Fortuna.FortunaGenerator import AESGenerator
import os
import time
import urllib.request as urllib2
from enum import Enum

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


def list_files(path):
    fs = os.walk(path)
    files = []
    dirs = []
    for x in fs:
        dirs.append(x[0])
        if x[2]:
            files += [os.path.join(x[0], _) for _ in x[2]]
    return dirs, files


def exec_cmd(cmd):
    msg = os.popen(cmd, 'r')
    for line in msg:
        print(line.rstrip())
    msg.close()


pad_1_it = lambda k: k + (16 - len(k) % 16) * '\0'


def pad_it(text):
    length, count = 16, len(text)
    return pad_1_it(text) if count < length else text + ('\0' * (length - (count % length)))


class Aspect:

    """
    AOP
    """

    def __init__(self):
        pass

    def __call__(self, func):
        def call(*args, **margs):
            """Do Something Before"""
            self.before()
            rs = func(*args, **margs)
            """Do Something After"""
            self.after()
            if rs:
                return rs
        return call

    def before(self):
        pass

    def after(self):
        pass


@Singleton
class Cipher:

    """
    python *
    """

    KEY = b'Stock-Share'
    BLOCK_SIZE = 16

    def __init__(self, mode = AES.MODE_ECB):
        self.mode = mode

    def encode(self, text, key):
        gen = AESGenerator()
        gen.reseed(key)
        sec_key = gen.pseudo_random_data(self.BLOCK_SIZE)
        if self.mode == AES.MODE_CBC:
            cipher = AES.new(pad_1_it(key), self.mode, sec_key)
        else:
            cipher = AES.new(sec_key, AES.MODE_ECB)
        rs = cipher.encrypt(pad_it(text))
        # 转化为16进制字符串
        return b2a_hex(rs)

    def decode(self, text, key):
        gen = AESGenerator()
        gen.reseed(key)
        sec_key = gen.pseudo_random_data(16)
        if self.mode == AES.MODE_CBC:
            cipher = AES.new(pad_1_it(key), self.mode, sec_key)
        else:
            cipher = AES.new(sec_key, AES.MODE_ECB)
        plain_text = cipher.decrypt(a2b_hex(text))
        return plain_text.rstrip(b'\x00')


class RequestMethod(Enum):
    PUT = "PUT"
    GET = "GET"
    DELETE = "DELETE"
    POST = "POST"


def format_time(fmt):
    return time.strftime(fmt, time.localtime(time.time()))


def do_http(url, parmas=None, method=RequestMethod.GET):
    request = urllib2.Request(url, parmas)
    request.add_header('Content-Type', 'application/json')
    request.get_method = lambda: method.value
    response = urllib2.urlopen(request)
    return response.read()




