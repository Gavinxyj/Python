#!/usr/bin/python
# -*- coding:utf-8 -*-
# @author   youjiang xie
# @E-mail   xie_youjiang@163.com
# @time     2017/6/9 0009 15:28
# @project  Python
# @file     ZkConfig
from common.Constant import ZOOKEEPER_ADDR, ZOOKEEPER_PATH
import zookeeper
import logging
import json

logger = logging.getLogger("kakou.utils")


class ZkConfig(object):

    def __init__(self):
        self.zk = zookeeper.init(ZOOKEEPER_ADDR)

    def get_data(self, path):
        if zookeeper.exists(self.zk, path):
            return zookeeper.get(self.zk, path)
        else:
            logger.error('path is not exists, please check it')
            return None

    def get_node_data(self):
        result = self.get_data(ZOOKEEPER_PATH)
        if result:
            return json.loads(result[0])
        else:
            return None
    def close(self):
        zookeeper.close(self.zk)
