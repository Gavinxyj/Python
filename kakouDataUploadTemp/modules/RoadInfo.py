#!/usr/bin/python
# -*- coding:utf-8 -*-
# @author   youjiang xie
# @E-mail   xie_youjiang@163.com
# @time     2017/6/12 0012 19:21
# @project  Python
# @file     RoadInfo
import cx_Oracle
import logging
from database.Connection import Connection

logger = logging.getLogger("kakou.modules")
    

class RoadInfo(object):

    _querySql = 'select lkbm, id from fndj.Road_Info'
    mapdata = {}

    @staticmethod
    def get_all_record():
        try:
            conn = Connection.get_conn('yushi')
            if conn is not None:
                cursor = conn.cursor()
                cursor.execute(RoadInfo._querySql)
                result = cursor.fetchall()
                for item in result:
                    RoadInfo.mapdata[item[0]] = item[1]

                cursor.close()
        except cx_Oracle.Error, e:
            conn.close()
            logger.error('Oracle Error: %d %s' % (e.args[0], e.args[1]))
