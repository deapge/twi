# -*- coding: utf-8 -*-
'''
Created on Jul 29, 2011

@author: wangyouhua
'''

import json

from t4py.tblog.tblog import TBlog
from t4py.tblog.constants import CONSUMER_KEY
from t4py.tblog.constants import CONSUMER_SECRET
from t4py.http.oauth import OAuthToken
from t4py.utils.token_util import TokenUtil

util = TokenUtil()
str = util.get_token_str('user_test')
t = TBlog(CONSUMER_KEY, CONSUMER_SECRET)
t._request_handler.access_token = OAuthToken.from_string(str)

friends = t.statuses_friends()
result = json.read(friends)    #get friends
for friend in result["users"]:    #Ĭ默认只返回30个关注列表
    print friend["name"].decode("utf-8") 