#/usr/bin/python
# -*- coding: utf8 -*-

'''
post twitter tweets
https://github.com/ryanmcgrath/twython
'''
from twython import Twython
import time
from webthumb.common import *

consumer_key        = 'qQYnSN2PkHD23431uwzDQA'
consumer_secret     = 'WjvqjjMk27TaVEBd7FBiDgY1b6ZufvYlYwU55EqsgI'
access_token_key    = '1083534500-QIw2lwUZ20cmUKF9li70b9QoBYoC74KMVlLmZWQ'
access_token_secret = 'tyyT7OdEcx9XZrVbITKt8IcaRhTfhSgkQLAXQ4IrI'
t = Twython(consumer_key, consumer_secret,
            access_token_key, access_token_secret)

# The file key that Twitter expects for updating a status with an image
# is 'media', so 'media' will be apart of the params dict.

# You can pass any object that has a read() function (like a StringIO object)
# In case you wanted to resize it first or something!
def post_twitter_tweets(params = []):
  for item in params:
    max_len = 140 - len(item.get('link',''))
    status_str  = item.get('title')[:max_len]+" "+item.get('link','')
    if item.get('pic', ''):
      photo = open(downLoadImg(item['pic']), 'rb')
      ret = t.update_status_with_media(media=photo, status=status_str)
    else:
      ret = t.update_status(status=status_str)
    print 'time sleepping(seconds): 2'
    time.sleep(2)
    print "Post success! Created at : "+ret['created_at']

'''
if __name__ == '__main__':
    params = []
    item = {}
    item['title'] = u'gameguyz.com bns http://www.gameguyz.com/pictures/cos/harlequin-s-doll-cosplay-with-tight-silk.html'
    item['pic']   = '/home/meadhu/Desktop/girl.jpg'
    params.append(item)
    print post_twitter_tweets(params)
'''