#-*-coding: utf-8 -*-

from distutils.core import setup
import py2exe

'''
将test.py变为test.exe
cmd下执行：python setup.py py2exe，在dist目录下有exe和必备dll
'''
setup(console=['winhook.py'])



