# -*- coding:utf-8 -*-
import threading
from DailySentence import *
from iciba_study_spider import *
from spder_record import *
from spder_record_finish import *
from jianghu_reading_spider import *
from adreep_spider import *
from Henxingwang_composition_spider import *
from Henxingwang_word_spider import *
from Henxingwang_listening_spider import *
from Henxingwang_yuedulijie_spider import *
from en8848_story_spider import *
from www_iyuba_com import *
from youdaoapp import *
from www_yingyu_xdf_cn import *
from joke import *
from chinavoa_com import *
from dict_eudic_spider import *
from toutiaospider import *
from toutiaospider_rh import *
from toutiaospider_yue import *
from toutiaospider_yw import *
from voa51_com import *
from chinadaily_spider import *

def dailySentence():
    try:
        print 'execfile------getDailySentence'
        getDailySentence()
    except:
        print traceback.format_exc()
    try:
        print 'execfile------getJokeTask'
        getJokeTask()
    except:
        print traceback.format_exc()

def iciba_study_spider():
    try:
        print 'execfile------iciba_study_spider.py'
        task_iciba_study_spider()
    except:
        print traceback.format_exc()

def jianghu_reading_spider():
    try:
        print 'execfile------jianghu_reading_spider.py'
        task_jianghu_reading_spider()
    except:
        print traceback.format_exc()

def toutiao_spider():
    try:
        print 'execfile------toutiao_spider.py'
        task_toutiaoapi()
    except:
        print traceback.format_exc()

def toutiao_yw_spider():
    try:
        print 'execfile------toutiao_yw_spider.py'
        task_toutiaoapi_yw()
    except:
        print traceback.format_exc()

def toutiao_rh_spider():
    try:
        print 'execfile------toutiao_rh_spider.py'
        task_toutiao_rh()
    except:
        print traceback.format_exc()

def toutiao_yue_spider():
    try:
        print 'execfile------toutiao_yue_spider.py'
        task_toutiaoapi_yue()
    except:
        print traceback.format_exc()

def voa51_com_spider():
    try:
        print 'execfile------voa51_com_spider.py'
        voa51()
    except:
        print traceback.format_exc()

def adreep_spider():
    try:
        print 'execfile------adreep_spider.py'
        task_adreep_spider()
    except:
        print traceback.format_exc()

def henxingwang_composition_spider():
    try:
        print 'execfile------Henxingwang_composition_spider.py'
        task_henxingwang_composition_spider()
    except:
        print traceback.format_exc()

def henxingwang_listening_spider():
    try:
        print 'execfile------Henxingwang_listening_spider.py'
        task_Henxingwang_listening_spider()
    except:
        print traceback.format_exc()

def henxingwang_word_spider():
    try:
        print 'execfile------Henxingwang_word_spider.py'
        task_henxingwang_word_spider()
    except:
        print traceback.format_exc()

def henxingwang_yuedulijie_spider():
    try:
        print 'execfile------Henxingwang_yuedulijie_spider.py'
        task_Henxingwang_yuedulijie_spider()
    except:
        print traceback.format_exc()

def en8848_story_spider():
    try:
        print 'execfile------en8848_story_spider.py'
        task_en8848_story_spider()
    except:
        print traceback.format_exc()

def www_iyuba_com():
    try:
        print 'execfile------www_iyuba_com.py'
        task_www_iyuba_com()
    except:
        print traceback.format_exc()

def www_yingyu_xdf_cn():
    try:
        print 'execfile------www_yingyu_xdf_cn.py'
        task_www_yingyu_xdf_cn()
    except:
        print traceback.format_exc()

def youdaoapp():
    try:
        print 'execfile------youdaoapp.py'
        task_youdaoapp()
    except:
        print traceback.format_exc()

def chinavoa_com():
    try:
        print 'execfile------chinavoa_com.py'
        task_chinavoa_com()
    except:
        print traceback.format_exc()

def chinadaily_com():
    try:
        print 'execfile------chinadaily_com.py'
        chinadaily_task()
    except:
        print traceback.format_exc()

def dict_education():
    try:
        print 'execfile------dict_education.py'
        task_dict_education()
    except:
        print traceback.format_exc()

if __name__ == '__main__':
    try:
        print 'execfile------spder_record.py'
        recordSpiderRunTime()
    except:
        print traceback.format_exc()
    threads = []
    t1 = threading.Thread(target=dailySentence, args=())
    threads.append(t1)
    t2 = threading.Thread(target=iciba_study_spider, args=())
    threads.append(t2)
    t3 = threading.Thread(target=jianghu_reading_spider, args=())
    threads.append(t3)
    t4 = threading.Thread(target=toutiao_spider, args=())
    threads.append(t4)
    t5 = threading.Thread(target=voa51_com_spider, args=())
    threads.append(t5)
    t6 = threading.Thread(target=adreep_spider, args=())
    threads.append(t6)
    t7 = threading.Thread(target=henxingwang_composition_spider, args=())
    threads.append(t7)
    t8 = threading.Thread(target=henxingwang_listening_spider, args=())
    threads.append(t8)
    t9 = threading.Thread(target=henxingwang_word_spider, args=())
    threads.append(t9)
    t10 = threading.Thread(target=henxingwang_yuedulijie_spider, args=())
    threads.append(t10)
    t11 = threading.Thread(target=chinadaily_com, args=())
    threads.append(t11)
    t12 = threading.Thread(target=en8848_story_spider, args=())
    threads.append(t12)
    t13 = threading.Thread(target=www_iyuba_com, args=())
    threads.append(t13)
    t14 = threading.Thread(target=www_yingyu_xdf_cn, args=())
    threads.append(t14)
    t15 = threading.Thread(target=youdaoapp, args=())
    threads.append(t15)
    t16 = threading.Thread(target=chinavoa_com, args=())
    threads.append(t16)
    t17 = threading.Thread(target=dict_education, args=())
    threads.append(t17)
    t18 = threading.Thread(target=toutiao_yw_spider, args=())
    threads.append(t18)
    t19 = threading.Thread(target=toutiao_rh_spider, args=())
    threads.append(t19)
    t20 = threading.Thread(target=toutiao_yue_spider, args=())
    threads.append(t20)

    for t in threads:
        t.setDaemon(True)
        t.start()

    t.join()
    try:
        print 'execfile------spder_record_finish.py'
        recordSpiderFinishTime()
    except:
        print traceback.format_exc()















