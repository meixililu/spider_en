#!/usr/bin/env python
# -*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
from datetime import *
import leancloud
from leancloud import Object
from leancloud import Query
import traceback
from ImageUtil import *

def is_exit(film_name,urls,imgs):
    query = Query('FilmDetail')
    query.equal_to('film_name', film_name)
    querys = query.find()
    if len(querys) > 0:
        isneedsave = False
        data = querys[0]
        if len(urls) > len(data.get('download_url')):
            data.set('download_url',urls)
            isneedsave = True
        if len(imgs) > len(data.get('film_imgs')):
            data.set('film_imgs',imgs)
            isneedsave = True
        if isneedsave:
            data.save()
            # print 'update data'
    return len(querys) > 0

def parseDetailPage(url,title,publish_time):
    try:
        global type_code
        # url = 'http://www.ygdy8.net/html/gndy/dyzz/20161225/52789.html'
        # url = 'http://www.ygdy8.net//html/tv/rihantv/20120510/37631.html'
        # print url
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'}
        req = requests.get(url, headers=headers)
        req.encoding = 'gb2312'
        soup = BeautifulSoup(req.text, "html5lib")
        content = ''
        urls = []
        imgs = []
        zoom = soup.find('div', id='Zoom')
        downurl_temp = zoom.find_all('a')
        imgs_temp = zoom.find_all('img')

        content = getContent(zoom.text.strip()).strip()

        for link in downurl_temp:
            if 'ftp://' in link['href']:
                urls.append(link['href'])

        if len(imgs_temp) > 0:
            for img in imgs_temp:
                (ratio, width, height) = getImageRatio(img['src'])
                if ratio == 5.5555:
                    pass
                else:
                    imgs.append(img['src'])

        # print '--------start---------'
        # print title
        # print publish_time
        # print content
        # print 'urls:'
        # print urls
        # print 'imgs:'
        # print imgs
        # print '--------end---------'

        if is_exit(title,urls,imgs):
            # print 'exit return'
            return

        FilmDetail = Object.extend('FilmDetail')
        mFilmDetail = FilmDetail()
        mFilmDetail.set('film_name', title)
        mFilmDetail.set('publish_time', publish_time)
        mFilmDetail.set('film_des', content)
        mFilmDetail.set('download_url', urls)
        mFilmDetail.set('film_imgs', imgs)
        mFilmDetail.set('type_code', type_code)
        mFilmDetail.set('source_url', url)
        mFilmDetail.save()
        # print('save item')
    except:
        # print 'exception'
        # print traceback.format_exc()
        return

def getContent(content):
    contents = ''
    for conn in content.splitlines():
        con = conn.strip()
        if con is None:
            continue
        elif u'下载地址' in con or u'温馨提示' in con or 'ftp://' in con or u'点击进去首发区' in con or u'下载方法' in con or u'点击进入' in con:
            if len(con) < 200:
                continue
            else:
                contents += con.strip()
                contents += '\n\n'
        elif con.startswith(u'第') or con.startswith(str('0')) or con.startswith(str('1')) or con.startswith(str('2')) or con.startswith(str('3')) or con.startswith(str('4')) or con.startswith(str('5')) or con.startswith(str('6')) or con.startswith(str('7')) or con.startswith(str('8')) or con.startswith(str('9')):
            continue
        # elif u'金山词霸微信版开通啦' in con or u'点击进入' in con or u'专为' in con or u'您的浏览器' in con or u'求关注' in con or 'ijinshanciba' in con or u'帐号：' in con or u'号外号外' in con:
        #     pass
        elif len(con) == 0:
            continue
        else:
            contents += con.strip()
            contents += '\n\n'
    contents = contents.strip().replace(u'◎', '\n')

    return contents


def getitem_list(url):
    # print url
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'}
    req = requests.get(url, headers=headers)
    req.encoding = 'gb2312'
    soup = BeautifulSoup(req.text, "html5lib")

    ulinks_temp = soup.find_all('a',class_='ulink')
    ulinks = []
    for link in ulinks_temp:
        if 'index.html' in link['href']:
            continue
        else:
            ulinks.append(link)

    times = soup.find_all('font',attrs={'color' : "#8F8C89"})
    # print len(times)
    if len(ulinks) > 0 and len(times) > 0:
        for i in range(0,len(ulinks)):
            title = ulinks[i].text
            publish_time = datetime.strptime(times[i].text[3:22].lstrip(), "%Y-%m-%d %H:%M:%S")
            url = 'http://www.ygdy8.net/' + ulinks[i]['href']
            parseDetailPage(url,title,publish_time)

type_code = ''
def dianyingtoutiaotask():
    initDYTT()
    global type_code
    urls = []
    urls.append("http://www.ygdy8.net/html/dongman/list_16_%d.html")
    urls.append("http://www.ygdy8.net/html/zongyi2013/list_99_%d.html")
    urls.append("http://www.ygdy8.net/html/tv/hytv/list_71_%d.html")
    urls.append("http://www.ygdy8.net/html/tv/rihantv/list_8_%d.html")
    urls.append("http://www.ygdy8.net/html/tv/oumeitv/list_9_%d.html")
    urls.append("http://www.ygdy8.net/html/gndy/rihan/list_6_%d.html")
    urls.append("http://www.ygdy8.net/html/gndy/china/list_4_%d.html")
    urls.append("http://www.ygdy8.net/html/gndy/oumei/list_7_%d.html")
    for url in urls:
        for i in range(1,2):
            # print 'page:'+ str(i)
            if 'gndy/oumei' in url:
                type_code = "10001"#欧美电影
            elif 'gndy/china' in url:
                type_code = "10002"#国内电影
            elif 'gndy/rihan' in url:
                type_code = "10003"#日韩电影
            elif 'tv/oumeitv' in url:
                type_code = "10004"#欧美电视剧
            elif 'tv/rihantv' in url:
                type_code = "10005"#日韩剧
            elif 'dongman' in url:
                type_code = "10008"#动漫
            elif 'tv/hytv' in url:
                type_code = "10006"#华语电视剧
            elif 'zongyi2013' in url:
                type_code = "10007"#综艺节目

            # print 'type_code:'+type_code
            getitem_list(url % i)

if __name__ == '__main__':
    dianyingtoutiaotask()
    # parseDetailPage('','','')
