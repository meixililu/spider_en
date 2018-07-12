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

def nowplaying_movies(url,img_url):
    # url = 'http://news.iciba.com/study/bilingual/1538012.shtml'
    global source_name
    global category
    global type
    global item_id
    global category_2
    global type_name
    contents = ''
    media_url = ''
    publish_time = ''
    headers = {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'}
    req = requests.get(url,headers=headers)
    req.encoding='utf-8'
    soup = BeautifulSoup(req.text,"html5lib")

    try:
        title = soup.find('p',class_='title1 f-f0').text
        if is_exit(title):
            print('already exit')
            return
        else:
            timestr = soup.find('p',class_='art_time').text
            publish_time = datetime.strptime(timestr.strip(), "%Y-%m-%d %H:%M")
            div = soup.find('div',class_='air_con f-f0')
            if div is None:
                # print 'content is none,div == none, return'
                return

            img = div.find('img')
            if img is not None:
                img_url = img['src']

            contentp = div.find_all('p')
            for conp in contentp:
                con = conp.get_text().strip()
                if con is None:
                    pass
                elif u'来源' in  con or u'爱语吧作者' in con or u'请勿转载' in con or u'完成阅读' in con or u'编辑' in con or u'公开课' in con or u'推荐' in con or u'别再错过' in con:
                    pass
                # elif u'未能参与现场' in  con or u'想参与' in con or u'【新东方在线】' in con or u'您的浏览器' in con or u'求关注' in con or 'ijinshanciba' in con or u'帐号：' in con or u'号外号外' in con:
                #     pass
                # elif u'金山词霸微信版开通啦' in  con or u'点击进入' in con or u'专为' in con or u'您的浏览器' in con or u'求关注' in con or 'ijinshanciba' in con or u'帐号：' in con or u'号外号外' in con:
                #     pass
                elif len(con) == 0:
                    pass
                else:
                    contents += con.strip()
                    contents += '\n\n'
            contents = contents.strip()

            if contents == '':
                # print('contents is empty, return')
                return


            # mp3div = soup.find('input',id='mp_')
            # if mp3div is not None:
            #     type = 'mp3'
            #     media_url = "http://news.iyuba.com/"+mp3div['value']
            # else:
            #     type = 'text'

            item_id += 1
            typeId = get_type_id(type_name)
            print title
            print item_id
            print typeId
            print type_name
            print media_url
            print img_url
            print publish_time
            print ('contents:\n' + contents)

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
            # mComposition.save()
            # print('save item')
    except:
        print traceback.format_exc()
        # print url
        return

def get_type_id(type_name):

    return '1016'

def is_exit(str):
    global category
    query = Query('Reading')
    query.equal_to('title', str)
    query.equal_to('category', category)
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
    ul = soup.find('ul',id='li_list')
    alinks = ul.find_all('a')
    for i in range(len(alinks)-1,-1,-1):
        href = alinks[i].get('href')
        print 'catch url:' + href
        nowplaying_movies(href,'')

item_id = 0
source_name = '新东方网'
category = 'shuangyu_reading'
type_name = '英语阅读'
category_2 = ''
type = 'text'

def task_www_yingyu_xdf_cn():
    global item_id
    global category
    global category_2
    global type_name
    item_id = get_lastest_item_id();
    # print('item_id %d' % item_id)
    urls = {"http://yingyu.xdf.cn/list_907_1.html",
            "http://yingyu.xdf.cn/list_1799_1.html",
            "http://yingyu.xdf.cn/list_6128_1.html",
            "http://yingyu.xdf.cn/list_6122_1.html",

            "http://yingyu.xdf.cn/list_903_1.html",
            "http://yingyu.xdf.cn/list_2458_1.html",

            "http://yingyu.xdf.cn/list_1793_1.html",
            "http://yingyu.xdf.cn/list_904_1.html",
            "http://yingyu.xdf.cn/list_1794_1.html"
            }
    for url in urls:
        if "list_1793_1" in url or "list_904_1" in url or "list_1794_1" in url:
            category = 'word'
            type_name = '英语词汇'
        elif "list_903_1" in url or "list_2458_1" in url:
            category = 'spoken_english'
            type_name = '英语口语'
        else:
            category = 'shuangyu_reading'
            type_name = '英语阅读'

        get_all_link(url)


if __name__ == '__main__':
    task_www_yingyu_xdf_cn()




