#!/usr/bin/python
# -*- coding:utf-8 -*-
# @author   youjiang xie
# @E-mail   xie_youjiang@163.com
# @time     2017/6/12 0012 13:48
# @project  Python
# @file     VehPass

import os, sys
import cx_Oracle
import logging
from datetime import datetime
from database.Connection import Connection
from FrmStatus import FrmStatus
from RoadInfo import RoadInfo

default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)
logger = logging.getLogger("kakou.modules")
import pdb


class VehPass(object):
    _insertSql = 'insert into veh_pass(id, hphm, hpys, hpzl, lkbh, fxbh, cdbh, clsd, csys, filepath1, filepath2, jgsj, hpzlid, lkid, fxid, cdid, sbbh, wfbj)' \
                 ' values (:id, :hphm, :hpys, :hpzl, :lkbh, :fxbh, :cdbh, :clsd, :csys, :filepath1, :filepath2, :jgsj, :hpzlid, :lkid, :fxid,  :cdid, :sbbh, :wfbj)'

    _insertHisSql = 'insert into veh_pass_his(id, hphm, hpys, hpzl, lkbh, fxbh, cdbh, clsd, csys, filepath1, filepath2, jgsj, hpzlid, lkid, fxid, cdid, sbbh, wfbj, txrq)' \
                    ' values (:id, :hphm, :hpys, :hpzl, :lkbh, :fxbh, :cdbh, :clsd, :csys, :filepath1, :filepath2, :jgsj, :hpzlid, :lkid, :fxid,  :cdid, :sbbh, :wfbj, :txrq)'

    _insertViolation = 'insert into veh_violation(id, sbbh, hphm, hpys, hpzl, lkbh, fxbh, cdbh, clsd, csys, cllx, filepath1, filepath2, filepath3, cjfs, jgsj, wfdz, shzt, hpzlid, wfddid, fxid, cdid, wfxw, wfxwid)' \
                       ' values (:id, :sbbh, :hphm, :hpys, :hpzl, :lkbh, :fxbh, :cdbh, :clsd, :csys, :cllx, :filepath1, :filepath2, :filepath3, :cjfs, :jgsj, :wfdz, :shzt, :hpzlid, :wfddid, :fxid, :cdid, :wfxw, :wfxwid)'

    _max_id = 0
    @staticmethod
    def insert_veh_pass(dictparams):
        try:
            conn = Connection.get_conn('yunwei')
            if conn:
                cursor = conn.cursor()
                cursor.prepare(VehPass._insertSql)

                cursor.executemany(None, dictparams)
                cursor.close()
                conn.commit()
        except cx_Oracle.Error, e:
            conn.rollback()
            logger.error('Oracle Error: %s' % e.args)
            logger.error('record = %s' % dictparams)

    @staticmethod
    def insert_veh_pass_his(dictparams):
        try:
            conn = Connection.get_conn('yunwei')
            if conn:
                cursor = conn.cursor()
                cursor.prepare(VehPass._insertHisSql)
                cursor.executemany(None, dictparams)
                cursor.close()
                conn.commit()
        except cx_Oracle.Error, e:
            conn.rollback()
            logger.error('Oracle Error: %s' % e.args)
            logger.error('record = %s' % dictparams)

    @staticmethod
    def insert_veh_pass_violation(dictparams):
        try:
            conn = Connection.get_conn('yunwei')
            if conn:
                cursor = conn.cursor()
                cursor.prepare(VehPass._insertViolation)
                cursor.executemany(None, dictparams)
                cursor.close()
                conn.commit()
        except cx_Oracle.Error, e:
            conn.rollback()
            logger.error('Oracle Error: %s' % e.args)
            logger.error('record = %s' % dictparams)

    @staticmethod
    def parser_format(item):

        data = []
        try:
            info = {}
            filename = os.path.split(item)[1]

            values = filename.split('_')

            if values[len(values) - 1] != '1.jpg':
                return None
            # id
            info['id'] = VehPass._max_id
            # 号牌号码
            info['hphm'] = values[2].strip()
            # pdb.set_trace()
            if info['hphm'] == '-':
                info['hphm'] = 'NA'
            # 号牌颜色
            info['hpys'] = values[3]
            # 号牌种类
            info['hpzl'] = '%02d' % int(values[4])
            # 路口编号
            info['lkbh'] = values[0][:-3] + '000'
            # 方向编号
            info['fxbh'] = '%02d' % int(values[7])
            if info['fxbh'] == '01':
                info['fxbh'] = '02'
            elif info['fxbh'] == '02':
                info['fxbh'] = '01'
            # 车道编号
            info['cdbh'] = values[5]
            # 车辆速度
            info['clsd'] = values[6]
            # 车身颜色
            info['csys'] = values[9]
            # filepath1
            info['filepath1'] = values[1][:10] + '/' + values[0][-3:] + '/' + filename
            # filepath2
            info['filepath2'] = values[1][:10] + '/' + values[0][-3:] + '/' + filename
            # 经过时间
            info['jgsj'] = datetime.strptime(values[1][:-3], '%Y%m%d%H%M%S')
            # 号牌种类id
            if info['hpzl'] in FrmStatus.data['hpzl'].keys():
                info['hpzlid'] = FrmStatus.data['hpzl'][info['hpzl']]
            else:
                logger.error('hpzl is no map value msg is %s' % item)
                return None
            # 路口id
            info['lkid'] = RoadInfo.mapdata[info['lkbh']]
            # 方向id
            info['fxid'] = FrmStatus.data['direction'][info['fxbh']]
            # 车道id
            info['cdid'] = FrmStatus.data['carpath'][info['cdbh']]
            # 设备编号
            info['sbbh'] = values[0][2:]
            # 违法报警
            info['wfbj'] = values[8]
            if values[8] != '0':
                info['wfbj'] = '1'
            data.append(info)
            logger.info('info = %s' % info)
        except Exception, e:
            logger.error('parser error %s, filename =', (e.message, item))
        return data

    @staticmethod
    def parser_his_format(item):
        data = []
        try:

            info = {}
            filename = os.path.split(item)[1]

            values = filename.split('_')

            if values[len(values) - 1] != '1.jpg':
                return None
            # id
            info['id'] = VehPass._max_id
            # 号牌号码
            info['hphm'] = values[2].strip()
            if info['hphm'] == '-':
                info['hphm'] = 'NA'
            # 号牌颜色
            info['hpys'] = values[3]
            # 号牌种类
            info['hpzl'] = '%02d' % int(values[4])
            # 路口编号
            info['lkbh'] = values[0][:-3] + '000'
            # 方向编号
            info['fxbh'] = '%02d' % int(values[7])
            if info['fxbh'] == '01':
                info['fxbh'] = '02'
            elif info['fxbh'] == '02':
                info['fxbh'] = '01'
            # 车道编号
            info['cdbh'] = values[5]
            # 车辆速度
            info['clsd'] = values[6]
            # 车身颜色
            info['csys'] = values[9]
            # filepath1
            info['filepath1'] = values[1][:10] + '/' + values[0][-3:] + '/' + filename
            # filepath2
            info['filepath2'] = values[1][:10] + '/' + values[0][-3:] + '/' + filename
            # 经过时间
            info['jgsj'] = datetime.strptime(values[1][:-3], '%Y%m%d%H%M%S')
            # 号牌种类id
            if info['hpzl'] in FrmStatus.data['hpzl'].keys():
                info['hpzlid'] = FrmStatus.data['hpzl'][info['hpzl']]
            else:
                logger.error('hpzl is no map value msg is %s' % item)
                return None
            # 路口id
            info['lkid'] = RoadInfo.mapdata[info['lkbh']]
            # 方向id
            info['fxid'] = FrmStatus.data['direction'][info['fxbh']]
            # 车道id
            info['cdid'] = FrmStatus.data['carpath'][info['cdbh']]
            # 设备编号
            info['sbbh'] = values[0][2:]
            # 违法报警
            info['wfbj'] = values[8]
            if values[8] != '0':
                info['wfbj'] = '1'
            # 通行日期
            info['txrq'] = values[1][5:8]
            logger.info('info = %s' % info)
            data.append(info)
        except Exception, e:
            logger.error('parser error %s, filename =', (e.message, item))

        return data

    @staticmethod
    def parser_violation_format(item):
        data = []
        try:
            info = {}
            filename = os.path.split(item)[1]

            values = filename.split('_')

            if values[len(values) - 1] != '1.jpg':
                return None

            if values[8] not in FrmStatus.data['wzxw'].keys():
                return None
            # id
            info['id'] = VehPass._max_id
            # 号牌号码
            info['hphm'] = values[2].strip()
            if info['hphm'] == '-':
                info['hphm'] = 'NA'
            # 号牌颜色
            info['hpys'] = values[3]
            # 号牌种类
            info['hpzl'] = '%02d' % int(values[4])
            # 路口编号
            info['lkbh'] = values[0][:-3] + '000'
            # 方向编号
            info['fxbh'] = '%02d' % int(values[7])
            if info['fxbh'] == '01':
                info['fxbh'] = '02'
            elif info['fxbh'] == '02':
                info['fxbh'] = '01'
            # 车道编号
            info['cdbh'] = values[5]
            # 车辆速度
            info['clsd'] = values[6]
            # 车身颜色
            info['csys'] = values[9]
            # filepath1
            if values[len(values) - 2] == '1':
                # filepath1
                info['filepath1'] = values[1][:10] + '/' + values[0][-3:] + '/' + filename
                # filepath2
                info['filepath2'] = values[1][:10] + '/' + values[0][-3:] + '/' + filename
                # filepath2
                info['filepath3'] = values[1][:10] + '/' + values[0][-3:] + '/' + filename
            elif values[len(values) - 2] == '2':
                info['filepath1'] = values[1][:10] + '/' + values[0][-3:] + '/' + filename
                # filepath2
                info['filepath2'] = values[1][:10] + '/' + values[0][-3:] + '/' + filename[:-5] + '.2.jpg'
                # filepath3
                info['filepath3'] = values[1][:10] + '/' + values[0][-3:] + '/' + filename[:-5] + '.2.jpg'
            else:
                info['filepath1'] = values[1][:10] + '/' + values[0][-3:] + '/' + filename
                # filepath2
                info['filepath2'] = values[1][:10] + '/' + values[0][-3:] + '/' + filename[:-5] + '.2.jpg'
                # filepath3
                info['filepath3'] = values[1][:10] + '/' + values[0][-3:] + '/' + filename[:-5] + '.3.jpg'
            # 经过时间
            info['jgsj'] = datetime.strptime(values[1][:-3], '%Y%m%d%H%M%S')
            # 号牌种类id
            if info['hpzl'] in FrmStatus.data['hpzl'].keys():
                info['hpzlid'] = FrmStatus.data['hpzl'][info['hpzl']]
            else:
                logger.error('hpzl is no map value msg is %s' % item)
                return None
            # 路口id
            info['cllx'] = ''
            # 方向id
            info['fxid'] = FrmStatus.data['direction'][info['fxbh']]
            # 车道id
            info['cdid'] = FrmStatus.data['carpath'][info['cdbh']]
            # 设备编号
            info['sbbh'] = values[0][2:]
            # 采集方式
            info['cjfs'] = '0'
            # 违法地址
            info['wfdz'] = RoadInfo.mapdata[info['lkbh']]
            # 审核状态
            info['shzt'] = ''
            # 违法地点id
            info['wfddid'] = RoadInfo.mapdata[info['lkbh']]
            # 违法行为
            info['wfxw'] = values[8]
            # 违法行为id
            info['wfxwid'] = FrmStatus.data['wzxw'][info['wfxw']]
            logger.info('info = %s' % info)
            data.append(info)
        except Exception, e:
            logger.error('parser error %s, filename =', (e.message, item))
        return data

    @staticmethod
    def insert_data(array_list):
        try:
            for item in array_list:
                VehPass._max_id = VehPass.getMaxId()
                if VehPass._max_id:
                    vehpass = VehPass.parser_format(item)

                    hispass = VehPass.parser_his_format(item)

                    violation = VehPass.parser_violation_format(item)

                    if vehpass:
                        VehPass.insert_veh_pass(vehpass)

                    if hispass:
                        VehPass.insert_veh_pass_his(hispass)

                    if violation:
                        VehPass.insert_veh_pass_violation(violation)
        except cx_Oracle.Error, e:
            logger.error('Oracle Error: %d %s' % (e.args[0], e.args[1]))

    @staticmethod
    def getMaxId():
        try:
            conn = Connection.get_conn('yushi')
            if conn:
                cursor = conn.cursor()
                # plsql入参
                table_name = 'VEH_PASS'
                # plsql出参
                max_id = cursor.var(cx_Oracle.STRING)
                # 调用存储过程
                cursor.callproc('fndj.getmaxid', [table_name, max_id])
                return max_id.getvalue()
        except cx_Oracle.Error, e:
            logger.error('Oracle Error: %s' % e.args)
    @staticmethod
    def test():
        data = []
        info = {}
        # id
        info['id'] = '1234567'
        # 号牌号码
        info['hphm'] = '苏AE31Z8'
        # 号牌颜色
        info['hpys'] = 'a'
        # 号牌种类
        info['hpzl'] = '01'
        # 路口编号
        info['lkbh'] = '1234567'
        # 方向编号
        info['fxbh'] = '01'

        # 车道编号
        info['cdbh'] = '01'
        # 车辆速度
        info['clsd'] = '43'
        # 车身颜色
        info['csys'] = 'b'
        # filepath1

        # filepath1
        info['filepath1'] = '123456'
        # filepath2
        info['filepath2'] = '123456'
        # filepath2
        info['filepath3'] = '123456'
        # 经过时间
        info['jgsj'] = datetime.strptime('20170731090723', '%Y%m%d%H%M%S')
        # 号牌种类id

        info['hpzlid'] = '201'

        info['cllx'] = 'A'
        # 方向id
        info['fxid'] = '4'
        # 车道id
        info['cdid'] = '01'
        # 设备编号
        info['sbbh'] = '123456'
        # 采集方式
        info['cjfs'] = '0'
        # 违法地址
        info['wfdz'] = '321'
        # 审核状态
        info['shzt'] = ''
        # 违法地点id
        info['wfddid'] = '201'
        # 违法行为
        info['wfxw'] = '201'
        # 违法行为id
        info['wfxwid'] = '201'
        data.append(info)
        VehPass.insert_veh_pass_violation(data)