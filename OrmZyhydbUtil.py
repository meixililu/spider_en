# -*- coding:utf-8 -*-
import datetime
from uuid import uuid4
from sqlalchemy import Column, String, create_engine,Integer,Text,DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

base=declarative_base()
engine=create_engine("mysql+pymysql://zyhy:zyhy888!@rm-wz9s08j1uws18yekpuo.mysql.rds.aliyuncs.com:3306/zyhydb?charset=utf8",echo=True,pool_size=100)
# engine=create_engine("mysql+pymysql://root:Xbkj2613569!@localhost/spider?charset=utf8",echo=True,pool_size=100)
DBSession = sessionmaker(bind=engine)
session = DBSession()
# query=session.execute('select * from Reading')
# query=query.fetchall()
# print query
# session.close()
class Reading(base):

    __tablename__ = "Reading"

    uuid = Column(String(64), unique=True, nullable=False, default=lambda: str(uuid4()), comment='objectId')
    id = Column(Integer, primary_key=True, autoincrement=True, comment=u'自增id')
    title = Column(String(300), index=True, comment=u'标题')
    category = Column(String(64), index=True, comment=u'分类')
    category_2 = Column(String(64), comment=u'分类2')
    type = Column(String(64), comment=u'类别')
    type_id = Column(String(64), comment=u'类别id')
    type_name = Column(String(64), comment=u'类别名称')
    content_type = Column(String(64), default='url', comment=u'内容类型')
    level = Column(String(36), index=True, comment=u'水平')
    content = Column(Text, comment=u'内容')
    source_name = Column(String(64), comment=u'来源')
    source_url = Column(String(300), index=True, comment=u'来源地址')
    lrc_url = Column(Text, comment=u'歌词地址')
    lrc_content = Column(Text, comment=u'歌词内容')
    media_url = Column(Text, comment=u'视频地址')
    img_url = Column(Text, comment=u'图片地址')
    img_urls = Column(Text, comment=u'图片地址集合')
    small_img = Column(Text, comment=u'小图地址集合')
    createdAt = Column(DateTime, default=datetime.datetime.now, comment=u'创建时间')
    updatedAt = Column(DateTime, default=datetime.datetime.now, comment=u'更新时间')
    publish_time = Column(DateTime, default=datetime.datetime.now, comment=u'文章发布时间')

# base.metadata.create_all(engine)


def isUrlExit(url):
    session = DBSession()
    query = session.query(Reading)
    count = query.filter(Reading.source_url == url).count()
    # count = query.all()
    # for item in count:
    #     print item.url
    session.close()
    return count > 0

def saveReadingItem(mData):
    session = DBSession()
    session.add(mData)
    session.commit()
    # print crawl.id
    # session.close()
    return mData.id