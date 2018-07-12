# -*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
import json
import leancloud
from leancloud import Object
from leancloud import Query
from datetime import *
import time
import re
import types
import traceback

leancloud.init('3fg5ql3r45i3apx2is4j9on5q5rf6kapxce51t5bc0ffw2y4', 'twhlgs6nvdt7z7sfaw76ujbmaw7l12gb8v6sdyjw1nzk9b1a')

def nowplaying_movies(url,publish_time):
    # url = 'http://www.hjenglish.com/new/p768394/'
    # url = 'http://www.hjenglish.com/new/p575854/'
    global source_name
    global category
    global type
    global item_id
    global category_2
    global type_name
    contents = ''
    media_url = ''
    img_url = ''
    headers = {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'}
    req = requests.get(url,headers=headers)
    req.encoding='utf-8'
    soup = BeautifulSoup(req.text,"html5lib")

    try:
        title = soup.find('h1',class_='title').text.strip()
        if u'秒杀攻略' in title or u'拼团好课' in title or u'优选好课' in title:
            return

        if is_exit(title):
            # print('already exit')
            return
        else:
            div = soup.find('div',class_='article-content')
            if div is None:
                # print 'content is none,div == none, return'
                return

            source = soup.find('div',class_='module module-breadcrumb')
            if source:
                source_text = source.text
                if u'英语听力' in source_text:
                    type_name = u'英语听力'
                    category = 'listening'
                elif u'英语考试' in source_text:
                    type_name = u'英语考试'  # 1010
                    category = 'examination'
                elif u'英语词汇' in source_text:
                    type_name = u'英语词汇'
                    category = 'word'
                elif u'英语口语' in source_text:
                    type_name = u'英语口语'
                    category = 'spoken_english'
                elif u'英语写作' in source_text:
                    type_name = u'英语写作'
                    category = 'composition'
                else:
                    type_name = u'英语阅读'
                    category = 'shuangyu_reading'

            if (u'.mp3' in req.text):
                if (u'soundFile=' in req.text):
                    media_start = req.text.index('soundFile=')
                    media_end = req.text.index('.mp3', media_start)
                    media_url = req.text[media_start + 10:media_end + 4]
                    type = 'mp3'
                elif (u'file=' in req.text):
                    media_start = req.text.index('file=')
                    media_end = req.text.index('.mp3', media_start)
                    media_url = req.text[media_start + 5:media_end + 4]
                    type = 'mp3'
                elif (u'son=' in req.text):
                    media_start = req.text.index('son=')
                    media_end = req.text.index('.mp3', media_start)
                    media_url = req.text[media_start + 4:media_end + 4]
                    type = 'mp3'

            img = div.select('p > img')
            if len(img) > 0:
                img_url = img[0]['src']
            type = 'text'
            for con in div.get_text().splitlines():
                if con is None:
                    pass
                elif u'扫二维码' in con or u'结合图片情景' in con or u'手机戳我直接进入' in con or u'声明' in con or u'新东方' in con or u'公开课' in con or u'别再错过' in con:
                    pass
                elif u'未能参与现场' in con or u'点击这里做听写' in con or u'HJPlayer' in con or u'6个励志' in con or u'名师指点' in con or u'帐号：' in con or u'号外号外' in con:
                    pass
                elif u'更多Quora神回答' in con or u'或手机直接访问' in con or u'沪江独家！' in con or u'您的浏览器' in con or u'求关注' in con or u'请关注' in con or u'开团' in con or u'购买' in con:
                    pass
                elif u'【Uni智能】' in con or u'戳图直达' in con or u'备考班' in con or u'戳我' in con or u'提升得分率' in con or u'优惠' in con or u'学班' in con or u'现价' in con:
                    pass
                elif u'戳我' in con or u'更多低价团' in con or u'优选好课' in con or u'更多关于' in con or u'精品课程' in con or u'直达班' in con:
                    pass
                elif u'相关热点' in con or u'英语君' in con or u'沪江网校' in con :
                    break
                elif len(con.strip()) == 0:
                    pass
                else:
                    contents += con.strip()
                    contents += '\n\n'

            contents = contents.strip()

            if len(contents) == 0:
                # print('contents is empty, return')
                return

            item_id += 1
            typeId = get_type_id(type_name)
            # print title
            # print item_id
            # print typeId
            # print type_name
            # print media_url
            # print img_url
            # print publish_time
            # print ('contents:\n' + contents)

            Composition = Object.extend('Reading')
            mComposition = Composition()
            mComposition.set('item_id', item_id)
            mComposition.set('title', title)
            mComposition.set('img_url', img_url)
            mComposition.set('img_type', 'url')
            mComposition.set('content', contents)
            mComposition.set('type_name', type_name)
            mComposition.set('publish_time', publish_time)
            mComposition.set('type_id', typeId)
            mComposition.set('source_url', url)
            mComposition.set('source_name', source_name)
            mComposition.set('category', category)
            mComposition.set('category_2', category_2)
            mComposition.set('type', type)
            mComposition.set('media_url', media_url)
            mComposition.save()
            # print('save item')
    except:
        print traceback.format_exc()
        # print url
        return

def get_type_id(type_name):
    return '1010'

def is_exit(str):
    global category
    query = Query('Reading')
    query.equal_to('title', str)
    query.equal_to('source_name', source_name)
    querys = query.find()
    return len(querys) > 0

def get_lastest_item_id():
    global source_name
    global category
    query = Query('Reading')
    query.equal_to('category', category)
    query.equal_to('source_name', source_name)
    query.descending("item_id")
    query.limit(1)
    querys = query.find()
    if len(querys) == 0:
        return 0
    else:
        return querys[0].get("item_id")

def get_all_link(url):
    global item_id
    headers = {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'}
    req = requests.get(url,headers=headers)
    req.encoding='utf-8'
    soup = BeautifulSoup(req.text,"html5lib")
    alist = soup.find_all('a', class_='big-link title-article')
    spans = soup.find_all('span', class_='col time')
    for i in range(len(alist)-1,-1,-1):
        href = alist[i]['href']
        publish_time = datetime.strptime(spans[i].text[0:16], "%Y-%m-%d %H:%M")
        url =  'http://www.hjenglish.com' + href
        # print url
        # print publish_time
        nowplaying_movies(url,publish_time)

item_id = 0
source_name = '沪江英语'
category = ''
category_2 = ''
type = 'text'
type_name = '英语阅读'

def task_jianghu_reading_spider():
    global item_id
    global category
    global category_2
    global type_name
    item_id = get_lastest_item_id()
    get_all_link("http://www.hjenglish.com/new/c1010")
    get_all_link("http://www.hjenglish.com/new/c1020")
    get_all_link("http://www.hjenglish.com/new/c1040")
    get_all_link("http://www.hjenglish.com/new/c1060")
    get_all_link("http://www.hjenglish.com/new/c1070")

if __name__ == '__main__':
    task_jianghu_reading_spider()




