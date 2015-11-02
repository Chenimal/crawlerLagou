## Crawler for www.lagou.com

Index the downloaded pages periodially. 

#### Background
The website only provide up to 30 pages of result(15 items in each one) at a time. Thus it needs to be executed once in a while. The script itself runs pretty fast (less than 1 second if not considering url request).
This is built for deepen my understanding of the trending of job market, as well as preparing for the next cralwer project.

#### Performance
Time consumming with different modes (seconds per 100 requests)
- Coroutine(Asynchronous I/O): 0.8s
- Multi-thread: 3.0s
- Synchronous: 22.0s

#### Feature
1. Implement newest Python library asyncio& aiohttp to achieve coroutine mode
2. Python's Multi-threads mode is not bad, but unable to sufficiently take the advantage of multi-core processor when deploying it to the server.
1. Use Python decorator to log running performance
2. Low system cost.

#### Usage
1. run init.py to initiate project
2. setup crontab
3. run crawlerXXX.py

#### Requirement
1. Python3
2. aiohttp(pip install aiohttp)
2. Sqlite

