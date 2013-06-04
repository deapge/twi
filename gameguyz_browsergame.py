#!/usr/bin/python
# -*- coding:utf-8 -*-

'''
  采集gameguyz.com站点 browser game
  http://www.gameguyz.com/browser-games.html
'''

from bs4 import BeautifulSoup
import urllib,os,simplejson
from weibo.sinaweibopy.sinaweibo import post_weibo_sina
from weibo.qqweibopy.postqqweibo import post_qq_weibo
from weibo.postweibo import postWeibo
from webthumb.common import *

# Get a file-like object for the Python Web site's home page.
f = urllib.urlopen("http://www.gameguyz.com/browser-games.html")
# Read from the object, storing the page's contents in 'html'.
html = f.read()
f.close()
#soup = BeautifulSoup(html)
soup = BeautifulSoup(''.join(html))

params = []
#item = {}
#item['title'] = u'google pic33q'
#item['pic']   = '/home/meadhu/Desktop/173628426.jpg'

# 大眼睛 -- 4
for thumb in soup.find(id="bigEyeHide").find_all('li'):
  item = {}
  item['title'] = thumb.p.text[:140]
  item['link']  = generate_short_url(thumb.a["href"])
  item['pic']   = downLoadImg(thumb.img["src"])
  params.append(item)
  
# 游戏 --- 10
#for i in soup.find(id="wgcList").find_all("li")[10]:
#  item = {}
#  if i == None or len(i.find_all("a")) <= 1: continue 
#  a_tag = i.find_all("a")[1]
#  item['title'] = a_tag.text[:140]+a_tag.get("href")
#  item['pic']   = downLoadImg(i.img['src'])
#  params.append(item)

# Recommended Topics -- 5
for i in soup.find_all("div", "speList")[0].find_all("div"):
  item = {}
  item['title'] = i.img['alt']
  item['link']  = generate_short_url(i.a['href'])
  item['pic']   = downLoadImg(i.img['src'])
  params.append(item)

# Pictures -- 10
for i in soup.find_all("ol","subbd")[0].find_all("li"):
  item = {}
  url = item.find_all("a","odd")[0].get("href")
  item['title'] = item.find_all("a","odd")[0].text
  item['link']  = generate_short_url(i.get("href"))
  item['pic']   = downLoadImg(i.img['src'])
  params.append(item)

if __name__ == '__main__':
  print params
  #params = []
  #item = {}
  #item['title'] = u'google pic33q'
  #item['pic']   = '/home/meadhu/Desktop/173628426.jpg'
  #params.append(item)
  #print post_weibo_sina(params)
  #print post_qq_weibo(params)
  #ret_params = postWeibo(params)
  #print simplejson.dumps(ret_params, indent=4)
  pass
