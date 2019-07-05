# -*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
import re
import traceback

def is404(url):
    url2 = url.replace("https://m.toutiao.com/group/", "https://www.ixigua.com/i")
    result1 = parseUrl(url)
    result2 = parseUrl(url2)
    return result1 or result2

def parseUrl(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'}
    req = requests.get(url, headers=headers)
    soup = BeautifulSoup(req.text, "html5lib")
    div = soup.find('title')
    # print "404" in div.text
    return "404" in div.text

def isUrlValid(url):
    url = url.replace("https://m.toutiao.com/group/", "https://www.ixigua.com/i")
    result = parseUrl(url)
    return result

def getVid(url):
    try:
        if isUrlValid(url):
            # print "404"
            return "404"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'}
        req = requests.get(url, headers=headers)
        soup = BeautifulSoup(req.text, "html5lib")
        div = soup.find('title')
        if "404" in div.text:
            # print "404"
            return "404"
        directUrl = req.url
        # print directUrl
        if 'www.365yg.com' in directUrl:
            result = re.search("videoId: '(\w+)'", req.text)
            if result.group():
                # print result.group(1)
                return result.group(1)
        elif 'www.ixigua.com' in directUrl:
            result = re.search("\"vid\":\"(\w+)\"", req.text)
            if result.group():
                # print result.group(1)
                return result.group(1)
        elif 'www.toutiao.com' in directUrl:
            result = re.search("videoid&#x3D;&#x27;(\w+)&#x27", req.text)
            if result.group():
                # print result.group(1)
                return result.group(1)
    except:
        # print traceback.format_exc()
        return

if __name__ == '__main__':
    url = "https://m.toutiao.com/group/6701480028263154189/"
    is404(url)