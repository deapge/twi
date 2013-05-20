#!/usr/bin/python
# -*- coding: utf-8 -*-

# 507607854

from qqweibo import *
import webbrowser,os
import time

def post_qq_weibo(params = []):
  app_key = '100705728'
  app_secret = '14e99e32a8bcca9c129b095ce62d9a01'
  init(app_key, app_secret)   # 设置AppKey和AppSecret(只需初始化一次)
  token = OAuthToken.get_request_token()  # 获取未授权的request token
  print "正在打开浏览器...,请在打开的浏览器中授权访问此应用!"
  webbrowser.open(token.get_authorize_url())  # 进入用户授权页面
  verifier = raw_input("授权码(Input the verifier): ").strip() 
  token.set_verifier(verifier)    # 设置授权码，并自动换取access token
  ret_params = []
  for item in params:
    title = item.get('title').replace(' ','-')
    pic = item.get('pic', '')
    ret_item = {}
    ret_item['title'] = title
    if len(pic)>0:
      result = t.add_pic(token, content = title, pic=pic) # 发表一条带图片的微博
      ret_item['created_at'] = result.data.time
      ret_item['id'] = result.data.id
    else:
      result = t.add(token, content = title) # 发表一条微博信息
      ret_item['created_at'] = result.data.time
      ret_item['id'] = result.data.id
    print result
    ret_params.append(ret_item)
    print 'time sleep 20 seconds...'
    time.sleep(20)
  #print simplejson.dumps(ret_params, indent=4)
  return ret_params

if __name__ == '__main__':
  app_key = '100705728'
  app_secret = '14e99e32a8bcca9c129b095ce62d9a01'
  init(app_key, app_secret)   # 设置AppKey和AppSecret(只需初始化一次)
  token = OAuthToken.get_request_token()  # 获取未授权的request token
  webbrowser.open(token.get_authorize_url())  # 进入用户授权页面
  verifier = raw_input("Input the verifier: ").strip() 
  token.set_verifier(verifier)    # 设置授权码，并自动换取access token
  t.add(token, content = u'测试发微博') # 发微博