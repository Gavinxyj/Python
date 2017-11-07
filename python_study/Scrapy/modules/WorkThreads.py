import threading
import re, os
from urllib import request

class WorkThreads(threading.Thread):
    """docstring for WorkThreads"""
    def __init__(self, work_queue, out_queue):
        super(WorkThreads, self).__init__()
        self.work_queue = work_queue
        self.out_queue = out_queue

    def run(self):
        self.deal_work()

    def deal_work(self):
        while True:
            content = self.work_queue.get()
            if content:
               
                pattern = re.compile(r'<div class="article block untagged mb15[\s\S]*?class="stats-vote".*?</div>', re.S)
                userinfos = re.findall(pattern, content)
                
                if userinfos:
                    pattern = re.compile(r'<a href="(.*?)".*?<h2>(.*?)</h2>.*?<div class="content">(.*?)</div>.*?<i class="number">(.*?)</i>', re.S)

                    picture = re.compile(r'<div class="thumb">.*?src="(.*?)"', re.S)

                    for userinfo in userinfos:
                        item = re.findall(pattern, userinfo)
                        pictures = re.findall(picture, userinfo)
                        try:
                            if item:
                                infos = []
                                userid, name, content, num = item[0]
                                # 去掉换行符，<span></span>，<br/>符号
                                userid = re.sub(r'\n|<span>|</span>|<br/>', '', userid)
                                name = re.sub(r'\n|<span>|</span>|<br/>', '', name)
                                content = re.sub(r'\n|<span>|</span>|<br/>|\x01', '', content)
                                
                                if pictures:
                                    path = './users/'
                                    if not os.path.exists(path):
                                        os.makedirs(path)

                                    request.urlretrieve('http:' + pictures[0], path + os.path.basename(pictures[0]))
                                    infos.append((userid, name, int(num), content, pictures[0]))
                                    self.out_queue.put((userid, name, int(num), content, pictures[0]))
                                else:
                                    infos.append((userid, name, int(num), content, ' '))
                                    self.out_queue.put((userid, name, int(num), content, ' '))
                                   
                        except Exception as e:
                            print(e)