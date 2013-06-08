#/usr/bin/python
# -*- coding:utf8 -*-

'''
遍历mongodb数据库,测试所有的ip连接是否正常,
  如果不正常的话,删除此IP地址.
'''

import pymongo,sys
import urllib
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

class CheckProxyServerThread(threading.Thread):
  def __init__(self, ip, port):
    threading.Thread.__init__(self)
    self.ip    = ip
    self.port  = port
  
  def run(self):
    if testSocket(self.ip, self.port) == 1:# 服务器帐号信息正常,存储起来
      print 'IP正常!--%s:%s' % (str(self.ip), str(self.port))
    else:
      collection.remove({"ip":"self.ip", "port":str(self.port)})
      print 'IP连接失败!--%s:%s' % (str(self.ip), str(self.port))
    pass

def checkProxyServer():
  for item in collection.find().sort({"last_changed":1}):
    thread = CheckProxyServerThread(item['ip'], item['port'])
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
  checkProxyServer()
