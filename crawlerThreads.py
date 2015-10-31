from crawlerBase import CrawlerBase
import threading
import queue
import time
import lib.functions as func

'''
Multi-thread Crawler

Better than synchronous, but still not good enough
Avg. = 2.2s
'''


class CrawlerThreads(CrawlerBase):

    def __init__(self):
        CrawlerBase.__init__(self)
        self.task_queue = queue.Queue()
        self.lock = threading.Lock()

    '''
    add a thread lock to ensure atomicity（原子性） because:
    1. query contains 'select' and 'insert' actions. it is a transaction(事务).
    2. need to update self.total_new which is a shared attr.
    '''

    def savePageContent(self, data):
        self.lock.acquire()
        c = CrawlerBase.savePageContent(self, data)
        self.total_new = self.total_new + c
        self.lock.release()
        return c

    # working method accept args from task_queue, and be handled by threads
    def working(self):
        while True:
            args = self.task_queue.get()
            self.singleRequest(args)
            self.task_queue.task_done()

    def fire(self):
        try:
            s = time.time()
            # set 10 threads
            for i in range(1, 10):
                t = threading.Thread(target=self.working)
                t.setDaemon(True)
                t.start()
            # put task into queue
            for i in range(1, 31):
                self.task_queue.put(i)
            # block threads. continue until all threads finished
            self.task_queue.join()

        except Exception as e:
            func.logger('crawler', time.strftime(
                '%Y-%m-%d %H:%M:%S ') + '[error][main] ' + str(e))
        finally:
            msg = '%s Time cost:%.4f New item:%d' % (
                time.strftime('%Y-%m-%d %H:%M:%S'), time.time() - s, self.total_new)
            func.logger('crawler', msg)


a = CrawlerThreads()
a.fire()
