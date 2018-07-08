#!/usr/bin/env python
# -*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
import json
import leancloud
from leancloud import Object
from leancloud import Query
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import re
from datetime import *
import time
import traceback

leancloud.init('3fg5ql3r45i3apx2is4j9on5q5rf6kapxce51t5bc0ffw2y4', 'twhlgs6nvdt7z7sfaw76ujbmaw7l12gb8v6sdyjw1nzk9b1a')

def is_exit(str):
    global category
    query = Query('Reading')
    query.equal_to('title', str)
    query.equal_to('category', category)
    querys = query.find()
    return len(querys) > 0

def is_title_exit(title):
    query = Query('Reading')
    query.contains('title', title)
    querys = query.find()
    return len(querys) > 0

def get_lastest_item_id():
    global source_name
    global category
    query = Query('Reading')
    query.equal_to('category', category)
    query.descending("item_id")
    query.limit(1)
    querys = query.find()
    if len(querys) == 0:
        return 0
    else:
        return querys[0].get("item_id")

def nowplaying_movies(url,publish_time):
    global item_id
    global source_name
    global category
    global category_2
    global type
    global type_name
    global level
    global isContinue
    mp4_url = ''
    mp3_url = ''
    media_url = ''
    content = ''
    title = ''
    img_url = ''
    img_urls = []
    try:
        browser = webdriver.PhantomJS(executable_path='/root/phantomjs/bin/phantomjs')
        # browser = webdriver.PhantomJS(executable_path='/Users/luli/Downloads/phantomjs-2.1.1-macosx/bin/phantomjs')
        browser.set_page_load_timeout(20)
        browser.get(url)
        soup = BeautifulSoup(browser.page_source, "html5lib")
        time.sleep(10)

        contentInfo = soup.find('div',class_='contentInfo')
        if contentInfo:
            title_tag = contentInfo.find('p',class_='title')
            if title_tag:
                title = title_tag.text
            img = contentInfo.find('img',class_='contentImg')
            if img:
                img_url = img.get('src','')
                if len(img_url) > 5:
                    img_urls.append(img_url)

        if len(title) < 1:
            title_tag = soup.find('div', class_='titleBar')
            if title_tag:
                titlestr = title_tag.text
                if u'当前播放：' in titlestr:
                    title = titlestr.replace(u'当前播放：', '')

        if len(title) < 1:
            return

        article = soup.find('div', id='article')
        if article:
            content = article.text.strip()
            content = getContent(content)
        else:
            # print 'no content'
            pass

        mp3_urls = re.findall('http.*?\);', soup.text)
        if len(mp3_urls) > 0:
            mp3_url = mp3_urls[0]
            mp3_url = mp3_url[:-3]

        mp4_div = soup.find('video', class_='video')
        if mp4_div:
            mp4_url = mp4_div.get('src', '')

        if len(mp4_url) > 0:
            type = 'video'
            media_url = mp4_url
        elif len(mp3_url) > 0:
            type = 'mp3'
            media_url = mp3_url
        else:
            type = 'text'
    except:
        # print 'exception nowplaying_movies'
        # print traceback.format_exc()
        pass

    if is_exit(title):
        # print('already exit')
        isContinue = False
        return

    item_id += 1
    # print item_id
    # print title
    # print source_name
    # print type_name
    # print media_url
    # print category
    # print category_2
    # print img_url
    # print type
    # print level
    # print publish_time
    # print content

    Composition = Object.extend('Reading')
    mComposition = Composition()
    mComposition.set('item_id', item_id)
    mComposition.set('title', title)
    mComposition.set('img_url', img_url)
    mComposition.set('img_type', 'url')
    mComposition.set('content', content)
    mComposition.set('type_name', type_name)
    mComposition.set('publish_time', publish_time)
    mComposition.set('source_url', url)
    mComposition.set('source_name', source_name)
    mComposition.set('level', level)
    mComposition.set('category', category)
    mComposition.set('category_2', category_2)
    mComposition.set('type', type)
    mComposition.set('media_url', media_url)
    mComposition.save()
    # print('save item')


def getContent(content):
    # content = filter_tags(content)
    content = content.replace(u'内容来自 听力课堂网：','')
    content = content.replace(u'用手机学英语，请加听力课堂微信公众号：tingclass123','')
    # content = filter_tags(content)
    contents = ''
    for con in content.splitlines():
        if con.strip() is None:
            continue
        elif u'未能成功加载' in con or u'内容来自' in con or u'显示字幕' in con or 'Credit:' in con or 'Image:' in con or u'摘录一些自己喜欢的知识点' in con or '$(".mp3-player")' in con or u'MP3下载' in con:
            continue
        elif u'更多内容' in con or '0/0' in con or u'下载' in con or u'查看全部' in con or u'只显示' in con or u'视频字幕' in con or '[ar:' in con or '[la:' in con or '[by:' in con:
            continue
        elif con.strip().startswith('http'):
            continue
        elif u'译文' in con or u'相关下载' in con or u'学习交流' in con or u'相关文章' in con or u'本课学习方法(适合大多数会员)' in con or u'查看完整回答' in con:
            continue
        # elif u'金山词霸微信版开通啦' in con or u'点击进入' in con or u'专为' in con or u'您的浏览器' in con or u'求关注' in con or 'ijinshanciba' in con or u'帐号：' in con or u'号外号外' in con:
        #     pass
        elif len(con.strip()) == 0:
            continue
        else:
            contents += con.strip()
            contents += '\n\n'
    contents = contents.strip()

    return contents

def get_links(url):
    global isContinue
    rooturl = 'http://dict.eudic.net/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'}
    req = requests.get(url, headers=headers)
    req.encoding = 'utf-8'
    soup = BeautifulSoup(req.text, "html5lib")
    div = soup.find('div', class_='contents frap')
    if div:
        dls = div.find_all('dl')
        for dl in dls:
            alink = dl.find('a')

            if 'javascript:void' not in alink['href']:
                link = rooturl + alink['href']
                title = dl.find('dd',class_='title').text
                time = dl.find('span',class_='date')
                publish_time = datetime.strptime(time.text.strip(), "%Y-%m-%d")
                # print link
                if not is_title_exit(title):
                    nowplaying_movies(link,publish_time)
                else:
                    # print 'title exit'
                    break
                if not isContinue:
                    # print 'not continue'
                    break

def get_all_link(url):
    global isContinue
    rooturl = 'http://dict.eudic.net/ting/article?id='
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'}
    req = requests.get(url, headers=headers)
    req.encoding = 'utf-8'
    soup = BeautifulSoup(req.text, "html5lib")
    div = soup.find('div', class_='itemContent frap')
    if div is not None:
        dls = div.find_all('dl')
        for dl in dls:
            # print rooturl + dl['id']
            isContinue = True
            get_links(rooturl + dl['id'])

def get_root_link(url):
    global type_name
    global category_2
    rooturl = 'http://dict.eudic.net'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'}
    req = requests.get(url, headers=headers)
    req.encoding = 'utf-8'
    soup = BeautifulSoup(req.text, "html5lib")
    divs = soup.find_all('div', class_='inner_warp')
    cateName = soup.find('a',class_='cateName')
    if cateName:
        type_name = cateName.text
        category_2 = cateName.text

    if len(divs) > 0:
        for div in divs:
            atags = div.find_all('a')
            if len(atags) > 0:
                for atag in atags:
                    # print (rooturl + atag['href'])
                    get_all_link(rooturl + atag['href'])


isContinue = True
item_id = 0
source_name = '每日英语听力'
category = 'listening'
category_2 = ''
type = 'mp3'
type_name = '英语听力'
level = '3'

def task_dict_education():
    global item_id
    item_id = get_lastest_item_id()
    # url = 'http://dict.eudic.net/ting/channel?id=aef14d58-2ae4-404b-9581-8e7863e0f059&type=category'
    # url = 'http://dict.eudic.net/ting/channel?id=6d1b756a-3ffc-11e5-83e4-000c29ffef9b&type=tag'
    # get_all_link(url)
    # nowplaying_movies('http://dict.eudic.net/webting/desktopplay?id=fcb7e57f-7cc0-11e7-bbeb-000c29ffef9b&token=QYN+eyJ0b2tlbiI6IiIsInVzZXJpZCI6IiIsInVybHNpZ24iOiJOdE44VzlGK3YzWUpjaTJ0a3Z2OHZldVE4eHM9IiwidCI6IkFCSU1UVXlNakUxTmpFNE1nPT0ifQ%3D%3D','')
    # nowplaying_movies('http://dict.eudic.net/webting/desktopplay?id=46fa19d5-7d6e-11e7-931d-e0dd755ac385&token=QYN+eyJ0b2tlbiI6IiIsInVzZXJpZCI6IiIsInVybHNpZ24iOiI2ZU9xYjNHRkxGZ3g5YjVwM1FCNTFKVGxLSDg9IiwidCI6IkFCSU1UVXlNakU1TVRjMU5RPT0ifQ%3D%3D','')
    # nowplaying_movies('http://dict.eudic.net/ting')

    get_root_link('http://dict.eudic.net/ting/channel?id=6d1b756a-3ffc-11e5-83e4-000c29ffef9b&type=tag')


if __name__ == '__main__':
    task_dict_education()



