#!/usr/bin/env python
# @author   youjiang xie
# @E-mail   xie_youjiang@163.com
# @time     2017/6/7 0007 20:23
# @project  Python
# @file     TimeUtils

import os
import time, datetime
import logging.config

logging.config.fileConfig('../config/logging.conf')
logger = logging.getLogger("kakou")
class TimeUtils(object):

    @staticmethod
    def convert_time_format(strTime, oldTimeFormat, newTimeFormat):
        try:

            if strTime.strip() == '' or oldTimeFormat.strip() == '' or newTimeFormat.strip() == '':
                logger.error('params is not empty! please check it')
                return None

            struct_time = time.strptime(strTime[:-3], oldTimeFormat)
            return time.strftime(newTimeFormat, struct_time) + ' ' + strTime[-3:]
        except Exception, e:
            logger.error("time format convert error %s" % e.message)
            return None

    @staticmethod
    def get_longtime(strtime, time_format):
        try:
            if not strtime or not time:
                logger.error('params is not empty! please check it')
                return None

            struct_time = time.strptime(strtime, time_format)
            return time.mktime(struct_time)
        except Exception, e:
            logger.error('time format convert error %s' % e.message)
            return None
if __name__ == '__main__':

    print TimeUtils.convert_time_format('20170607203802123', '%Y%m%d%H%M%S', '%Y-%m-%d %H:%M:%S')