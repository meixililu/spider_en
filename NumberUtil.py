# -*- coding:utf-8 -*-
import re

def getNumber(num):
    result = re.search("\d+(\.\d+)?",num)
    if result.group():
        print result.group()
        return float(result.group())
    else:
        return 0

def getVid(url):
    result = re.search("video_id=(\w+)&",url)
    if result.group():
        print result.group(1)
        return result.group(1)
    else:
        return ''

if __name__ == '__main__':
    getVid("https://aweme.snssdk.com/aweme/v1/play/?video_id=v0200f1b0000bf0v5taepr19b8vho3q0&line=0&app_id=13")