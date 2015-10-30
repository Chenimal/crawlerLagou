from crawlerBase import CrawlerBase
import time
import lib.functions as func
import model

'''
Synchronous Crawler for www.lagou.com

The most in-efficient way
Avg.= 15 secs
'''


class CrawlerSync(CrawlerBase):

    # record time cost
    t0, t1, t2, t3, total_new = 0.0, 0.0, 0.0, 0.0, 0

    # constructor
    def __init__(self):
        CrawlerBase.__init__(self)

    # single request(page)
    @func.timerAccumulate('t1')
    def fetchPageContent(self, post={}):
        return CrawlerBase.fetchPageContent(self, post)

    # checkout duplicate before insert
    @func.timerAccumulate('t2')
    def hasDuplicate(self, data):
        return CrawlerBase.hasDuplicate(self, data)

    # for single new record
    @func.timerAccumulate('t3')
    def addRecord(self, data):
        return CrawlerBase.addRecord(self, data)

    # single request
    @func.timerAccumulate('t0')
    def singleRequest(self, i):
        return CrawlerBase.singleRequest(self, i)

    # trigger
    def fire(self):
        try:
            total_cnt = 0
            # generate insert query
            self.model = model.dbSqlite()
            self.iq_1 = self.model.insertQuery(self.table)
            self.ip_1 = self.model.insertParam(self.table)
            for i in range(1, 31):
                total_cnt = total_cnt + self.singleRequest(i)
        except Exception as e:
            print('Error: ' + str(e))
            func.logger('crawler', time.strftime(
                '%Y-%m-%d %H:%M:%S ') + '[error] ' + str(e))
        finally:
            print('Time spent: %.2f' % self.t0)
            # 日志
            func.logger('crawler', '%s Total:%.2fs Request:%.4f Check duplicates:%.4f Save:%.4f New item:%d' %
                        (time.strftime('%Y-%m-%d %H:%M:%S'), self.t0, self.t1, self.t2, self.t3, total_cnt))


a = CrawlerSync()
a.fire()
