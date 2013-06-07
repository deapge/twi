#/usr/bin/python
# -*- coding: utf8 -*-

#import vkontakte
#vk = vkontakte.API('3692412', '9ZpAti3w0N0TPUFLiKM0')
#print vk.getServerTime()

# 登陆 浏览器登陆vk


import sys,re,urllib2,urllib,cookielib,json,simplejson
from bs4 import BeautifulSoup

class VK(object):
  def __init__(self, name, pwd, cookie_file):
    self.name = name
    self.pwd  = pwd
    self.cookie_file = cookie_file
    self.cj = cookielib.LWPCookieJar()
    try:
      self.cj.revert(self.cookie_file)
    except Exception, e:
      print e
    self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj))
    urllib2.install_opener(self.opener)
    
  # get cookie
  def get_cookie(self):
    req = urllib2.Request('http://vk.com/')
    self.operate = self.opener.open(req)
    self.cj.save(self.cookie_file)
    
  def login(self):
    # step 1: get cookie
    self.get_cookie()
    # seep 2: login
    params = {
              'act':'login',
              'role':'al_frame',
              'expire':'',
              'captcha_sid':'',
              'captcha_key':'',
              '_origin':'http://vk.com',
              'ip_h':'f8f429a811ecab6599',
              'email':self.name,
              'pass':self.pwd,
              }
    self.opener.addheaders = [('User-agent','Opera/9.23')]
    req = urllib2.Request(
                          'https://login.vk.com/?act=login',
                          urllib.urlencode(params)
                          )
    self.operate = self.opener.open(req)
    self.cj.save(self.cookie_file)
    
    # upload an image
    self.opener.addheaders = [("Content-type", "application/x-www-form-urlencoded; charset=UTF-8")]
    req = urllib2.Request(
                          'http://vk.com/album213448865_000?act=add',
                          urllib.urlencode({
                                            'photo':open('/home/meadhu/Desktop/delete-icon.png'),
                                            })
                          )
    self.operate = self.opener.open(req)
    print self.operate.read()
    
    # check login ??
    #req = urllib2.Request("http://vk.com/feed")
    #self.operate = self.opener.open(req)
    #response = self.operate.read()
    #soup = BeautifulSoup(response)
    #print soup.prettify()

name = 'meadhu1@yahoo.com'
pwd  = 'meadhu1!@#'
cookie_file = 'vk.cookie'
vk = VK(name,pwd,cookie_file)
vk.login()



