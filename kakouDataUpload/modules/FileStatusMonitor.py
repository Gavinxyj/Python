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
import logging
logger = logging.getLogger("kakou.modules")


class EventHandler(ProcessEvent):

    createdFile = {}
    bFlag = False
    _fileutils = None
    _jsonobj = None
    _carinfo = None
    _kafkaconn = None
    _tdms_tgs = None
    _redis = None
    _timeutils = None
    _array_list = []

    @staticmethod
    def init_params(**args):
        EventHandler._fileutils = args['fileutils']
        EventHandler._jsonobj = args['jsonobj']
        EventHandler._carinfo = args['carinfo']
        EventHandler._kafkaconn = args['kafkaconn']
        EventHandler._tdms_tgs = args['tdmstgs']
        EventHandler._redis = args['redis']
        EventHandler._timeutils = args['timeutils']

    """事件处理"""
    def process_IN_CREATE(self, event):
        if not self.bFlag:
            filename = os.path.join(event.path, event.name)
            self.createdFile[filename] = 1

        if os.path.isfile(os.path.join(event.path, event.name)):
            try:
                logger.debug('Create file :%s' % os.path.join(event.path, event.name))
                EventHandler._array_list.append(os.path.join(event.path, event.name))
                strJson = EventHandler._carinfo.parser_format(EventHandler._array_list, EventHandler._tdms_tgs.mapdata)

                if strJson:
                    EventHandler._kafkaconn.send_message(strJson[0])
                    EventHandler._kafkaconn.producer.flush()

                dest_dir = EventHandler._jsonobj['kakouFilter']['destDir'] + '/' + EventHandler._carinfo.dest_dir_format(event.name)
                EventHandler._fileutils.copy_file(os.path.join(event.path, event.name), dest_dir)
                curFileTime = EventHandler._timeutils.get_format_time(os.path.getmtime(os.path.join(event.path, event.name)), '%Y-%m-%d %H:%M:%S')
                EventHandler._redis.setkey('scanPoint', curFileTime)

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
