#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @author   youjiang xie
# @E-mail   xie_youjiang@163.com
# @time     2017/6/6 0006 9:08
# @project  Python
# @file     connection

import cx_Oracle
import logging.config
logging.config.fileConfig('../config/logging.conf')
logger = logging.getLogger("kakou")


class Connection(object):

    connMgr = {}
    connParams = None

    def __init__(self, conParams):
        self.connParams = conParams

    # 获取数据库连接

    @staticmethod
    def get_conn(strType):
        try:
            if strType in Connection.connMgr:
                if Connection.connMgr[strType] is not None:
                    return Connection.connMgr

            if strType in Connection.connParams.keys():
                values = Connection.connParams[strType]
                dsn = cx_Oracle.makedsn(values['ip'], int(values['port']), values['sid']).replace('SID', 'SERVICE_NAME')
                conn = cx_Oracle.connect(values['username'], values['password'], dsn)
                Connection.connMgr[strType] = conn
                return conn

        except cx_Oracle.Error, e:
            logger.error('cx_Oralce Error : %s' % (e.args[0], e.args[1]))