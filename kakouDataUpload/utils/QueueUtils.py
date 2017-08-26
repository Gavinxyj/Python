#!/usr/bin/python
# -*- coding:utf-8 -*-
# @author   youjiang xie
# @E-mail   xie_youjiang@163.com
# @time     2017/6/12 0012 22:59
# @project  Python
# @file     QueueUtils
import Queue

class QueueUtils(object):

    _queueObj = None
    _queue_ftp = None

    @staticmethod
    def get_queue(types):
        if types == 'ftp':
            if QueueUtils._queue_ftp:
                return QueueUtils._queue_ftp
            else:
                QueueUtils._queue_ftp = Queue.Queue(10240)
                return QueueUtils._queue_ftp
        else:
            if QueueUtils._queueObj:
                return QueueUtils._queueObj
            else:
                QueueUtils._queueObj = Queue.Queue(10240)
                return QueueUtils._queueObj

    @staticmethod
    def get_message(types):
        queue = QueueUtils.get_queue(types)
        if not queue.empty():
            return queue.get()

    @staticmethod
    def put_message(msg, types):
        queue = QueueUtils.get_queue(types)
        if queue:
            queue.put(msg)

