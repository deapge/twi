#!/usr/bin/python
# -*- coding:utf-8 -*-

'''
  采集sc2.gameguyz.com站点图片墙所有图片信息
  http://sc2.gameguyz.com/pictures.html
  
'''

from bs4 import BeautifulSoup
import urllib,os,simplejson,json,urllib2
from weibo.sinaweibopy.sinaweibo import post_weibo_sina
from weibo.qqweibopy.postqqweibo import post_qq_weibo
from weibo.postweibo import postWeibo
from webthumb.common import *

# Get a file-like object for the Python Web site's home page.
#f = urllib.urlopen("http://www.gameguyz.com")
# Read from the object, storing the page's contents in 'html'.
#html = f.read()
#f.close()
#soup = BeautifulSoup(html)
#soup = BeautifulSoup(''.join(html))

params = []
#item = {}
#item['title'] = u'google pic33q'
#item['pic']   = '/home/meadhu/Desktop/173628426.jpg'

# Beauty -- 20
url = "http://sc2.gameguyz.com/waterfall_callback?page=1&num=5"
json_data = json.load(urllib2.urlopen(url))
data = json_data.get("data", [])
for i in data:
  item = {}
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
