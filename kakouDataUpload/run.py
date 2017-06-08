#!/usr/bin/env python
# @author   youjiang xie
# @E-mail   xie_youjiang@163.com
# @time     2017/6/6 0006 9:07
# @project  Python
# @file     run

from utils.FileUtils import FileUtils
from modules.CarInfo import CarInfo
from modules.TdmsTgs import TdmsTgs
from database.RedisOperatorImpl import RedisImpl
import time

if __name__ == '__main__':

    startup_nodes = [{'host': '13.53.147.233', 'port': '6379'},
                     {'host': '13.53.147.233', 'port': '6380'},
                     {'host': '13.53.147.235', 'port': '6381'}]
    redis = RedisImpl(*startup_nodes)

    print redis.getkey('scanPoint')

   # listdata = FileUtils.scan_file('/data/source', time.time() - 10 * 60)

   # TdmsTgs.get_record()

   # CarInfo.parser_format(listdata, TdmsTgs.mapdata)
