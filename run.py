#coding=gb2312
import subprocess
import os

with open("ios_runlist.bat","w") as f:
    for name in os.listdir(r'G:/lessons/iOSӦ�ÿ���'):
            f.write('scrapy crawl course_spider -a courses="%s"' % name +'\n')
          