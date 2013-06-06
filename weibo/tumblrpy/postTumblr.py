#/usr/bin/python
# -*- coding:utf8 -*-

# https://github.com/tumblr/pytumblr

import webbrowser,sys,time
import pytumblr
from Thumblr import *

def get_oauth_authorize_code():
  APP_KEY    = 'N15tNNUlFhCdgBhQv3t6Xf3fy0novQfEwyRPu4DqXPPCHD9zUt'
  APP_SECRET = 'ocWe4FHxBboBTkbx8ewatdXYDBRqave3sK1fqno6HZMxYdSmWS'
  client = APIClient(oauth_consumer_key=APP_KEY, oauth_consumer_secret=APP_SECRET)
  url = client.get_authorize_url()
  print "正在打开浏览器...,请在打开的浏览器中授权访问此应用!"
  print url
  webbrowser.open(url)  # 进入用户授权页面
  # 获取URL参数code: d7af087da275a410ba4067faf8274ea3
  r = client.request_access_token(raw_input("input code:").strip())  
  client = pytumblr.TumblrRestClient(
      APP_KEY,
      APP_SECRET,
      r['oauth_token'],
      r['oauth_token_secret'],
  )
  return client

def post_tumblr(params = []):
  client = get_oauth_authorize_code()
  data = client.info()
  name = data['user']['name'] # 获取 name
  for item in params:
    body = '<a target="_blank" href="%s">%s</a>' % (item['link'], item['title'])
    try:
      # 发送一条文字消息
      ret = client.create_text(name, body=body)
      print "文字发送状态: "
      print ret
      if len(item.get('pic', '')) > 0:
        # 发送一张图片
        ret = client.create_photo(name, source=item['pic'])
        print "发送图片状态: "
        print ret
      time.sleep(5)
    except Exception,e:
      print e

if __name__ == '__main__':
  params = []
  item = {}
  item['title'] = u'Test oauth pic link 2'
  item['link']  = 'http://www.gameguyz.com'
  item['pic']   = 'http://www.djparty.org/sitebuildercontent/sitebuilderpictures/.pond/fgsdf2.jpg.w300h201.jpg'
  params.append(item)
  post_tumblr(params)
  #print post_weibo_sina(u'测试OAuth 2.0带图片发微博http://www.gameguyz.com','/home/meadhu/Desktop/173628426.jpg')
  pass


