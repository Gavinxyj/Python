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

    @staticmethod
    def get_queue():
        if QueueUtils._queueObj:
            return QueueUtils._queueObj
        else:
            QueueUtils._queueObj = Queue.Queue(10240)
            return QueueUtils._queueObj

    @staticmethod
    def get_message():
        queue = QueueUtils.get_queue()
        if not queue.empty():
            return queue.get()

    @staticmethod
    def put_message(msg):
        queue = QueueUtils.get_queue()
        if queue:
            queue.put(msg)

