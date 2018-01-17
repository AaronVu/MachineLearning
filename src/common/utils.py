# -*- coding:utf-8 -*-
import re
import os
import datetime


def format_time():
    days = []
    day = datetime.date.today()
    for _ in range(732):
        day = day + datetime.timedelta(days=-1)
        days.append(day.strftime('%Y-%m-%d'))
    print(days)


def list_files(path, allFile):
    dirs = os.listdir(path)
    for fileName in dirs:
        filePath = os.path.join(path, fileName)
        if os.path.isdir(filePath):
            list_files(filePath, allFile)
        else:
            allFile.append(filePath)


def exec_cmd(cmd):
    m = os.popen('ipconfig', 'r')
    for line in m:
        print (re.findall(r'', line.rstrip()))
    m.close()


