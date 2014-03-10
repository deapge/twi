#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Created on Apr 26, 2013
发weibo函数
@author: meadhu
'''
import sys,os
path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(path)

from webthumb.webthumb import generateThumb
from weibo.postweibo import postWeibo
import simplejson
from settings import *
from hashlib import md5
from datetime import datetime
now = datetime.now()
m = md5()

if __name__ == '__main__':
    params = []
    for site in site_lists:
      print site.get('site_url')
      #m.update(site.get('site_url')+now.strftime("%Y%m%d%H"))
      #thumb_path = '/tmp/'+m.hexdigest()+'.jpg'
      #if os.path.isfile(thumb_path) == False:
        #thumb_path = generateThumb(site.get('site_url'), thumb_path)
      thumb_path = generateThumb(site.get('site_url'))
      item = {}
      item['title'] = now.strftime("%Y-%m-%d")+site.get('site_title')+site.get('site_url')
      item['pic']   = thumb_path
      params.append(item)
    ret_params = postWeibo(params)
    print simplejson.dumps(ret_params, indent=4)
