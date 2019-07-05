# -*- coding:utf-8 -*-
import json
import leancloud
from leancloud import Query

from OrmSpiderUtil import saveSpiderDBUrl
from OrmZyhydbUtil import Reading, saveReadingItem, isUrlExit

leancloud.init('3fg5ql3r45i3apx2is4j9on5q5rf6kapxce51t5bc0ffw2y4', 'twhlgs6nvdt7z7sfaw76ujbmaw7l12gb8v6sdyjw1nzk9b1a')

def copyTask(count):
    global counter
    query = Query('Reading')
    query.descending('createdAt')
    query.skip(count+counter)
    querys = query.find()
    print len(querys)
    size = len(querys)
    if size == 0:
        return

    for data in querys:
        counter += 1
        title = data.get('title')
        source_url = data.get('source_url')
        print(counter)
        print(title)
        print(data.id)
        print(source_url)

        if isUrlExit(source_url):
            print('-------rds already has this url--------')
            pass
        else:
            mReading = Reading()
            mReading.title = data.get('title')
            mReading.content = data.get('content')
            mReading.content_type = data.get('content_type')
            mReading.source_url = source_url
            mReading.source_name = data.get('source_name')
            mReading.createdAt = data.get('createdAt')
            mReading.publish_time = data.get('publish_time')
            mReading.updatedAt = data.get('updatedAt')
            mReading.uuid = data.id
            mReading.media_url = data.get('media_url')
            mReading.img_url = data.get('img_url')
            img_urls = None
            if data.get('img_urls'):
                img_urls = json.dumps(data.get('img_urls'))
            small_img = None
            if data.get('small_img'):
                small_img = json.dumps(data.get('small_img'))
            mReading.img_urls = img_urls
            mReading.small_img = small_img
            mReading.type = data.get('type')
            mReading.type_id = data.get('type_id')
            mReading.type_name = data.get('type_name')
            mReading.level = data.get('level')
            mReading.lrc_url = data.get('lrc_url')
            mReading.category_2 = data.get('category_2')
            mReading.category = data.get('category')
            print saveReadingItem(mReading)
            print saveSpiderDBUrl(source_url)
            print('save item')


counter = 1335
page = 0
if __name__ == '__main__':
    for i in range(0,100):
        page = i
        print i
        copyTask(i*100)
        # is_exit(0)






