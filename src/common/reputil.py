# coding:utf-8
import re
import os
import urllib
from queue import Queue
import urllib3
import src.common.threads as threads
import time


class ReqUtil:

    cookie_filename = 'cookie.txt'
    thread_count = 5
    file_suffix = '.temp'

    def __init__(self, timeout = 10, enable_proxy = False, proxy_info = {}):
        self.enable_proxy = enable_proxy
        self.timeout = timeout
        if enable_proxy and len(proxy_info) > 1:
            self.setProxy(proxy_info)


    def doGet(self, url, data={}, header={}):
        data = urllib.urlencode(data)
        geturl = url + "?" + data
        request = urllib3.Request(geturl)
        for (key,val) in header:
            request.add_header(key, val)
        try:
            response = urllib3.urlopen(request)
        except urllib3.HTTPError as e:
            print(e.code)
        except urllib3.URLError as e:
            print(e.reason)
        else:
            print(response.read())


    def doPost(self, url, data={},header={}):
        data = urllib.urlencode(data)
        request = urllib3.Request(url, data, header)
        response = urllib3.urlopen(request)
        print(response.read())

    def doPut(self, url, data={}):
        request = urllib3.Request(url, data=data)
        request.get_method = lambda: 'PUT'  # or 'DELETE'
        response = urllib3.urlopen(request)
        print(response.read())

    def doDelete(self, url, data={}):
        request = urllib3.Request(url, data=data)
        request.get_method = lambda: 'DELETE'
        response = urllib3.urlopen(request)
        print(response.read())

    def setProxy(self, proxy_info):
        proxy_handler = urllib3.ProxyHandler({"http": "http://%(host)s:%(port)d"%proxy_info})
        opener = urllib3.build_opener(proxy_handler)
        urllib3.install_opener(opener)

    def openDebug(self):
        httpHandler = urllib3.HTTPHandler(debuglevel=1)
        httpsHandler = urllib3.HTTPSHandler(debuglevel=1)
        opener = urllib3.build_opener(httpHandler, httpsHandler)
        urllib3.install_opener(opener)

    def doHttpWithCookie(self, url, data={}, save_cookie = False):
        cookie = cookielib.CookieJar()
        cookie.load(self.cookie_filename, ignore_discard=True, ignore_expires=True)
        if save_cookie:
            cookie = cookielib.MozillaCookieJar(self.cookie_filename)
        handler = urllib3.HTTPCookieProcessor(cookie)
        opener = urllib3.build_opener(handler)
        response = opener.open(url)
        for item in cookie:
            print('Name = ' + item.name)
            print('Value = ' + item.value)
        if save_cookie:
            cookie.save(ignore_discard=True, ignore_expires=True)

    def downLoad(self, url): #单步下载
        print (u"文件下载中...")
        file_name = url.split('/')[-1]
        u = urllib3.urlopen(url)
        f = open(file_name, 'wb')
        meta = u.info()
        file_size = int(meta.getheaders("Content-Length")[0])
        cur_size = 0
        block_sz = 8192
        while True:
            buffer = u.read(block_sz)
            if not buffer:
                break
            cur_size += len(buffer)
            print ("已下载："+str(cur_size*100 / float(file_size))[0:2]+"%")
            f.write(buffer)
        f.close()


    #多线程断点下载
    def downloadWithPoint(self, url):
        support, total_size = self.support_point(url)
        if support:
            finished = False
            filename = url.split('/')[-1]
            (filename, _) = re.subn('[\\\/\:\*\?\"\<\>\|]', '', filename)
            tmp_filename = filename + self.file_suffix
            point_size = 0
            try:
                with open(tmp_filename, 'rb') as tmp_file:
                    point_size = int(tmp_file.read()) + 1
            except:
                with open(tmp_filename, 'w') as tmp:
                    pass

            r = int(total_size) - point_size
            blocks = self.cutBlock(r)
            self.block_queue = Queue.Queue()
            for i in range(len(blocks)):
                th = threads.ReptilesThread('block'+str(i), url, blocks[i])
                th.start()
                self.block_queue.put(th)
            self.link(filename, point_size)

    def support_point(self, url):
        req = urllib3.Request(url)
        req.add_header('Range', 'bytes=0-20')
        res = urllib2.urlopen(req)
        content_length = res.headers['Content-Length']
        content_range = res.headers['Content-Range']
        if content_length and content_range:
            m = re.match('bytes 0-', content_range)
            if m:
                size = content_range.split('/')[1]
                return True,size
        return False,0

    def cutBlock(self, size):
        n = size/self.thread_count
        blocks = []
        for count in range(self.thread_count):
            if count == 0:
                blocks.append("bytes=0-%d" % (n,))
            elif count+1 == self.thread_count:
                blocks.append("bytes=%d-" % (count * n + 1),)
            else:
                data = "bytes=%d-%d"%(count * n + 1, (count + 1) * n)
                blocks.append(data)
        return blocks

    def link(self, filename, point_size):
        tmp_filename = filename + self.file_suffix
        with open(filename, 'ab+') as fin:
            while not self.block_queue.empty():
                th = self.block_queue.get()
                while th.isAlive():
                    time.sleep(0.01)
                with open(th.name, 'rb') as fout:
                    while True:
                        data = fout.read(1024)
                        if not data:
                            break
                        fin.write(data)
                        point_size += len(data)
                    fout.close()
                    if not th.finished:
                        while not self.block_queue.empty():
                            t = self.block_queue.get()
                            os.remove(th.name)
                            with open(tmp_filename, 'wb') as ftmp:
                                ftmp.write(str(point_size))
                        break
                os.remove(th.name)
            os.remove(tmp_filename)











reptile = ReqUtil(False)
#print reptile.cutBlock(818)
reptile.downloadWithPoint('https://www.python.org/ftp/python/3.5.4/Python-3.5.4.tgz')