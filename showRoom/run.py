#!/usr/bin/python
# -*- coding:utf-8 -*-
# @author   youjiang xie
# @E-mail   xie_youjiang@163.com
# @time     2017/7/6 0006 11:42
# @project  Python
# @file     run
import logging.config
import os
import sys
from modules.Scheduler import Scheduler

os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

logging.config.fileConfig('config/logging.conf')
logger = logging.getLogger("kakou")

if __name__ == '__main__':
    scheduler = Scheduler()
    scheduler.do_scheduler()

    print 'main thread exit'
