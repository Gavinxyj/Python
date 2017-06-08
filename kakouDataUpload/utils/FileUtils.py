#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @author   youjiang xie
# @E-mail   xie_youjiang@163.com
# @time     2017/6/7 0007 9:21
# @project  Python
# @file     FileUtils

import os
import os.path
import shutil
import logging.config

logging.config.fileConfig('config/logging.conf')
logger = logging.getLogger("kakou")


class FileUtils(object):

    @staticmethod
    def copy_file(srcfile, desdir):
        try:
            path = os.path.split(desdir)
            if not os.path.exists(path[0]):
                os.makedirs(path[0])
            shutil.copy(srcfile, desdir)
        except shutil.Error, e:
            logger.error("shutil.Error %d: %s" % (e.args[0], e.args[1]))

    'Traverse all files in the directory'
    @staticmethod
    def scan_file(path, scanTime):
        array_list = []
        for parentdir, dirs, files in os.walk(path):
            for filename in files:
                fileTime = os.path.getmtime(os.path.join(parentdir, filename))
                if fileTime >= scanTime:
                    logger.debug('filename = %s' % os.path.join(parentdir, filename))
                    array_list.append(os.path.join(parentdir, filename))
        return array_list

    '''
    Delete the file before the specified time
    path: delete file path
    delTime: specified time, time format is mktime
    '''
    @staticmethod
    def del_file(path, delTime):
        try:
            for parentdir, dirs, files in os.walk(path):
                for fileName in files:
                    print fileName
                    fileTime = os.path.getmtime(os.path.join(parentdir, fileName))
                    if fileTime < delTime:
                        os.remove(os.path.join(parentdir, fileName))
                for name in dirs:
                    if os.listdir(os.path.join(parentdir, name)):
                        continue
                    else:
                        os.rmdir(os.path.join(parentdir, name))
        except OSError, e:
            logger.error("OSError %d: %s" % (e.args[0], e.args[1]))

if __name__ == '__main__':
    print '%02d' % int('1')
