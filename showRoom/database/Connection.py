#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @author   youjiang xie
# @E-mail   xie_youjiang@163.com
# @time     2017/6/6 0006 9:08
# @project  Python
# @file     connection

import os
import cx_Oracle
import logging
logger = logging.getLogger("kakou.database")
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'  #或者os.environ['NLS_LANG'] = 'AMERICAN_AMERICA.AL32UTF8'


class Connection(object):
    _connParams = None
    _connMgr = None

    @staticmethod
    def init_conn(params):
        Connection._connParams = params

    # 获取数据库连接
    @staticmethod
    def get_conn_hik():
        try:
            if Connection._connMgr:
                return Connection._connMgr

            if Connection._connMgr is None:
                dsn = cx_Oracle.makedsn('192.168.88.59', '1521', 'ORCL').replace('SID', 'SERVICE_NAME')
                conn = cx_Oracle.connect('IVMS86X0', 'IVMS86X0', dsn, events=True)
                Connection._connMgr = conn
                return conn

        except cx_Oracle.Error, e:
            logger.error('cx_Oralce Error : %s' % (e.args[0], e.args[1]))

        return None

    # 获取数据库连接
    @staticmethod
    def get_conn_yunwei():
        try:
            if Connection._connMgr:
                return Connection._connMgr

            if Connection._connMgr is None:
                dsn = cx_Oracle.makedsn('192.168.88.59', '1521', 'ORCL').replace('SID', 'SERVICE_NAME')
                conn = cx_Oracle.connect('IVMS86X0', 'IVMS86X0', dsn)
                Connection._connMgr = conn
                return conn

        except cx_Oracle.Error, e:
            logger.error('cx_Oralce Error : %s' % (e.args[0], e.args[1]))

        return None
