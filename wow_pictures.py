#!/usr/bin/python
# -*- coding:utf-8 -*-

'''
  采集wow.gameguyz.com站点图片墙所有图片信息
  http://wow.gameguyz.com/pictures
  差不多每天更新3条记录
'''

from bs4 import BeautifulSoup
import urllib,os,simplejson,json,urllib2
from weibo.sinaweibopy.sinaweibo import post_weibo_sina
from weibo.qqweibopy.postqqweibo import post_qq_weibo
from weibo.postweibo import postWeibo
from webthumb.common import *
# 
f = urllib.urlopen("http://wow.gameguyz.com/pictures")
html = f.read()
f.close()
soup = BeautifulSoup(''.join(html))

params = []
#item = {}
#item['title'] = u'google pic33q'
#item['pic']   = '/home/meadhu/Desktop/173628426.jpg'

# Beauty -- 20
for i in soup.find(id="picwall").find_all("li"):
  item = {}
  if len(i.get("title","")) <= 0: continue 
  item['title'] = i.get("title")[:140]
  item['link']  = generate_short_url(i.get("href"))
  item['pic'] = i.get("img")
  params.append(item)

if __name__ == '__main__':
  #params = []
  #item = {}
  #item['title'] = u'google pic33q'
  #item['pic']   = '/home/meadhu/Desktop/173628426.jpg'
  #params.append(item)
  #print post_weibo_sina(params)
  #print post_qq_weibo(params)
  ret_params = postWeibo(params)
  #print simplejson.dumps(ret_params, indent=4)
  pass
