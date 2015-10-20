# -*- coding: utf-8 -*-
import urllib
import urllib2
import json
import time
# resolve chinese character encoding problem
import sys
reload(sys)
sys.setdefaultencoding('utf8')

'''
目前执行一次需要6秒多，速度还是不理想。
95% 在 数据下载
5%  在数据处理和io 操作
'''


# grab web contents 抓取页面基本信息

t1 = 0.00


def fetch_page_content(site='', params='', post={}):
    if site == '':
        return False

    start = time.time()

    f = urllib2.urlopen(
        url=site + params, data=urllib.urlencode(post), timeout=10)
    data = f.read()

    end = time.time()
    global t1
    t1 = t1 + (end - start)

    return data

# save raw data to a file 保存到文件


def append_to_file(filepath, contents):
    if filepath == '':
        return False
    f = open(filepath, 'a')
    f.write(contents + '\n')
    f.close()

# write log 写日志


def logger(name=__name__, message=''):
    if not message:
        return False
    f = open('/Users/chen/web/personal/python/log/' + name + '.log', 'a')
    f.write(message + '\n')
    f.close()

# extract data


t2 = 0.0
t3 = 0.0
t4 = 0.0


def extract_data(data='', dirs=''):

    start = time.time()

    if not data:
        return False
    decoded = json.loads(data)
    cnt_new = 0
    for item in decoded['content']['result']:

        pid = str(item['positionId'])

        start1 = time.time()

        f = open(dirs + 'data/position_lagou_uniq_ids.txt', 'a+')
        # in order to read lines, move file pointer to the beginning
        f.seek(0, 0)
        ids = f.readlines()

        end1 = time.time()
        global t3
        t3 = t3 + (end1 - start1)

        start2 = time.time()

        duplicate = None
        for existed_id in ids:
            if existed_id.strip() == pid:
                duplicate = 1
                break

        end2 = time.time()
        global t4
        t4 = t4 + (end2 - start2)

        if not duplicate:
            f.write(pid + '\n')
            decoded_item = json.dumps(item).decode('raw_unicode_escape')
            append_to_file(dirs + 'data/position_lagou.txt',
                           decoded_item)
            cnt_new = cnt_new + 1
        f.close()
    print str(cnt_new) + ' new positions were added'

    end = time.time()
    global t2
    t2 = t2 + (end - start)

    return cnt_new

# main function


def main():
    start_time = time.time()

    params = {
        'url_base': 'http://www.lagou.com',
        'url_params': '/jobs/positionAjax.json?px=new',
        'local_dir': '/Users/chen/web/personal/python/'
    }

    cnt_new = 0
    for i in range(1, 31):
        post_data = {'pn': i}
        raw_data = fetch_page_content(
            params['url_base'], params['url_params'], post_data)
        cnt_new = cnt_new + extract_data(raw_data, params['local_dir'])

    end_time = time.time()

    global t1, t2, t3, t4
    # 日志
    logger(message=time.strftime('%Y-%m-%d %H:%M:%S')
           + ', finished in ' + '%.2f' % (end_time - start_time)
           + ' secs, ' + str(cnt_new)
           + ' items added. network = %.4f , process = %.4f, readlines = %.4f, check_dups = %.4f' % (t1, t2, t3, t4))


main()
