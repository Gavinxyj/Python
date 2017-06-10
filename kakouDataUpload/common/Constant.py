#!/usr/bin/python
# -*- coding:utf-8 -*-
# @author   youjiang xie
# @E-mail   xie_youjiang@163.com
# @time     2017/6/9 0009 17:24
# @project  Python
# @file     Constant

import os

_current_dir = os.path.abspath(os.path.dirname(__file__))
ROOT_PATH = os.path.normpath(os.path.join(_current_dir, '..', '..', '..'))
ZOOKEEPER_ADDR = 'localhost:2181'
ZOOKEEPER_PATH = '/zookeeper/kakouFilter'
