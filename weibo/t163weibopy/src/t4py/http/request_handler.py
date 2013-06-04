"""
The MIT License

Copyright (c) 2011 t.163.com

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

from urllib2 import Request, urlopen
from t4py.tblog.tblog_exception import TBlogException
import httplib
import urllib
import mimetypes
import oauth
import os

class RequestHandler(object):
    """API request handler"""
    def __init__(self, consumer_key, consumer_secret):
        self._consumer = oauth.OAuthConsumer(consumer_key, consumer_secret)
        self._sign_method = oauth.OAuthSignatureMethod_HMAC_SHA1()    # API suggests to use "HMAC_SHA1" signature method
        self.request_token = None
        self.access_token = None
    
    def _update_request_token(self):
        request_token_url = 'http://api.t.163.com/oauth/request_token'
        request = oauth.OAuthRequest.from_consumer_and_token(self._consumer, http_url=request_token_url)
        request.sign_request(self._sign_method, self._consumer, None)
        resp = urlopen(Request(request_token_url, headers=request.to_header()))
        self.request_token = oauth.OAuthToken.from_string(resp.read())
    
    def _pack_image(self, filename, contentname):
        maxsize = 2048
        try:
            if os.path.getsize(filename) > (maxsize * 1024):
                raise TBlogException('File is too big, must be less than %s.' % str(maxsize))
        except os.error:
            raise TBlogException('Unable to access file')
        
        file_type = mimetypes.guess_type(filename)
        if file_type is None:
            raise TBlogException('Could not determine file type')
        file_type = file_type[0]
        if file_type not in ['image/gif', 'image/png', 'image/bmp', 'image/jpeg', 'image/pjpeg']:
            raise TBlogException('Invalid file type for image: %s' % file_type)
        
        fp = open(filename, 'rb')
        body = []
        body.append('--t163py')
        body.append('Content-Disposition: form-data; name="' + contentname +'"; filename="%s"' % filename)
        body.append('Content-Type: %s' % file_type)
        body.append('Content-Transfer-Encoding: binary')
        body.append('')
        body.append(fp.read())
        body.append('--t163py--')
        body.append('')
        fp.close()        
        body.append('--t163py--')
        body.append('')
        body = '\r\n'.join(body)
        # build headers
        headers = {
            'Content-Type': 'multipart/form-data; boundary=t163py',
            'Content-Length': len(body)
        }
        return headers, body
    
    def get_auth_url(self, callback_url):
        auth_url = 'http://api.t.163.com/oauth/authorize'
        if callback_url != None:
            auth_url = 'http://api.t.163.com/oauth/authenticate'
        self._access_token_url = 'http://api.t.163.com/oauth/access_token'
        self._update_request_token()
        request = oauth.OAuthRequest.from_token_and_callback(self.request_token, http_url=auth_url, callback=callback_url)
        return request.to_url()
    
    def get_request_token(self):
        self._update_request_token()
        return self.request_token
    
    def update_access_token(self, pin):
        request = oauth.OAuthRequest.from_consumer_and_token(self._consumer, self.request_token, http_url=self._access_token_url,verifier=str(pin))
        request.sign_request(self._sign_method, self._consumer, self.request_token)
        resp = urlopen(Request(self._access_token_url, headers=request.to_header()))
        self.access_token = oauth.OAuthToken.from_string(resp.read())
        return self.access_token
    
    def get_access_token(self,pin):
        self.update_access_token(pin)
        return self.access_token
    
    def send_request(self, url, http_method, parameters, post_data=None, headers={}):
        if len(parameters)> 0:
            if http_method == 'GET':
                    url = '%s?%s' % (url, urllib.urlencode(parameters))
            else:
                headers.setdefault('User-Agent','python')
                if post_data is None:
                    headers.setdefault('Accept','text/html')
                    headers.setdefault('Content-Type','application/x-www-form-urlencoded')
                    post_data = urllib.urlencode(parameters)
        request = oauth.OAuthRequest.from_consumer_and_token(self._consumer, http_url="http://api.t.163.com"+url, http_method=http_method, token=self.access_token,parameters=parameters)
        request.sign_request(self._sign_method, self._consumer, self.access_token)
        headers.update(request.to_header())
        conn = httplib.HTTPConnection('api.t.163.com')
        conn.request(http_method, url, headers=headers, body=post_data)
        resp = conn.getresponse()
        result = resp.read()
        conn.close()
        return result
    
    def send_upload_image_request(self, url, http_method, filename, contentname, parameters):
        headers, post_data = self._pack_image(filename, contentname)
        return self.send_request(url, http_method, parameters=parameters, post_data=post_data, headers=headers)
    
