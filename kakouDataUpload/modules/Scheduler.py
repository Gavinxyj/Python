#!/usr/bin/python
# -*- coding:utf-8 -*-
# @author   youjiang xie
# @E-mail   xie_youjiang@163.com
# @time     2017/6/9 0009 16:48
# @project  Python
# @file     Scheduler


import logging.config
import pdb
import sys, signal, time
import json
import threading
from utils.ZkConfig import ZkConfig
from utils.TimeUtils import TimeUtils
from database.Connection import Connection
from common.Constant import ZOOKEEPER_ADDR, ZOOKEEPER_PATH
from FileStatusMonitor import EventHandler
from utils.FileUtils import FileUtils
from CarInfo import CarInfo
from TdmsTgs import TdmsTgs
from database.KafkaOperatorImpl import KafkaImpl
from database.RedisOperatorImpl import RedisImpl

logging.config.fileConfig('config/logging.conf')
logger = logging.getLogger("kakou")


class Scheduler(object):

    def __init__(self):
        self.is_exit = False
        self.zkObj = ZkConfig(ZOOKEEPER_ADDR)
        self.jsonObj = self.get_zkconfig()
        self.redis = RedisImpl(self.jsonObj['kakouFilter']['redis-cluster']['startup_nodes'])

    def handler(self, signum, frame):
        self.is_exit = True
        print 'receive a signal %d, is_exit = %d ' % (signum, self.is_exit)
        logger.info('receive a signal %d, is_exit = %d ' % (signum, self.is_exit))
        sys.exit()

    def do_scheduler(self):
        signal.signal(signal.SIGINT, self.handler)
        signal.signal(signal.SIGTERM, self.handler)

        '初始化数据库连接参数'
        Connection.init_conn(self.jsonObj['kakouFilter'])

        # 从运维数据库获取卡口编号与路口编号映射关系
        TdmsTgs.get_record()

        # start file monitor
        # EventHandler.file_monitor(self.jsonObj['kakouFilter']['listenPath'])

        # pdb.set_trace()
        # start scan file
        scantime = self.redis.getkey('scanPoint')
        if scantime is not None:
            scantime = TimeUtils.get_longtime(scantime[:-4], '%Y-%m-%d %H:%M:%S')
        else:
            scantime = 0

        threads = []

        # 文件状态监听线程
        monitor_thread = threading.Thread(target=EventHandler.file_monitor, args=(self.jsonObj['kakouFilter']['listenPath'],))

        # 文件扫描线程
        scan_thread = threading.Thread(target=self.scan_file, args=(self.jsonObj['kakouFilter']['listenPath'], scantime))

        # 文件删除线程
        del_thread = threading.Thread(target=self.del_file_by_time)

        threads.append(monitor_thread)
        threads.append(scan_thread)
        threads.append(del_thread)

        for t in threads:
            t.setDaemon(True)
            t.start()

        while True:
            alive = False
            for t in threads:
                alive = alive or t.isAlive()

            if not alive:
                break

    def get_zkconfig(self):
        result = self.zkObj.get_data(ZOOKEEPER_PATH)
        if result:
            return json.loads(result[0])
        else:
            return None

    def del_file_by_time(self):
        while True:
            curTime = time.time()
            path = self.jsonObj['kakouFilter']['listenPath']
            deleteTime = self.jsonObj['kakouFilter']['deleteTime']
            FileUtils.del_file(path, curTime - deleteTime * 60 * 60)

    def scan_file(self, path, scantime):

        array_list = FileUtils.scan_file(path, scantime)
        # 转换数据格式
        kafkaInfo = CarInfo.parser_format(array_list, TdmsTgs.mapdata)

        # 实例化kafka连接
        kafkaConn = KafkaImpl(self.jsonObj['kakouFilter']['kafka'])

        # 将转换后的消息发送到kafka队列里

        for item in kafkaInfo:
            logger.debug('strJson = %s' % item)
            # kafkaConn.send_message(item)

        kafkaConn.producer.flush()

        EventHandler.bFlag = True
        EventHandler.createdFile.clear()

