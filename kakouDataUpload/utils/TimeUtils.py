#!/usr/bin/env python
# @author   youjiang xie
# @E-mail   xie_youjiang@163.com
# @time     2017/6/7 0007 20:23
# @project  Python
# @file     TimeUtils

import os
import time, datetime
import logging.config

logging.config.fileConfig('config/logging.conf')
logger = logging.getLogger("kakou")
class TimeUtils(object):

    @staticmethod
    def convert_time_format(strTime, oldTimeFormat, newTimeFormat):
        try:

            if strTime.strip() == '' or oldTimeFormat.strip() == '' or newTimeFormat.strip() == '':
                logger.error('params is not empty! please check it')
                return None
            struct_time = time.strptime(strTime, oldTimeFormat)
            return time.strftime(newTimeFormat, struct_time)
        except:
            logger.error('time format convert error')
            return None

if __name__ == '__main__':
    print TimeUtils.convert_time_format('2017-06-07 20:38:02', '%Y-%m-%d %H:%M:%S', '%Y%m%d%H%M%S')