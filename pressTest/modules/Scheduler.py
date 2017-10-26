import threading

class Scheduler(object):

    def do_scheduler(self, obj):
        threads = []
        
        for index in range(10):
            work_thread = threading.Thread(target=obj.handle)
            threads.append(work_thread)
        for t in threads:
            t.setDaemon(True)
            t.start()

        while True:
            alive = False
            for t in threads:
                alive = alive or t.isAlive()

            if not alive:
                break