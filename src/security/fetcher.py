# <-*- coding: utf-8 -*->
import urllib.request as urllib2
from bs4 import BeautifulSoup
from urllib.parse import urlsplit
from os.path import basename
from PIL import Image
from PIL.ExifTags import TAGS

def findImages(url):
    print('[+] Finding images on %s'%url)
    urlContent = urllib2.urlopen(url).read()
    soup = BeautifulSoup(urlContent)
    imgTags = soup.findAll('img')
    return imgTags

def downloadImages(imgTag):
    try:
        print('[+] Dowloading image...')
        imgSrc = ('http:'+imgTag['src'])
        imgContent = urllib2.urlopen(imgSrc).read()
        imgFileName = basename(urlsplit(imgSrc)[2])
        imgFile = open("F://"+imgFileName, 'wb')
        imgFile.write(imgContent)
        imgFile.close()
        return imgFileName
    except:
        print('Error')

def gainExif(imgFileName):
    try:
        exifData = {}
        imgFile = Image.open(imgFileName)
        info = imgFile._getexif()
        if info:
            for (tag, value) in info.items():
                decoded = TAGS.get(tag, tag)
                exifData[decoded] = value
            exifGPS = exifData['GPSInfo']
            if exifGPS:
                print ('[*] %s contains GPSMetaData'%imgFileName)
    except:
        pass


imgTags = findImages("http://image.baidu.com/search/index?tn=baiduimage&ct=201326592&lm=-1&cl=2&ie=gbk&word=%CD%BC%C6%AC&fr=ala&ala=1&alatpl=others&pos=0")
for imgTag in imgTags:
    gainExif(downloadImages(imgTag))

