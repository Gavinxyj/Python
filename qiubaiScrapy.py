#!/usr/bin/env python

import urllib
import urllib2
import re
url = 'http://www.qiushibaike.com/'
user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
headers = {'User-Agent': user_agent}
try:
    request = urllib2.Request(url, headers = headers)
    response = urllib2.urlopen(request)
    content = response.read().decode('utf-8')


    pattern  = re.compile('<div class="article block untagged mb15".*?<h2>(.*?)</h2>.*?class="content".*?<span>(.*?)</span>',re.S)
    items = re.findall(pattern,content)
    print items
    for item in items:
        print item[0], item[1]
except urllib2.URLError, e:
    if hasattr(e, 'code'):
        print e.code
    if hasattr(e, 'reason'):
        print e.reason

