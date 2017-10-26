
import os
from urllib import request
import logging
logger = logging.getLogger("notify_domain.modules")
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
pc_headers = {'User-Agent': user_agent}

class WorkProcess(object):

    def __init__(self,headers):
        self.headers = headers


    def notify_domain(self, *item):
        #print('pid = %d, item = %s' % (os.getpid(), item[0][1]))
        queue = item[0][0]
        url = item[0][1]
        try:
            req = request.Request(url, headers=self.headers)

            response = request.urlopen(req)
            if response.getcode() == 200:
                print('queue-size = %d' % queue.qsize())
                queue.put('success='+ url)
            
        except Exception as e:
            try:
                req = request.Request(url, headers=pc_headers)

                response = request.urlopen(req)
                if response.getcode() == 200:
                    queue.put('pc_useable=' + url)
            except Exception as e:
                logging.error('error-msg = %s, url = %s' % (e, url))
                queue.put('error='+ url)
            
        
