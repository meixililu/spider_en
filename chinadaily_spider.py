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


def is_exit(url):
    global category
    query = Query('Reading')
    query.equal_to('category', category)
    query.equal_to('source_url', url)
    querys = query.find()
    return len(querys) > 0

def parse_detail(url,img_url):
    global source_name
    global category
    global type
    global item_id
    global category_2
    global type_name
    type = 'text'
    title = ''
    contents = ''
    img_urls = []
    media_url = ''
    lrc_url = ''
    publish_time = datetime.strptime('2019-05-01 08:00:00', "%Y-%m-%d %H:%M:%S")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'}
    req = requests.get(url, headers=headers)
    # req.encoding = 'utf-8'
    soup = BeautifulSoup(req.text, "html5lib")
    try:
        try:
            time_tag = soup.find('p',class_='main_title3')
            if time_tag:
                timeStr = time_tag.text.strip()
                result = re.search('\d+.+',timeStr)
                timeStr = result.group()
                publish_time = datetime.strptime(timeStr, "%Y-%m-%d %H:%M")
                # print publish_time
        except:
            # print traceback.format_exc()
            publish_time = datetime.strptime('2019-05-01 09:00:00', "%Y-%m-%d %H:%M:%S")

        mp3_tag = soup.find('audio')
        if mp3_tag:
            media_url = urlparse.urljoin(url,mp3_tag['src'])
            type = 'mp3'

        title_tag = soup.find('span',class_='main_title1')
        if title_tag:
            title = title_tag.text.strip()
        content_tag = soup.find('div',id='Content')
        if content_tag:
            contents = contentUtil.getTingclassContent(content_tag.text.strip())

        img_urls.append(img_url)
        img_tags = content_tag.find_all('img')
        if img_tags:
            for imgTag in img_tags:
                if imgTag.has_attr('src'):
                    src = urlparse.urljoin(url,imgTag['src'])
                    img_urls.append(src)
    #
        if is_exit(url):
            pass
            # print 'item exit'
        else:
            # print title
            # print img_url
            # print img_urls
            # print lrc_url
            # print publish_time
            # print media_url
            # print source_name
            # print category
            # print type
            # print category_2
            # print type_name
            # print contents
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
            # print 'save item'
    except:
        # print traceback.format_exc()
        # print url
        return



def parse_category_list(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'}
    req = requests.get(url, headers=headers)
    req.encoding = 'utf-8'
    soup = BeautifulSoup(req.text, "html5lib")
    try:
        divTags = soup.find_all('div',class_='gy_box')
        # print len(alinks)
        for div in divTags:
            detail = ''
            imgUrl = ''
            imgTag = div.find('img')
            alink = div.find('a')
            if imgTag:
                imgUrl = urlparse.urljoin(url,imgTag['src'])
            if alink:
                detail = urlparse.urljoin(url,alink['href'])
                # print detail
                parse_detail(detail,imgUrl)
    except:
        pass
        # print traceback.format_exc()
        # print url

    # try:
    #     nextLinks = soup.find_all('a',class_='pagestyle')
    #     for link in nextLinks:
    #         if link:
    #             if 'Next' in link.text:
    #                 nextLink = urlparse.urljoin(url,link['href'])
    #                 print nextLink
    #                 parse_category_list(nextLink)
    #                 return
    # except:
    #     print traceback.format_exc()
    #     print url


source_name = u'英语点津'
category = u'shuangyu_reading'
type_name = ''
category_2 = ''
type = 'text'
level = '1'
code = ''

def chinadaily_task():
    global category
    global type_name
    global level
    global code
    category = u'shuangyu_reading'
    type_name = u'双语阅读'
    urls = []
    urls.append("https://language.chinadaily.com.cn/news_bilingual/")
    urls.append("https://language.chinadaily.com.cn/audio_cd/")
    urls.append("https://language.chinadaily.com.cn/news_hotwords/")
    urls.append("https://language.chinadaily.com.cn/trans_collect/")
    urls.append("https://language.chinadaily.com.cn/columnist/")
    urls.append("https://language.chinadaily.com.cn/5af95d44a3103f6866ee845c/")
    urls.append("https://language.chinadaily.com.cn/englishexams/")
    for url in urls:
        if 'news_bilingual' in url:
            category = u'shuangyu_reading'
            type_name = u'双语阅读'
        elif 'audio_cd' in url:
            category = u'listening'
            type_name = u'英语听力'
        elif 'englishexams' in url:
            category = u'examination'
            type_name = u'英语考试'
        elif 'news_hotwords' in url or 'trans_collect' in url:
            category = u'word'
            type_name = u'新闻热词'
        else:
            category = u'shuangyu_reading'
            type_name = u'双语阅读'
        parse_category_list(url)


if __name__ == '__main__':
    chinadaily_task()