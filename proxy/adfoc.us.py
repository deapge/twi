#/usr/bin/python
# -*- coding: utf8 -*-

import httplib2
import socks # http://socksipy.sourceforge.net/
import pymongo,sys,re
import socket,time,cookielib
import urllib2,urllib
from socket import error as socket_error
from bs4 import BeautifulSoup
import threading
import mechanize

# create connection
connection = pymongo.Connection('localhost', 27017)
# switch db
db = connection.proxy_server
# get collection
collection = db.proxy_server_collection

httplib2.debuglevel=0

urls = [
        'http://adfoc.us/15216225404658'
        ]

def testSocket(ip, port):
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
    print ip+':'+port+'--status:ok'
    return 1
  except socket_error as serr: # connection error
    sock.close()
    print ip+':'+port+'--status:error--Connection refused.'
    return 0

class ProxyThread(threading.Thread):
  def __init__(self, opener, url):
    threading.Thread.__init__(self)
    self.opener = opener
    self.url    = url
    pass
  def run(self):
    try:
      self.opener.open(url)
    except Exception,e:
      print 'self.h.request error ---- '
      print e

for item in collection.find():
  ip   = item['ip']
  port = item['port']
  # 此处要测试代理帐号是否可用
  if testSocket(ip, port) == 0:
    print collection.remove({"ip":ip, "port":port})
    print '失效的帐号,已删除!---'+str(ip)+str(port)
    continue
  test_url = "http://adfoc.us/15216225404658"
  
  # sock
  httplib2.debuglevel=0
  h = httplib2.Http(proxy_info = httplib2.ProxyInfo(socks.PROXY_TYPE_HTTP, str(ip), int(port)))
  try:
    r,c = h.request(test_url)
    print r
  except Exception,e:
    print e
  continue
  
  #模拟浏览器的过程
  br = mechanize.Browser()
  cj = cookielib.LWPCookieJar()
  br.set_cookiejar(cj)##关联cookies
  ###设置一些参数，因为是模拟客户端请求，所以要支持客户端的一些常用功能，比如gzip,referer等
  br.set_handle_equiv(True)
  #br.set_handle_gzip(True)
  br.set_handle_redirect(True)
  br.set_handle_referer(True)
  br.set_handle_robots(False)
  br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=30)
  ###这个是degbug##你可以看到他中间的执行过程，对你调试代码有帮助
  #br.set_debug_http(True)
  #br.set_debug_redirects(True)
  #br.set_debug_responses(True)
  br.addheaders = [('User-agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.1.11) Gecko/20100701 Firefox/3.5.11')]##模拟浏览器头
  # proxy
  br.set_proxies({"http":"%s:%s" % (str(ip),str(port))})
  try:
    br.open(test_url)
    print br.response().info()
  except Exception,e:
    print e
  
  
'''
  # urllib2.urlopen()
  test_url = "http://adfoc.us/15216225404658"
  proxy_handler = urllib2.ProxyHandler({"http" : "http://%s:%s/" % (str(ip), str(port))})
  opener = urllib2.build_opener(proxy_handler)
  try:
    urllib2.install_opener(opener)
    #opener.open(test_url)
    urllib2.urlopen(test_url).read()
  except Exception,e:
    print e
  for url in urls:
    pass
    #thread = ProxyThread(opener, url)
    #thread.start()
    #time.sleep(6)
    
'''    
    
    
    
    
    
    
    
    
    
    
    
    
