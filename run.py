#coding=gb2312
import subprocess
import os

with open("ios_runlist.bat","w") as f:
    for name in os.listdir(r'G:/lessons/iOS应用开发'):
        line = 'scrapy crawl course_spider -a courses="%s"' % name
        subprocess.call(line)
          