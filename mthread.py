#!/usr/bin/env python

import threading
import thread
from time import sleep, ctime

exitFlag = 0
class myThread(threading.Thread):
    def __init__(self, func, args, name = ''):
        threading.Thread.__init__(self)
        self.args     = args
        self.name     = name
        self.func     = func
    def run(self):
        
        self.res = self.func(*self.args)
        
def print_time(threadName, delay, counter):
		
    while counter:
        sleep(delay)
        print '%s: %s' % (threadName, ctime())
        counter -= 1
        if counter == 0:
            thread.exit()
        
print print_time.__name__        
thread1 = myThread(print_time, ('Thread-1', 1, 5), print_time.__name__)
thread2 = myThread(print_time, ('Thread-2', 1, 5), print_time.__name__)

thread1.start()
thread2.start()

print 'Exiting Main Thread'