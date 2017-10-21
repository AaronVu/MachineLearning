# coding:utf-8
import threading
import sys
import urllib.request as urllib2


class ReptilesThread(threading.Thread):

    def __init__(self, block, url = '', range = ''):
        super(ReptilesThread, self).__init__()
        self.range = range
        self.url = url
        self.block = block
        self.finished = False
        self.name = block

    def run(self):
        req = urllib2.Request(self.url)
        req.add_header('Range', self.range)
        res = urllib2.urlopen(req)
        point_size = 0
        with open(self.block, 'wb') as local_file:
            local_file.seek(0)
            local_file.truncate()
            try:
                while True:
                    buffer = res.read(1024)
                    if not buffer:
                        break
                    local_file.write(buffer)
                    point_size += len(buffer)
                    local_file.flush()
                    sys.stdout.write('\b' * 64 +self.name+ 'Now: %d, Total: %s' % (point_size, '272'))
                    sys.stdout.flush()
                self.finished = True
            except:
                pass
