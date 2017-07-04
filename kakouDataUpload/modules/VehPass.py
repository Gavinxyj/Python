#!/usr/bin/python
# -*- coding:utf-8 -*-
# @author   youjiang xie
# @E-mail   xie_youjiang@163.com
# @time     2017/6/12 0012 13:48
# @project  Python
# @file     VehPass

import cx_Oracle
import os, sys
import logging
from datetime import datetime
from database.Connection import Connection
from FrmStatus import FrmStatus
from RoadInfo import RoadInfo
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'  #或者os.environ['NLS_LANG'] = 'AMERICAN_AMERICA.AL32UTF8'
logger = logging.getLogger("kakou.modules")
import pdb

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
            conn = Connection.get_conn('yunwei')
            if conn:
                cursor = conn.cursor()
                cursor.prepare(VehPass._insertSql)
                # pdb.set_trace()
                cursor.executemany(None, dictparams)
                cursor.close()
                conn.commit()
        except cx_Oracle.Error, e:
            conn.rollback()
            logger.error('Oracle Error: %s' % e.args)

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

    @staticmethod
    def parser_format(array_list):

        data = []
        for item in array_list:
            try:

                info = {}
                filename = os.path.split(item)[1]

                values = filename.split('_')

                if values[len(values) - 1] != '1.jpg':
                    continue

                # 号牌号码
                info['hphm'] = values[2].encode('gbk') # values[2].encode('utf-8') # unicode(values[2]).encode('utf8')
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
                    info['filepath1'] = values[1][:10] + '/' + values[0][-3:] + '/' # + filename
                    # filepath2
                    info['filepath2'] = values[1][:10] + '/' + values[0][-3:] + '/' # + filename
                else:
                    info['filepath1'] = values[1][:10] + '/' + values[0][-3:] + '/' # + filename
                    # filepath2
                    info['filepath2'] = values[1][:10] + '/' + values[0][-3:] + '/' # + filename[:-5] + '2.jpg'
                # 经过时间
                info['jgsj'] = datetime.strptime(values[1][:-3], '%Y%m%d%H%M%S')
                # 号牌种类id
                if info['hpzl'] in FrmStatus.data['hpzl'].keys():
                    info['hpzlid'] = FrmStatus.data['hpzl'][info['hpzl']]
                else:
                    continue
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
    def parser_his_format(array_list):
        data = []
        for item in array_list:
            info = {}
            filename = os.path.split(item)[1]

            values = filename.split('_')

            if values[len(values) - 1] != '1.jpg':
                continue

            # 号牌号码
            info['hphm'] = '123456' # values[2]
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
            # filepath1
            if values[len(values) - 2] == '1':
                # filepath1
                info['filepath1'] = values[1][:10] + '/' + values[0][-3:] + '/' + filename
                # filepath2
                info['filepath2'] = values[1][:10] + '/' + values[0][-3:] + '/' + filename
            else:
                info['filepath1'] = values[1][:10] + '/' + values[0][-3:] + '/' + filename
                # filepath2
                info['filepath2'] = values[1][:10] + '/' + values[0][-3:] + '/' + filename[:-5] + '.2.jpg'
            # 经过时间
            info['jgsj'] = datetime.strptime(values[1][:-3], '%Y%m%d%H%M%S')
            # 号牌种类id
            if info['hpzl'] in FrmStatus.data['hpzl'].keys():
                info['hpzlid'] = FrmStatus.data['hpzl'][info['hpzl']]
            else:
                continue
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

            if values[len(values) - 1] != '1.jpg':
                continue

            if values[8] not in FrmStatus.data['wzxw'].keys():
                continue
            # 号牌号码
            info['hphm'] = '123456' #values[2]
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
                info['filepath2'] = values[1][:10] + '/' + values[0][-3:] + '/' + filename[:-5] + '.2.jpg'
            else:
                info['filepath1'] = values[1][:10] + '/' + values[0][-3:] + '/' + filename
                # filepath2
                info['filepath2'] = values[1][:10] + '/' + values[0][-3:] + '/' + filename[:-5] + '.2.jpg'
                # filepath3
                info['filepath2'] = values[1][:10] + '/' + values[0][-3:] + '/' + filename[:-5] + '.3.jpg'
            # 经过时间
            info['jgsj'] = datetime.strptime(values[1][:-3], '%Y%m%d%H%M%S')
            # 号牌种类id
            if info['hpzl'] in FrmStatus.data['hpzl'].keys():
                info['hpzlid'] = FrmStatus.data['hpzl'][info['hpzl']]
            else:
                continue
            # 路口id
            info['cllx'] = ''
            # 方向id
            info['fxid'] = FrmStatus.data['direction'][info['fxbh']]
            # 车道id
            info['cdid'] = FrmStatus.data['carpath'][info['cdbh']]
            # 设备编号
            info['sbbh'] = values[0][2:]
            # 采集方式
            info['cjfx'] = ''
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
            data.append(info)
        return data

    @staticmethod
    def insert_data(array_list):
        try:
            vehpass = VehPass.parser_format(array_list)
            # hispass = VehPass.parser_his_format(array_list)
            # violation = VehPass.parser_violation_format(array_list)

            if vehpass:
                VehPass.insert_veh_pass(vehpass)
            '''
            if hispass:
                VehPass.insert_veh_pass_his(hispass)
            if violation:
                VehPass.insert_veh_pass_violation(violation)
            '''
        except cx_Oracle.Error, e:
            logger.error('Oracle Error: %d %s' % (e.args[0], e.args[1]))
