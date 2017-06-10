#!/usr/bin/python
# -*- coding:utf-8 -*-
# @author   youjiang xie
# @E-mail   xie_youjiang@163.com
# @time     2017/6/9 0009 15:28
# @project  Python
# @file     ZkConfig

import zookeeper
import logging.config

logging.config.fileConfig('config/logging.conf')
logger = logging.getLogger("kakou")


class ZkConfig(object):

    def __init__(self, conn):
        print conn
        self.zk = zookeeper.init(conn)
        print self.zk

    def get_data(self, path):
        if zookeeper.exists(self.zk, path):
            return zookeeper.get(self.zk, path)
        else:
            logger.error('path is not exists, please check it')
            return None
