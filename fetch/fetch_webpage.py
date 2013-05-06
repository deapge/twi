#!/usr/bin/python
# -*- coding:utf-8 -*-

from bs4 import BeautifulSoup
import re,sys
import urllib

# Get a file-like object for the Python Web site's home page.
f = urllib.urlopen("http://www.python.org")
# Read from the object, storing the page's contents in 'html'.
html = f.read()
f.close()
#soup = BeautifulSoup(html)
soup = BeautifulSoup(''.join(html))

# 采集 gameguyz.com
# 大眼睛

