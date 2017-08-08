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
#os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'  #或者os.environ['NLS_LANG'] = 'AMERICAN_AMERICA.AL32UTF8'
import threading  
 

class Connection(object):
    _connParams = None
    _connMgr = {}
    _mylock = threading.RLock() 
    @staticmethod
    def init_conn(params):
        Connection._connParams = params

    # 获取数据库连接
    @staticmethod
    def get_conn(strType):
        # conn = Connection._connParams
        try:
            
            if strType in Connection._connMgr:
                if Connection._connMgr[strType] is not None:
                    Connection._mylock.acquire() 
                    conn = Connection._connMgr[strType]
                    Connection._mylock.release() 
                    return conn
            logger.debug('strType = %s, _connMgr = %s' % (strType, Connection._connMgr))
            if strType in Connection._connParams.keys():
                values = Connection._connParams[strType]
                dsn = cx_Oracle.makedsn(values['url'], values['port'], values['sid']).replace('SID', 'SERVICE_NAME')
                conn = cx_Oracle.connect(values['username'], values['password'], dsn)
                if conn:
                    Connection._mylock.acquire() 
                    Connection._connMgr[strType] = conn
                    Connection._mylock.release() 
                else:
                    Connection._mylock.acquire() 
                    Connection._connMgr[strType] = None
                    Connection._mylock.release() 
                return conn
            
        except cx_Oracle.Error, e:
            logger.error('cx_Oralce Error : %s' % (e.args[0], e.args[1]))

        return None
