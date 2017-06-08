#!/usr/bin/env python
# @author   youjiang xie
# @E-mail   xie_youjiang@163.com
# @time     2017/6/7 0007 11:38
# @project  Python
# @file     RedisOperatorImpl

from rediscluster import StrictRedisCluster


class RedisImpl(object):

    def __init__(self, *args):
        self.conn = StrictRedisCluster(startup_nodes=args, decode_responses=True)

    def getkey(self, key):
        return self.conn.get(key)

    def setkey(self, key, value):
        self.conn.set(key, value)
