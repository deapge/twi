#/usr/bin/python
# -*- coding: utf8 -*-

'''
生成 short link
http://adfoc.us/api/?key=3c233524834df35c386025109f9412eb&url=http://www.google.com/
http://adfoc.us/serve/sitelinks/?id=152162&url=http://www.google.com/
>>>>>>>>>>>>  http://adfoc.us/serve/?id=15216225398195

http://2ad.in/api.php?key=649b470a8bedc3488d943a3df2c8ab20&uid=432&adtype=banner&url=http://www.google.com
 >>>>>>>>>>>  http://2ad.in/XRXU
'''
import urllib
import os
from hashlib import md5
from datetime import datetime
import threading
import sys
import socket
from socket import error as socket_error
now = datetime.now() # now.strftime("%Y-%m-%d %H:%M:%S")
m = md5()

import pymongo
# create connection
connection = pymongo.Connection('localhost', 27017)
# switch db
db = connection.proxy_server

# 将生成好的链接地址,存储到mongodb中
def save_url_to_mongo(link, domain):
  collection = db.short_urls
  posts = {
           'short_link' : link,
           'domain'     : domain,
           }
  row = collection.find_one(posts)
  if row == None:
    print collection.insert(posts)
    print posts

def generate_short_url(link, is_gen = 1):
  if is_gen == 0: return link
  if link == None:
    return ''
  url_conf = {
              #'joturl.com':'https://api.joturl.com/a/v1/shorten?format=plain&login=471e83dd38c57e0ad439f8beccfde467&key=f103d0a241a2bd5495a158ce31c55329&url=',
              'adfoc.us' : 'http://adfoc.us/api/?key=3c233524834df35c386025109f9412eb&url=',
              #'2ad.in'   : 'http://2ad.in/api.php?key=649b470a8bedc3488d943a3df2c8ab20&uid=432&adtype=banner&url=',
              }
  domain = url = ''
  for d in url_conf:
    if testSocket(d, '80') == 1:
      domain = d
      url    = url_conf[d]
      break
  if len(url) == 0: return link
  print '正在生成链接...'
  url += link
  #proxy = '33.33.33.11:8118'
  #proxies={'http': proxy}
  #urllib.urlopen(url, data, proxies)
  response = urllib.urlopen(url)
  result = response.read()
  response.close()
  if len(result) >= 0:
    print '生成链接成功!: '+result
    save_url_to_mongo(result, domain)
    return result
  else:
    return link

  # 通过图片链接,下载图片并存储在本机
def downLoadImg(src):
    if "http" != src[:4]: return src
    m.update(src+now.strftime("%Y%m%d")) 
    thumb_path = '/tmp/'+m.hexdigest()+'.jpg'
    if os.path.isfile(thumb_path) == True:
      print '使用已经存在的图片...';
      return thumb_path
    print '正在下载图片...';
    f = open(thumb_path, 'wb')
    #f.write(urllib.urlopen(src).read())
    response = urllib.urlopen(src)
    result = response.read()
    f.write(result)
    f.close()
    return thumb_path
    pass


def testSocket(hostname, port):
  '''
  socket连接测试，用来测试远程服务器连接是否通畅，适用于没有VPN连接时，测试twitter.com,facebook.com,youtube.com
  '''
  print '正在测试socket连接...'
  hostinfo = socket.gethostbyname_ex(hostname)
  domain = hostinfo[0]
  ip   = hostinfo[2][0]
  port = port
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  try:
    sock.settimeout(10)
    sock.connect((ip, int(port)))
    #sock.send('meta')
    sock.close()
    print '['+domain+'] '+ip+':'+port+'--status:ok'
    return 1
  except socket_error as serr: # connection error
    sock.close()
    print '['+domain+'] '+ip+':'+port+'--status:error--Connection refused.'
    return 0
