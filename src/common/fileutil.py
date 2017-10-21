# -*- coding:utf-8 -*-
import os
import hashlib
from PyQt5 import QtCore


class FileUtil(QtCore.QObject):
    
    process = QtCore.pyqtSignal(int, int)  # cur, total

    def __init__(self):
        super(FileUtil, self).__init__()

    def ListFilesMD5(self, path):
        fileMD5 = {}
        files = self.listfiles(path)
        total = len(files)
        cur = 0
        for file in files:
            md5 = self.getfilemd5(file)
            fileMD5[file] = md5
            cur += 1
            self.process.emit(cur, total)
        return self.duplicate_checking(fileMD5)

    def duplicate_checking(self, md5Map):
        dupMap = {}
        for key,val in md5Map.items():
            if val in dupMap:
                files = dupMap[val]
                files.append(key)
            else:
                files = []
                files.append(key)
                dupMap[val] = files
        return dupMap

    def listfiles(self, path, files=[]):
        list = os.listdir(path)
        for index in range(len(list)):
            file = os.path.join(str(path), list[index])
            if os.path.isfile(file):
                files.append(file)
            else:
                self.listfiles(file, files)
        return files

    def getfilemd5(self, filename):
        hash = hashlib.md5()
        with open(filename, 'rb') as fin:
            while True:
                data = fin.read(8192)
                if not data:
                    break
                hash.update(data)
            md5 = hash.hexdigest()
            return md5


'''
util = FileUtil()
md5Map = util.ListFilesMD5('E:\images\Windows hook demo (CppWindowsHook)\Windows hook demo (CppWindowsHook)\C++\CppHookDll')
for key in md5Map:
    le = len(md5Map[key])
    if le > 1:
        print key +"重复个数: "+str(len(rs[key]))
    else:
        print key + "不存在重复 "

'''
