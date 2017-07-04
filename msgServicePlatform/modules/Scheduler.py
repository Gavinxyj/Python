#!/usr/bin/python
# -*- coding:utf-8 -*-
# @author   youjiang xie
# @E-mail   xie_youjiang@163.com
# @time     2017/6/15 0015 20:14
# @project  Python
# @file     Scheduler
from utils.ZkConfig import ZkConfig



class Scheduler(object):
    def __init__(self):
        self.zkObj = ZkConfig()

