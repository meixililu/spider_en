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

leancloud.init('3fg5ql3r45i3apx2is4j9on5q5rf6kapxce51t5bc0ffw2y4', 'twhlgs6nvdt7z7sfaw76ujbmaw7l12gb8v6sdyjw1nzk9b1a')

def nowplaying_movies(url,publish_time):
    # url = 'http://www.en8848.com.cn//bec/kouyu/tiantianshuo/227471.html'
    global source_name
    global category
    global type
    global item_id
    global category_2
    global type_name
    contents = ''
    img_url = ''
    media_url = ''
    headers = {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'}
    req = requests.get(url,headers=headers)
    req.encoding='utf-8'
    soup = BeautifulSoup(req.text,"html5lib")

    try:
        if soup.find('div',class_='info-qh') != None and soup.find('div',id='articlebody') != None:
            if len(soup.find('div',id='articlebody').find_all('p')) > 0:
                div = soup.find('div',id='articlebody')
            else:
                div = soup.find('div',class_='info-qh')
        elif soup.find('div',class_='info-qh') != None:
            div = soup.find('div',class_='info-qh')
        elif soup.find('div',id='articlebody') != None:
            div = soup.find('div',id='articlebody')

        if div == None:
            # print('div == none, return')
            return

        size = len(div.find_all('p'))
        divsize = len(div.find_all('div'))
        # print len(div.text)
        # print div.text.strip()
        if size > 0:
            for i in range(0,size):
                con = div.find_all('p')[i].text
                if len(con) > 0:
                    tem = con.lstrip()
                    contents += tem
                    contents += '\n'
        elif divsize > 0:
            for i in range(0,divsize):
                con = div.find_all('div')[i].text
                if len(con) > 0:
                    tem = con.lstrip()
                    contents += tem
                    contents += '\n'


        if contents.strip() == '':
            if len(div.text) > 0:
                contents = re.sub(r'[\n]+',r'\n', div.text.strip(), flags=re.S)

        # print contents
        if contents.strip() == '':
            # print('contents is empty, return')
            return

        imgsize = len(div.find_all('img'))
        if imgsize > 0:
            img_url = 'http://www.en8848.com.cn/'+div.find_all('img')[0]['src']

        mp3div = soup.find('div',class_='jp-type-single')
        if mp3div != None:
            type = 'mp3'
            media_start = soup.text.index('mp3:"http:')
            media_end = soup.text.index('.mp3',media_start)
            media_url = soup.text[media_start+5:media_end+4]
            # print 'has mp3 player'
        else:
            type = 'text'


        # avi = soup.find('a',id='tempa')
        # if avi != None:
        #     media_url = avi['href']
        #     type = 'video'
        # else:
        #     type = 'text'

        title = soup.find('h1',id='toph1bt').text

        if is_exit(title):
            # print('already exit')
            return
        else:
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
        print 'exception'.encode('utf-8')
        # print url
        return

def get_type_id(type_name):
    return '1009'

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
    ulstr = soup.find_all('div', class_='ch_li_right')
    dates = soup.find_all('div', class_='ch_li_left')
    for i in range(0,len(ulstr)):
        href = 'http://www.en8848.com.cn/' + ulstr[i].find('a')['href']
        datestr = dates[i].text[-12:].strip()
        publish_time = datetime.strptime(datestr.lstrip(), "%Y-%m-%d")
        # print('catch url:' + href)
        # print publish_time
        nowplaying_movies(href,publish_time)

item_id = 0
source_name = '小e英语'
category = 'shuangyu_reading'
category_2 = ''
type = 'text'
type_name = ''

def task_en8848_story_spider():
    global item_id
    global category
    global type_name
    global category_2
    item_id = get_lastest_item_id();
    # print('item_id %d' % item_id)
    type_url = ''
    type0 = [('story',1),('proseessay',1),('culture',1),('poems',1),('jokes',1),('zc',1),('lyrics',1),('dlrw',1),('bi',1)]
    type1 = [('basic',1),('slang',1),('live',1),('use',1),('crazy',1),('learnfilm',1),('hangye',1),('brand',1),('fy',1)]
    type2 = [('primary',1),('speech',1),('voaspecial',1),('meiwen',1),('brand',1),('news',1),('program',1),('movietv',1)]
    type3 = [('kouyu',1),('ms',1)]
    type4 = [('kouyu',1),('waimao',1),('use',1),('write',1),('cihui',1)]
    for index in range(0,5):
        if index == 0:
            type_name = '英语阅读'
            type = type0
        elif index == 1:
            type_name = '英语口语'
            type = type1
        elif index == 2:
            type_name = '英语听力'
            type = type2
        elif index == 3:
            type_name = '职场英语'
            type = type3
        elif index == 4:
            type_name = '商务英语'
            type = type4

        for item in type:
            # for i in range(1,2):
            for i in range(item[1],0,-1):
                if index == 0:
                    type_url = 'read'
                    if item[0] == 'jokes':
                        category = 'jokes'
                    else:
                        category = 'shuangyu_reading'
                    category_2 = ''
                elif index == 1:
                    type_url = 'kouyu'
                    category = 'spoken_english'
                    category_2 = ''
                elif index == 2:
                    type_url = 'tingli'
                    category = 'listening'
                    category_2 = ''
                elif index == 3:
                    type_url = 'office'
                    category = 'spoken_english'
                    category_2 = ''
                elif index == 4:
                    type_url = 'bec'
                    if item[0] == 'write':
                        category = 'composition'
                    elif item[0] == 'cihui':
                        category = 'word'
                    else:
                        category = 'spoken_english'
                # print category
                if i == 1:
                    url = 'http://www.en8848.com.cn/%s/%s/index.html' % (type_url,item[0])
                else:
                    url = 'http://www.en8848.com.cn/%s/%s/index_%d.html'% (type_url,item[0],i)
                print('root url:'+url)
                get_all_link(url)


if __name__ == '__main__':
    task_en8848_story_spider()




