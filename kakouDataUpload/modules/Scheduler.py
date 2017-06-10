#!/usr/bin/python
# -*- coding:utf-8 -*-
# @author   youjiang xie
# @E-mail   xie_youjiang@163.com
# @time     2017/6/9 0009 16:48
# @project  Python
# @file     Scheduler
import logging.config
import sys, signal, time
import json
import threading
from utils.ZkConfig import ZkConfig
from database.Connection import Connection
from common.Constant import ZOOKEEPER_ADDR, ZOOKEEPER_PATH
from FileStatusMonitor import EventHandler
from utils.FileUtils import FileUtils
from Carinfo import Carinfo
from TdmsTgs import TdmsTgs
from database.KafkaOperatorImpl import KafkaOperatorImpl
logging.config.fileConfig('config/logging.conf')
logger = logging.getLogger("kakou")


class Scheduler(object):

    def __init__(self):
        self.is_exit = False
        self.zkObj = ZkConfig(ZOOKEEPER_ADDR)

    def hander(self, signum):
        self.is_exit = True
        logger.info('receive a signal %d, is_exit = %d ' %(signum, self.is_exit))
        sys.exit()

    def do_scheduler(self):
        signal.signal(signal.SIGINT, self.handler)
        signal.signal(signal.SIGTERM, self.handler)
        # 从运维数据库获取卡口编号与路口编号映射关系
        TdmsTgs.get_record()
        '初始化数据库连接参数'
        Connection(self.get_zkconfig()['kakouFilter'])

        # start file monitor
        EventHandler.file_monitor(self.get_zkconfig()['kakouFilter']['listenPath'])

        # start scan file
        array_list = FileUtils.scan_file(self.get_zkconfig()['kakouFilter']['listenPath'], time.time() - self.get_zkconfig()['kakouFilter']['deleteTime'])

        # 实例化kafka连接
        kafkaConn = KafkaOperatorImpl(self.get_zkconfig()['kakouFilter']['kafka'])

        # 转换数据格式
        kafkaInfo = Carinfo.parser_format(array_list, TdmsTgs.mapdata)

        # 将转换后的消息发送到kafka队列里
        for item in kafkaInfo:
            logger.debug('strJson = %s' % item)
            kafkaConn.send_message(item)

        kafkaConn.producer.flush()

        EventHandler.bFlag = True
        EventHandler.createdFile.clear()

        # 开始一个删除文件线程
        threads = []

        thread = threading.Thread(target=self.del_file_thread, args=(self, []))
        threads.append(thread)
        for t in threads:
            t.setDaemon(True)
            t.start()

    def get_zkconfig(self):
        result = self.zkObj.get_data(ZOOKEEPER_PATH)
        if result:
            return json.loads(result[0])
        else:
            return None

    def del_file_thread(self):
        while True:
            curTime = time.time()
            path = self.get_zkconfig()['kakouFilter']['listenPath']
            deleteTime = self.get_zkconfig()['kakouFilter']['deleteTime']
            FileUtils.del_file(path, curTime - deleteTime * 60 * 60)
