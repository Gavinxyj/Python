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
from violation import Violation

logger = logging.getLogger("kakou.modules")


class Scheduler(object):
    _bFlag = False
    dict_filename = {}
    count = 0
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

        items = Violation.get_all_record()

        
        for item in items:
            filepath = os.path.basename(item[1])
            values = filepath.split('_')
            filename = '%d' % int(item[0]) + '_' + values[3] + '_' + values[0] + '_0.jpg'
            filename2 = '%d' % int(item[0]) + '_' + values[3] + '_' + values[0] + '_1.jpg'
            filename3 = '%d' % int(item[0]) + '_' + values[3] + '_' + values[0] + '_2.jpg'
            self.dict_filename[filename] = item[1]
            self.dict_filename[filename2] = item[2]
            self.dict_filename[filename3] = item[3]
        print len(self.dict_filename)
        threads = []
        ftp_threads = threading.Thread(target=self.ftp_thread_proc)
        threads.append(ftp_threads)
        
        scantime = TimeUtils.get_longtime('2017-09-07 00:00:00', '%Y-%m-%d %H:%M:%S')
         # 文件扫描线程
        #pdb.set_trace()
        scan_thread = threading.Thread(target=FileUtils.scan_file, args=('/data/img/20170907', scantime))
        # 数据库插入，ftp上传线程
        
        
        
        threads.append(scan_thread)
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
        curTime = scantime

        while True:
            time.sleep(60 * 60)
            logger.info('delete file thread start')
            FileUtils.del_file(path, curTime - deletetime * 60 * 60)
            curTime = time.time()
            logger.info('delete file thread end')

    def scan_file(self, path, scantime):
        try:
            array_list = FileUtils.scan_file(path, scantime)
            '''
            # 转换数据格式
            kafkaInfo = CarInfo.parser_format(array_list, TdmsTgs.mapdata)

            # 将转换后的消息发送到kafka队列里

            for item in kafkaInfo:
                self.kafkaConn.send_message(item)

            self.kafkaConn.producer.flush()

            for item in array_list:
                filename = os.path.split(item)[1]
                if filename:
                    dest_dir = CarInfo.dest_dir_format(filename)
                    if dest_dir:
                        FileUtils.copy_file(item, self.jsonObj['kakouFilter']['destDir'] + '/' + dest_dir)
            '''

            # 插入到数据库
            # pdb.set_trace()
            logger.debug('array_list len = %d' % len(array_list))

            for item in array_list:
                try:
                    # 上传文件到宇视的ftp服务器
                    ftpPath = VehPass.filename_format(os.path.basename(item))
                    logger.debug('Ftp upload file: %s' % ftpPath)
                    FtpUtils.upload_file(item, '/' + ftpPath)
                    # 写入宇视的数据库
                    array_temp = []
                    array_temp.append(item)
                    VehPass.insert_data(array_temp)
                except Exception, e:
                    logger.error('ftp upload failed %s, filename: %s' % (e.message, item))
            # Scheduler._bFlag = True
            EventHandler.bFlag = True
            EventHandler.createdFile.clear()
        except Exception, e:
            logger.error('scan_file is failed %s, len = %d' % (e.message, len(array_list)))

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
                        self.kafkaConn.send_message(strJson[0])
                        self.kafkaConn.producer.flush()

                    # 复制一份到本地另一个目录下
                    dest_filepath = CarInfo.dest_dir_format(os.path.basename(filename))
                    dest_dir = self.jsonObj['kakouFilter']['destDir'] + '/' + dest_filepath
                    FileUtils.copy_file(filename, dest_dir)
                    curFileTime = TimeUtils.get_format_time(os.path.getmtime(filename), '%Y-%m-%d %H:%M:%S')
                    self.redis.setkey('scanPoint', curFileTime)
                    logger.debug('thread-monitor send kafka and copy file is complete!')

            except Exception, e:
                logger.error('deal_monitor_file is failed %s' % e.message)

    # ftp,数据库处理线程
    def ftp_thread_proc(self):
        while True:
            filename = QueueUtils.get_message('ftp')
            if filename:
                try:
                    
                    logger.debug('get queue msg : %s queue-size: %d' % (filename, QueueUtils.get_queue('ftp').qsize()))
                    if os.path.basename(filename) in self.dict_filename.keys():             
                        logger.debug('msg : %s ' % filename)
                        # 上传文件到宇视的ftp服务器
                        # ftp_path = VehPass.filename_format(os.path.basename())
                        logger.debug('Ftp upload file: %s' % (self.dict_filename[os.path.basename(filename)]))
                        FtpUtils.upload_file(filename, '/' + Scheduler.dict_filename[os.path.basename(filename)])
                        self.count += 1
                        logger.debug('Ftp file: %s is upload complete! count = %d' % (os.path.basename(filename), self.count))
                        
                except Exception, e:
                    logger.error('ftp upload failed %s, filename: %s' % (e.message, filename))
