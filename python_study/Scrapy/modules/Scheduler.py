from .AccessThread import AccessThread
from .WorkThreads import WorkThreads
from .OutThread import OutThread
import queue

class Scheduler(object):

    def __init__(self):
        self.work_queue = queue.Queue()
        self.out_queue = queue.Queue()
        
    def handle(self):
        threads = []
        dict_info = {}
        dict_info['url'] = 'https://www.qiushibaike.com/8hr/page/'
        dict_info['headers'] = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 MicroMessenger/6.5.2.501 NetType/WIFI WindowsWechat QBCore/3.43.691.400 QQBrowser/9.0.2524.400'}

        acc_thread = AccessThread(self.work_queue, dict_info)
        
        for _ in range(10):
            work_thread = WorkThreads(self.work_queue, self.out_queue)
            threads.append(work_thread)
        
        out_thread = OutThread(self.out_queue)

        threads.append(acc_thread)
        threads.append(out_thread)

        for t in threads:
            t.daemon = True
            t.start()

        while True:
            alive = False
            for t in threads:
                alive = alive or t.is_alive()

            if not alive:
                break

            
            
            


    