#/usr/bin/python
# -*- coding: utf8 -*-

'''
chromedriver 安装步骤
1.下载http://code.google.com/p/chromedriver/downloads/list, chromedriver_linux64_2.0.zip
  http://code.google.com/p/selenium/wiki/ChromeDriver
2.将chromedriver 复制到 $PATH 任意路径下
3.如果不复制的话:
chromedriver = "/home/meadhu/Desktop/chromedriver"
desired_capabilities = {
                        'javascriptEnabled':True,
                        'proxy':{'proxyType':'manual', 'httpProxy':'190.75.77.188:8080'}
                        }
#driver = webdriver.Chrome(executable_path=chromedriver, desired_capabilities = desired_capabilities)

http://jeanphix.me/Ghost.py/ -- 同样的效果
http://stackoverflow.com/questions/13287490/is-there-a-way-to-use-phantomjs-in-python
npm -g install phantomjs
http://selenium-python.readthedocs.org/en/latest/api.html
http://stackoverflow.com/questions/14699718/how-do-i-set-a-proxy-for-phantomjs-ghostdriver-in-python-webdriver

python 设置代理
http://stackoverflow.com/questions/14699718/how-do-i-set-a-proxy-for-phantomjs-ghostdriver-in-python-webdriver
http://stackoverflow.com/questions/17117802/how-to-assign-to-workers-a-proxy-that-requires-user-name-password-and-a-custom
'''

import httplib2,os
import socks # http://socksipy.sourceforge.net/
import pymongo,sys,re
import socket,time,cookielib
import urllib2,urllib
from datetime import datetime
from socket import error as socket_error
import threading
from selenium import webdriver
# DesiredCapabilities API :  http://code.google.com/p/selenium/wiki/DesiredCapabilities
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

# create connection
connection = pymongo.Connection('localhost', 27017)
# switch db
db = connection.proxy_server
# get collection
#collection = db.proxy_server_collection
collection = db.proxy_server_usa

# http://adfoc.us/

httplib2.debuglevel=0

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
    print title+'--'+ip+':'+port+'--status:ok'
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
      time.sleep(5)
      print "thead name:"+ self.thread_name + " ,response.title: "+ self.driver.title
    except Exception,e:
      print '--error--thread sleep 10 seconds...'
      print e
      time.sleep(10)
      self.driver.refresh()
    
# PhantomJS threading
def method1(url, desired_capabilities):
    driver = webdriver.PhantomJS(desired_capabilities = desired_capabilities)
    i = 0
    for item in db.short_urls.find({"domain":"adfoc.us"}).sort("_id", -1):# 1 ASC,-1 DESC
      i += 1
      url = item['short_link']
      print '正在开启线程:%s' % i
      thread = ProxyThread(driver, url, str(i))
      thread.start()
      if i%5 == 4:
        print '当前5个进程同时进行,线程等待 20 秒.'
        time.sleep(20)
    driver.close()
    driver.quit()

# 单个URL处理
def method21(url, desired_capabilities):
    try:
      driver = webdriver.PhantomJS(desired_capabilities = desired_capabilities)
      if True:
        driver.get(url)
        print driver.title
      driver.close()
      driver.quit()
    except Exception,e:
      print e

# proxy
def method4(url, desired_capabilities):
    try:
      proxy_handler = urllib2.ProxyHandler({'http': 'http://%s:%s/' % (str(ip), str(port))})
      opener = urllib2.build_opener(proxy_handler)
      # This time, rather than install the OpenerDirector, we use it directly:
      f = opener.open(url)
      print f.read()
    except Exception,e:
      print e
    pass
  
if __name__ == '__main__':
  if len(sys.argv) < 2:
    url = raw_input('请输入URL: ')
  else:
    url = sys.argv[1]
  
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
      collection.update({"ip":ip, "port":port}, {"$set": {"last_changed": str(datetime.now())}})
    # 此处要测试代理帐号
    desired_capabilities = {
                          'javascriptEnabled':True,
                          'proxy':{'proxyType':'manual', 'httpProxy':'%s:%s' % (str(ip),str(port))},
                          'phantomjs.page.settings.userAgent':"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_5) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.95 Safari/537.11"
                          }
    '''
    dcap = dict(DesiredCapabilities.PHANTOMJS)
dcap["phantomjs.page.settings.userAgent"] = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/53 "
    "(KHTML, like Gecko) Chrome/15.0.87"
)
driver = webdriver.PhantomJS(desired_capabilities=dcap)
    '''
    method1(url, desired_capabilities)
    #method21(url, desired_capabilities)
