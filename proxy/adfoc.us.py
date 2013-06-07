#/usr/bin/python
# -*- coding: utf8 -*-

'''
http://jeanphix.me/Ghost.py/ -- 同样的效果
http://stackoverflow.com/questions/13287490/is-there-a-way-to-use-phantomjs-in-python
npm -g install phantomjs
http://selenium-python.readthedocs.org/en/latest/api.html
http://stackoverflow.com/questions/14699718/how-do-i-set-a-proxy-for-phantomjs-ghostdriver-in-python-webdriver
'''

import httplib2
import socks # http://socksipy.sourceforge.net/
import pymongo,sys,re
import socket,time,cookielib
import urllib2,urllib
from datetime import datetime
from socket import error as socket_error
import threading
from selenium import webdriver

# create connection
connection = pymongo.Connection('localhost', 27017)
# switch db
db = connection.proxy_server
# get collection
collection = db.proxy_server_collection

httplib2.debuglevel=0

urls = [
        'http://adfoc.us/15216225404658',
        'http://adfoc.us/15216225572533',
        'http://adfoc.us/15216225575507',
        'http://adfoc.us/15216225575508',
        'http://adfoc.us/15216225575509'
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
  def __init__(self, driver, url, thread_name):
    threading.Thread.__init__(self)
    self.driver = driver
    self.url    = url
    self.thread_name = thread_name
    pass
  def run(self):
    try:
      self.driver.get(self.url)
      #driver.save_screenshot('bns.gameguyz.com.png') # save a screenshot to disk
      print "thead name "+ self.thread_name + self.driver.title
    except Exception,e:
      print '--error--thread sleep 30 seconds...'
      time.sleep(30)
      self.driver.refresh()
      print e

short_url_cols = db.short_urls

for item in collection.find():
  ip   = item['ip']
  port = item['port']
  # 此处要测试代理帐号是否可用
  if testSocket(ip, port) == 0:
    print collection.remove({"ip":ip, "port":port})
    print '失效的帐号,已删除!---'+str(ip)+str(port)
    continue
  else:
    print collection.update({"ip":ip, "port":port}, {"$set": {"last_changed": str(datetime.now())}})
  
  service_args = [
    '--proxy=%s:%s' % (ip,port),
    '--proxy-type=http',
  ]
  driver = webdriver.PhantomJS(service_args=service_args)
  driver.set_window_size(200, 300) # optional
  i = 0
  for item in short_url_cols.find():
    url = item['short_link']
    thread = ProxyThread(driver, url, str(i))
    thread.start()
    print 'thread sleep 5 seconds ...'
    time.sleep(5)
    print '---'+str(i)+'----------'+str(datetime.now())+'------------------'
    print url
    i += 1
    if i == 50:
      print 'thread sleep 15 seconds ...'
      time.sleep(20)
      i = 0
  
  driver.close()
  driver.quit()
  
