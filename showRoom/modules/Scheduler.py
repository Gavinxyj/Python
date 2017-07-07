#!/usr/bin/python
# -*- coding:utf-8 -*-
# @author   youjiang xie
# @E-mail   xie_youjiang@163.com
# @time     2017/6/9 0009 16:48
# @project  Python
# @file     Scheduler


import logging
import os, time
import pdb
import sys, signal, time
import cx_Oracle
from database.Connection import Connection
from database.KafkaOperatorImpl import KafkaImpl
from utils.QueueUtils import QueueUtils
from VehPass import VehPass
import threading
logger = logging.getLogger("kakou.modules")


class Scheduler(object):

    is_exit = False

    def __init__(self):
        args = {'url': '192.168.102.142:9092,192.168.102.143:9092,192.168.102.144:9092', 'topic': 'traffic-record-test1'}
        self.kafkaConn = KafkaImpl(args)

    def handler(self, signum, frame):
        self.is_exit = True
        time.sleep(1)
        print 'receive a signal %d, is_exit = %d ' % (signum, self.is_exit)
        logger.info('receive a signal %d, is_exit = %d ' % (signum, self.is_exit))
        sys.exit()

    def do_scheduler(self):
        signal.signal(signal.SIGINT, self.handler)
        signal.signal(signal.SIGTERM, self.handler)

        subscriptionInsert = Connection.get_conn_hik().subscribe(callback=self.OnChanges,\
                                 operations=cx_Oracle.OPCODE_INSERT, rowids=True)

        subscriptionInsert.registerquery('select * from TRAFFIC_VEHICLE_PASS')

        threads = []
        # 数据处理线程
        deal_thread = threading.Thread(target=self.deal_data)
        threads.append(deal_thread)

        for t in threads:
            t.setDaemon(True)
            t.start()

        while True:
            alive = False
            for t in threads:
                alive = alive or t.isAlive()

            if not alive:
                break

    def OnChanges(self, message):
        for table in message.tables:
            if table.rows is None or table.operation & cx_Oracle.OPCODE_ALLROWS:
               pass
            else:
                for row in table.rows:
                    QueueUtils.put_message(row.rowid)

    def deal_data(self):
        #try:
        while True and not self.is_exit:
            msg = QueueUtils.get_message()
            if msg:
                row = VehPass.query_data_by_rowid(msg)
                if row:
                    strJson = VehPass.parser_format(row[0])
                    if strJson:
                        self.kafkaConn.send_message(strJson)
                        self.kafkaConn.producer.flush()

        #except Exception, e:
        #    logger.error('deal_data failed, msg : %s error: %s' % (row[0], e.message))

