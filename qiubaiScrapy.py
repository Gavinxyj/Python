#!/usr/bin/env python

import urllib
import urllib2
import re
url = 'https://www.t66y.com/thread0806.php?fid=16'
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
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

