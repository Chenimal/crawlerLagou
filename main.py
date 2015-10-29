import time
import urllib.request
import urllib.parse
import json
import sys
import lib.functions
import model

'''
Crawler for www.lagou.com
Author: Chen Sun
Since: 10.21.2015
Version: 1.1.0

Todo:
create init file
add another company types table
Use cache instead of I/O
'''


class SpiderLagou():

    # record time cost
    t1, t2, t3, t4 = 0.0, 0.0, 0.0, 0.0

    # constructor
    def __init__(self):
        self.table = 'lagou_basic'
        self.url_base = 'http://www.lagou.com'
        self.url_params = '/jobs/positionAjax.json?px=new'

    # single request(page)
    def fetchPageContent(self, post={}):
        try:
            start = time.time()
            f = urllib.request.urlopen(
                url=self.url_base + self.url_params,
                data=urllib.parse.urlencode(post).encode('utf-8'),
                timeout=5)
            d = f.read().decode('utf-8')
            d = json.loads(d)
            return d['content']['result']
        except Exception as e:
            print('Error: Page '+ str(post['pn']) +' ' + str(e))
            return []
        finally:
            self.t1 = self.t1 + time.time() - start

    # save content for single request(page)
    def savePageContent(self, data):
        c = 0
        for i in data:
            s = self.addRecord(i)
            c = c+1 if s else c
        return c

    # for single new record
    def addRecord(self, data):
        # detemine if it's existed
        start = time.time()
        r = self.model.findAll("select * from %s where position_id = '%s'" % (self.table, data['positionId']))
        self.t2 = self.t2 + time.time() - start
        if r:
            return False
        start = time.time()
        p = list(map(lambda x: data.get(x),self.insert_param))
        self.model.cursor.execute(self.insert_query, p)
        self.model.conn.commit()
        self.t3 = self.t3 + time.time() - start
        return True

    # main function
    def run(self):
        try:
            start_time = time.time()
            # generate insert query
            self.model = model.dbSqlite()
            self.insert_query = self.model.insertQuery('lagou_basic')
            self.insert_param = self.model.insertParam('lagou_basic')
            total_cnt = 0
            # requests with diffrent page number
            for i in range(1, 31):
                post_data = {'pn': i}
                d = self.fetchPageContent(post_data)
                c = self.savePageContent(d)
                print('Page %d : %d items were added' % (i,c))
                total_cnt = total_cnt + c
            end_time = time.time()
            print('Time spent: %.2f' % (end_time - start_time))
            # 日志
            lib.functions.logger(self.__class__.__name__, '%s  Total time:%.2f secs. New item:%d. Request:%.4f. Check duplicates:%.4f, Save:%.4f' %
                                 (time.strftime('%Y-%m-%d %H:%M:%S'), (end_time - start_time), total_cnt, self.t1, self.t2, self.t3))
        except Exception as e:
            print('Error: ' + str(e))
            lib.functions.logger(self.__class__.__name__, time.strftime(
                '%Y-%m-%d %H:%M:%S\t') + '[error] ' + str(e))


a = SpiderLagou()
a.run()
