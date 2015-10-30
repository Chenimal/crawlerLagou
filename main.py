import time
import urllib.request
import urllib.parse
import json
import sys
import lib.functions as func
import model

'''
Crawler for www.lagou.com
Author: Chen Sun
Since: 10.21.2015
Version: 1.1.2

Todo:
Use cache instead of I/O
'''


class SpiderLagou():

    # record time cost
    t0, t1, t2, t3, total_new = 0.0, 0.0, 0.0, 0.0, 0

    # constructor
    def __init__(self):
        self.table = 'lagou_basic'
        self.table2 = 'lagou_company_label'
        self.url_base = 'http://www.lagou.com'
        self.url_params = '/jobs/positionAjax.json?px=new'

    # single request(page)
    @func.timerAccumulate('t1')
    def fetchPageContent(self, post={}):
        try:
            f = urllib.request.urlopen(
                url=self.url_base + self.url_params,
                data=urllib.parse.urlencode(post).encode('utf-8'),
                timeout=2)
            d = f.read().decode('utf-8')
            d = json.loads(d)
            return d['content']['result']
        except Exception as e:
            print('Error: Page ' + str(post['pn']) + ' ' + str(e))
            return []

    # save content for single request(page)
    def savePageContent(self, data):
        c = 0
        for i in data:
            if not self.hasDuplicate(i):
                s = self.addRecord(i)
                c = c + 1 if s else c
        return c

    # checkout duplicate before insert
    @func.timerAccumulate('t2')
    def hasDuplicate(self, data):
        r = self.model.findAll(
            "select * from %s where position_id = '%s'" % (self.table, data['positionId']))
        return True if r else False

    # for single new record
    @func.timerAccumulate('t3')
    def addRecord(self, data):
        p = list(map(lambda x: data.get(x), self.ip_1))
        self.model.cursor.execute(self.iq_1, p)
        self.model.conn.commit()
        # insert into lagou_company_label
        p = list(
            map(lambda x: (data['positionId'], x), data['companyLabelList']))
        q = "insert into " + self.table2 + " (position_id, label) values(?,?)"
        self.model.cursor.executemany(q, p)
        self.model.conn.commit()
        return True

    #
    @func.timerAccumulate('t0')
    def singleRequest(self, i):
        # requests with diffrent page number
        d = self.fetchPageContent({'pn': i})
        c = self.savePageContent(d)
        print('Page %d : %d items were added' % (i, c))
        self.total_new = self.total_new + c

    # trigger
    def fire(self):
        try:
            total_cnt = 0
            # generate insert query
            self.model = model.dbSqlite()
            self.iq_1 = self.model.insertQuery(self.table)
            self.ip_1 = self.model.insertParam(self.table)
            for i in range(1, 31):
                self.singleRequest(i)
        except Exception as e:
            print('Error: ' + str(e))
            func.logger(self.__class__.__name__, time.strftime(
                '%Y-%m-%d %H:%M:%S ') + '[error] ' + str(e))
        finally:
            print('Time spent: %.2f' % self.t0)
            # 日志
            func.logger(self.__class__.__name__, '%s Total:%.2fs Request:%.4f Check duplicates:%.4f Save:%.4f New item:%d' %
                        (time.strftime('%Y-%m-%d %H:%M:%S'), self.t0, self.t1, self.t2, self.t3, total_cnt))


a = SpiderLagou()
a.fire()
