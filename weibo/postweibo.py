#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
发weibo方法
  params = []
  item = {}
  item['title'] = "titlesafaf"
  item['pic'] = 'picasdfas'
  params.append(item)
  for item in params:
    print item['title']
'''
from sinaweibopy.sinaweibo import post_weibo_sina
from qqweibopy.postqqweibo import post_qq_weibo
from twpython.posttwitter  import post_twitter_tweets
from tumblrpy.postTumblr   import post_tumblr
from webthumb.common       import *

def notifySend():
  from gi.repository import Notify
  Notify.init ("Weibo Post Status")
  Hello=Notify.Notification.new ("Weibo Post Status","Weibo Post Finished.","dialog-information")
  Hello.show ()

def postWeibo(params = []):
  post_tumblr(params)
  if testSocket('api.twitter.com','80') == 1:
    post_twitter_tweets(params)
  post_weibo_sina(params)
  post_qq_weibo(params)
  notifySend()
  pass


if __name__ == '__main__':
  params = []
  item = {}
  item['title'] = u'google pic33q'
  item['pic']   = '/home/meadhu/Desktop/173628426.jpg'
  params.append(item)
  #print post_twitter_tweets(params)
  print postWeibo(params)
  notifySend()
  pass
