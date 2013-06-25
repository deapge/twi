#/usr/bin/python
# -*- coding:utf8 -*-

'''
采集最新的代理服务器信息,并存储在mongodb数据库中.
http://spys.ru/free-proxy-list/us/

此文件功能：
  1.用来从代理服务器页面中获取 代理帐号，并测试，将测试通过帐号存储到mongodb中;
  2.检测代理帐号是否正常连接，使用多线程，不正常的，删除掉。
'''

import pymongo,sys
import urllib,urllib2
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
collection = db.proxy_server_collection

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

def fetchProxyServer(url):
  '''
   抓取proxy server 信息
  '''
  variables = {
               'OneSixZeroFive^Five6Six'          : '0',
               'EightSixSixZero^ThreeFourNine'    : '1',
               'SevenOneFiveTwo^Six5Two'          : '2',
               'ThreeSevenSevenSix^FiveFiveEight' : '3',
               'FiveFiveFourOne^Nine3Four'        : '4',
               'NineOneThreeSeven^Eight5Zero'     : '5',
               'Eight3NineNine^One7Five'          : '6',
               'Nine8OneEight^NineSixOne'         : '7',
               'Four1TwoThree^Zero3Seven'         : '8',
               'FourNineEightFour^SixZeroThree'   : '9'
               }
  headers = { 'User-Agent' : 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)' }
  req = urllib2.Request(url, headers = headers)
  response = urllib2.urlopen(req)
  result = response.read()
  soup = BeautifulSoup(result)
  trdata = soup.find_all("tr",class_=re.compile("spy1x"))
  for item in trdata[2:]:
    td = item.find_all("td")
    temp = td[0].find_all("font",class_="spy14")[0].text.split('document.write("<font class=spy2>:<\\/font>"')
    ip    = temp[0]
    port  = temp[1]
    for key in variables.keys():
      print port.replace(key, "aa")
    
    port  = temp[1]
    title = temp[2]
    thread = FetchProxyServerThread(ip, port, title)
    thread.start()

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

if __name__ == '__main__':
  url = "http://spys.ru/free-proxy-list/us/"
  fetchProxyServer(url)
  for i in range(1,4):
    url = "http://spys.ru/free-proxy-list%d/US/" % i
    fetchProxyServer(url)
