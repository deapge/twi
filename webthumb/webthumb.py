#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
 调用生成图片的方法:
"""
from bluga import get_thumbnail_bluga
import os
from hashlib import md5
from datetime import datetime
now = datetime.now()
m = md5()

'''
生成图片
@param url 需要生成图片的网址
@param thumb_path 生成图片路径
@param type_style 使用哪个API去生成图片,默认为1(bluga)
'''
def generateThumb(url = 'http://www.gameguyz.com/',thumb_path = '/tmp/rossp_org.jpg', type_style = '1'):
  #url = 'http://www.rossp.org/'
  #thumb_path = '/home/meadhu/Desktop/rossp_org.jpg'
  m.update(url+now.strftime("%Y%m%d%H"))
  thumb_path = '/tmp/'+m.hexdigest()+'.jpg'
  if os.path.isfile(thumb_path) == True:
    print '使用已经存在的图片...';
    return thumb_path
  print '正在生成图片...';
  result = {
            '1' : lambda x,y: get_thumbnail_bluga(x,y),
            '2' : lambda x,y: ''
            }[type_style](url, thumb_path)
  #result = get_thumbnail(url, thumb_path)
  print '图片生成成功!!!';
  print '图片路径:'+thumb_path;
  if result == True:
    return thumb_path
  else:
    print False
