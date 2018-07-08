# -*- coding:utf-8 -*-
import sys
import os
import time
import traceback
import threading
from DailySentence import *
from iciba_study_spider import *
from spder_record import *
from spder_record_finish import *
from jianghu_reading_spider import *
from yingyu_com_chilren_story_spider import *
from yingyu_com_chilren_spoken_english_spider import *
from adreep_spider import *
from Henxingwang_composition_spider import *
from Henxingwang_word_spider import *
from Henxingwang_listening_spider import *
from Henxingwang_yuedulijie_spider import *
from cuyoo_spider import *
from en8848_story_spider import *
from www_iyuba_com import *
from youdaoapp import *
from www_yingyu_xdf_cn import *
from joke import *
from neihanduanziapp import *
from dytt8 import *
from chinavoa_com import *
from dict_eudic_spider import *

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
    try:
        print 'execfile------neihanduanziapp'
        neihanduanziapp()
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

def yingyu_com_chilren_story_spider():
    try:
        print 'execfile------yingyu_com_chilren_story_spider.py'
        task_yingyu_com_chilren_story_spider()
    except:
        print traceback.format_exc()

def yingyu_com_chilren_spoken_english_spider():
    try:
        print 'execfile------yingyu_com_chilren_spoken_english_spider.py'
        task_yingyu_com_chilren_spoken_english_spider()
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

def cuyoo_spider():
    try:
        print 'execfile------cuyoo_spider.py'
        task_cuyoo_spider()
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
    t4 = threading.Thread(target=yingyu_com_chilren_story_spider, args=())
    threads.append(t4)
    t5 = threading.Thread(target=yingyu_com_chilren_spoken_english_spider, args=())
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
    t11 = threading.Thread(target=cuyoo_spider, args=())
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

    for t in threads:
        t.setDaemon(True)
        t.start()

    t.join()
    try:
        print 'execfile------spder_record_finish.py'
        recordSpiderFinishTime()
    except:
        print traceback.format_exc()















