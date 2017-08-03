#!/usr/bin/env python
# @author   youjiang xie
# @E-mail   xie_youjiang@163.com
# @time     2017/6/6 0006 9:07
# @project  Python
# @file     run

import os, sys
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
import logging.config

from showRoom.modules.Scheduler import Scheduler


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
