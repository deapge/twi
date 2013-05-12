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
from hashlib import md5
from datetime import datetime
now = datetime.now() # now.strftime("%Y-%m-%d %H:%M:%S")
m = md5()

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

# 通过图片链接,下载图片并存储在本机
def downLoadImg(src):
  m.update(src+now.strftime("%Y%m%d%H")) 
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

# 大眼睛 -- 4
for thumb in soup.find(id="bigEyeHide").find_all('li'):
  item = {}
  item['title'] = thumb.p.text[:140]
  item['url']   = thumb.a["href"]
  item['title'] = item['title']+item['url']
  item['pic']   = downLoadImg(thumb.img["src"])
  params.append(item)
  
# 游戏 --- 10
for i in soup.find(id="wgcList").find_all("li")[10]:
  item = {}
  a_tag = i.find_all("a")[1]
  item['title'] = a_tag.text[:140]+a_tag.get("href")
  item['pic']   = downLoadImg(i.img['src'])
  params.append(item)

# Recommended Topics -- 5
for i in soup.find_all("div", "speList")[0].find_all("div"):
  item = {}
  item['title'] = i.img['alt']+i.a['href']
  item['pic']   = downLoadImg(i.img['src'])
  params.append(item)

# Pictures -- 10
for i in soup.find_all("a","hotPic"):
  item = {}
  item['title'] = i.get("title")+i.get("href")
  item['pic']   = downLoadImg(i.img['src'])
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
