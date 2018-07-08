# -*- coding:utf-8 -*-

import leancloud
import datetime
from leancloud import Object


leancloud.init('3fg5ql3r45i3apx2is4j9on5q5rf6kapxce51t5bc0ffw2y4', 'twhlgs6nvdt7z7sfaw76ujbmaw7l12gb8v6sdyjw1nzk9b1a')


def recordSpiderRunTime():
    now = datetime.datetime.now()
    ymd = now.strftime("%Y-%m-%d")
    run_time = now.strftime('%Y-%m-%d %H:%M:%S') + "  " + "execfile.py start"

    SpiderRecord = Object.extend('SpiderRecord')
    mSpiderRecord = SpiderRecord()
    mSpiderRecord.set('ymd', ymd)
    mSpiderRecord.set('run_time', run_time)
    mSpiderRecord.save()
    # print('save item')

def recordSpiderRunTime_dytt():
    now = datetime.datetime.now()
    ymd = now.strftime("%Y-%m-%d")
    run_time = now.strftime('%Y-%m-%d %H:%M:%S') + "  " + "execfile_dytt.py start"

    SpiderRecord = Object.extend('SpiderRecord')
    mSpiderRecord = SpiderRecord()
    mSpiderRecord.set('ymd', ymd)
    mSpiderRecord.set('run_time', run_time)
    mSpiderRecord.save()


if __name__ == '__main__':
    recordSpiderRunTime()