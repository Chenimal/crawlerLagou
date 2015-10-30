import urllib.request
import urllib.parse
import json
import lib.functions as func
import time

'''
Base Crawler for www.lagou.com
Author: Chen Sun
Since: 10.21.2015
Version: 1.1.2
'''


class CrawlerBase():

    # constructor

    def __init__(self):
        self.table = 'lagou_basic'
        self.table2 = 'lagou_company_label'
        self.url_base = 'http://www.lagou.com'
        self.url_params = '/jobs/positionAjax.json?px=new'

    # single request(page)
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
            msg = time.strftime('%Y-%m-%d %H:%M:%S') + ' [error][network] ' + str(e)
            print(msg)
            func.logger('crawler', msg)
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
    def hasDuplicate(self, data):
        r = self.model.findAll(
            "select * from %s where position_id = '%s'" % (self.table, data['positionId']))
        return True if r else False

    # for single new record
    def addRecord(self, data):
        try:
            p = list(map(lambda x: data.get(x), self.ip_1))
            self.model.cursor.execute(self.iq_1, p)
            self.model.conn.commit()
            # insert into lagou_company_label
            p = list(
                map(lambda x: (data['positionId'], x), data['companyLabelList']))
            q = "insert into " + self.table2 + \
                " (position_id, label) values(?,?)"
            self.model.cursor.executemany(q, p)
            self.model.conn.commit()
            return True
        except Exception as e:
            msg = time.strftime('%Y-%m-%d %H:%M:%S') + ' [error][database] ' + str(e)
            print(msg)
            func.logger('crawler', msg)
            return False

    # single request
    def singleRequest(self, i):
        # requests with diffrent page number
        d = self.fetchPageContent({'pn': i})
        c = self.savePageContent(d)
        print('Page %d : %d items were added' % (i, c))
        return c
