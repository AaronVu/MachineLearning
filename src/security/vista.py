# coding:utf-8
import sys, os, re
import urllib
from winreg import OpenKey, HKEY_LOCAL_MACHINE, EnumKey, EnumValue, CloseKey, QueryValueEx

#wifi记录
KEY_PATH = "SOFTWARE\Microsoft\Windows NT\CurrentVersion\NetworkList\Signatures\Unmanaged"
#sid查用户名
SID_PATH = "SOFTWARE\Microsoft\Windows NT\CurrentVersion\ProfileList\%s"


def printNets(username, password):
    key = OpenKey(HKEY_LOCAL_MACHINE, KEY_PATH)
    print
    '[*] Networks You have Joined.'
    for i in range(100):
        try:
            guid = EnumKey(key, i)
            netKey = OpenKey(key, str(guid))
            (n, addr, t) = EnumValue(netKey, 5)
            (n, name, t) = EnumValue(netKey, 4)
            macAddr = val2addr(addr)
            netName = str(name)
            print
            '[+] %s %s' % (netName, macAddr)
            wiglePrint(username, password, macAddr)
            CloseKey(netKey)
        except:
            pass


def val2addr(val):
    addr = ''
    for ch in val:
        addr += '%02x ' % ord(ch)
    addr = addr.strip(' ').replace(' ', ':')[0:17]
    return addr


def wiglePrint(username, password, netid):
    browser = mechanize.Browser()
    browser.open("http://wigle.net")
    reqData = urllib.urlencode({'credential_0': username, 'credential_1': password})
    browser.open("https://wigle.net//gps/gps/main/login")
    params = {}
    params['netid'] = netid
    reqParams = urllib.urlencode(params)
    respURL = 'http://wigle.net/gps/gps/main/confirmquery/'
    resp = browser.open(respURL, reqParams).read()
    mapLat = 'N/A'
    mapLon = 'N/A'
    rLat = re.findall(r'maplat=.*\&', resp)
    if rLat:
        mapLat = rLat[0].split('&')[0].split('=')[1]
    rLon = re.findall(r'maplon=.*\&', resp)
    if rLon:
        mapLon = rLat[0].split
    print('[-] Lat: ' + mapLat + ', Lon: ' + mapLon)


def returnDir():
    dirs = ['C:\\Recycler\\', 'C:\\Recycled\\', 'C:\\$Recycle.Bin\\']
    for recycleDir in dirs:
        if os.path.isdir(recycleDir):
            return recycleDir
    return None


def sid2user(sid):
    try:
        key = OpenKey(HKEY_LOCAL_MACHINE, SID_PATH % sid)
        (value, type) = QueryValueEx(key, 'ProfileImagePath')
        user = value.split('\\')[-1]
        return user
    except:
        return sid


def findRecycled(recycleDir):
    dirList = os.listdir(recycleDir)
    for sid in dirList:
        files = os.listdir(recycleDir + sid)
        user = sid2user(sid)
        print
        '[*] Listing File For User: ' + str(user)
        for file in files:
            print
            '  [+] Found File: ' + str(file)


def main():
    recycledDir = returnDir()
    findRecycled(recycledDir)
    # printNets('', '')

