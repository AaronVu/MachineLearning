# -*- coding:utf-8 -*-
from jpype import *
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex
from Crypto.Random.Fortuna.FortunaGenerator import AESGenerator

instances = {}
pad_1_it = lambda k: k + (16 - len(k) % 16) * '\0'


def singleton(cls, *args, **kw):
    """
    单例装饰器
    """
    global instances

    def _singleton(*args, **kw):
        if cls.__name__ not in instances:
            instances[cls.__name__] = cls(*args, **kw)
        return instances[cls.__name__]
    return _singleton


def pad_it(text):
    length, count = 16, len(text)
    return pad_1_it(text) if count < length else text + ('\0' * (length - (count % length)))


class JVM:

    """
    控制JVM的生命周期
    """

    def __init__(self):
        pass

    def __call__(self, func):
        def call(*args, **margs):
            if not isJVMStarted():
                startJVM(getDefaultJVMPath(), "-Djava.class.path=../PasswdEncode.class:")
            if margs.has_key('has_next') and margs['has_next']:
                return func(*args, **margs)
            rs = func(*args, **margs)
            shutdownJVM()
            return rs
        return call


@singleton
class Encryptor:

    """
    java aes_*
    python *
    """

    NAME_KEY = 'VMEININ_NAME'
    PWD_KEY = 'VMEININ_PWD'
    BLOCK_SIZE = 16

    def __init__(self, mode = AES.MODE_ECB):
        self.next = False
        self.cipher = None
        self.mode = mode

    def __before(self, has_next):
        if not self.next:
            self.cipher = JClass("PasswdEncode")
        self.next = has_next

    @JVM()
    def aes_encode(self, text, key, has_next=False):
        self.__before(has_next)
        return self.cipher.aesEncode(text, key)

    @JVM()
    def aes_decode(self, text, key, has_next=False):
        self.__before(has_next)
        return self.cipher.aesDecode(text, key)

    def encode(self, text, key):
        gen = AESGenerator()
        gen.reseed(key)
        sec_key = gen.pseudo_random_data(Encryptor.BLOCK_SIZE)
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


def main():
    encryptor = Encryptor()
    en = encryptor.aes_encode("SCOTT", Encryptor.NAME_KEY, has_next=True)
    print(en)
    de = encryptor.aes_decode(en, Encryptor.NAME_KEY)
    print(de)


if __name__ == "__main__":
    main()
