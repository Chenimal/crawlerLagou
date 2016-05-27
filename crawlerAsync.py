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
Avg.= 0.8 sec per 100 requests
'''


class CrawlerAsync(CrawlerBase):

    def __init__(self):
        CrawlerBase.__init__(self)
        # 使用长连接，所有请求都用一个 session
        self.session = aiohttp.ClientSession()

    async def singleRequest(self, i):
        '''
        do not invoke fetchPageContent, use aiohttp instead
        '''
        try:
            t1 = time.time()
            print('start request :' + str(i))
            async with self.session.post(url=self.url_base + self.url_params, data={'pn': i}) as response:
                d = await response.json()
                # save data
                c = self.savePageContent(
                    d['content']['positionResult']['result'])
                print('Page %2d : %d items added, using %.4f secs' %
                      (i, c, time.time() - t1))
                self.total_new = self.total_new + c
        except Exception as e:
            msg = time.strftime(
                '%Y-%m-%d %H:%M:%S') + " [error][asyncio] " + str(i) + ' ' + str(e)
            func.logger('crawler_error', msg)

    def bug():
        raise Exception("not consumed")

    # trigger
    def fire(self):
        try:
            s = time.time()
            loop = asyncio.get_event_loop()
            tasks = [self.singleRequest(i)
                     for i in range(1, 31)]
            loop.run_until_complete(asyncio.wait(tasks, timeout=100))
            self.session.close()
            loop.close()
        except Exception as e:
            print('Error: ' + str(e))
            func.logger('crawler_error', time.strftime(
                '%Y-%m-%d %H:%M:%S ') + '[error] ' + str(e))
        finally:
            msg = '%s Time cost(Asynchr):%.4f New item:%d' % (
                time.strftime('%Y-%m-%d %H:%M:%S'), time.time() - s, self.total_new)
            func.logger('crawler', msg)


a = CrawlerAsync()
a.fire()
