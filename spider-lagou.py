# -*- coding: utf-8 -*-
import time
import urllib2
import urllib
import sys
import json
# resolve chinese character encoding problem
reload(sys)
sys.setdefaultencoding('utf8')


class SpiderLagou():

    # record time cost
    t1, t2, t3, t4 = 0.0, 0.0, 0.0, 0.0

    # constructor
    def __init__(self):
        self.path = sys.path[0]
        self.url_base = 'http://www.lagou.com'
        self.url_params = '/jobs/positionAjax.json?px=new'
        self.data_ids = 'position_lagou_uniq_ids.txt'
        self.data_raw = 'position_lagou.txt'

    # append to file
    def append_to_file(self, filepath, contents):
        if filepath == '':
            return False
        f = open(filepath, 'a')
        f.write(contents + '\n')
        f.close()

    # write log
    def logger(self, name=__name__, message=''):
        path = self.path + '/log/' + name + '.log'
        return self.append_to_file(path, message)

    # get content from web
    def fetch_page_content(self, post={}):
        start = time.time()
        f = urllib2.urlopen(
            url=self.url_base + self.url_params,
            data=urllib.urlencode(post), timeout=10)
        data = f.read()
        self.t1 = self.t1 + (time.time() - start)
        return data

    def extract_data(self, data=''):
        start = time.time()
        if not data:
            return False
        decoded = json.loads(data)
        cnt_new = 0
        for item in decoded['content']['result']:
            s3 = time.time()
            pid = str(item['positionId'])
            f = open(self.path + '/data/' + self.data_ids, 'a+')
            f.seek(0, 0)
            ids = f.readlines()
            self.t3 = self.t3 + (time.time() - s3)
            s4 = time.time()
            pid = pid + '\n'
            if pid not in ids:
                print "%s not exists yet" % pid
                f.write(pid)
                decoded_item = json.dumps(item).decode('raw_unicode_escape')
                self.append_to_file(
                    self.path + '/data/' + self.data_raw, decoded_item)
                cnt_new = cnt_new + 1
            self.t4 = self.t4 + (time.time() - s4)
            f.close()
        print str(cnt_new) + ' new positions were added'
        end = time.time()
        self.t2 = self.t2 + (end - start)
        return cnt_new

    # main function
    def run(self):
        start_time = time.time()
        cnt_new = 0
        for i in range(1, 31):
            post_data = {'pn': i}
            raw_data = self.fetch_page_content(post_data)
            cnt_new = cnt_new + self.extract_data(raw_data)
        end_time = time.time()
        print 'time spent: %.2f' % (end_time - start_time)
        # 日志
        self.logger(message='%s, finished in %.2f  secs, %d items added. network = %.4f , process = %.4f, readlines = %.4f, check_dups = %.4f' %
                    (time.strftime('%Y-%m-%d %H:%M:%S'), (end_time - start_time), cnt_new, self.t1, self.t2, self.t3, self.t4))

a = SpiderLagou()
a.run()
