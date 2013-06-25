#/usr/bin/python
# -*- coding:utf8 -*-

'''
采集最新的代理服务器信息,并存储在mongodb数据库中.
http://hidemyass.com/proxy-list/search-225414

此文件功能：
  1.用来从代理服务器页面中获取 代理帐号，并测试，将测试通过帐号存储到mongodb中;
  2.检测代理帐号是否正常连接，使用多线程，不正常的，删除掉。
'''

import pymongo,sys
import urllib
from bs4 import BeautifulSoup
import socket
import threading
from socket import error as socket_error
from datetime import datetime

# create connection
connection = pymongo.Connection('localhost', 27017)
# switch db
db = connection.proxy_server
# get collection
collection = db.proxy_server_usa

class FetchProxyServerThread(threading.Thread):
  def __init__(self, ip, port, title):
    threading.Thread.__init__(self)
    self.ip    = ip
    self.port  = port
    self.title = title
  
  def run(self):
    if testSocket(self.ip, self.port) == 1:# 服务器帐号信息正常,存储起来
      posts = {
               'ip'    : self.ip,
               'port'  : self.port,
               'title' : self.title,
               'last_changed': str(datetime.now())
               }
      row = collection.find_one({"ip":self.ip,"port":self.port})
      if row == None:
        print collection.insert(posts)
        print '帐号添加成功!'
        print posts
    pass

def fetchProxyServer(url, ip, port):
  '''
   抓取proxy server 信息
  '''
  import urllib2,cookielib
  '''
  req = urllib2.Request(url)
  req.add_header('GET', '/proxy-list/search-225414 HTTP/1.1')
  req.add_header('Host', 'hidemyass.com')
  req.add_header('User-Agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0')
  req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
  req.add_header('Accept-Language', 'en-US,en;q=0.5')
  req.add_header('Accept-Encoding', 'gzip, deflate')
  req.add_header('DNT', '1')
  req.add_header('Connection', 'keep-alive')
  req.add_header('Cache-Control', 'max-age=0')
  r = urllib2.urlopen(req)
  response = urllib.urlopen(url)
  result = response.read()
  soup = BeautifulSoup(result)
  print soup
  '''
  cookie_file = '/tmp/hidemypass.cookie'
  cj = cookielib.LWPCookieJar()
  try:
    cj.revert(cookie_file)
  except Exception, e:
    print e
  proxy_handler = urllib2.ProxyHandler({'http': 'http://%s:%s/' % (str(ip), str(port))})
  #opener = urllib2.build_opener(HTTPHandler=urllib2.HTTPCookieProcessor(cj),ProxyHandler=proxy_handler)
  opener = urllib2.build_opener(proxy_handler)
  urllib2.install_opener(opener)
  req = urllib2.Request(url)
  operate = opener.open(req)
  print operate.read()
  sys.exit()
  spandata = soup.find_all("div",class_="cont_font")[0].find("span")
  item_arr = spandata.text.split()
  for item in item_arr:
    temp  = item.replace(":", " ").replace("@", " ").split()
    if len(temp) != 3: continue
    ip    = temp[0]
    port  = temp[1]
    title = temp[2]
    thread = FetchProxyServerThread(ip, port, title)
    thread.start()

def testSocket(ip, port, title):
  '''
  socket连接测试
  '''
  print '正在测试socket连接...'
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  try:
    sock.settimeout(10)
    sock.connect((ip, int(port)))
    #sock.send('meta')
    sock.close()
    print title+'---'+ip+':'+port+'--status:ok'
    return 1
  except socket_error as serr: # connection error
    sock.close()
    print title+'---'+ip+':'+port+'--status:error--Connection refused.'
    return 0

if __name__ == '__main__':
  #if len(sys.argv) <= 1:
  #  url = raw_input('URL : ')
  #else:
    #url = sys.argv[1]
  url = "http://hidemyass.com/proxy-list/search-225414"
  for item in collection.find().sort("last_changed", -1):# 1 ASC,-1 DESC
    ip   = item['ip']
    port = item['port']
    title = item['title']
    # 此处要测试代理帐号是否可用
    if testSocket(ip, port, title) == 0:
      collection.remove({"ip":ip, "port":port})
      print '失效的帐号,已删除!---'+str(ip)+":"+str(port)
      continue
    else:
      fetchProxyServer(url, ip, port)
