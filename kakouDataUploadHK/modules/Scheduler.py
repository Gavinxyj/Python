#!/usr/bin/python
# -*- coding:utf-8 -*-
# @author   youjiang xie
# @E-mail   xie_youjiang@163.com
# @time     2017/6/9 0009 16:48
# @project  Python
# @file     Scheduler


import logging
import os
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
from utils.FtpUtils import FtpUtils
from CarInfo import CarInfo
from TdmsTgs import TdmsTgs
from database.KafkaOperatorImpl import KafkaImpl
from database.RedisOperatorImpl import RedisImpl
from FrmStatus import FrmStatus
from RoadInfo import RoadInfo
from utils.QueueUtils import QueueUtils
from VehPass import VehPass

logger = logging.getLogger("kakou.modules")


class Scheduler(object):
    _bFlag = False

    def __init__(self):
        self.is_exit = False
        self.zkObj = ZkConfig(ZOOKEEPER_ADDR)
        self.jsonObj = self.get_zkconfig()
        self.redis = RedisImpl(self.jsonObj['kakouFilter']['redis-cluster']['startup_nodes'])
        # 实例化kafka连接
        self.kafkaConn = KafkaImpl(self.jsonObj['kakouFilter']['kafka'])

    def handler(self, signum, frame):
        self.is_exit = True
        self.zkObj.close()
        self.kafkaConn.close()
        print 'receive a signal %d, is_exit = %d ' % (signum, self.is_exit)
        logger.info('receive a signal %d, is_exit = %d ' % (signum, self.is_exit))
        sys.exit()

    def do_scheduler(self):
        signal.signal(signal.SIGINT, self.handler)
        signal.signal(signal.SIGTERM, self.handler)

        '初始化数据库连接参数'
        Connection.init_conn(self.jsonObj['kakouFilter'])

        '初始化Ftp连接参数'
        FtpUtils.init_conn(self.jsonObj['kakouFilter'])

        # 从运维数据库获取卡口编号与路口编号映射关系
        TdmsTgs.get_record()
        # 取二期卡口的字段记录
        FrmStatus.get_all_record()
        # 去二期卡口的道路信息
        RoadInfo.get_all_record()
        # start file monitor
        # EventHandler.file_monitor(self.jsonObj['kakouFilter']['listenPath'])

        # pdb.set_trace()
        # start scan file
        scantime = self.redis.getkey('scanPointHik')
        if scantime is not None:
            scantime = TimeUtils.get_longtime(scantime[:-4], '%Y-%m-%d %H:%M:%S')
        else:
            scantime = 0

        deletetime = self.jsonObj['kakouFilter']['deleteTime']
        # array_list = ['/data/source/20170807/13/835081001000/835081001022_20170807134809913_\xe5\x86\x80B7723F_2_2_1_93_1_6023_B_2_3_1.jpg']
        # VehPass.insert_data(array_list)

        threads = []
        # 文件状态监听线程
        monitor_thread = threading.Thread(target=EventHandler.file_monitor, args=(self.jsonObj['kakouFilter']['listenPath']['hik'],))
        
        # 文件扫描线程
        scan_thread = threading.Thread(target=FileUtils.scan_file, args=(self.jsonObj['kakouFilter']['listenPath']['hik'], scantime))

        # 发送kafka队列线程
        kafka_thread = threading.Thread(target=self.deal_monitor_file)

        # 文件删除线程
        del_thread = threading.Thread(target=self.del_file_by_time, args=(self.jsonObj['kakouFilter']['listenPath']['hik'], scantime, deletetime))

        # 数据库插入，ftp上传线程
        for index in range(1):
            ftp_threads = threading.Thread(target=self.ftp_thread_proc, args=(index,))
            threads.append(ftp_threads)

        threads.append(monitor_thread)
        threads.append(scan_thread)
        threads.append(kafka_thread)
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
  
    def del_file_by_time(self, path, scantime, deletetime):
        """[summary]
        
        [delete files by time thread]
        
        Arguments:
            path {[string]} -- [delete files path]
            scantime {[string]} -- [current scan files time]
            deletetime {[string]} -- [delete how long time files]
        """
        # 第一次启动只允许删除上次扫描点之前的文件
        cur_time = scantime

        while True:
            time.sleep(60 * 60)
            logger.info('delete file thread start')
            if cur_time == 0:
                cur_time = time.time()
            FileUtils.del_file(path, cur_time - deletetime * 60 * 60)
            cur_time = time.time()
            logger.info('delete file thread end')

    def deal_monitor_file(self):
        while True:
            try:
                filename = QueueUtils.get_message('kafka')
                # filename = '20170824/08/635061100136/635031013136_20170828141234520_冀B2673U_蓝_9_3_0_1_13093_Z_1_1_H_467.jpg'
                if filename:
                    logger.debug('thread-monitor get queue msg : %s queue-size: %d' % (filename, QueueUtils.get_queue('kafka').qsize()))

                    # array_list = []
                    # array_list.append(filename)

                    # 发送到kafka
                    strJson = CarInfo.parser_format(filename, TdmsTgs.mapdata)
                    if strJson:
                        self.kafkaConn.send_message(strJson)
                        self.kafkaConn.producer.flush()
                        # 复制一份到本地另一个目录下
                        dest_filepath = CarInfo.dest_dir_format(json.loads(strJson))
                        dest_dir = self.jsonObj['kakouFilter']['destDir'] + '/' + dest_filepath
                        FileUtils.copy_file(filename[:-3] + 'jpg', dest_dir)
                        logger.info('the file has been copied to dest_dir: %s' % dest_dir)
                        curFileTime = TimeUtils.get_format_time(os.path.getmtime(filename), '%Y-%m-%d %H:%M:%S')
                        self.redis.setkey('scanPointHik', curFileTime)
                        logger.debug('thread-monitor send kafka and copy file is complete!')

            except Exception, e:
                logger.error('deal_monitor_file is failed %s' % e.message)

    # ftp,数据库处理线程
    def ftp_thread_proc(self, thread_id):
        while True:
            filename = QueueUtils.get_message('ftp')
            if filename:
                try:
                    if filename[-3:] == 'ini':
                        logger.debug('thread-%d get queue msg : %s queue-size: %d' % (thread_id, filename, QueueUtils.get_queue('ftp').qsize()))
                        # 上传文件到宇视的ftp服务器
                        ftp_path = VehPass.filename_format(filename)
                        logger.debug('thread-%d Ftp upload file: %s' % (thread_id, ftp_path))
                        FtpUtils.upload_file(filename[:-3] + 'jpg', '/' + ftp_path)
                        logger.debug('thread-%d Ftp file: %s is upload complete!' % (thread_id, os.path.basename(filename)))
                        # 写入宇视的数据库
                        logger.debug('thread-%d insert database operator start!' % thread_id)
                        VehPass.insert_data(filename)
                        logger.debug('thread-%d insert database operator complete! filename: %s' % (thread_id, filename))
                except Exception, e:
                    logger.error('thread-%d ftp upload failed %s, filename: %s' % (thread_id, e.message, filename))
