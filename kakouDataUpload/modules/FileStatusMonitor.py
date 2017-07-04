#!/usr/bin/python
# -*- coding:utf-8 -*-
# @author   youjiang xie
# @modified hwasin 2017/06/19
# @E-mail   xie_youjiang@163.com
# @time     2017/6/9 0009 16:55
# @project  Python
# @file     FileStatusMonitor
import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)
import os
import pyinotify
from utils.QueueUtils import QueueUtils
import logging
logger = logging.getLogger("kakou.modules")


class EventHandler(pyinotify.ProcessEvent):

    createdFile = {}
    bFlag = False

    """事件处理"""
    def process_IN_CREATE(self, event):
        if os.path.isdir(event.pathname):
            logger.debug('event name:'+event.maskname+',dir ' + event.pathname + ' is created.')
        else:
            logger.debug('event name:'+event.maskname+',file ' + event.pathname + ' is created.')

        '''
        print 'input msg : %s' % os.path.join(event.path, event.name)
        if not self.bFlag:
            filename = os.path.join(event.path, event.name)
            self.createdFile[filename] = 1

        if os.path.isfile(os.path.join(event.path, event.name)):
            try:
                logger.debug('input msg : %s' % os.path.join(event.path, event.name))
                #QueueUtils.put_message(os.path.join(event.path, event.name))
            except Exception, e:
                logger.error('operator failed: %s' % e.message)
        '''

    def process_IN_DELETE(self, event):
        logger.debug('Delete file: %s' % os.path.join(event.path, event.name))

    def process_IN_MODIFY(self, event):
        pass

    def process_IN_CLOSE_WRITE(self, event):
        logger.debug('Close write file: %s' % event.pathname)
        try:
            logger.debug('input msg : %s' % event.pathname)
            QueueUtils.put_message(event.pathname)
        except Exception, e:
            logger.error('operator failed: %s' % e.message)

    @staticmethod
    def file_monitor(path='.'):
        wm = pyinotify.WatchManager()
        mask = pyinotify.IN_CLOSE_WRITE | pyinotify.IN_DELETE | pyinotify.IN_CREATE | pyinotify.IN_MODIFY
        notifier = pyinotify.Notifier(wm, EventHandler())
        try:
            wm.add_watch(path, mask, rec=True, auto_add=True)
        except pyinotify.WatchManagerError as err:
            logger.warn(err)
            logger.warn(err.wmd)

        logger.info('start monitor path: %s' % path)
        notifier.loop()
