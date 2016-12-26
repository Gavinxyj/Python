#!/usr/bin/env python

import threading
from time import sleep, ctime

loops = [4, 2]

def loop(nLoop, nsec):
    print 'start loop', nLoop, 'at:', ctime()
    sleep(nsec)
    print 'loop', nLoop, 'done at:', ctime()

def main():
    print 'starting at:', ctime()
    threads = []
    nLoops = range(len(loops))
    
    for index in nLoops:
        nThread = threading.Thread(target=loop, args = (index, loops[index]))
        threads.append(nThread)
    
    for index in nLoops:
        threads[index].start()
        
    for index in nLoops:
        threads[index].join()
        
    print 'all DONE at:', ctime()

if __name__ == '__main__':
    main()