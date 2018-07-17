# -*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
import json
import leancloud
from leancloud import Object
from leancloud import Query
from datetime import *
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
    global type_name
    query = Query('Reading')
    # query.equal_to('title', str)
    query.equal_to('source_url', str)
    querys = query.find()
    # if len(querys) > 0:
    #     data = querys[0]
    #     data.set('type_name', type_name)
    #     data.set('category', category)
    #     data.save()
    #     print 'update success'

    return len(querys) > 0



def detail(url,title,publish_time,img_url,small_img):
    try:
        # headers = {
        #     'User-Agent': 'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Mobile Safari/537.36'}
        # dcap = dict(DesiredCapabilities.PHANTOMJS)
        # dcap["phantomjs.page.settings.userAgent"] = (
        #     "Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Mobile Safari/537.36"
        # )
        #
        # # browser = webdriver.PhantomJS(executable_path='/root/phantomjs/bin/phantomjs')
        # browser = webdriver.PhantomJS(executable_path='/Users/luli/Downloads/phantomjs-2.1.1-macosx/bin/phantomjs', desired_capabilities=dcap)
        # # browser = webdriver.PhantomJS(executable_path='/Users/luli/Downloads/phantomjs-2.1.1-macosx/bin/phantomjs')
        # browser.implicitly_wait(1)
        # browser.get(url)
        #
        # soup = BeautifulSoup(browser.page_source, "html5lib")
        # media_url = ''
        # print browser.current_url
        global category
        global type_name

        if is_exit(url):
            print 'url is exit'
            return

        # sourceTag = soup.find('source')
        # if sourceTag:
        #     media_url = sourceTag['src']
        #     print media_url

        item_id = get_lastest_item_id()

        Composition = Object.extend('Reading')
        mComposition = Composition()
        mComposition.set('item_id', item_id)
        mComposition.set('title', title)
        mComposition.set('img_url', img_url)
        mComposition.set('small_img', small_img)
        mComposition.set('img_type', 'url')
        mComposition.set('content', "")
        mComposition.set('content_type', "url")
        mComposition.set('type_name', type_name)
        mComposition.set('publish_time', publish_time)
        mComposition.set('source_url', url)
        mComposition.set('source_name', u"今日头条")
        mComposition.set('level', "")
        mComposition.set('category', category)
        mComposition.set('category_2', "")
        mComposition.set('type', "video")
        mComposition.set('media_url', "")
        mComposition.save()
        print('save item')
    except:
        print 'exception detail'
        print traceback.format_exc()
        pass


def search(url):
    global category
    global type_name
    req = requests.get(url)
    result = json.loads(req.text)
    html = result['html']
    # print html
    # print "----------------------"
    soup = BeautifulSoup(html, "html5lib")
    sections = soup.find_all('section')
    small_img = []
    img_url = ''
    timestr = ''
    publish_time = datetime.now()
    if len(sections) > 0:
        for section in sections:
            # print section
            aTag = section.find('a')
            href = aTag['href']
            if len(href) > 0:
                detail_url = "https://m.toutiao.com"+aTag['href']
                h3 = section.find('h3')
                if h3:
                    title = h3.text
                span = section.find('span',class_='time fr')
                if span:
                    timestr = span['title']
                    publish_time = datetime.strptime(timestr, "%Y-%m-%d %H:%M:%S")
                imgs = section.find_all('img')
                if len(imgs) > 0:
                    img_url = imgs[0]['src']
                    for img in imgs:
                        small_img.append(img['src'])


                print title
                print category
                print type_name
                print detail_url
                print timestr
                print img_url
                print small_img
                print "----------"
                detail(detail_url,title,publish_time,img_url,small_img)

category = "shuangyu_reading"
type_name = u"英语学习"

def task_toutiaoapi():
    global category
    global type_name
    types = [u'英语',u'英语口语',u'英语听力',u'英语四级',u'英语写作',u'英语单词',u'英语考试',
             u'英语语法',u'初中英语',u'英语故事',u'英语小说',u'高中英语',u'大学英语',u'英语视频',
             u'英语学习',u'中级英语',u'高级英语',u'英语学习方法',u'英语音标',u'英语入门',u'英语基础',
             u'小学英语',u'考研英语',u'英语教学',u'英语发音']
    for type in types:
        if u'口语' in type:
            category = "spoken_english"
        elif u'听力' in type:
            category = "listening"
        elif u'写作' in type:
            category = "composition"
        elif u'单词' in type:
            category = "word"
        elif u'考试' in type:
            category = "examination"
        elif u'故事' in type:
            category = "story"
        else:
            category = "shuangyu_reading"
        type_name = type

        for i in range(0,20,20):
            # url = 'https://m.toutiao.com/search_content/?offset=%d&count=20&from=search_tab&keyword=英语'%(i)英语听力
            #video
            url = 'https://m.toutiao.com/search_content/?offset=%d&count=20&from=video&keyword=%s'%(i,type)
            print url
            search(url)



if __name__ == '__main__':
    task_toutiaoapi()