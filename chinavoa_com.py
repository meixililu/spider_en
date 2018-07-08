# -*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
import json
import leancloud
from leancloud import Object
from leancloud import Query
from datetime import datetime
from datetime import timedelta
import time
import re
import types
import traceback

leancloud.init('3fg5ql3r45i3apx2is4j9on5q5rf6kapxce51t5bc0ffw2y4', 'twhlgs6nvdt7z7sfaw76ujbmaw7l12gb8v6sdyjw1nzk9b1a')


def get_lastest_item_id():
    global source_name
    global category
    query = Query('Reading')
    query.descending("item_id")
    query.limit(1)
    querys = query.find()
    if len(querys) == 0:
        return 0
    else:
        return querys[0].get("item_id")

def is_exit(str):
    query = Query('Reading')
    query.equal_to('title', str)
    querys = query.find()
    return len(querys) > 0

def parse_page(url,publish_time):
    # print url
    global source_name
    global category
    global type
    global item_id
    global category_2
    global level
    global type_name
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'}
    req = requests.get(url, headers=headers)
    req.encoding = 'utf-8'
    soup = BeautifulSoup(req.text, "html5lib")
    # [s.extract() for s in soup('script')]
    imgTags = []
    title = ''
    mp3 = ''
    mp4 = ''
    media_url = ''
    content = ''
    exceptTime = 0
    try:
        mp4 = re.findall('http.*?\.mp4', req.text)[0]
    except:
        exceptTime+=1
        # print "has not mp4"

    # try:
    #     soup.find('textarea',id='lrc_content').clear()
    #     print 'remove lrc'
    # except:
    #     print 'do not has lrc'

    try:
        title = soup.find('h2').text
        if u'您要找？' in title:
            # print 'article do not exist'
            return
    except:
        exceptTime += 1
        # print 'has no title'
        # print traceback.format_exc()
        return
    try:
        contentTag = soup.find('div', class_='neirong clickCi')
        if contentTag:
            content = contentTag.text
            imgTags = contentTag.find_all('img')
        else:
            contentTag = soup.find('div', class_='neirong')
            if contentTag:
                content = contentTag.text
        content = getContent(content)
    except:
        exceptTime += 1
        # print 'has no content'
        # print traceback.format_exc()
        content = '请认真听！'

    try:
        mp3 = soup.find('audio', id='mediaPlayId')['m-src']
    except:
        exceptTime += 1
        mp3 = ''
        # print 'do not have mp3 file'

    try:
        category_2 = soup.select('a[style="color:#03C;"]')[0].text
    except:
        exceptTime += 1
        # print 'do not have category_2'

    imgs = []
    img = ''
    index = 0
    if len(mp4) > 0:
        type = 'video'
        media_url = mp4
    elif len(mp3) > 0:
        type = 'mp3'
        media_url = mp3
    else:
        type = 'text'
    for imgT in imgTags:
        srctemp = imgT.get('src','')
        imgs.append(srctemp)
        if index == 0:
            img = srctemp
        index+=1

    if len(media_url) == 0:
        # print 'has no media_url'
        if '.swf' in req.text:
            # print 'swf video return'
            return

        # return

    try:
        if is_exit(title):
            # print('already exit')
            return
        else:

            item_id += 1
            # print title
            # print item_id
            # print imgs
            # print img
            # print level
            # print type
            # print type_name
            # print category
            # print category_2
            # print media_url
            # print publish_time
            # print content

            Composition = Object.extend('Reading')
            mComposition = Composition()
            mComposition.set('item_id', item_id)
            mComposition.set('title', title)
            mComposition.set('img_url', img)
            mComposition.set('img_type', 'url')
            mComposition.set('content', content)
            mComposition.set('type_name', type_name)
            mComposition.set('publish_time', publish_time)
            mComposition.set('source_url', url)
            mComposition.set('source_name', source_name)
            mComposition.set('category', category)
            mComposition.set('level', level)
            mComposition.set('category_2', category_2)
            mComposition.set('type', type)
            mComposition.set('img_urls', imgs)
            mComposition.set('media_url', media_url)
            mComposition.save()
            # print('save item')
    except:
        # print traceback.format_exc()
        # print url
        return

def getContent(content):
    # content = filter_tags(content)
    content = content.replace(u'内容来自 听力课堂网：','')
    content = content.replace(u'用手机学英语，请加听力课堂微信公众号：tingclass123','')
    content = filter_tags(content)
    contents = ''
    for con in content.splitlines():
        if con.strip() is None:
            continue
        elif 'adsbygoogle = window.adsbygoogle' in con or u'内容来自' in con or 'link:' in con or 'Credit:' in con or 'Image:' in con or u'加载更多' in con or '$(".mp3-player")' in con or u'MP3下载' in con:
            continue
        elif u'更多内容' in con or '00:00' in con or u'下载' in con or u'查看全部' in con or u'点击单词' in con or '[ti:' in con or '[ar:' in con or '[la:' in con or '[by:' in con:
            continue
        elif con.strip().startswith('http'):
            continue
        elif u'本课学习方法(适合大多数会员)' in con or u'相关下载' in con or u'学习交流' in con or u'相关文章' in con or u'本课学习方法(适合大多数会员)' in con or u'查看完整回答' in con:
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

def filter_tags(htmlstr):
  #先过滤CDATA
  re_cdata=re.compile('//<!\[CDATA\[[^>]*//\]\]>',re.I) #匹配CDATA
  re_script=re.compile('<\s*script[^>]*>[^<]*<\s*/\s*script\s*>',re.I)#Script
  re_style=re.compile('<\s*style[^>]*>[^<]*<\s*/\s*style\s*>',re.I)#style
  re_br=re.compile('<br\s*?/?>')#处理换行
  re_h=re.compile('</?\w+[^>]*>')#HTML标签
  re_comment=re.compile('<!--[^>]*-->')#HTML注释
  re_http=re.compile('http://\S+')#HTML注释
  s=re_cdata.sub('',htmlstr)#去掉CDATA
  s=re_script.sub('',s) #去掉SCRIPT
  s=re_style.sub('',s)#去掉style
  s=re_br.sub('\n',s)#将br转换为换行
  s=re_h.sub('',s) #去掉HTML 标签
  s=re_comment.sub('',s)#去掉HTML注释
  s=re_http.sub('',s)#去掉http
  #去掉多余的空行
  blank_line=re.compile('\n+')
  s=blank_line.sub('\n',s)
  s=replaceCharEntity(s)#替换实体
  return s

def replaceCharEntity(htmlstr):
    CHAR_ENTITIES={'nbsp':' ','160':' ',
                    'lt':'<','60':'<',
                   'gt':'>','62':'>',
                   'amp':'&','38':'&',
                   'quot':'"','34':'"',}

    re_charEntity=re.compile(r'&#?(?P<name>\w+);')
    sz=re_charEntity.search(htmlstr)
    while sz:
        entity=sz.group()#entity全称，如>
        key=sz.group('name')#去除&;后entity,如>为gt
        try:
            htmlstr=re_charEntity.sub(CHAR_ENTITIES[key],htmlstr,1)
            sz=re_charEntity.search(htmlstr)
        except KeyError:
        #以空串代替
            htmlstr=re_charEntity.sub('',htmlstr,1)
            sz=re_charEntity.search(htmlstr)
    return htmlstr


def get_all_link(url):
    global item_id
    item_id = get_lastest_item_id();
    headers = {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'}
    req = requests.get(url,headers=headers)
    req.encoding='utf-8'
    soup = BeautifulSoup(req.text,"html5lib")
    dl = soup.find('dl', class_='block_con')
    if dl:
        dd = dl.find('dd')
        if dd:
            ul = dd.find('ul')
            if ul:
                alinks = ul.find_all('a')
                if alinks:
                    for link in alinks:
                        try:
                            time_str = link.find('span')
                            if time_str:
                                timeStr = '2017-' + time_str.text
                                publish_time = datetime.strptime(timeStr, "%Y-%m-%d")
                                parse_page(link['href'],publish_time)
                        except:
                            parse_page(link['href'], time.time())
                            # print 'no time'

def task_chinavoa_com():
    get_all_link('http://m.chinavoa.com/list-811-1.html')
    get_all_link('http://m.chinavoa.com/npr/')
    get_all_link('http://m.chinavoa.com/60_second_science/')
    get_all_link('http://m.chinavoa.com/cnn/')
    get_all_link('http://m.chinavoa.com/bbc/')
    get_all_link('http://m.chinavoa.com/list-8266-1.html')
    get_all_link('http://m.chinavoa.com/51voa/')


item_id = 0
source_name = '听力课堂'
category = 'listening'
type_name = '美国之音'
category_2 = ''
type = 'mp3'
level = '3'
code = 'voa'

if __name__ == '__main__':
    task_chinavoa_com()


