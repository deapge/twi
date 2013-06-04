# -*- coding: utf-8 -*-
'''
Created on Jul 29, 2011

@author: wangyouhua
'''

from t4py.tblog.tblog import TBlog
from t4py.tblog.constants import CONSUMER_KEY
from t4py.tblog.constants import CONSUMER_SECRET
from t4py.http.oauth import OAuthToken
from t4py.utils.token_util import TokenUtil

util = TokenUtil()
str = util.get_token_str('user_test')
t = TBlog(CONSUMER_KEY, CONSUMER_SECRET)
t._request_handler.access_token = OAuthToken.from_string(str)

print t.statuses_retweets({'id':'1112152297221206741', 'since_id':'-2551774633877939158'})