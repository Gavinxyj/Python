#!/usr/bin/env python

import urllib
import urllib2
import re
url = 'http://image.baidu.com/search/index?tn=baiduimage&ipn=r&ct=201326592&cl=2&lm=-1&st=-1&fm=result&fr=&sf=1&fmq=1482479984154_R&pv=&ic=0&nc=1&z=&se=1&showtab=0&fb=0&width=&height=&face=0&istype=2&ie=utf-8&word=%E7%BE%8E%E5%A5%B3&f=3&oq=meinv+&rsp=0'
user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
headers = {'User-Agent' : user_agent}
try:
    request  = urllib2.Request(url, headers = headers)
    response = urllib2.urlopen(request)
    content  = response.read().decode('utf-8')
    pattern  = re.compile('<img.*?src="(.*?)"',re.S)
    items = re.findall(pattern,content)
    #print items
    for item in items:
        print item               
except urllib2.URLError, e:
    if hasattr(e, 'code'):
        print e.code
    if hasattr(e, 'reason'):
        print e.reason 