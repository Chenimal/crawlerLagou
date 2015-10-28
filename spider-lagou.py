import time
import urllib.request
import urllib.parse
import json
import sys
import lib.functions


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

    # get content from web
    def fetch_page_content(self, post={}):
        start = time.time()
        f = urllib.request.urlopen(
            url=self.url_base + self.url_params,
            data=urllib.parse.urlencode(post).encode('utf8'),
            timeout=10)
        data = f.read().decode('utf8')
        self.t1 = self.t1 + (time.time() - start)
        return data

    # check duplicate
    def has_duplicate(self, a, b):
        if a in b:
            return True
        return False

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
            if not self.has_duplicate(pid, ids):
                f.write(pid)
                encoded_item = json.dumps(item, ensure_ascii=False)
                self.append_to_file(
                    self.path + '/data/' + self.data_raw, encoded_item)
                cnt_new = cnt_new + 1
            self.t4 = self.t4 + (time.time() - s4)
            f.close()
        print(str(cnt_new) + ' new positions were added')
        end = time.time()
        self.t2 = self.t2 + (end - start)
        return cnt_new

    # main function
    def run(self):
        try:
            start_time = time.time()
            cnt_new = 0
            for i in range(1, 31):
                post_data = {'pn': i}
                raw_data = self.fetch_page_content(post_data)
                cnt_new = cnt_new + self.extract_data(raw_data)
            end_time = time.time()
            print('time spent: %.2f' % (end_time - start_time))
            # 日志
            lib.functions.logger(self.__class__.__name__, '%s, finished in %.2f  secs, %d items added. network = %.4f , process = %.4f, readlines = %.4f, check_dups = %.4f' %
                                 (time.strftime('%Y-%m-%d %H:%M:%S'), (end_time - start_time), cnt_new, self.t1, self.t2, self.t3, self.t4))
        except Exception as e:
            lib.functions.logger(self.__class__.__name__, time.strftime(
                '%Y-%m-%d %H:%M:%S\t') + '[error] ' + str(e))

a = SpiderLagou()
a.run()
