#!/usr/bin/env python

import random import randint
from time import sleep
from Queue import Queue

def writeQ(queue):
    print 'producing object for Q...',
    queue.put('xxx', 1)
    print 'size now:', queue.qsize()

def readQ(queue):
    val = queue.get(1)
    print 'consumed object from Q... size now:', queue.qsize()
    
def writer(queue, loops):
    for index in range(loops):
        writeQ(queue)
        sleep(randint(1,3))

def reader(queue, loops):
    for index in range(loops):
        readQ(queue)
        sleep(randint(2,5))

funcs = [write, reader]
nfuncs = range(len(funcs))

def main():
    nloop = randint(2, 5)
    
    q = Queue(32)
    threads = []
    