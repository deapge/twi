#/usr/bin/python
# -*- coding: utf8 -*-

'''
https://github.com/simplegeo/python-oauth2

http://www.tumblr.com/oauth/apps
http://www.tumblr.com/docs/en/api/v2
'''

import urlparse,sys
import httplib,urllib
import oauth2 as oauth

class APIClient(object):
  request_token_url = 'http://www.tumblr.com/oauth/request_token' # POST
  access_token_url  = 'http://www.tumblr.com/oauth/access_token' # POST
  authorize_url     = 'http://www.tumblr.com/oauth/authorize'
  def __init__(self,oauth_consumer_key, oauth_consumer_secret):
    self.oauth_consumer_key    = oauth_consumer_key
    self.oauth_consumer_secret = oauth_consumer_secret
    self.consumer = oauth.Consumer(oauth_consumer_key, oauth_consumer_secret)
    self.client = oauth.Client(self.consumer)

  # Step 1: Get a request token. This is a temporary token that is used for 
  # having the user authorize an access token and to sign the request to obtain 
  # said access token.
  # Step 2: Redirect to the provider. Since this is a CLI script we do not 
  # redirect. In a web application you would redirect the user to the URL
  # below.
  def get_authorize_url(self):
    # step 1:
    resp, content = self.client.request(self.request_token_url, "GET")
    if resp['status'] != '200':
        raise Exception("Invalid response %s." % resp['status'])
    self.request_token = dict(urlparse.parse_qsl(content))
    #print "Request Token:"
    #print "    - oauth_token        = %s" % self.request_token['oauth_token']
    #print "    - oauth_token_secret = %s" % self.request_token['oauth_token_secret']
    #print 
    # step 2:
    #print "Go to the following link in your browser:"
    return "%s?oauth_token=%s" % (self.authorize_url, self.request_token['oauth_token'])
    #print 

# After the user has granted access to you, the consumer, the provider will
# redirect you to whatever URL you have told them to redirect to. You can 
# usually define this in the oauth_callback argument as well.
#accepted = 'n'
#while accepted.lower() == 'n':
#    accepted = raw_input('Have you authorized me? (y/n) ')
#oauth_verifier = raw_input('What is the PIN? ')

# Step 3: Once the consumer has redirected the user back to the oauth_callback
# URL you can request the access token the user has approved. You use the 
# request token to sign this request. After this is done you throw away the
# request token and use the access token returned. You should store this 
# access token somewhere safe, like a database, for future use.
  def request_access_token(self, oauth_verifier):
    token = oauth.Token(self.request_token['oauth_token'],
        self.request_token['oauth_token_secret'])
    token.set_verifier(oauth_verifier)
    client = oauth.Client(self.consumer, token)
    
    resp, content = client.request(self.access_token_url, "POST")
    if resp['status'] != '200':
      raise Exception("Invalid response %s." % resp['status'])
    return dict(urlparse.parse_qsl(content))
  
  def set_access_token(self, oauth_token, oauth_token_secret):
    self.oauth_token = oauth_token
    self.oauth_token_secret = oauth_token_secret


