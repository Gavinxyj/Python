import threading
from .database.MySQLImpl import MySQLImpl
from .database.SqliteImpl import SqliteImpl
from .database.SqlalchemyImpl import SqlalchemyImpl

class OutThread(threading.Thread):
    """docstring for OutThread"""
    def __init__(self, out_queue):
        super(OutThread, self).__init__()

        self.out_queue = out_queue
        self.sqlite = SqliteImpl()

    def run(self):
        self.out_work()


    def out_work(self):
        while True:
            msg = self.out_queue.get()
            #print(msg)
            if msg:
                self.sqlite.insert_record(msg)
