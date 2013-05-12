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
from hashlib import md5
from datetime import datetime
now = datetime.now() # now.strftime("%Y-%m-%d %H:%M:%S")
m = md5()

f = urllib.urlopen("http://wow.gameguyz.com/pictures")
html = f.read()
f.close()
soup = BeautifulSoup(''.join(html))

params = []
#item = {}
#item['title'] = u'google pic33q'
#item['pic']   = '/home/meadhu/Desktop/173628426.jpg'

# 通过图片链接,下载图片并存储在本机
def downLoadImg(src):
  m.update(src+now.strftime("%Y%m%d")) 
  thumb_path = '/tmp/'+m.hexdigest()+'.jpg'
  if os.path.isfile(thumb_path) == True:
    print '使用已经存在的图片...';
    return thumb_path
  print '正在下载图片...';
  f = open(thumb_path, 'wb')
  f.write(urllib.urlopen(src).read())
  f.close()
  return thumb_path
  pass

# Beauty -- 20
for i in soup.find(id="picwall").find_all("li"):
  item = {}
  item['title'] = i.get("title")[:140]+i.get("href")
  item['pic'] = downLoadImg(i.get("img"))
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
