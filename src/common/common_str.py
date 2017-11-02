# -*- coding:utf-8 -*-
import re


def strh(a, b, com_str):
    for i in range(0, len(a)):
        for j in range(0, len(b)):
            if a[i] == b[j]:
                count_len(a[i], i, j, a, b, com_str)


def count_len(cur, i, j, a, b, com_str):
    s = cur
    if i+1 == len(a) or j+1 == len(b) or a[i+1] != b[j+1]:
        index = com_str[0]
        if index == 0:
            com_str.append(s)
            com_str[0] = com_str[0]+1
        else:
            for k in range(1, len(com_str)):
                m = re.search(' '+s, com_str[index])
                if m is None:
                    m = re.search(s+' ', com_str[index])
                    if m is None:
                        m = re.search(com_str[index], s)
                        if m is not None:
                            com_str[index] = s
                        else:
                            com_str.append(s)
                            com_str[0] = com_str[0]+1
    else:
        s = s+' '+a[i+1]
        count_len(s, i+1, j+1, a, b, com_str)


def common_ground(a, b):
    com_str = [0]
    if a is None or b is None or a.strip() == '' or b.strip() == '':
        print('death')
        return
    a = re.sub(r'\s+',' ',a).strip()
    b = re.sub(r'\s+',' ',b).strip()
    if a == b:
        print(a)
        return
    list_a = a.lower().split()
    list_b = b.lower().split()
    strh(list_a, list_b, com_str)
    if len(com_str) == 1:
        print("death")
    else:
        print(''.join(com_str[x]+' ' for x in range(1, len(com_str))))


def test():
    common_ground('Hello  world la', 'Hello world     lalala')
    common_ground('eat chicken', 'eat chicken and rice')
    common_ground('eat a burger and drink a coke', 'drink a coke')
    common_ground('i like trutles', 'what are you talking aboue')
    common_ground('aa bb', 'aa bb cc')
    common_ground('aa bb cc', 'bb cc')
    common_ground('aa bb cc', 'bb cc bb aa')
    common_ground('aa bb', 'cc dd')
    common_ground('aa bb', '')
    common_ground('', 'cc dd')


