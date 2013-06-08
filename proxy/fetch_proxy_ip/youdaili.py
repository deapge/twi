#/usr/bin/python
# -*- coding:utf8 -*-

'''
采集最新的代理服务器信息,并存储在mongodb数据库中.
http://www.youdaili.cn/Daili/

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
  response = urllib.urlopen(url)
  result = response.read()
  soup = BeautifulSoup(result)
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
  if len(sys.argv) <= 1:
    print ('Usage: python youdaili.py URL')
  else:
    fetchProxyServer(sys.argv[1])
