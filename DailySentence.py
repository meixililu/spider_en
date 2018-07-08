# -*- coding:utf-8 -*-
import requests
import json
import leancloud
from leancloud import Object
from leancloud import Query
from datetime import *


leancloud.init('3fg5ql3r45i3apx2is4j9on5q5rf6kapxce51t5bc0ffw2y4', 'twhlgs6nvdt7z7sfaw76ujbmaw7l12gb8v6sdyjw1nzk9b1a')


def getDailySentence():
    url = 'http://open.iciba.com/dsapi/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'}
    req = requests.get(url, headers=headers)
    req.encoding = 'utf-8'
    data = json.loads(req.text)

    if is_exit(data['dateline']) < 1:
        DailySentence = Object.extend('DailySentence')
        mDailySentence = DailySentence()
        mDailySentence.set('picture2', data['picture2'])
        mDailySentence.set('tts', data['tts'])
        mDailySentence.set('dateline', data['dateline'])
        mDailySentence.set('content', data['content'])
        mDailySentence.set('note', data['note'])
        mDailySentence.save()
        # print 'save item'
    else:
        print 'already exit'.encode('utf-8')


def is_exit(str):
    query = Query('DailySentence')
    query.equal_to('dateline', str)
    querys = query.find()
    size = len(querys)
    # print size
    return size


if __name__ == '__main__':
    getDailySentence()