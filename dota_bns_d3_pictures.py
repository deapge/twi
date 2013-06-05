#!/usr/bin/python
# -*- coding:utf-8 -*-

'''
  采集dota.gameguyz.com站点图片墙所有图片信息
  http://dota2.gameguyz.com/pictures.html
  每天更新2条记录
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

######################dota2###########################

# Beauty -- 20
url = "http://dota2.gameguyz.com/waterfall_callback?a=gettopchannels&m=channel&start=1&end=5"
json_data = json.load(urllib2.urlopen(url))
data = json_data.get("data", [])
for i in data:
  item = {}
  item['title'] = i.get("title")[:140]
  item['link']  = generate_short_url(i.get("href"))
  item['pic']   = i.get("img")
  params.append(item)

#####################bns############################
# Beauty -- 20
url = "http://bns.gameguyz.com/waterfall_callback?a=gettopchannels&m=channel&start=1&end=10"
json_data = json.load(urllib2.urlopen(url))
data = json_data.get("data", [])
for i in data:
  item = {}
  item['title'] = i.get("title")[:140]
  item['link']  = generate_short_url(i.get("href"))
  item['pic']   = i.get("img")
  params.append(item)

###################d3################################
f = urllib.urlopen("http://d3.gameguyz.com/pictures.html")
html = f.read()
f.close()
soup = BeautifulSoup(''.join(html))
# Beauty -- 20
for i in soup.find(id="picwall").find_all("li"):
  item = {}
  if len(i.find_all("span","subname")) <= 0:
    continue
  item['title'] = i.find_all("span","subname")[0].text
  item['link']  = generate_short_url(i.get("href"))
  item['pic']   = i.img['src']
  params.append(item)
  
###############gw2###################################
url = "http://gw2.gameguyz.com/waterfall_callback?a=gettopchannels&m=channel&start=1&end=5"
json_data = json.load(urllib2.urlopen(url))
data = json_data.get("data", [])
for i in data:
  item = {}
  item['title'] = i.get("title")[:140]
  item['link']  = generate_short_url(i.get("href"))
  item['pic']   = i.get("img")
  params.append(item)

if __name__ == '__main__':
  #params = []
  #item = {}
  #item['title'] = u'google pic33q'
  #item['pic']   = '/home/meadhu/Desktop/173628426.jpg'
  #params.append(item)
  #print post_weibo_sina(params)
  #print post_qq_weibo(params)
  postWeibo(params)
  #print test_socket('api.twitter.com','80')
  #print simplejson.dumps(ret_params, indent=4)
  pass
