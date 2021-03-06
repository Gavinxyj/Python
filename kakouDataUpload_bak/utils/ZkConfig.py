#!/usr/bin/python
# -*- coding:utf-8 -*-
# @author   youjiang xie
# @E-mail   xie_youjiang@163.com
# @time     2017/6/9 0009 15:28
# @project  Python
# @file     ZkConfig

import zookeeper
import logging

logger = logging.getLogger("kakou.utils")


class ZkConfig(object):

    def __init__(self, conn):
        self.zk = zookeeper.init(conn)

    def get_data(self, path):
        if zookeeper.exists(self.zk, path):
            return zookeeper.get(self.zk, path)
        else:
            logger.error('path is not exists, please check it')
            return None

    def close(self):
        zookeeper.close(self.zk)
