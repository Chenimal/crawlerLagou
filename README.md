## Crawler for www.lagou.com

Index the downloaded pages periodially. 

The website only provide up to 30 pages of result(15 items in each one) at a time. Thus it needs to be executed once in a while. The script itself runs pretty fast (less than 1 second if not considering url request).

I'm going to keep it in crontab for a while.

#### Usage
1. run init.py to initiate project
2. setup crontab
3. run main.py

#### Requirement
1. Python3
2. Sqlite

#### Feature
1. Use Python decorator to log running performance
2. Low system cost. I run it on my laptop
