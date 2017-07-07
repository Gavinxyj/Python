#!/usr/bin/python
# -*- coding:utf-8 -*-
# @author   youjiang xie
# @E-mail   xie_youjiang@163.com
# @time     2017/7/6 0006 15:33
# @project  Python
# @file     VehPass
import pdb
import cx_Oracle
import logging
import json
from utils.TimeUtils import TimeUtils
from database.Connection import Connection
from datetime import datetime
logger = logging.getLogger("kakou.modules")


class VehPass(object):

    _querySql = 'select PASS_ID, CROSSING_ID, LANE_NO, DIRECTION_INDEX, PLATE_NO, PLATE_TYPE, PASS_TIME, VEHICLE_SPEED, '\
                'PLATE_COLOR, VEHICLE_TYPE, PLATE_STATE, VEHICLE_STATE from TRAFFIC_VEHICLE_PASS where rowid = :row_id'

    _querySqlImg = 'select PLATEPICURL, VEHICLEPICURL from picurl_info where VEHICLELSH=:urlid'

    @staticmethod
    def parser_format(values):
        #try:
        info = {}

        # id
        info['id'] = values[0]
        # 车辆品牌
        info['clpp'] = ''
        # 抓拍方向
        info['zpfx'] = ''
        # 设备编号
        info['sbbh'] = ''
        # 卡口编号
        info['kkbh'] = '11'
        # 车辆通过时间
        info['tgsj'] = values[6].strftime('%Y-%m-%d %H:%M:%S.%f')
        # 号牌号码
        info['hphm'] = values[4]

        # 车辆通行状态
        info['cltxzt'] = values[11]

        # 号牌种类
        info['hpzl'] = '%02d' % int(values[5])
        # 行驶速度
        info['xssd'] = values[7]
        # 车道编号
        info['cdbh'] = '%02d' % int(values[2])
        # 车行方向
        info['cxfx'] = '%02d' % int(values[3])
        if values[7] == '1':
            info['cxfx'] = '02'
        elif values[7] == '2':
            info['cxfx'] = '01'
        # 车身颜色
        info['csys'] = values[9]
        imgPath = VehPass.query_img_path_rowid(values[0])
        # 车辆特征图像1
        if imgPath[0][1]:
            info['tplj1'] = 'http://192.168.88.59:8088' + imgPath[0][1]
        # 车辆特征图像2
        if imgPath[0][0]:
            info['tplj2'] = 'http://192.168.88.59:8088' + imgPath[0][0]
        # 车辆特征图像3
        info['tplj3'] = ''
        strjson = json.dumps(info, ensure_ascii=False, sort_keys=True)
        logger.debug('strJson = %s' % strjson)
        return json.loads(strjson)

        #except Exception, e:
        #    logger.error('parser format failed msg ' % e.message)

    @staticmethod
    def query_data_by_rowid(rowid):
        try:
            conn = Connection.get_conn_hik()
            if conn:
                cursor = conn.cursor()
                cursor.prepare(VehPass._querySql)
                cursor.execute(None, {'row_id': rowid})
                result = cursor.fetchall()
                return result
        except cx_Oracle.Error, e:
            conn.rollback()
            logger.error('Oracle Error: %s' % e.args)

    @staticmethod
    def query_img_path_rowid(urlid):
        try:
            conn = Connection.get_conn_hik()
            if conn:
                cursor = conn.cursor()
                cursor.prepare(VehPass._querySqlImg)
                cursor.execute(None, {'urlid': urlid})
                result = cursor.fetchall()
                return result
        except cx_Oracle.Error, e:
            conn.rollback()
            logger.error('Oracle Error: %s' % e.args)