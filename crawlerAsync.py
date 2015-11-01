from crawlerBase import CrawlerBase
import asyncio
import aiohttp
import time
import lib.functions as func

'''
Asynchronous Crawler

Coroutine in single thread (asynchronous I/O)
Use asyncio and aiohttp packages
So far the fastest method
'''


class CrawlerAsync(CrawlerBase):

    def __init__(self):
        CrawlerBase.__init__(self)

    @asyncio.coroutine
    def singleRequest(self, i):
        '''
        do not invoke fetchPageContent, use aiohttp instead
        '''
        try:
            response = yield from aiohttp.request('post', url=self.url_base + self.url_params, data={'pn': i})
            d = yield from asyncio.wait_for(response.read_and_close(decode=True), timeout=1)
            # save data
            c = self.savePageContent(d['content']['result'])
            print('Page %2d : %d items were added' % (i, c))
            self.total_new = self.total_new + c
        except Exception as e:
            msg = time.strftime(
                '%Y-%m-%d %H:%M:%S') + " [error][asyncio] " + str(e)
            func.logger('crawler', msg)

    @asyncio.coroutine
    def bug():
        raise Exception("not consumed")

    # trigger
    def fire(self):
        try:
            s = time.time()
            loop = asyncio.get_event_loop()
            tasks = [asyncio.async(self.singleRequest(i))
                     for i in range(1, 31)]
            loop.run_until_complete(asyncio.wait(tasks))
            loop.close()
        except Exception as e:
            print('Error: ' + str(e))
            func.logger('crawler', time.strftime(
                '%Y-%m-%d %H:%M:%S ') + '[error] ' + str(e))
        finally:
            msg = '%s Time cost(Asynchr):%.4f New item:%d' % (
                time.strftime('%Y-%m-%d %H:%M:%S'), time.time() - s, self.total_new)
            func.logger('crawler', msg)


a = CrawlerAsync()
a.fire()
