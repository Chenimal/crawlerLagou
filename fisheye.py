# -*- coding: utf-8 -*-

# 常用函数
import os

# notify function


def notify(title='', subtitle='', message='', url=''):
    t = '-title {!r}'.format(title)
    s = '-subtitle {!r}'.format(subtitle)
    m = '-message {!r}'.format(message)
    u = '-open {!r}'.format(url)
    os.system('/usr/local/bin/terminal-notifier {}'.format(' '.join([m, t, s, u])))
