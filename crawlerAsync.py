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

    async def singleRequest(self, i):
        '''
        do not invoke fetchPageContent, use aiohttp instead
        '''
        try:
            with aiohttp.ClientSession() as session:
                async with session.post(url=self.url_base + self.url_params, data={'pn': i}) as response:
                    d = await response.json()
                    # save data
                    c = self.savePageContent(
                        d['content']['positionResult']['result'])
                    print('Page %2d : %d items were added' % (i, c))
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
            tasks = [asyncio.async(self.singleRequest(i))
                     for i in range(1, 31)]
            loop.run_until_complete(asyncio.wait(tasks, timeout=100))
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
