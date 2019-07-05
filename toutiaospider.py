# -*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
import json
import leancloud
from leancloud import Object
from leancloud import Query
from datetime import *
import traceback
import HttpUtil


leancloud.init('3fg5ql3r45i3apx2is4j9on5q5rf6kapxce51t5bc0ffw2y4', 'twhlgs6nvdt7z7sfaw76ujbmaw7l12gb8v6sdyjw1nzk9b1a')


def is_exit(str):
    global category
    global type_name
    query = Query('Reading')
    query.equal_to('source_url', str)
    querys = query.find()
    return len(querys) > 0

def search(url):
    global category
    global type_name
    try:
        req = requests.get(url)
        result = json.loads(req.text)
        print result
        data = result['data']
        if len(data) == 0:
            # print 'len==0'
            return
        for item in data:
            small_img = []
            img_urls = []
            img_url = ''
            try:
                publish_time = datetime.strptime(item['datetime'], "%Y-%m-%d %H:%M:%S")
            except:
                # print traceback.format_exc()
                return
            title = item['title']
            content = item['abstract']
            img_url = item['large_image_url']
            if len(img_url) == 0:
                img_url = item['middle_image_url']
            source_url = 'https://m.toutiao.com' + item['open_url']

            # print "----------"
            # print title
            # print category
            # print type_name
            # print publish_time
            # print source_url
            # print img_url

            if HttpUtil.is404(source_url):
                # print 'is 404'
                return
            if is_exit(source_url):
                # print 'url is exit'
                return
            mediaUrl = "media_url"
            content_type = "url"
            mediaUrlroot = "http://api.huoshan.com/hotsoon/item/video/_playback/?video_id=#&line=0&app_id=13"
            vid = HttpUtil.getVid(source_url)
            if "404" == vid:
                return
            elif vid:
                mediaUrl = mediaUrlroot.replace("#", vid)
                content_type = "url_media"

            Composition = Object.extend('Reading')
            mComposition = Composition()
            mComposition.set('title', title)
            mComposition.set('img_url', img_url)
            mComposition.set('img_type', 'url')
            mComposition.set('content', content)
            mComposition.set('content_type', content_type)
            mComposition.set('type_name', type_name)
            mComposition.set('publish_time', publish_time)
            mComposition.set('source_url', source_url)
            mComposition.set('source_name', u"今日头条")
            mComposition.set('level', "")
            mComposition.set('category', category)
            mComposition.set('category_2', "")
            mComposition.set('type', "video")
            mComposition.set('media_url', mediaUrl)
            mComposition.save()
            # print('save item')
    except:
        # print traceback.format_exc()
        return

category = "shuangyu_reading"
type_name = u"英语学习"

def task_toutiaoapi():
    global category
    global type_name

    types = [u'英语',u'英语口语',u'英语听力',u'英语四级',u'英语写作',u'英语单词',u'英语考试',
             u'英语语法',u'初中英语',u'英语故事',u'英语小说',u'高中英语',u'大学英语',u'英语视频',
             u'英语学习',u'中级英语',u'高级英语',u'英语学习方法',u'英语音标',u'英语入门',u'英语基础',
             u'小学英语',u'考研英语',u'英语教学',u'英语发音',u'优说英语',u'地道英语',u'cc皇家学院',
            u'Kevin英语情报局',u'英语小救星',u'英语频道',
            u'听书问道',u'人人英语',u'海涛英语',u'不学英语',u'英语干货铺',u'杰杰英语']
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

        for i in range(0,150,10):
            url = 'https://www.toutiao.com/search_content/?offset=%d&format=json&keyword=%s&autoload=true&count=10&cur_tab=2&from=video&aid=24'%(i,type)
            search(url)



if __name__ == '__main__':
    task_toutiaoapi()