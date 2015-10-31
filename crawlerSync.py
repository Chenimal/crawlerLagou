from crawlerBase import CrawlerBase
import time
import lib.functions as func

'''
Synchronous Crawler for www.lagou.com

The most in-efficient way
Avg.= 7.2 secs
'''


class CrawlerSync(CrawlerBase):

    # record time cost
    t0, t1, t2, t3, total_new = 0.0, 0.0, 0.0, 0.0, 0

    # constructor
    def __init__(self):
        CrawlerBase.__init__(self)

    ''' add decorator to record time consumming for each part '''
    @func.timerAccumulate('t1')
    def fetchPageContent(self, post={}):
        return CrawlerBase.fetchPageContent(self, post)

    @func.timerAccumulate('t2')
    def hasDuplicate(self, data):
        return CrawlerBase.hasDuplicate(self, data)

    @func.timerAccumulate('t3')
    def addRecord(self, data):
        return CrawlerBase.addRecord(self, data)

    @func.timerAccumulate('t0')
    def singleRequest(self, i):
        return CrawlerBase.singleRequest(self, i)

    # trigger
    def fire(self):
        try:
            for i in range(1, 31):
                self.total_new = self.total_new + self.singleRequest(i)
        except Exception as e:
            print('Error: ' + str(e))
            func.logger('crawler', time.strftime(
                '%Y-%m-%d %H:%M:%S ') + '[error] ' + str(e))
        finally:
            msg = '%s Time cost(Synchro):%.4f Request:%.4f Check duplicates:%.4f Save:%.4f New item:%d' % (
                time.strftime('%Y-%m-%d %H:%M:%S'), self.t0, self.t1, self.t2, self.t3, self.total_new)
            func.logger('crawler', msg)


a = CrawlerSync()
a.fire()
