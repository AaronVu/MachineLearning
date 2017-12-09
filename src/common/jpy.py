# -*- coding:utf-8 -*-
from jpype import *


class JVM:

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


class Encryptor:

    NAME_KEY = 'VMEININ_NAME'
    PWD_KEY = 'VMEININ_PWD'

    def __init__(self):
        pass

    @JVM()
    def aes_encode(self, text, key, has_next=False):
        encryptor = JClass("PasswdEncode")
        return encryptor.aesEncode(text, key)

    @JVM()
    def aes_decode(self, text, key, has_next=False):
        encryptor = JClass("PasswdEncode")
        return encryptor.aesDecode(text, key)


def main():
    cipher = Encryptor()
    en = cipher.aes_encode("SCOTT", Encryptor.NAME_KEY, has_next=True)
    print(en)
    de = cipher.aes_decode('0B92AA4029CADA31A7319EACE2D99F91', Encryptor.NAME_KEY)
    print(de)


if __name__ == "__main__":
    main()
