#/usr/bin/python
# -*- coding: utf8 -*-

'''
http://jeanphix.me/Ghost.py/ -- 同样的效果
http://stackoverflow.com/questions/13287490/is-there-a-way-to-use-phantomjs-in-python
npm -g install phantomjs
http://selenium-python.readthedocs.org/en/latest/api.html
http://stackoverflow.com/questions/14699718/how-do-i-set-a-proxy-for-phantomjs-ghostdriver-in-python-webdriver
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
      time.sleep(5)
      #driver.save_screenshot('bns.gameguyz.com.png') # save a screenshot to disk
      print "thead name:"+ self.thread_name + " ,response.title: "+ self.driver.title
    except Exception,e:
      print '--error--thread sleep 30 seconds...'
      print e
      time.sleep(30)
      self.driver.refresh()
      print e

service_args = [
    '--proxy=%s:%s' % ("190.93.243.166",80),
    '--proxy-type=http',
  ]
chromedriver = "/home/meadhu/Desktop/chromedriver"
#os.environ["webdriver.chrome.driver"] = chromedriver
#driver = webdriver.Chrome(chromedriver)
driver = webdriver.Chrome(executable_path=chromedriver, service_args = service_args)
driver.get("http://whatismyipaddress.com/")
time.sleep(10)
print driver.title
driver.quit()
sys.exit()



#if __name__ == '__main__':
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
  #driver = webdriver.PhantomJS(service_args=service_args)
  # 此处要测试代理帐号
  driver = webdriver.Chrome("/home/meadhu/Desktop/chromedriver1", )
  driver.set_window_size(1024, 768) # optional
  url = "http://adfoc.us/15216225581956" # http://www.baidu.com/
  for i in range(1, 2):
    print '正在开启线程:%d' % i
    thread = ProxyThread(driver, url, str(i))
    thread.start()
  driver.close()
  driver.quit()
  
  
  
  
'''
import os
chromedriver = "/home/meadhu/Desktop/chromedriver"
os.environ["webdriver.chrome.driver"] = chromedriver
#driver = webdriver.Chrome(chromedriver)
driver = webdriver.Chrome(executable_path=chromedriver)
driver.get("http://adfoc.us/15216225581956")
print driver.title
driver.quit()
sys.exit()
'''
  
