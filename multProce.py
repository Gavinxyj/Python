#!/usr/bin/env python

import multiprocessing
from time import sleep, ctime
import os
class myProcess(multiprocessing.Process):
    def __init__(self, counter, lock):
        multiprocessing.Process.__init__(self)
        self.counter = counter
        self.lock    = lock
    def run(self):
        print_counter(self.pid, self.counter, lock)

def print_counter(pid, counter, lock):
    while counter:
        #sleep(1)
        lock.acquire()
        print 'pid = %d, counter = %d' % (pid, counter)
        lock.release()
        counter -= 1

if __name__ == '__main__':
    lock = multiprocessing.Lock()
    for index in range(5):
        p = myProcess(50000, lock)
        p.daemon = True       
        p.start()
        p.join()
        
    print 'Main process ended!'