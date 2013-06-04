# -*- coding: utf-8 -*-
'''
Created on Jul 28, 2011

@author: wangyouhua
'''


from __future__ import with_statement  
import ConfigParser 
from t4py.tblog.constants import ACCESS_TOKEN_FILE 

'''
This class is used for getting or setting oauth access token credentials to configuration file
'''
class TokenUtil:
    def __init__(self):
        self.config = ConfigParser.ConfigParser()  
    
    def get_token(self, user_id):
        self.config.readfp(open(ACCESS_TOKEN_FILE))
        return self.config.get(user_id, 'oauth_token')

    def get_token_secret(self, user_id):
        self.config.readfp(open(ACCESS_TOKEN_FILE))
        return self.config.get(user_id, 'oauth_token_secret')
    
    def get_token_str(self, user_id):
        self.config.readfp(open(ACCESS_TOKEN_FILE))
        return self.config.get(user_id, 'token_str')

    def add_token(self, user_id, token, secret):
        self.config.add_section(user_id)
        self.config.set(user_id, 'oauth_token', token)
        self.config.set(user_id, 'oauth_token_secret', secret)
        self.config.write(open(ACCESS_TOKEN_FILE, 'a'))

    def update_token(self, user_id, token, secret):
        self.config.read(ACCESS_TOKEN_FILE)
        self.config.set(user_id, 'oauth_token', token)
        self.config.set(user_id, 'oauth_token_secret', secret)
        self.config.write(open(ACCESS_TOKEN_FILE, 'r+'))
    
    def add_token_str(self, user_id, token_str):
        self.config.add_section(user_id)
        self.config.set(user_id, 'token_str', token_str)
        self.config.write(open(ACCESS_TOKEN_FILE, 'a'))

    def update_token_str(self, user_id, token_str):
        self.config.read(ACCESS_TOKEN_FILE)
        self.config.set(user_id, 'token_str', token_str)
        self.config.write(open(ACCESS_TOKEN_FILE, 'r+'))  