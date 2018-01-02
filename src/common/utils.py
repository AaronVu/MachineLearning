import re
import os


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


