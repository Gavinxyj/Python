from multiprocessing import Pool, Queue, Manager
from modules.workprocess import WorkProcess
from modules.outprocess import OutProcess
import threading
user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 MicroMessenger/6.5.2.501 NetType/WIFI WindowsWechat QBCore/3.43.691.400 QQBrowser/9.0.2524.400'

headers = {'User-Agent': user_agent}

class Scheduler(object):

    def __init__(self):
        self.workobject = WorkProcess(headers)
        self.outobject = OutProcess()
        self.queue = Manager().Queue(1024)

    def handle(self, filename):
        try:

            with open(filename) as fp:
                self.items = ['http://www.' + line.strip('\n') for line in fp.readlines()]
            
            print(self.items)
            threads = []
            thread_check = threading.Thread(target=self.check_domain, args=(self.queue, self.items))
           
            thread_out = threading.Thread(target=self.outobject.write_file, args=(self.queue,))
            
            threads.append(thread_check)
            threads.append(thread_out)

            for t in threads:
                t.setDaemon(True)
                t.start()

            while True:
                alive = False
                for t in threads:
                    alive = alive or t.isAlive()
                if not alive:
                    break
            print('handle exit...')
        except Exception as e:
            raise e

    def check_domain(self, queue, items):
        try:
            pool = Pool(processes=10)         
            for item in items:
                pool.map_async(self.workobject.notify_domain, [(queue, item)])
            pool.close()
            pool.join()
        except Exception as e:
            print(e)       