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
import contentUtil
import re


leancloud.init('3fg5ql3r45i3apx2is4j9on5q5rf6kapxce51t5bc0ffw2y4', 'twhlgs6nvdt7z7sfaw76ujbmaw7l12gb8v6sdyjw1nzk9b1a')

def is_exit(str,url):
    global category
    query = Query('Reading')
    query.equal_to('title', str)
    query.equal_to('category', category)
    query.equal_to('source_url', url)
    querys = query.find()
    return len(querys) > 0

def is_category_exit(name):
    global category
    global level
    global code
    query = Query('SubjectList')
    query.equal_to('name', name)
    query.equal_to('category', category)
    querys = query.find()
    if len(querys) == 0:
        Composition = Object.extend('SubjectList')
        mComposition = Composition()
        mComposition.set('name', name)
        mComposition.set('category', category)
        mComposition.set('type', level)
        mComposition.set('level', level)
        mComposition.set('code', code)
        mComposition.save()
        print 'save SubjectList item'
    else:
        print len(querys)
        print 'SubjectList name exit'

def parse_detail(url):
    global source_name
    global category
    global type
    global item_id
    global category_2
    global type_name
    # url = 'http://www.tingclass.net/show-8418-400335-1.html'
    type = 'text'
    title = ''
    contents = ''
    img_url = ''
    img_urls = []
    media_url = ''
    lrc_url = ''
    publish_time = datetime.strptime('2019-05-01 08:00:00', "%Y-%m-%d %H:%M:%S")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'}
    req = requests.get(url, headers=headers)
    req.encoding = 'utf-8'
    if 'video.qq' in req.text or 'v.qq.com' in req.text or 'player.youku.com' in req.text \
            or 'player.video.qiyi.com' in req.text or 'player.pps.tv' in req.text or '.swf' in req.text:
        return False
    soup = BeautifulSoup(req.text, "html5lib")
    try:
        try:
            time_tag = soup.find_all('p',class_='fl p-left ml10')
            for ttag in time_tag:
                temp = ttag.text.strip()
                if u'年' in temp:
                    temp = temp.replace(u'年','-')
                    temp = temp.replace(u'月','-')
                    temp = temp.replace(u'日','')
                    publish_time = datetime.strptime(temp, "%Y-%m-%d")
        except:
            publish_time = datetime.strptime('2019-05-01 09:00:00', "%Y-%m-%d %H:%M:%S")

        try:
            mp4str = re.findall('http.*?\.mp4', req.text)
            if mp4str:
                media_url = mp4str[0]
                type = 'video'
            if len(media_url) == 0:
                mp4str = re.findall('http.*?\.f4v', req.text)
                if mp4str:
                    media_url = mp4str[0]
                    type = 'video'
        except:
            pass

        div_tag = soup.select('div.tit-class-con h1')
        if div_tag:
            title = div_tag[0].text.strip()

        mp3_tag = soup.find('div',id='mp3')
        if mp3_tag:
            media_url = mp3_tag.text.strip()
            type = 'mp3'

        content_tag = soup.find('div',class_='arti-con rel')
        if content_tag:
            contents = contentUtil.getTingclassContent(content_tag.text.strip())

        img_tags = soup.select('div.arti-con.rel img')
        for imgTag in img_tags:
            if imgTag.has_attr('src'):
                src = imgTag['src']
                if ('n1image.hjfile.cn' in src or 'tingclass' in src):
                    if 'statics/images/2014' not in src:
                        img_url = src
                        img_urls.append(src)

        if is_exit(title,url):
            pass
            print 'item exit'
        else:
            print title
            print img_url
            print img_urls
            print lrc_url
            print publish_time
            print media_url
            print source_name
            print category
            print type
            print category_2
            print type_name
            print contents
            Composition = Object.extend('Reading')
            mComposition = Composition()
            mComposition.set('title', title)
            mComposition.set('img_url', img_url)
            mComposition.set('img_urls', img_urls)
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
            print 'save item'
    except:
        print traceback.format_exc()
        print url
        return

def parse_page_num(url):
    isParseNext = True
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'}
    req = requests.get(url, headers=headers)
    req.encoding = 'utf-8'
    soup = BeautifulSoup(req.text, "html5lib")
    try:
        alinks = soup.select('ul.list-unit-1.list-qz > li > a.ell')
        for link in alinks:
            if link:
                print 'parse_title_list:' + link['href']
                isParseNext = parse_detail(link['href'])
    except:
        print traceback.format_exc()
        print url

    try:
        nextPages = soup.find_all('a',class_='a1 next')
        if len(nextPages) > 1:
            if nextPages[1].has_attr('href'):
                nextP = urlparse.urljoin(url, nextPages[1]['href'])
                print 'nextPage:'+ nextP
                parse_page_num(nextP)
    except:
        print traceback.format_exc()
        print url

def parse_category_list(url):
    global category_2
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'}
    req = requests.get(url, headers=headers)
    req.encoding = 'utf-8'
    soup = BeautifulSoup(req.text, "html5lib")
    try:
        alinks = soup.find_all('li',class_='ell')
        # print len(alinks)
        for link in alinks:
            nextLink = ''
            alink = link.find_all('a')
            if len(alink) > 1:
                nextLink = alink[1]['href']
                category_2 = alink[1].text
            elif len(alink) == 1:
                nextLink = alink[0]['href']
                category_2 = alink[0].text
            print nextLink
            print category_2
            is_category_exit(category_2)
            parse_page_num(nextLink)
    except:
        print traceback.format_exc()
        print url
        return


source_name = u'听力课堂'
category = u'shuangyu_reading'
type_name = ''
category_2 = ''
type = 'text'
level = '3'
code = '3'

def tingclass_spoken_english():
    global category
    global type_name
    global level
    global code
    category = u'spoken_english'
    type_name = u'启蒙英语'
    urls = []
    urls.append("http://www.tingclass.net/list-8381-1.html")
    urls.append("http://www.tingclass.net/list-36-1.html")
    urls.append("http://www.tingclass.net/list-5-1.html")
    urls.append("http://www.tingclass.net/list-8379-1.html")
    urls.append("http://www.tingclass.net/list-8380-1.html")
    urls.append("http://www.tingclass.net/list-8311-1.html")
    urls.append("http://www.tingclass.net/list-8312-1.html")
    for url in urls:
        parse_category_list(url)

def tingclass_doctor_english():
    global category
    global type_name
    global level
    global code
    category = u'spoken_english'
    type_name = u'生活大爆炸'
    urls = []
    # urls.append("http://www.tingclass.net/list-67-1.html")
    urls.append("http://www.tingclass.net/list-8598-1.html")
    for url in urls:
        parse_category_list(url)

def doTingclassTask():
    tingclass_doctor_english()



if __name__ == '__main__':
    doTingclassTask()