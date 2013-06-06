#/usr/bin/python
# -*- coding: utf8 -*-

import httplib2
import socks # http://socksipy.sourceforge.net/
# http://code.google.com/p/httplib2/wiki/Examples

import pymongo,sys,re
import socket,time,mechanize,cookielib
import urllib2,urllib
from socket import error as socket_error
from bs4 import BeautifulSoup
import threading
import webbrowser
from selenium import webdriver #http://selenium-python.readthedocs.org/en/latest/installation.html
'''
selenium
https://pypi.python.org/pypi/selenium
http://www.51testing.com/?uid-437299-action-viewspace-itemid-816036
'''
# create connection
connection = pymongo.Connection('localhost', 27017)
# switch db
db = connection.proxy_server
# get collection
collection = db.proxy_server_collection

httplib2.debuglevel=0

urls = [
        #'http://adfoc.us/1521621',
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
  def __init__(self, h, url):
    threading.Thread.__init__(self)
    self.h   = h
    self.url = url
    pass
  def run(self):
    headers = { 'User-Agent' : 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)' }
    try:
      r,c = self.h.request(self.url,headers=headers)
      #r = self.h.open(self.url)
      print r
    except Exception,e:
      print 'self.h.request error ---- '
      print e
      

def mechanize_url(url, ip, port):
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
  br.set_debug_http(True)
  br.set_debug_redirects(True)
  br.set_debug_responses(True)
  br.addheaders = [('User-agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.1.11) Gecko/20100701 Firefox/3.5.11')]##模拟浏览器头
  # proxy
  br.set_proxies({"http":"%s:%s" % (str(ip),str(port))})
  br.open(url)
  result = br.response().read()
  new_url = re.compile(".src='(.*?)&size=").findall(result)[0]
  print br.geturl()
  for link in br.links():
    print link
    br.follow_link(link)
    br.back()
  #br.open(new_url)
  new_url += "&frame1&size=10x10&ref="+re.compile('name="site" src="(.*?)"').findall(result)[0]
  #br.open(new_url)
  #print br.geturl()
  #result = br.response().read()
  sys.exit()
  #req = urllib2.Request(url=new_url)
  #opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj),urllib2.ProxyHandler({str(ip):str(port)}))
  #f = opener.open(req)
  #print f.read()
  #response = urllib.urlopen(new_url, proxies = {str(ip):str(port)})
  #print response.geturl()


class SeleniumThread(threading.Thread):
  def __init__(self, profile, url):
    threading.Thread.__init__(self)
    self.profile = profile
    self.url     = url
    
  def run(self):
    try:
      dr = webdriver.Firefox(firefox_profile = self.profile)
      dr.get(self.url)
      dr.quit()
    except Exception,e:
      print e
    
def selenium_url(url, ip, port):
  #dr = webdriver.Chrome()
  profile = webdriver.FirefoxProfile()
  profile.set_preference("network.proxy.type",1)
  profile.set_preference("network.proxy.http",str(ip))
  profile.set_preference("network.proxy.http_port", int(port))
  profile.update_preferences()
  dr = webdriver.Firefox(firefox_profile = profile)
  dr.get(url)
  dr.quit()
  '''
  from selenium import webdriver
  PROXY = "23.23.23.23:3128" # IP:PORT or HOST:PORT
  chrome_options = webdriver.ChromeOptions()
  chrome_options.add_argument('--proxy-server=%s' % PROXY)
  chrome = webdriver.Chrome(chrome_options=chrome_options)
  chrome.get("http://whatismyipaddress.com")
  '''

profile = webdriver.FirefoxProfile()

for item in collection.find():
  ip   = item['ip']
  port = item['port']
  # 此处要测试代理帐号是否可用
  if testSocket(ip, port) == 0:
    print collection.remove({"ip":ip, "port":port})
    print '失效的帐号,已删除!---'+str(ip)+str(port)
    continue
  
  #proxy_handler = urllib2.ProxyHandler({'http': 'http://%s:%s/' % (str(ip),str(port))})
  #h = urllib2.build_opener(proxy_handler)
  #for url in urls:
  #url = 'http://2ad.in/gzwX'
  #url = 'http://adf.ly/Q5cxg'
  #url = "http://ye15ywn3.Lvvk.com/"
  #url = "http://richlink.com/app/webscr?cmd=_click&key=ye15ywn3"
  #thread = ProxyThread(h, url)
  #thread.start()
  #time.sleep(1)
  #mechanize_url(url, ip, port)
  #selenium_url(url, ip, port)
  #time.sleep(5)
  
  '''
  profile.set_preference("network.proxy.type",1)
  profile.set_preference("network.proxy.http",str(ip))
  profile.set_preference("network.proxy.http_port", int(port))
  profile.update_preferences()
  thread = SeleniumThread(profile, url)
  thread.start()
  print 'threading sleep 10 seconds.'
  time.sleep(10)
  '''
  

  #h = httplib2.Http(proxy_info = httplib2.ProxyInfo(socks.PROXY_TYPE_HTTP, ip, int(port)))
  #headers = { 'User-Agent' : 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)' }
  #r,c = h.request(url,headers=headers)
  #print r
  #print c
  #for url in urls:
  #  url = 'http://2ad.in/7oRP'
  #  thread = ProxyThread(h, url)
  #  thread.start()
  #  time.sleep(1)
  #time.sleep(10)
