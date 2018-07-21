# -*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
import leancloud
from leancloud import Object
from leancloud import Query
from datetime import *
import time
import traceback
import urlparse


leancloud.init('3fg5ql3r45i3apx2is4j9on5q5rf6kapxce51t5bc0ffw2y4', 'twhlgs6nvdt7z7sfaw76ujbmaw7l12gb8v6sdyjw1nzk9b1a')



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

def is_exit(str,url,lrc_url):
    global category
    query = Query('Reading')
    query.equal_to('title', str)
    query.equal_to('category', category)
    query.equal_to('source_url', url)
    querys = query.find()
    # if len(querys) > 0:
    #     data = querys[0]
    #     data.set('lrc_url',lrc_url)
    #     data.save()
    #     print 'update success'

    return len(querys) > 0

def parse_detail(url):
    global source_name
    global category
    global type
    global item_id
    global category_2
    global type_name
    title = ''
    contents = ''
    media_url = ''
    publish_time = ''
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'}
    req = requests.get(url, headers=headers)
    req.encoding = 'utf-8'
    soup = BeautifulSoup(req.text, "html5lib")
    try:
        div_tag = soup.find('div',id='title')
        if len(div_tag) > 0:
            for (index,child) in enumerate(div_tag.children):
                if index == 0:
                    title = child.text.strip()
                else:
                    time_str = child.text.strip()
                    if '-' in time_str:
                        publish_time = datetime.strptime(time_str, "%Y-%m-%d")
                    elif '/' in time_str:
                        publish_time = datetime.strptime(time_str, "%m/%d/%Y")
        content_tag = soup.select('div#txt > li')
        if len(content_tag) > 0:
            for child in content_tag:
                contents += child.text
                contents += "\n\n"


        lrc_url=''
        lrc_tag = soup.find('a',id='btndl-lrc')
        if lrc_tag:
            lrc_url = urlparse.urljoin(url, lrc_tag['href'])
        mp3_tag = soup.find('a',id='btndl-mp3')
        if mp3_tag:
            media_url = urlparse.urljoin(url, mp3_tag['href'])
            type = 'mp3'


        # print title
        # print lrc_url
        # print media_url
        # print publish_time
        # print contents

        item_id = get_lastest_item_id() + 1;
        if is_exit(title,url,lrc_url):
            pass
            # print 'item exit'
        else:
            Composition = Object.extend('Reading')
            mComposition = Composition()
            mComposition.set('item_id', item_id)
            mComposition.set('title', title)
            mComposition.set('img_url', '')
            mComposition.set('img_type', 'url')
            mComposition.set('content', contents)
            mComposition.set('type_name', type_name)
            mComposition.set('publish_time', publish_time)
            mComposition.set('type_id', '')
            mComposition.set('source_url', url)
            mComposition.set('source_name', source_name)
            mComposition.set('category', category)
            mComposition.set('category_2', category_2)
            mComposition.set('lrc_url', lrc_url)
            mComposition.set('type', type)
            mComposition.set('media_url', media_url)
            mComposition.save()
            # print('save item mp3')

        title = title + u' 视频'
        if is_exit(title,url,lrc_url):
            return

        mp4_tag = soup.find('a', id='btndl-mp4')
        if mp4_tag:
            media_url = urlparse.urljoin(url, mp4_tag['href'])
            type = 'video'
        # print media_url
        item_id += 1

        Composition = Object.extend('Reading')
        mComposition = Composition()
        mComposition.set('item_id', item_id)
        mComposition.set('title', title)
        mComposition.set('img_url', '')
        mComposition.set('img_type', 'url')
        mComposition.set('content', contents)
        mComposition.set('type_name', type_name)
        mComposition.set('publish_time', publish_time)
        mComposition.set('type_id', '')
        mComposition.set('source_url', url)
        mComposition.set('source_name', source_name)
        mComposition.set('category', category)
        mComposition.set('category_2', category_2)
        mComposition.set('lrc_url', lrc_url)
        mComposition.set('type', type)
        mComposition.set('media_url', media_url)
        mComposition.save()
        # print('save item mp4')

    except:
        # print traceback.format_exc()
        # print url
        return

def parse_list(url):
    global category_2
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'}
    req = requests.get(url, headers=headers)
    req.encoding = 'utf-8'
    soup = BeautifulSoup(req.text, "html5lib")
    try:
        lis = soup.select('div#listall > ul > li')
        # print len(lis)
        for li in lis:
            span_tag = li.find('span')
            if span_tag:
                category_2 = span_tag.text
            a_tag = li.find_all('a')
            if len(a_tag) > 1:
                url = 'http://www.voase.cn' + a_tag[1]['href']
                # print url
                parse_detail(url)

    except:
        # print traceback.format_exc()
        # print url
        return


item_id = 0
source_name = u'VOA慢速英语精听网'
category = u'listening'
type_name = u'英语精听'
category_2 = ''
type = 'text'

def task_voase_cn():
    url = ''
    for i in range(1,2):
        if i == 1:
            url = 'http://www.voase.cn/index.htm'
        else:
            url = 'http://www.voase.cn/index-%d.htm' % (i)
        # print url
        parse_list(url)


if __name__ == '__main__':
    task_voase_cn()