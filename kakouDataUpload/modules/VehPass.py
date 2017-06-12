#!/usr/bin/python
# -*- coding:utf-8 -*-
# @author   youjiang xie
# @E-mail   xie_youjiang@163.com
# @time     2017/6/12 0012 13:48
# @project  Python
# @file     VehPass

import cx_Oracle
import os
import logging
from database.Connection import Connection
from FrmStatus import FrmStatus
from RoadInfo import RoadInfo
logger = logging.getLogger("kakou.modules")


class VehPass(object):

    _insertSql = 'insert into veh_pass(hphm, hpys, hpzl, lkbh, fxbh, cdbh, clsd, csys, filepath1, filepath2, jgsj, hpzlid, lkid, fxid, cdid, sbbh, wfbj)' \
                 ' values (:hphm, :hpys, :hpzl, :lkbh, :fxbh, :cdbh, :clsd, :csys, :filepath1, :filepath2, :jgsj, :hpzlid, :lkid, :fxid,  :cdid, :sbbh, :wfbj)'

    _insertHisSql = 'insert into veh_pass_his(hphm, hpys, hpzl, lkbh, fxbh, cdbh, clsd, csys, filepath1, filepath2, jgsj, hpzlid, lkid, fxid, cdid, sbbh, wfbj, txrq)' \
                    ' values (:hphm, :hpys, :hpzl, :lkbh, :fxbh, :cdbh, :clsd, :csys, :filepath1, :filepath2, :jgsj, :hpzlid, :lkid, :fxid,  :cdid, :sbbh, :wfbj, :txrq)'

    _insertViolation = 'insert into veh_violation(sbbh, hphm, hpys, hpzl, lkbh, fxbh, cdbh, clsd, csys, cllx, pathfile1, pathfile2, pathfile3, cjfs, jgsj, wfdz, shzt, hpzlid, wfddid, fxid, cdid, wfxw, wfxwid)' \
                       ' values (:sbbh, :hphm, :hpys, :hpzl, :lkbh, :fxbh, :cdbh, :clsd, :csys, :cllx, :pathfile1, :pathfile2, :pathfile3, :cjfs, :jgsj, :wfdz, :shzt, :hpzlid, :wfddid, :fxid, :cdid, :wfxw, :wfxwid)'

    @staticmethod
    def insert_veh_pass(dictparams):
        try:
            conn = Connection.get_conn('yushi')
            if conn:
                cursor = conn.cursor()
                cursor.prepare(VehPass._insertHisSql)
                cursor.executemany(None, dictparams)
                cursor.close()
                conn.commit()
        except cx_Oracle.Error, e:
            conn.rollback()
            logger.error('Oracle Error: %d %s' % (e.args[0], e.args[1]))

    @staticmethod
    def insert_veh_pass_his(dictparams):
        try:
            conn = Connection.get_conn('yushi')
            if conn:
                cursor = conn.cursor()
                cursor.prepare(VehPass._insertHisSql)
                cursor.executemany(None, dictparams)
                cursor.close()
                conn.commit()
        except cx_Oracle.Error, e:
            conn.rollback()
            logger.error('Oracle Error: %d %s' % (e.args[0], e.args[1]))

    @staticmethod
    def insert_veh_pass_violation(dictparams):
        try:
            conn = Connection.get_conn('yushi')
            if conn:
                cursor = conn.cursor()
                cursor.prepare(VehPass._insertViolation)
                cursor.executemany(None, dictparams)
                cursor.close()
                conn.commit()
        except cx_Oracle.Error, e:
            conn.rollback()
            logger.error('Oracle Error: %d %s' % (e.args[0], e.args[1]))

    @staticmethod
    def parser_format(array_list):
        data = []
        for item in array_list:
            info = {}
            filename = os.path.split(item)[1]

            values = filename.split('_')
            # 号牌号码
            info['hphm'] = values[2]
            # 号牌颜色
            info['hpys'] = values[3]
            # 号牌种类
            info['hpzl'] = '%02d' % values[4]
            # 路口编号
            info['lkbh'] = values[0]
            # 方向编号
            info['fxbh'] = values[7]
            if info['fxbh'] == '1':
                info['fxbh'] = '02'
            elif info['fxbh'] == '2':
                info['fxbh'] = '01'
            # 车道编号
            info['cdbh'] = values[5]
            # 车辆速度
            info['clsd'] = values[6]
            # 车身颜色
            info['csys'] = values[9]
            # filepath1
            info['filepath1'] = ''
            # filepath2
            info['filepath2'] = ''
            # 经过时间
            info['jgsj'] = values[1]
            # 号牌种类id
            info['hpzlid'] = FrmStatus.data['hpzl'][info['hpzl']]
            # 路口id
            info['lkid'] = RoadInfo.mapdata[info['lkbh']]
            # 方向id
            info['fxid'] = FrmStatus.data['direction'][info['fxbh']]
            # 车道id
            info['cdid'] = FrmStatus.data['carpath'][info['cdbh']]
            # 设备编号
            info['sbbh'] = ''
            # 违法报警
            info['wfbj'] = values[8]

            data.append(info)
        return data

    @staticmethod
    def parser_his_format(array_list):
        data = []
        for item in array_list:
            info = {}
            filename = os.path.split(item)[1]

            values = filename.split('_')
            # 号牌号码
            info['hphm'] = values[2]
            # 号牌颜色
            info['hpys'] = values[3]
            # 号牌种类
            info['hpzl'] = '%02d' % values[4]
            # 路口编号
            info['lkbh'] = values[0]
            # 方向编号
            info['fxbh'] = values[7]
            if info['fxbh'] == '1':
                info['fxbh'] = '02'
            elif info['fxbh'] == '2':
                info['fxbh'] = '01'
            # 车道编号
            info['cdbh'] = values[5]
            # 车辆速度
            info['clsd'] = values[6]
            # filepath1
            info['filepath1'] = ''
            # filepath2
            info['filepath2'] = ''
            # 经过时间
            info['jgsj'] = values[1]
            # 号牌种类id
            info['hpzlid'] = FrmStatus.data['hpzl'][info['hpzl']]
            # 路口id
            info['lkid'] = RoadInfo.mapdata[info['lkbh']]
            # 方向id
            info['fxid'] = FrmStatus.data['direction'][info['fxbh']]
            # 车道id
            info['cdid'] = FrmStatus.data['carpath'][info['cdbh']]
            # 设备编号
            info['sbbh'] = ''
            # 违法报警
            info['wfbj'] = values[8]
            # 通行日期
            info['txrq'] = values[5:8]
            data.append(info)
        return data

    @staticmethod
    def parser_violation_format(array_list):
        data = []
        for item in array_list:
            info = {}
            filename = os.path.split(item)[1]

            values = filename.split('_')
            # 号牌号码
            info['hphm'] = values[2]
            # 号牌颜色
            info['hpys'] = values[3]
            # 号牌种类
            info['hpzl'] = '%02d' % values[4]
            # 路口编号
            info['lkbh'] = values[0]
            # 方向编号
            info['fxbh'] = values[7]
            if info['fxbh'] == '1':
                info['fxbh'] = '02'
            elif info['fxbh'] == '2':
                info['fxbh'] = '01'
            # 车道编号
            info['cdbh'] = values[5]
            # 车辆速度
            info['clsd'] = values[6]
            # filepath1
            info['filepath1'] = ''
            # filepath2
            info['filepath2'] = ''
            # filepath3
            info['filepath3'] = ''
            # 经过时间
            info['jgsj'] = values[1]
            # 号牌种类id
            info['hpzlid'] = FrmStatus.data['hpzl'][info['hpzl']]
            # 路口id
            info['cllx'] = ''
            # 方向id
            info['fxid'] = FrmStatus.data['direction'][info['fxbh']]
            # 车道id
            info['cdid'] = FrmStatus.data['carpath'][info['cdbh']]
            # 设备编号
            info['sbbh'] = ''
            # 违法报警
            info['wfbj'] = values[8]
            # 采集方式
            info['cjfx'] = ''
            # 违法地址
            info['wfdz'] = RoadInfo.mapdata[info['lkbh']]
            # 审核状态
            info['shzt'] = ''
            # 违法地点id
            info['wfddid'] = RoadInfo.mapdata[info['lkbh']]
            # 违法行为
            info['wfxw'] = ''
            # 违法行为id
            info['wfxwid'] = ''
            data.append(info)
        return data
