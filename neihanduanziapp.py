#!/usr/bin/env python
# -*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
import json
import leancloud
from leancloud import Object
from leancloud import Query
from datetime import *
import traceback
import cStringIO, urllib2
from PIL import Image

leancloud.init('3fg5ql3r45i3apx2is4j9on5q5rf6kapxce51t5bc0ffw2y4', 'twhlgs6nvdt7z7sfaw76ujbmaw7l12gb8v6sdyjw1nzk9b1a')


def is_exit(str):
    query = Query('Joke')
    query.equal_to('text', str)
    querys = query.find()
    return len(querys) > 0

def is_exit_img(img):
    query = Query('Joke')
    query.equal_to('img', img)
    querys = query.find()
    return len(querys) > 0


def neihanduanziapp():
    # longitude = 115.89946 & latitude = 24.423765 &
    urls = []
    urls.append('http://lf.snssdk.com/neihan/stream/mix/v1/?mpic=1&webp=1&essence=1&content_type=-301&message_cursor=-1&count=30&min_time=0&screen_width=1080&double_col_mode=1&iid=8754737914&device_id=35385271889&ac=wifi&channel=xiaomi&aid=7&app_name=joke_essay&version_code=614&version_name=6.1.4&device_platform=android&ssmix=a&device_type=Mi+Note+2&device_brand=Xiaomi&os_api=23&os_version=6.0.1&uuid=869782023526463&openudid=5cb5e6a88448f537&manifest_version_code=614&resolution=1080*1920&dpi=440&update_version_code=6140')
    urls.append('http://lf.snssdk.com/neihan/stream/mix/v1/?mpic=1&webp=1&essence=1&content_type=-102&message_cursor=-1&count=30&min_time=0&screen_width=1080&double_col_mode=0&iid=8754737914&device_id=35385271889&ac=wifi&channel=xiaomi&aid=7&app_name=joke_essay&version_code=614&version_name=6.1.4&device_platform=android&ssmix=a&device_type=Mi+Note+2&device_brand=Xiaomi&os_api=23&os_version=6.0.1&uuid=869782023526463&openudid=5cb5e6a88448f537&manifest_version_code=614&resolution=1080*1920&dpi=440&update_version_code=6140')
    urls.append('http://lf.snssdk.com/neihan/stream/mix/v1/?mpic=1&webp=1&essence=1&content_type=-104&message_cursor=-1&count=30&min_time=0&screen_width=1080&double_col_mode=0&iid=8754737914&device_id=35385271889&ac=wifi&channel=xiaomi&aid=7&app_name=joke_essay&version_code=614&version_name=6.1.4&device_platform=android&ssmix=a&device_type=Mi+Note+2&device_brand=Xiaomi&os_api=23&os_version=6.0.1&uuid=869782023526463&openudid=5cb5e6a88448f537&manifest_version_code=614&resolution=1080*1920&dpi=440&update_version_code=6140')
    urls.append('http://lf.snssdk.com/neihan/stream/mix/v1/?mpic=1&webp=1&essence=1&content_type=-103&message_cursor=-1&count=30&min_time=0&screen_width=1080&double_col_mode=0&iid=8754737914&device_id=35385271889&ac=wifi&channel=xiaomi&aid=7&app_name=joke_essay&version_code=614&version_name=6.1.4&device_platform=android&ssmix=a&device_type=Mi+Note+2&device_brand=Xiaomi&os_api=23&os_version=6.0.1&uuid=869782023526463&openudid=5cb5e6a88448f537&manifest_version_code=614&resolution=1080*1920&dpi=440&update_version_code=6140')
    urls.append('http://lf.snssdk.com/neihan/stream/mix/v1/?mpic=1&webp=1&essence=1&content_type=-101&message_cursor=-1&count=30&min_time=0&screen_width=1080&double_col_mode=0&iid=8754737914&device_id=35385271889&ac=wifi&channel=xiaomi&aid=7&app_name=joke_essay&version_code=614&version_name=6.1.4&device_platform=android&ssmix=a&device_type=Mi+Note+2&device_brand=Xiaomi&os_api=23&os_version=6.0.1&uuid=869782023526463&openudid=5cb5e6a88448f537&manifest_version_code=614&resolution=1080*1920&dpi=440&update_version_code=6140')
    for i in range(0,2):
        for url in urls:
            req = requests.get(url)
            # print req.text
            result = json.loads(req.text)
            if 'success' == result['message']:
                datas = result['data']['data']
                img = ''
                type = ''
                title = ''
                video_url = ''
                source_url = ''
                for data in datas:
                    if 1 == data['type']:
                        group = data['group']
                        media_type = group['media_type']
                        if 3 == media_type:
                            type = '4'
                            video_url = group['mp4_url']
                            title = group['text']
                            source_url = group['share_url']
                            img = group['large_cover']['url_list'][0]['url']
                            ratio = getImageRatio(img)
                        elif 2 == media_type:
                            type = '3'
                            video_url = ''
                            title = group['text']
                            source_url = group['share_url']
                            img = group['large_image']['url_list'][0]['url']
                            ratio = getImageRatio(img)
                        elif 1 == media_type:
                            type = '1'
                            video_url = ''
                            title = group['text']
                            source_url = group['share_url']
                            img = group['large_image']['url_list'][0]['url']
                            ratio = getImageRatio(img)
                        elif 0 == media_type:
                            type = '5'
                            video_url = ''
                            title = group['text']
                            source_url = group['share_url']
                        else:
                            continue

                        if title == '':
                            # print 'title is none'
                            if is_exit_img(img):
                                # print 'exit'
                                continue
                        elif is_exit(title):
                            # print 'exit'
                            continue


                        # print title
                        # print video_url
                        # print img
                        # print source_url
                        # print type
                        # Reading = Object.extend('Joke')
                        # mReading = Reading()
                        # mReading.set('text', title)
                        # mReading.set('img', img)
                        # mReading.set('ratio', ratio)
                        # mReading.set('video_url', video_url)
                        # mReading.set('source_url', source_url)
                        # mReading.set('type', type)
                        # mReading.set('category', '102')
                        # # mReading.save()
                        # print('save item')

def getImageRatio(url):
    try:
        send_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20100101 Firefox/16.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Connection': 'keep-alive'
        }
        # print 'getImageRatio img:' + url
        # url = 'http://wimg.spriteapp.cn/ugc/2017/03/15/58c8b5067cd1adad.gif'
        if len(url) > 5:
            req = urllib2.Request(url, headers=send_headers)
            file = urllib2.urlopen(req)
            tmpIm = cStringIO.StringIO(file.read())
            im = Image.open(tmpIm)
            (width, height) = im.size
            ratio = float(width) / height
            # print ratio
            if ratio < 0.04:
                return 0.8
            return ratio
        else:
            return 0.8
    except urllib2.HTTPError, e:
        # print e.code
        if e.code == 404:
            return 5.5555
        if e.code == 403:
            return 5.5555
        # print 'except getImageRatio'
        print traceback.format_exc()
        return 0.8;

#category 101 搞笑; 102 段子; 103 美女; 104
#type 1 img; 2 ; 3 gif; 4 video; 5 text; 6 url；
if __name__ == '__main__':
    neihanduanziapp()
