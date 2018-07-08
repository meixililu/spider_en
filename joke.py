#!/usr/bin/env python
# -*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
import json
import leancloud
from leancloud import Object
from leancloud import Query
from datetime import *
import time
import traceback
import cStringIO, urllib2
from PIL import Image

leancloud.init('3fg5ql3r45i3apx2is4j9on5q5rf6kapxce51t5bc0ffw2y4', 'twhlgs6nvdt7z7sfaw76ujbmaw7l12gb8v6sdyjw1nzk9b1a')
sign = '?showapi_appid=11619&showapi_sign=f27574671ec14eb4a97faacb2eee3ef2'

def is_exit(str):
    global category
    query = Query('Joke')
    query.equal_to('text', str)
    querys = query.find()
    return len(querys) > 0

def is_source_exit(source_url):
    global category
    query = Query('Joke')
    query.equal_to('source_url', source_url)
    querys = query.find()
    return len(querys) > 0

def is_img_exit(img):
    global category
    query = Query('Joke')
    query.equal_to('img', img)
    querys = query.find()
    return len(querys) > 0

def laifudaotupianxiaohua():
    global sign
    url = 'http://route.showapi.com/107-33'+ sign
    # print url
    req = requests.get(url)
    # print req.text
    result = json.loads(req.text)
    if 0 == result['showapi_res_code']:
        newslist = result['showapi_res_body']['list']
        for data in newslist:
            if is_exit(data['title'].strip()):
                # print 'exit and continue'
                continue
            else:
                time.sleep(3)
                # print data['title'].strip()
                # print data['thumburl']
                ratio = getImageRatio(data['thumburl'])
                Reading = Object.extend('Joke')
                mReading = Reading()
                mReading.set('text', data['title'].strip())
                mReading.set('img', data['thumburl'])
                mReading.set('ratio', ratio)
                mReading.set('type', '1')
                mReading.set('category', '101')
                if ratio != 5.5555:
                    mReading.save()
                    # print('save item')

def laifudaoxiaohua():
    global sign
    url = 'http://route.showapi.com/107-32'+ sign
    # print url
    req = requests.get(url)
    # print req.text
    result = json.loads(req.text)
    if 0 == result['showapi_res_code']:
        newslist = result['showapi_res_body']['list']
        for data in newslist:
            if is_exit(data['content'].strip()):
                # print 'exit and continue'
                continue
            else:
                # print data['content'].strip()
                # print data['url']
                Reading = Object.extend('Joke')
                mReading = Reading()
                mReading.set('text', data['content'].strip())
                # mReading.set('img', data['picUrl'])
                mReading.set('source_url', data['url'])
                # mReading.set('publish_time', publish_time)
                mReading.set('type', '5')
                mReading.set('category', '101')
                mReading.save()
                # print('save item')

def xiaohuadaquan_gif():
    global sign
    for page in range(1,2):
        para = '&page=%s&maxResult=20' % (page)
        url = 'http://route.showapi.com/341-3'+ sign + para
        # print page
        # print url
        req = requests.get(url)
        # print req.text
        result = json.loads(req.text)
        if 0 == result['showapi_res_code']:
            newslist = result['showapi_res_body']['contentlist']
            for data in newslist:
                if is_exit(data['title'].strip()):
                    # print 'exit and continue'
                    continue
                else:
                    publish_time = datetime.strptime(str(data['ct']), "%Y-%m-%d %H:%M:%S.%f")
                    # print data['title'].strip()
                    # print publish_time
                    # print data['img']
                    ratio = getImageRatio(data['img'])
                    if ratio == 5.5555:
                        continue
                    Reading = Object.extend('Joke')
                    mReading = Reading()
                    mReading.set('text', data['title'].strip())
                    mReading.set('img', data['img'])
                    mReading.set('ratio', ratio)
                    # mReading.set('source_url', data['url'])
                    mReading.set('publish_time', publish_time)
                    mReading.set('type', '3')
                    mReading.set('category', '101')
                    mReading.save()
                    # print('save item')

def tupianxiaohua():
    global sign
    for page in range(1,2):
        para = '&page=%s&maxResult=20&time=2015-07-10' % (page)
        url = 'http://route.showapi.com/341-2'+ sign + para
        # print page
        # print url
        req = requests.get(url)
        # print req.text
        result = json.loads(req.text)
        if 0 == result['showapi_res_code']:
            newslist = result['showapi_res_body']['contentlist']
            for data in newslist:
                if is_exit(data['title'].strip()):
                    # print 'exit and continue'
                    continue
                else:
                    # print data['title'].strip()
                    # print data['img']
                    ratio = getImageRatio(data['img'])
                    if ratio == 5.5555:
                        continue
                    Reading = Object.extend('Joke')
                    mReading = Reading()
                    mReading.set('text', data['title'].strip())
                    mReading.set('img', data['img'])
                    mReading.set('ratio', ratio)
                    mReading.set('type', '1')
                    mReading.set('category', '101')
                    mReading.save()
                    # print('save item')

def wenbenxiaohua():
    global sign
    for page in range(1,2):
        para = '&page=%s&maxResult=20' % (page)
        url = 'http://route.showapi.com/341-1'+ sign + para
        # print page
        # print url
        req = requests.get(url)
        # print req.text
        result = json.loads(req.text)
        if 0 == result['showapi_res_code']:
            newslist = result['showapi_res_body']['contentlist']
            for data in newslist:
                if is_exit(data['text'].strip()):
                    # print 'exit and continue'
                    continue
                else:
                    # print data['text'].strip()
                    Reading = Object.extend('Joke')
                    mReading = Reading()
                    mReading.set('text', data['text'].strip())
                    mReading.set('type', '5')
                    mReading.set('category', '101')
                    mReading.save()
                    # print('save item')

def budejie():
    global sign
    for page in range(1,3):
        para = '&page=%s' % (page)
        url = 'http://route.showapi.com/255-1'+ sign + para
        # print page
        # print url
        req = requests.get(url)
        # print req.text
        result = json.loads(req.text)
        if 0 == result['showapi_res_code']:
            datas = result['showapi_res_body']['pagebean']['contentlist']
            for data in datas:
                if is_exit(data['text'].strip()):
                    # print 'exit and continue'
                    continue
                else:
                    # print '--------------------'
                    # print data['text'].strip()

                    img = ''
                    video_url = ''
                    type = ''
                    ratio = 0.8
                    if data['type'] == '10':
                        type = '1'
                        img = data['image0']
                        pos = img.rfind(".")
                        if img[pos+1:] == 'gif':
                            type = '3'
                    elif data['type'] == '29':
                        type = '5'
                    elif data['type'] == '31':
                        type = '7'
                        video_url = data['voice_uri']
                        if 'image3' in data.keys():
                            if len(data['image3']) > 0:
                                img = data['image3']
                        if 'image0' in data.keys():
                            if len(data['image0']) > 0:
                                img = data['image0']
                    elif data['type'] == '41':
                        type = '4'
                        video_url = data['video_uri']

                    # print type
                    # print data['weixin_url']
                    # print img
                    # print video_url
                    ratio = getImageRatio(img)
                    if ratio == 5.5555:
                        continue
                    Reading = Object.extend('Joke')
                    mReading = Reading()
                    mReading.set('text', data['text'].strip())
                    mReading.set('img', img)
                    mReading.set('source_url', data['weixin_url'])
                    mReading.set('video_url', video_url)
                    mReading.set('ratio', ratio)
                    mReading.set('type', type)
                    mReading.set('category', '102')
                    mReading.save()
                    # print('save item')

def budejie_app_api():
    urls = []
    urls.append('http://s.budejie.com/topic/list/zuixin/1/budejie-android-6.6.6/0-20.json?market=360zhushou&ver=6.6.6&visiting=&os=6.0.1&appname=baisibudejie&client=android')
    urls.append('http://s.budejie.com/topic/tag-topic/164/hot/budejie-android-6.6.6/0-20.json?market=360zhushou&ver=6.6.6&visiting=&os=6.0.1&appname=baisibudejie&client=android')
    urls.append('http://s.budejie.com/topic/tag-topic/3176/hot/budejie-android-6.6.6/0-20.json?market=360zhushou&ver=6.6.6&visiting=&os=6.0.1&appname=baisibudejie&client=android')
    urls.append('http://s.budejie.com/topic/tag-topic/117/hot/budejie-android-6.6.6/0-20.json?market=360zhushou&ver=6.6.6&visiting=&os=6.0.1&appname=baisibudejie&client=android')
    urls.append('http://s.budejie.com/topic/tag-topic/3096/hot/budejie-android-6.6.6/0-20.json?market=360zhushou&ver=6.6.6&visiting=&os=6.0.1&appname=baisibudejie&client=android')
    urls.append('http://s.budejie.com/topic/list/remen/1/budejie-android-6.6.6/0-20.json?market=360zhushou&ver=6.6.6&visiting=&os=6.0.1&appname=baisibudejie&client=android')
    urls.append('http://s.budejie.com/topic/tag-topic/6513/hot/budejie-android-6.6.6/0-20.json?market=360zhushou&ver=6.6.6&visiting=&os=6.0.1&appname=baisibudejie&client=android')
    urls.append('http://d.api.budejie.com/topic/list/chuanyue/29/budejie-android-6.6.6/0-20.json?market=360zhushou&ver=6.6.6&visiting=&os=6.0.1&appname=baisibudejie&client=android')
    urls.append('http://s.budejie.com/topic/tag-topic/64/hot/budejie-android-6.6.6/0-20.json?market=360zhushou&ver=6.6.6&visiting=&os=6.0.1&appname=baisibudejie&client=android')
    urls.append('http://s.budejie.com/topic/tag-topic/3176/hot/budejie-android-6.6.6/0-20.json?market=360zhushou&ver=6.6.6&visiting=&os=6.0.1&appname=baisibudejie&client=android')
    urls.append('http://d.api.budejie.com/topic/recommend/budejie-android-6.6.6/0-20.json?market=360zhushou&ver=6.6.6&visiting=&os=6.0.1&appname=baisibudejie&client=android')
    urls.append('http://s.budejie.com/topic/list/jingxuan/41/budejie-android-6.6.6/0-20.json?market=360zhushou&ver=6.6.6&visiting=&os=6.0.1&appname=baisibudejie&client=android')
    urls.append('http://s.budejie.com/topic/list/jingxuan/1/budejie-android-6.6.6/0-20.json?market=360zhushou&ver=6.6.6&visiting=&os=6.0.1&appname=baisibudejie&client=android')
    for url in urls:
        req = requests.get(url)
        result = json.loads(req.text)
        # print len(result['list'])
        if len(result['list']) > 0:
            datas = result['list']
            for data in datas:
                if is_exit(data['text'].strip()) or is_source_exit(data['share_url']):
                    # print 'text exit and continue'
                    # print data['text'].strip()
                    continue
                else:
                    img = ''
                    video_url = ''
                    type = ''
                    ratio = 0.8
                    if data['type'] == 'image':
                        type = '1'
                        img = data['image']['big'][0]
                        ratio = float(data['image']['width']) / float(data['image']['height'])
                    elif data['type'] == 'text':
                        type = '5'
                        ratio = 1
                    elif data['type'] == 'gif':
                        type = '3'
                        img = data['gif']['images'][0]
                        ratio = float(data['gif']['width']) / float(data['gif']['height'])
                    elif data['type'] == 'video':
                        type = '4'
                        video_url = data['video']['video'][0]
                        img = data['video']['thumbnail'][0]
                        ratio = float(data['video']['width']) / float(data['video']['height'])
                    else:
                        # print data['type']+' not parse'
                        continue

                    if ratio < 0.08:
                        ratio = 0.8

                    # print type
                    # print data['share_url']
                    # print data['text'].strip()
                    # print img
                    # print video_url

                    Reading = Object.extend('Joke')
                    mReading = Reading()
                    mReading.set('text', data['text'].strip())
                    mReading.set('img', img)
                    mReading.set('source_url', data['share_url'])
                    mReading.set('video_url', video_url)
                    mReading.set('ratio', ratio)
                    mReading.set('type', type)
                    mReading.set('category', '102')
                    mReading.save()
                    # print('save item')

def qiushibaike_app_api():
    urls = []
    urls.append('http://circle.qiushibaike.com/video/recommend?count=30')
    urls.append('http://m2.qiushibaike.com/article/list/day?page=1&count=30')
    urls.append('http://m2.qiushibaike.com/article/list/imgrank?page=1&count=30')
    for url in urls:
        req = requests.get(url)
        result = json.loads(req.text)
        datas = []
        type = ''
        if result.has_key('items'):
            datas = result['items']
        elif result.has_key('data'):
            datas = result['data']
            type = '4'

        img = ''
        video_url = ''
        ratio = 0.8
        text = ''
        share_url = ''
        if len(datas) > 0:
            for data in datas:
                text = data['content']
                if type == '4':
                    share_url = data['video']['high_url']
                    img = data['video']['pic_url']
                else:
                    if data['format'] == 'image':
                        type = '1'
                        img = 'http:'+data['high_loc']
                        ratio = float(data['image_size']['m'][0]) / float(data['image_size']['m'][1])
                    elif data['format'] == 'word':
                        type = '5'
                        ratio = 0.8
                    else:
                        # print data['type']+' not parse'
                        continue

                if ratio < 0.08:
                    ratio = 0.8

                # print type
                # print share_url
                # print text
                # print img
                # print ratio
                # print video_url

                if type == '5':
                    if is_exit(text):
                        # print 'text exit and continue'
                        # print text
                        continue
                    else:
                        Reading = Object.extend('Joke')
                        mReading = Reading()
                        mReading.set('text', text)
                        mReading.set('img', img)
                        mReading.set('source_url', share_url)
                        mReading.set('video_url', video_url)
                        mReading.set('ratio', ratio)
                        mReading.set('type', type)
                        mReading.set('category', '101')
                        mReading.save()
                else:
                    if is_exit(text) or is_img_exit(img):
                        # print 'text exit and continue'
                        # print text
                        continue
                    else:
                        Reading = Object.extend('Joke')
                        mReading = Reading()
                        mReading.set('text', text)
                        mReading.set('img', img)
                        mReading.set('source_url', share_url)
                        mReading.set('video_url', video_url)
                        mReading.set('ratio', ratio)
                        mReading.set('type', type)
                        mReading.set('category', '101')
                        mReading.save()


def neihanduanzi():
    urls = []
    urls.append('http://lf.snssdk.com/neihan/stream/mix/v1/?mpic=1&webp=1&essence=1&content_type=-102&message_cursor=-1&count=30&screen_width=1080&double_col_mode=0&ac=wifi&channel=xiaomi&aid=7&app_name=joke_essay&version_code=614&version_name=6.1.4&device_platform=android&ssmix=a&device_type=Mi+Note+2&device_brand=Xiaomi&os_api=23&os_version=6.0.1&manifest_version_code=614')
    urls.append('http://lf.snssdk.com/neihan/stream/mix/v1/?mpic=1&webp=1&essence=1&content_type=-103&message_cursor=-1&count=30&screen_width=1080&double_col_mode=0&ac=wifi&channel=xiaomi&aid=7&app_name=joke_essay&version_code=614&version_name=6.1.4&device_platform=android&ssmix=a&device_type=Mi+Note+2&device_brand=Xiaomi&os_api=23&os_version=6.0.1&manifest_version_code=614')
    urls.append('http://lf.snssdk.com/neihan/stream/mix/v1/?mpic=1&webp=1&essence=1&content_type=-301&message_cursor=-1&count=30&screen_width=1080&double_col_mode=1&ac=wifi&channel=xiaomi&aid=7&app_name=joke_essay&version_code=614&version_name=6.1.4&device_platform=android&ssmix=a&device_type=Mi+Note+2&device_brand=Xiaomi&os_api=23&os_version=6.0.1&manifest_version_code=614')
    urls.append('http://lf.snssdk.com/neihan/stream/mix/v1/?mpic=1&webp=1&essence=1&content_type=-104&message_cursor=-1&count=30&screen_width=1080&double_col_mode=0&ac=wifi&channel=xiaomi&aid=7&app_name=joke_essay&version_code=614&version_name=6.1.4&device_platform=android&ssmix=a&device_type=Mi+Note+2&device_brand=Xiaomi&os_api=23&os_version=6.0.1&manifest_version_code=614')
    urls.append('http://lf.snssdk.com/neihan/stream/mix/v1/?mpic=1&webp=1&essence=1&content_type=-103&message_cursor=-1&count=30&screen_width=1080&double_col_mode=0&ac=wifi&channel=xiaomi&aid=7&app_name=joke_essay&version_code=612&version_name=6.1.2&device_platform=android&ssmix=a&device_type=Mi+Note+2&device_brand=Xiaomi&os_api=23&os_version=6.0.1&manifest_version_code=612')
    for url in urls:
        req = requests.get(url)
        result = json.loads(req.text)
        # print len(result['data']['data'])
        if len(result['data']['data']) > 0:
            datas = result['data']['data']
            for data in datas:
                if data['type'] == 5:
                    # print 'ad return'
                    continue

                if not data.has_key('group'):
                    continue

                if is_exit(data['group']['text'].strip()) or is_source_exit(data['group']['share_url']):
                    # print 'text exit and continue'
                    # print data['group']['text'].strip()
                    continue
                else:
                    img = ''
                    video_url = ''
                    type = ''
                    ratio = 0.8

                    if data['group']['media_type'] == 1:
                        type = '1'
                        img = data['group']['large_image']['url_list'][0]['url']
                        ratio = float(data['group']['large_image']['width']) / float(data['group']['large_image']['height'])
                    elif data['group']['media_type'] == 0:
                        type = '5'
                        ratio = 1
                    elif data['group']['media_type'] == 2:
                        type = '3'
                        img = data['group']['large_image']['url_list'][0]['url']
                        ratio = float(data['group']['large_image']['width']) / float(data['group']['large_image']['height'])
                    elif data['group']['media_type'] == 3:
                        type = '4'
                        video_url = data['group']['mp4_url']
                        img = data['group']['large_cover']['url_list'][0]['url']
                        ratio = 0.8
                    else:
                        # print str(data['type'])+' not parse'
                        continue

                    if ratio < 0.08:
                        ratio = 0.8

                    # print type
                    # print data['group']['share_url']
                    # print data['group']['text'].strip()
                    # print img
                    # print video_url

                    Reading = Object.extend('Joke')
                    mReading = Reading()
                    mReading.set('text', data['group']['text'].strip())
                    mReading.set('img', img)
                    mReading.set('source_url', data['group']['share_url'])
                    mReading.set('video_url', video_url)
                    mReading.set('ratio', ratio)
                    mReading.set('type', type)
                    mReading.set('category', '102')
                    mReading.save()
                    # print('save item')


def txapi():
    global sign
    for page in range(1,2):
        para = '&page=%s&num=20&rand=1' % (page)
        url = 'http://route.showapi.com/197-1'+ sign + para
        # print page
        # print url
        req = requests.get(url)
        # print req.text
        result = json.loads(req.text)
        if 0 == result['showapi_res_code']:
            newslist = result['showapi_res_body']['newslist']
            for data in newslist:
                if is_exit(data['title']):
                    # print 'exit and continue'
                    continue
                else:
                    # print data['title']
                    # print data['picUrl']
                    # print data['url']
                    ratio = getImageRatio(data['picUrl'])
                    if ratio == 5.5555:
                        continue
                    Reading = Object.extend('Joke')
                    mReading = Reading()
                    mReading.set('text', data['title'])
                    mReading.set('img', data['picUrl'])
                    mReading.set('ratio', ratio)
                    mReading.set('source_url', data['url'])
                    mReading.set('type', '1')
                    mReading.set('category', '103')
                    mReading.save()
                    # print('save item')

def huabanfuli():
    global sign
    # 34 37 39
    types = [34, 37, 39]
    for tyep in types:
        for page in range(1,2):
            para = '&page=%s&num=10&type=%s' % (page, tyep)
            url = 'http://route.showapi.com/819-1'+ sign + para
            # print url
            req = requests.get(url)
            # print req.text
            result = json.loads(req.text)
            if 0 == result['showapi_res_code']:
                for i in range(0,10):
                    data = result['showapi_res_body'][str(i)]
                    if is_exit(data['title']):
                        # print 'exit and continue'
                        continue
                    else:
                        # print data['title']
                        # print data['thumb']
                        # print data['url']
                        ratio = getImageRatio(data['thumb'])
                        Reading = Object.extend('Joke')
                        mReading = Reading()
                        mReading.set('text', data['title'])
                        mReading.set('img', data['thumb'])
                        mReading.set('ratio', ratio)
                        mReading.set('source_url', data['url'])
                        mReading.set('type', '1')
                        mReading.set('category', '103')
                        if ratio != 5.5555:
                            mReading.save()
                            # print('save item')

def getImageRatio(url):
    try:
        send_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20100101 Firefox/16.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Connection': 'keep-alive'
        }
        # print 'getImageRatio img:'+url
        # url = 'http://p1.pstatp.com/large/1926000458935a3fb296.webp'
        # url = 'http://wimg.spriteapp.cn/ugc/2017/03/26/58d728d9a6ace_1.jpg'
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

#category 101 搞笑; 102 段子; 103 美女;
#type 1 img; 2 imgs; 3 gif; 4 video; 5 text; 6 url, 7 mp3；
def getJokeTask():
    try:
        wenbenxiaohua()
    except:
        print 'except wenbenxiaohua'
        print traceback.format_exc()
    try:
        huabanfuli()
    except:
        print 'except huabanfuli'
        print traceback.format_exc()
    try:
        txapi()
    except:
        print 'except txapi'
        print traceback.format_exc()
    try:
        tupianxiaohua()
    except:
        print 'except tupianxiaohua'
        print traceback.format_exc()
    try:
        xiaohuadaquan_gif()
    except:
        print 'except xiaohuadaquan_gif'
        print traceback.format_exc()
    try:
        laifudaoxiaohua()
    except:
        print 'except laifudaoxiaohua'
        print traceback.format_exc()
    try:
        laifudaotupianxiaohua()
    except:
        print 'except laifudaotupianxiaohua'
        print traceback.format_exc()
    try:
        budejie()
    except:
        print 'except budejie'
        print traceback.format_exc()
    try:
        qiushibaike_app_api()
    except:
        print 'except budejie'
        print traceback.format_exc()
    try:
        neihanduanzi()
    except:
        print 'except budejie'
        print traceback.format_exc()
    try:
        budejie_app_api()
    except:
        print 'except budejie'
        print traceback.format_exc()

if __name__ == '__main__':
    getJokeTask()
