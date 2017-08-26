#!/usr/bin/python
# -*- coding:utf-8 -*-
# @author   youjiang xie
# @E-mail   xie_youjiang@163.com
# @time     2017/6/12 0012 18:50
# @project  Python
# @file     FrmStatus
import cx_Oracle
import logging
from database.Connection import Connection
logger = logging.getLogger("kakou.modules")


class FrmStatus(object):

    _querySql = 'select id, dmlb, dmz from fndj.frm_status'
    data = {}

    @staticmethod
    def get_all_record():
        try:
            conn = Connection.get_conn('yushi')
            if conn is not None:
                cursor = conn.cursor()
                cursor.execute(FrmStatus._querySql)
                result = cursor.fetchall()
                for item in result:
                    if item[1] in FrmStatus.data.keys():
                        FrmStatus.data[item[1]][item[2].strip()] = item[0]
                    else:
                        info = {}
                        info[item[2].strip()] = item[0]
                        FrmStatus.data[item[1]] = info
                cursor.close()
        except cx_Oracle.Error, e:
            conn.close()
            logger.error('Oracle Error: %d %s' % (e.args[0], e.args[1]))
