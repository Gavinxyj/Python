#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @author   youjiang xie
# @E-mail   xie_youjiang@163.com
# @time     2017/6/7 0007 9:21
# @project  Python
# @file     FileUtils

import sys, shutil
import os
import os.path
import hashlib


def md5_sum(filename):
    if not os.path.isfile(filename):
        return None

    myhash = hashlib.md5()
    f = file(filename, 'rb')

    while True:
        b = f.read(8096)
        if not b :
            break

        myhash.update(b)

    f.close()
    return myhash.hexdigest()

def do_patch(src_path, dest_path):
    print 'do patch'

    for rt, dirs, files in os.walk(src_path):
        for f in files:
            src_file = os.path.join(rt, f)
            dest_file = dest_path + '/' + '/' + f

            print 'src_file: %s, dest_file: %s' % (src_file, dest_file)

            if not os.path.exists(dest_file):
                print 'make dir: %s' % dest_path + '/' 
                #os.makedirs(os.path.join(dest_path, dirs))

            src_sum = md5_sum(src_file)
            dest_sum = md5_sum(dest_file)

            print 'src_sum: %s, dest_sum: %s' % (src_sum, dest_sum)
            if src_sum != dest_sum:
                print 'md5 is different!'
                #shutil.copy(src_file, dest_file)

if __name__ == '__main__':
    do_patch('/data/source/20170617', '/data/img/20170617')
