# -*- coding:utf-8 -*-
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex
from Crypto.Random.Fortuna.FortunaGenerator import AESGenerator

KEY = b'0123456789ABCDEF'
NAME_KEY = 'VMEININ_NAME'
PWD_KEY = 'VMEININ_PWD'
MODE = AES.MODE_CBC
name = "SCOTT"
pwd = "vme1023"
sec_name = "0B92AA4029CADA31A7319EACE2D99F91"
sec_pwd = "D350A8F1437A0393C703F4041ACB0EF8"


pad_1_it = lambda k: k + (16 - len(k) % 16) * '\0'


def aes_encode(text, key):
    gen = AESGenerator()
    gen.reseed(key)
    sec_key = gen.pseudo_random_data(16)
    cipher = AES.new(sec_key, AES.MODE_ECB)
    rs = cipher.encrypt(pad_it(text))
    # 转化为16进制字符串
    return b2a_hex(rs)


def aes_decode(text, key):
    gen = AESGenerator()
    gen.reseed(key)
    sec_key = gen.pseudo_random_data(16)
    cipher = AES.new(sec_key, MODE, sec_key)
    plain_text = cipher.decrypt(a2b_hex(text))
    return plain_text.rstrip(b'\x00')


def pad_it(text):
    length, count = 16, len(text)
    return pad_1_it(text) if count < length else text + ('\0' * (length - (count % length)))


print(name, sec_name)


e = aes_encode(name, NAME_KEY).upper()  # 加密
print(name, e)
# d = aes_decode(e, NAME_KEY)  # 解密
# print("Decrypto:", d)
