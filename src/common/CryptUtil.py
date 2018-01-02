# coding:utf-8
import zipfile
import optparse
from threading import Thread


def extractFile(zFile, pwd):
    try:
        zFile.extractall(pwd=pwd)
        print(pwd)
        return pwd
    except:
        pass

def extract():
    parser = optparse.OptionParser("usage%prog -f <zipfile> -d <dictionary>")
    parser.add_option("-f", dest="zname", type="string", help="specify zip file")
    parser.add_option("-d", dest="dname", type="string", help="specify dictionary file")
    (options, args) = parser.parse_args()
    if (options.zname is None) | (options.dname is None):
        print(parser.usage)
    else:
        zname = options.zname
        dname = options.dname
    zFile = zipfile.ZipFile(zname)
    passFile = open(dname)
    for line in passFile.readlines():
        pwd = line.strip('\n')
        t = Thread(target=extractFile, args=(zFile, pwd))
        t.start()


def test():
    zFile = zipfile.ZipFile("1.zip")
    passFile = open("../../resources/dictionary.txt")
    for line in passFile.readlines():
        pwd = line.strip('\n')
        guess = extractFile(zFile, pwd)
        if guess:
            print("Password = " + pwd)
            exit(0)

#
# if __name__ == "__main__":
#     extract()
