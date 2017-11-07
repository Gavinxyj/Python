import threading
from urllib import request
from urllib import error

class AccessThread(threading.Thread):
    """docstring for AccessThread"""
    def __init__(self, work_queue, args):
        super(AccessThread, self).__init__()
        self.args = args
        self.work_queue = work_queue

    def run(self):
        self.request_url()

    def request_url(self):
        try:
            for page in range(1, 14):

                req = request.Request(self.args['url'] + str(page), headers=self.args['headers'])
                print(self.args['url'] + str(page))
                # 打开一个请求
                response = request.urlopen(req)
                # 读取服务器返回的页面数据内容
                content = response.read().decode('utf-8')
                self.work_queue.put(content)

        except error.URLError as e:
            print(e.reason)
