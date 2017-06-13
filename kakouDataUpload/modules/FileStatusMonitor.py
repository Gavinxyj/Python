#!/usr/bin/python
# -*- coding:utf-8 -*-
# @author   youjiang xie
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
from pyinotify import WatchManager, Notifier, \
    ProcessEvent, IN_DELETE, IN_CREATE, IN_MODIFY
from utils.QueueUtils import QueueUtils
import logging
logger = logging.getLogger("kakou.modules")


class EventHandler(ProcessEvent):

    createdFile = {}
    bFlag = False

    """事件处理"""
    def process_IN_CREATE(self, event):
        if not self.bFlag:
            filename = os.path.join(event.path, event.name)
            self.createdFile[filename] = 1

        if os.path.isfile(os.path.join(event.path, event.name)):
            try:
                logger.debug('input msg : %s' % os.path.join(event.path, event.name))
                QueueUtils.put_message(os.path.join(event.path, event.name))
            except Exception, e:
                logger.error('operator failed: %s' % e.message)

    def process_IN_DELETE(self, event):
        logger.debug('Delete file: %s' % os.path.join(event.path, event.name))

    def process_IN_MODIFY(self, event):
        pass

    @staticmethod
    def file_monitor(path='.'):
        wm = WatchManager()
        mask = IN_DELETE | IN_CREATE | IN_MODIFY
        notifier = Notifier(wm, EventHandler())
        wm.add_watch(path, mask, rec=True)
        logger.info('start monitor path: %s' % path)
        while True:
            try:
                notifier.process_events()
                if notifier.check_events():
                    notifier.read_events()
            except KeyboardInterrupt:
                logger.error('file monitor is over!')
                notifier.stop()
                break
