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
from selenium import webdriver
import traceback

leancloud.init('3fg5ql3r45i3apx2is4j9on5q5rf6kapxce51t5bc0ffw2y4', 'twhlgs6nvdt7z7sfaw76ujbmaw7l12gb8v6sdyjw1nzk9b1a')

def get_lastest_item_id():
    query = Query('Reading')
    query.descending("item_id")
    query.limit(1)
    querys = query.find()
    if len(querys) == 0:
        return 0
    else:
        return querys[0].get("item_id")

def is_exit(str):
    global category
    query = Query('Reading')
    query.equal_to('title', str)
    query.equal_to('category', category)
    querys = query.find()
    return len(querys) > 0

def list(url):
    global category
    req = requests.get(url)
    result = json.loads(req.text)
    item_id = get_lastest_item_id()
    for card in result['cards']:
        # print '------------'
        publish_time = datetime.strptime(str(card['startTime']), "%Y%m%d%H%M")
        if u'有道精品课' in card['type']:
            return

        if card['media'] == 'VIDEO':
            # print card['title'].encode('utf-8')
            # print card['type'].encode('utf-8')
            # print card['url'].encode('utf-8')
            # print card['image'][0].encode('utf-8')
            # print card['videourl'].encode('utf-8')
            # print publish_time

            if is_exit(card['title']):
                # print 'exit'
                continue
            else:
                item_id += 1
                content = u'\n\n\n\n来源:%s\n\n\n\n' % (card['type'])
                Reading = Object.extend('Reading')
                mReading = Reading()
                mReading.set('item_id', item_id)
                mReading.set('title', card['title'])
                mReading.set('img_url', card['image'][0])
                mReading.set('img_urls', card['image'])
                mReading.set('img_type', 'url')
                mReading.set('content', content)
                mReading.set('type_name', u'英语学习')
                mReading.set('publish_time', publish_time)
                mReading.set('type_id', '')
                mReading.set('source_url', card['url'])
                mReading.set('source_name', u'有道英语')
                mReading.set('category', category)
                mReading.set('media_url', card['videourl'])
                mReading.set('type', 'video')
                mReading.save()
                # print('save item')
        else:
            parseYoudaoWebPage(card['url'], item_id, publish_time, card['media'], card['audiourl'])


def parseYoudaoWebPage(url,item_id,publish_time,media,audiourl):
    global category
    # print 'parseYoudaoWebPage:%s'%(url)
    browser = webdriver.PhantomJS(executable_path='/root/phantomjs/bin/phantomjs')
    browser.get(url)
    time.sleep(3)
    item_id += 1
    Reading = Object.extend('Reading')
    mReading = Reading()
    mReading.set('item_id', item_id)
    mReading.set('img_type', 'url')
    mReading.set('type_name', u'英语学习')
    mReading.set('publish_time', publish_time)
    mReading.set('type_id', '')
    mReading.set('source_url', url)
    mReading.set('source_name', u'有道英语')
    mReading.set('category', category)
    if media == 'AUDIO':
        mReading.set('type', 'mp3')
        if len(audiourl) > 10:
            mReading.set('media_url', audiourl)
        else:
            try:
                mp3_div = browser.find_element_by_css_selector('div.audio-play-btn.new-audio')
                mp3_url = mp3_div.get_attribute('src')
                # print 'mp3_url:' + mp3_url
                if mp3_url is not None:
                    mReading.set('media_url', mp3_url)
            except:
                print traceback.format_exc()
                # print 'has not mp3_div---div.audio-play-btn.new-audio'


    else:
        mReading.set('media_url', "")
        mReading.set('type', 'text')

    try:
        title = browser.find_element_by_css_selector('h1#heading')
        summary = browser.find_element_by_css_selector('div.summary')
        content = browser.find_element_by_css_selector('div#article')
        imgs = content.find_elements_by_tag_name('img')
        if u'有道原创'in summary.text:
            # print '有道原创禁止转载'
            return

        if is_exit(title.text):
            # print 'exit'
            return

        if len(title.text) == 0:
            return

        contents = getContent(content.text)
        if contents is None:
            return

        images = []
        for item in imgs:
            if 'shared' not in item.get_attribute('src'):
                images.append(item.get_attribute('src'))

        # print title.text.encode('utf-8')
        # print summary.text.encode('utf-8')
        # print images
        # print contents.encode('utf-8')
        image = ''
        if len(images) > 0:
            image = images[0]

        mReading.set('title', title.text)
        mReading.set('img_url', image)
        mReading.set('img_urls', images)
        mReading.set('content', contents)
        mReading.save()
        # print('save item')

    except:
        print traceback.format_exc()
        # print '-------------'
        try:
            title = browser.find_element_by_xpath("//div[@class='figure']/h1")
            content = browser.find_element_by_css_selector('div.content.preview-img-container')
            imgs = content.find_elements_by_tag_name('img')
            contents = getContent(content.text)
        except:
            return

        if is_exit(title.text):
            # print 'exit'
            return

        if len(title.text) == 0:
            return

        if contents is None:
            return

        if media == 'AUDIO':
            mReading.set('type', 'mp3')
            if len(audiourl) > 10:
                mReading.set('media_url', audiourl)
            else:
                try:
                    mp3_div = browser.find_element_by_css_selector('div.audio-play-strip.icon-playing')
                    mp3_url = mp3_div.get_attribute('src')
                    # print 'mp3_url:'+mp3_url
                    if mp3_url is not None:
                        mReading.set('media_url', mp3_url)
                except:
                    print traceback.format_exc()
                    # print 'has not mp3_div---div.audio-play-strip.icon-playing'


        images=[]
        for item in imgs:
             if 'shared' not in item.get_attribute('src'):
                images.append(item.get_attribute('src'))


        # print title.text.encode('utf-8')
        # print images
        # print contents.encode('utf-8')
        image = ''
        if len(images) > 0:
            image = images[0]

        mReading.set('title', title.text)
        mReading.set('img_url', image)
        mReading.set('img_urls', images)
        mReading.set('content', contents)
        mReading.save()
        # print('save item')




def getContent(content):
    contents = ''
    for con in content.splitlines():
        if con is None:
            continue
        elif u'摄影' in con or u'编辑：' in con or 'link:' in con or 'Credit:' in con or 'Image:' in con or u'本文系有道词典原创内容' in con or u'本文内容系版权作者合法授权有道词典转载' in con or '00:00' in con:
            continue
        elif u'主持人介绍' in con or u'【单词卡】' in con or u'老外粉丝福利：' in con or u'快快留言' in con or u'有道词典首页' in con or u'查看完整回答' in con:
            continue
        # elif u'金山词霸微信版开通啦' in con or u'点击进入' in con or u'专为' in con or u'您的浏览器' in con or u'求关注' in con or 'ijinshanciba' in con or u'帐号：' in con or u'号外号外' in con:
        #     pass
        elif len(con) == 0:
            continue
        else:
            contents += con.strip()
            contents += '\n\n'
    contents = contents.strip()

    return contents


lastId = 0
category = 'shuangyu_reading'

def task_youdaoapp():
    # video
    list('http://dict.youdao.com/infoline/list?client=mobile&lastId=0&mode=publish&entranceId=37&keyfrom=mdict.7.2.0.android&model=MI_5&mid=6.0.1&imei=867861047382482&vendor=youdaoweb&screen=1080x1920&ssid=fbdsfls&network=wifi&abtest=3')
    # web
    list('http://dict.youdao.com/infoline/list?client=mobile&lastId=0&mode=publish&entranceId=35&keyfrom=mdict.7.2.0.android&model=MI_5&mid=6.0.1&imei=861069127869242&vendor=youdaoweb&screen=1080x1920&ssid=coffese&network=wifi&abtest=3')
    # 英乐
    list('http://dict.youdao.com/infoline/list?client=mobile&lastId=0&mode=publish&entranceId=33&keyfrom=mdict.7.2.0.android&model=Mi_Note_2&mid=6.0.1&imei=869782023526463&vendor=xiaomi&screen=1080x1920&ssid=405&network=wifi&abtest=2')
    # 听说
    list('http://dict.youdao.com/infoline/list?client=mobile&lastId=0&mode=publish&entranceId=31&keyfrom=mdict.7.2.0.android&model=Mi_Note_2&mid=6.0.1&imei=878635269202463&vendor=xiaomi&screen=1080x1920&ssid=disdsdsd&network=wifi&abtest=2')
    # 科普
    list('http://dict.youdao.com/infoline/list?client=mobile&lastId=0&mode=publish&entranceId=48&keyfrom=mdict.7.2.0.android&model=Mi_Note_2&mid=6.0.1&imei=868209715726463&vendor=xiaomi&screen=1080x1920&ssid=8888888&network=wifi&abtest=2')
    # 趣味
    list('http://dict.youdao.com/infoline/list?client=mobile&lastId=0&mode=publish&entranceId=2&keyfrom=mdict.7.2.0.android&model=Mi_Note_2&mid=6.0.1&imei=869023527825353&vendor=xiaomi&screen=1080x1920&ssid=ljdsdsd888&network=wifi&abtest=2')

if __name__ == '__main__':
    task_youdaoapp()