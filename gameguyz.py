#!/usr/bin/python
# -*- coding:utf-8 -*-

'''
  采集gameguyz.com站点
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
f = urllib.urlopen("http://www.gameguyz.com")
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
for thumb in soup.find(id="iPThumb").find_all('div'):
  item = {}
  item['title'] = thumb.img["bigtipscontent"]
  item['url']   = thumb.a["href"]
  item['title'] = item['title']+item['url']
  item['pic']   = downLoadImg(thumb.img["bigsrc"])
  params.append(item)
  
# 右侧新闻 -- 12
for i in soup.find(id="iPFr").find_all("li"):
  item = {}
  item['title'] = i.a['title']+i.a['href']
  item['pic']   = ''
  params.append(item)

# Game Videos -- 5
for i in soup.find_all("table", "game_videos")[0].find_all("td"):
  item = {}
  item['title'] = i.img['alt']+i.a['href']
  item['pic']   = downLoadImg(i.img['src'])
  params.append(item)

# Game News -- 10
item = {}
game_news = soup.find_all("div","iGameNewsBox")[0].find_all("div","iGNPicBox")[0]
item['title'] = game_news.p.text+game_news.a['href']
item['pic'] = downLoadImg(game_news.img['src'])
params.append(item)
for i in soup.find_all("div","iGameNewsBox")[0].find_all("div","iGNList"):
  item = {}
  item['title'] = i.a['title']+i.a['href']
  params.append(item)

# Game Vendor -- 4, Browser Games -- 3
for i in soup.find_all("div","around_the_network"):
  item = {}
  item['title'] = i.p.text[:140]+i.a['href']
  item['pic'] = downLoadImg(i.img['src'])
  params.append(item)

# Pictures -- 6
for i in soup.find_all("table","game_photos")[0].find_all("td"):
  item = {}
  item['title'] = i.img['alt'][:140]+i.a['href']
  item['pic'] = downLoadImg(i.img['src'])
  params.append(item)

# Flash Games -- 6
#for i in soup.find_all("table","front_flash_game")[0].find_all("td"):
#  item = {}
#  item['title'] = i.img['alt'][:140]+i.a['href']
#  item['pic'] = downLoadImg(i.img['src'])
#  params.append(item)

# Gossips -- 7
item = {}
gossips = soup.find_all("div","iGossips")[0].find("a")
item['title'] = gossips.img['alt'][:140]+gossips.get('href')
item['pic'] = downLoadImg(gossips.img['src'])
params.append(item)
for i in soup.find_all("div","iGossips")[0].find_all("li"):
  item = {}
  item['title'] = i.a.text[:140]+i.a['href']
  params.append(item)

# Beauty -- 9
for i in soup.find_all("table","gg_friends")[0].find_all("td"):
  item = {}
  item['title'] = i.img['alt'][:140]+i.a['href']
  item['pic'] = downLoadImg(i.img['src'])
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
