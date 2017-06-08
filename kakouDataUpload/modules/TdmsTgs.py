#!/usr/bin/python
# -*- coding:utf-8 -*-
# @author   youjiang xie
# @E-mail   xie_youjiang@163.com
# @time     2017/6/7 0007 21:33
# @project  Python
# @file     TdmsTgs

import cx_Oracle
import logging.config
from database.Connectino import Connection

logging.config.fileConfig('../config/logging.conf')
logger = logging.getLogger("kakou")


class TdmsTgs(object):

    querySql = 'select kkbh, kkxh from v_tdms_tgs'
    mapdata = {}

    @staticmethod
    def get_record():
        try:
            conn = Connection.get_conn('yunwei')
            cursor = conn.cursor()
            cursor.execute(TdmsTgs.querySql)
            result = cursor.fetchall()
            for item in result:
                TdmsTgs.mapdata[item[0]] = item[1]

            cursor.close()
        except cx_Oracle.Error, e:
            conn.close()
            logger.error('Oracle Error: %d %s' % (e.args[0], e.args[1]))

