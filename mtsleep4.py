#!/usr/bin/env python

import threading
from time import sleep, ctime

loops = [4,2]

class ThreadFunc(object):
    def __init__(self, func, args, name = ''):
        self.name = name
        self.func = func
        self.args = args
    def __call__(self):
        self.res = self.func(*self.args)
    
def loop(nloop, nsec):
    print 'start loop', nloop, 'at:', ctime()
    sleep(nsec)
    print 'loop', nloop, 'done at:', ctime()
    
def main():
    print 'starting at:', ctime()
		    
    threads = []
    nloops  = range(len(loops))
    
    for index in nloops:
        nThread = threading.Thread(target = ThreadFunc(loop, (index, loops[index]), loop.__name__))
        threads.append(nThread)
        
    for index in nloops:
        threads[index].start()
        
    for index in nloops:
        threads[index].join()
    
    print 'all DONE at:', ctime()		    
        
if __name__ == '__main__':
    main()    
        