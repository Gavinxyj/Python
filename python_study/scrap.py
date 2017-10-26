#!/usr/bin/env python

import urllib
from urllib import request
import re

'''
url = 'https://www.baidu.com'
user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 MicroMessenger/6.5.2.501 NetType/WIFI WindowsWechat QBCore/3.43.691.400 QQBrowser/9.0.2524.400'
headers = {'User-Agent': user_agent}
try:
    req = request.Request('http://www.zzhfks.com', headers=headers)
    response = request.urlopen(req, timeout=2)
    #content = response.read().decode('utf-8')
    #ret = re.findall(r"<div class='article block untagged mb15[\s\S]*?</span>([\s\S]*?)</span>", re.S)
    print (response.getcode())
except Exception as e:
   print(e)

'''
temp = ('a', 'b', 'c')
for value, index in enumerate(temp, 1):
	print(value, index)
