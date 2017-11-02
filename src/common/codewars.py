# coding:utf-8
import re
import base64


def dbl_linear(n):
    arr = [1]
    y = 0
    z = 0
    while len(arr) < n + 1:
        Y = 2 * arr[y] + 1
        Z = 3 * arr[z] + 1
        if Y > Z:
            if Z != arr[len(arr) - 1]:
                arr.append(Z)
            z += 1
        else:
            if Y != arr[len(arr) - 1]:
                arr.append(Y)
            y += 1
    return arr


def is_valid_ip(strng):
    arr = strng.split('.')
    pat = re.compile(r'([0-9]{1,3})')
    for x in arr:
        r = re.findall(pat, x)
        if not r:
            return False
    if len(arr) != 4:
        return False
    return all(map(lambda x: -1 < x < 256, map(int, arr)))


def solution(n):
    roman_numerals = {1000: 'M', 900: 'CM', 500: 'D', 400: 'CD', 100: 'C', 90: 'XC', 50: 'L', 40: 'XL', 10: 'X',
                      9: 'IX', 5: 'V', 4: 'IV', 1: 'I'}
    roman_str = ''
    for key in sorted(roman_numerals.keys(), reverse=True):
        while n >= key:
            roman_str += roman_numerals[key]
            n -= key
    return roman_str


base = (
'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X',
'Y', 'Z',
'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x',
'y', 'z',
'0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '+', '/')


def to_base_64(string):
    ch = []
    str_bin = '';
    for s in string:
        binary = bin(ord(s)).replace("0b", '')
        if len(binary) < 8:
            binary = '0' * (8 - len(binary)) + binary
            str_bin += binary
    b = re.findall(r'.{6}', str_bin)
    rs = ''
    for i in range(len(b)):
        b[i] = '0' * 2 + b[i]
        b[i] = int(b[i], 2)
        rs += base[b[i]]
    return rs


def from_base_64(string):
    return base64.b64decode(string)


def loop_size(node):
    m = {}
    n = 1
    while True:
        cur_node = node.next
        if cur_node:
            if m.get(cur_node):
                return n - m[cur_node] + 1
            n += 1
            m[cur_node] = n
            node = cur_node
        else:
            break
    return 0


class Node:
    def __init__(self, value=None, next=None):
        self.value = value
        self.next = next


def spiralize(size):
    spiral = [[1] * size for _ in range(size)]

    def ok(y, x):
        return y < size and x < size >= 0 and x >= 0 and spiral[y][x]

    y, x, dy, dx = 1, -1, 0, 1
    while ok(y + dy, x + dx):
        if ok(y + 2 * dy, x + 2 * dx):
            y += dy
            x += dx
        else:
            dx, dy = dy * (2 * dx - 1), dx
        spiral[y][x] = 0
    return spiral
