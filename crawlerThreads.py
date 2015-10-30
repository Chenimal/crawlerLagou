from crawlerBase import CrawlerBase
import threading
import queue
import time
import lib.functions as func

'''
Multi-thread Crawler

Better than synchronous, but still not good enough
Avg. = ? s

todo:
include print into looger(optional)
fix thread problem(probably sqlite)
trying to log time consumming in threads way
'''


class CrawlerThreads(CrawlerBase):

    def __init__(self):
        CrawlerBase.__init__(self)
        self.task_queue = queue.Queue()

    # working method accept args from task_queue, and be handled by threads
    def working(self):
        while True:
            args = self.task_queue.get()
            self.total_new = self.total_new + self.singleRequest(args)
            self.task_queue.task_done()

    def fire(self):
        try:
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

            print('everything is done')
        except Exception as e:
            print('Error: ' + str(e))
            func.logger('crawler', time.strftime(
                '%Y-%m-%d %H:%M:%S ') + '[error] ' + str(e))
        finally:
            msg = '%s Time cost:xxx New item:%d' % (
                time.strftime('%Y-%m-%d %H:%M:%S'), self.total_new)
            print(msg)
            func.logger('crawler', msg)


a = CrawlerThreads()
a.fire()
