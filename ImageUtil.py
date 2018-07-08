# -*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
import json
import leancloud
from leancloud import Object
from leancloud import Query
import os
import cStringIO, urllib2
from PIL import Image
import traceback

def initDYTT():
    leancloud.init('PGw4c4KlYFavFHmw6nOwg3Li', 'XiC1O9I9oNfzcglUwfxt5uEY')

def initZYHY():
    leancloud.init('3fg5ql3r45i3apx2is4j9on5q5rf6kapxce51t5bc0ffw2y4',
                   'twhlgs6nvdt7z7sfaw76ujbmaw7l12gb8v6sdyjw1nzk9b1a')

def getImageRatio(url):
    try:
        send_headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
            'Connection': 'keep-alive'
        }
        # print 'getImageRatio img:' + url
        # url = 'http://wimg.spriteapp.cn/ugc/2017/03/15/58c8b5067cd1adad.gif'
        if len(url) > 5:
            req = urllib2.Request(url, headers=send_headers)
            file = urllib2.urlopen(req,timeout=30)
            tmpIm = cStringIO.StringIO(file.read())
            im = Image.open(tmpIm)
            (width, height) = im.size
            ratio = float(width) / height
            # print ratio
            if ratio < 0.04:
                return (0.8,width,height)
            return (ratio,width,height)
        else:
            # print 'error url:' + url
            return (5.5555,0,0)
    except:
        # print 'except getImageRatio'
        # print traceback.format_exc()
        return (5.5555,0,0)