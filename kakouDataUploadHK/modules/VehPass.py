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
import threading  
'''
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)
'''
logger = logging.getLogger("kakou.modules")
import pdb


class VehPass(object):
    _insertSql = 'insert into veh_pass(id, hphm, hpys, hpzl, lkbh, fxbh, cdbh, clsd, csys, filepath1, filepath2, jgsj, hpzlid, lkid, fxid, cdid, sbbh, wfbj)' \
                 ' values (:id, :hphm, :hpys, :hpzl, :lkbh, :fxbh, :cdbh, :clsd, :csys, :filepath1, :filepath2, :jgsj, :hpzlid, :lkid, :fxid,  :cdid, :sbbh, :wfbj)'

    _insertHisSql = 'insert into veh_pass_his(id, hphm, hpys, hpzl, lkbh, fxbh, cdbh, clsd, csys, filepath1, filepath2, jgsj, hpzlid, lkid, fxid, cdid, sbbh, wfbj, txrq)' \
                    ' values (:id, :hphm, :hpys, :hpzl, :lkbh, :fxbh, :cdbh, :clsd, :csys, :filepath1, :filepath2, :jgsj, :hpzlid, :lkid, :fxid,  :cdid, :sbbh, :wfbj, :txrq)'

    _insertViolation = 'insert into veh_violation(id, sbbh, hphm, hpys, hpzl, lkbh, fxbh, cdbh, clsd, csys, cllx, filepath1, filepath2, filepath3, cjfs, jgsj, wfdz, shzt, hpzlid, wfddid, fxid, cdid, wfxw, wfxwid, shr, tzsh, shsj, tzrq)' \
                       ' values (:id, :sbbh, :hphm, :hpys, :hpzl, :lkbh, :fxbh, :cdbh, :clsd, :csys, :cllx, :filepath1, :filepath2, :filepath3, :cjfs, :jgsj, :wfdz, :shzt, :hpzlid, :wfddid, :fxid, :cdid, :wfxw, :wfxwid, :shr, :tzsh, :shsj, :tzrq)'

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
            logger.error('Oracle Error: %s record = %s' % (e.message, dictparams))

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
            logger.error('Oracle Error: %s record = %s' % (e.message, dictparams))

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
            logger.error('Oracle Error: %s record = %s' % (e.message, dictparams))

    @staticmethod
    def parser_format(item):

        data = []
        try:
            info = {}
            values = None
            with open(item, 'r') as file_object:
                items = [line.strip('\r\n') for line in file_object.readlines()]
                values = items
            if values:
                # id
                info['id'] = VehPass.getMaxId('VEH_PASS')
                # 号牌号码
                info['hphm'] = values[2][5:].decode('gbk').strip()#.decode('utf-8').encode('gbk')
                # pdb.set_trace()
                if info['hphm'] == '无车牌':
                    info['hphm'] = 'NA'
                # 号牌颜色
                info['hpys'] = values[3][5:].decode('gbk').strip()
                if info['hpys'] == '白':
                    info['hpys'] = '0'
                elif info['hpys'] == '黃':
                    info['hpys'] = '1'
                elif info['hpys'] == '蓝':
                    info['hpys'] = '2'
                elif info['hpys'] == '黑':
                    info['hpys'] = '3'
                elif info['hpys'] == '未知':
                    info['hpys'] = '4'
                # 号牌种类
                info['hpzl'] = '02'
                # 路口编号
                info['lkbh'] = values[0][5:][:-3] + '000'
                # 方向编号
                info['fxbh'] = values[7][5:].decode('gbk').strip()
                if info['fxbh'] == '由东向西':
                    info['fxbh'] = '02'
                elif info['fxbh'] == '由西向东':
                    info['fxbh'] = '01'
                elif info['fxbh'] == '由南向北':
                    info['fxbh'] = '03'
                elif info['fxbh'] == '由北向南':
                    info['fxbh'] = '04'
                # 车道编号
                info['cdbh'] = '%d' % int(values[5][5:])
                # 车辆速度
                info['clsd'] = values[6][5:]
                # 车身颜色
                info['csys'] = values[9][5:]
                # 经过时间
                info['jgsj'] = datetime.strptime(values[1][5:][:-3], '%Y%m%d%H%M%S')
                # filepath1
                info['filepath1'] = VehPass.filename_format(item)#.decode('utf-8').encode('gbk')
                # filepath2
                info['filepath2'] = VehPass.filename_format(item)#.decode('utf-8').encode('gbk')
                # 号牌种类id
                if info['hpzl'] in FrmStatus.data['hpzl'].keys():
                    info['hpzlid'] = FrmStatus.data['hpzl'][info['hpzl']]
                else:
                    logger.error('hpzl is no map value msg is %s' % item)
                    return None
                # 路口id
                if info['lkbh'] in RoadInfo.mapdata.keys():
                    info['lkid'] = RoadInfo.mapdata[info['lkbh']]
                else:
                    logger.error('lkbh is no map value msg is %s' % info['lkbh'])
                    return None
                # 方向id
                info['fxid'] = FrmStatus.data['direction'][info['fxbh']]
                # 车道id
                info['cdid'] = FrmStatus.data['carpath'][info['cdbh']]
                # 设备编号
                info['sbbh'] = '147' + values[0][5:][5:]
                # 违法报警
                info['wfbj'] = values[8][5:]
                if values[8][5:] != '0':
                    info['wfbj'] = '1'
                data.append(info)
                logger.info('info = %s' % info)
                return data
        except Exception, e:
            logger.error('parser error %s, filename =', (e.message, item))

    @staticmethod
    def parser_his_format(item):
        data = []
        try:

            info = {}
            values = None
            with open(item, 'r') as file_object:
                items = [line.strip('\r\n') for line in file_object.readlines()]
                values = items

            if values:
                # id
                info['id'] = VehPass.getMaxId('VEH_PASS_HIS')
                # 号牌号码
                info['hphm'] = values[2][5:].decode('gbk').strip()#.decode('utf-8').encode('gbk')
                if info['hphm'] == '无车牌':
                    info['hphm'] = 'NA'
                # 号牌颜色
                info['hpys'] = values[3][5:].decode('gbk')
                if info['hpys'] == '白':
                    info['hpys'] = '0'
                elif info['hpys'] == '黃':
                    info['hpys'] = '1'
                elif info['hpys'] == '蓝':
                    info['hpys'] = '2'
                elif info['hpys'] == '黑':
                    info['hpys'] = '3'
                elif info['hpys'] == '未知':
                    info['hpys'] = '4'
                # 号牌种类
                info['hpzl'] = '02'
                # 路口编号
                info['lkbh'] = values[0][5:][:-3] + '000'
                # 方向编号
                info['fxbh'] = values[7][5:].decode('gbk').strip()
                if info['fxbh'] == '由东向西':
                    info['fxbh'] = '02'
                elif info['fxbh'] == '由西向东':
                    info['fxbh'] = '01'
                elif info['fxbh'] == '由南向北':
                    info['fxbh'] = '03'
                elif info['fxbh'] == '由北向南':
                    info['fxbh'] = '04'  
                # 车道编号
                info['cdbh'] = '%d' % int(values[5][5:])
                # 车辆速度
                info['clsd'] = values[6][5:]
                # 车身颜色
                info['csys'] = values[9][5:]

                # filepath1
                info['filepath1'] = VehPass.filename_format(item)#.decode('utf-8').encode('gbk')
                # filepath2
                info['filepath2'] = VehPass.filename_format(item)#.decode('utf-8').encode('gbk')
                # 经过时间
                info['jgsj'] = datetime.strptime(values[1][5:][:-3], '%Y%m%d%H%M%S')
                # 号牌种类id
                if info['hpzl'] in FrmStatus.data['hpzl'].keys():
                    info['hpzlid'] = FrmStatus.data['hpzl'][info['hpzl']]
                else:
                    logger.error('hpzl is no map value msg is %s' % item)
                    return None
                # 路口id
                if info['lkbh'] in RoadInfo.mapdata.keys():
                    info['lkid'] = RoadInfo.mapdata[info['lkbh']]
                else:
                    logger.error('lkbh is no map value msg is %s' % info['lkbh'])
                    return None
                # 方向id
                info['fxid'] = FrmStatus.data['direction'][info['fxbh']]
                # 车道id
                info['cdid'] = FrmStatus.data['carpath'][info['cdbh']]
                # 设备编号
                info['sbbh'] = '147' + values[0][5:][5:]
                # 违法报警p
                info['wfbj'] = values[8][5:]
                if values[8][5:] != '0':
                    info['wfbj'] = '1'
                # 通行日期
                info['txrq'] = values[1][5:][5:8]
                logger.info('info = %s' % info)
                data.append(info)
                return data
        except Exception, e:
            logger.error('parser error %s, filename =', (e.message, item))

    @staticmethod
    def parser_violation_format(item):
        data = []
        try:
            info = {}
            values = None
            with open(item, 'r') as file_object:
                items = [line.strip('\r\n') for line in file_object.readlines()]
                values = items

            if values:
                if values[8][5:] not in FrmStatus.data['wzxw'].keys():
                    logger.error('database is not exist current wzxw: %s' % values[8][5:])
                    return None
                
                if values[8][5:] == '1211':
                    return None
                logger.debug('violation-file: %s' % item)
                # id
                info['id'] = VehPass.getMaxId('VEH_VIOLATION')
                # 号牌号码
                info['hphm'] = values[2][5:].decode(gbk).strip()#.decode('utf-8').encode('gbk')
                if info['hphm'] == '无车牌':
                    info['hphm'] = 'NA'
                # 号牌颜色
                info['hpys'] = values[3][5:].decode('gbk')
                if info['hpys'] == '白':
                    info['hpys'] = '0'
                elif info['hpys'] == '黃':
                    info['hpys'] = '1'
                elif info['hpys'] == '蓝':
                    info['hpys'] = '2'
                elif info['hpys'] == '黑':
                    info['hpys'] = '3'
                elif info['hpys'] == '未知':
                    info['hpys'] = '4'
                # 号牌种类
                info['hpzl'] = '02'
                # 路口编号
                info['lkbh'] = values[0][5:][:-3] + '000'
                # 方向编号
                info['fxbh'] = values[7][5:].decode('gbk').strip()
                if info['fxbh'] == '由东向西':
                    info['fxbh'] = '02'
                elif info['fxbh'] == '由西向东':
                    info['fxbh'] = '01'
                elif info['fxbh'] == '由南向北':
                    info['fxbh'] = '03'
                elif info['fxbh'] == '由北向南':
                    info['fxbh'] = '04'
                # 车道编号
                info['cdbh'] = '%d' % int(values[5][5:])
                # 车辆速度
                info['clsd'] = values[6][5:]
                # 车身颜色
                info['csys'] = values[9][5:]
                # filepath
                info['filepath1'] = VehPass.filename_format(item)#.decode('utf-8').encode('gbk')
                # filepath2
                info['filepath2'] = VehPass.filename_format(item)#.decode('utf-8').encode('gbk')
                # filepath3
                info['filepath3'] = VehPass.filename_format(item)#.decode('utf-8').encode('gbk')
                # 经过时间
                info['jgsj'] = datetime.strptime(values[1][5:][:-3], '%Y%m%d%H%M%S')
                # 号牌种类id
                if info['hpzl'] in FrmStatus.data['hpzl'].keys():
                    info['hpzlid'] = FrmStatus.data['hpzl'][info['hpzl']]
                else:
                    logger.error('hpzl is no map value msg is %s' % item)
                    return None
                # 车辆类型
                info['cllx'] = ''
                # 方向id
                info['fxid'] = FrmStatus.data['direction'][info['fxbh']]
                # 车道id
                info['cdid'] = FrmStatus.data['carpath'][info['cdbh']]
                # 设备编号
                info['sbbh'] = '147' + values[0][5:][5:]
                # 采集方式
                info['cjfs'] = '0'
                # 违法地址
                info['wfdz'] = RoadInfo.mapdata[info['lkbh']]
                # 审核状态
                info['shzt'] = '0'
                # 违法地点id
                info['wfddid'] = RoadInfo.mapdata[info['lkbh']]
                # 违法行为
                info['wfxw'] = values[8][5:]
                # 违法行为id
                info['wfxwid'] = FrmStatus.data['wzxw'][info['wfxw']]
                
                info['shr'] = 0
                info['tzsh'] = 0
                info['shsj'] = datetime.strptime(values[1][5:][:-3], '%Y%m%d%H%M%S')
                info['tzrq'] = datetime.strptime(values[1][5:][:-3], '%Y%m%d%H%M%S')
                
                logger.info('violation = %s' % info)
                data.append(info)
                return data
        except Exception, e:
            logger.error('parser error %s, filename =', (e.message, item))
        
    @staticmethod
    def insert_data(item):
        try:
            vehpass = VehPass.parser_format(item)
            if vehpass:
                VehPass.insert_veh_pass(vehpass)
        except Exception, e:
            logger.error('Oracle Error: %s filename: %s' % (e.message, item))
        
        try:
            hispass = VehPass.parser_his_format(item)
            if hispass:
                VehPass.insert_veh_pass_his(hispass)
        except Exception, e:
            logger.error('Oracle Error: %s filename: %s' % (e.message, item))
        
        try:
            violation = VehPass.parser_violation_format(item)
            if violation:
                VehPass.insert_veh_pass_violation(violation)
        except Exception, e:
            logger.error('Oracle Error: %s filename: %s' % (e.message, item))
                    
    @staticmethod
    def getMaxId(table_name):
        try:
            conn = Connection.get_conn('yushi')
            if conn:
                cursor = conn.cursor()
                # plsql出参
                max_id = cursor.var(cx_Oracle.STRING)
                # 调用存储过程
                cursor.callproc('fndj.getmaxid', [table_name, max_id])
                cursor.close()
                return max_id.getvalue()
			
        except cx_Oracle.Error, e:
            logger.error('Oracle Error: %s' % e.args)

    @staticmethod
    def filename_format(filename):
        try:
            values = None
            with open(filename, 'r') as file_object:
                items = [line.strip('\r\n') for line in file_object.readlines()]
                values = items

            if values:
                date = values[1][5:][:10]
                ip = values[0][5:][-3:]
                jgsj = values[1][5:]
                fxbh = values[7][5:].decode('gbk').strip()
                if fxbh == '由东向西':
                    fxbh = '2'
                elif fxbh == '由西向东':
                    fxbh = '1'
                elif fxbh == '由南向北':
                    fxbh = '3'
                elif fxbh == '由北向南':
                    fxbh = '4'
                cdbh = '%d' % int(values[5][5:])
                hphm = values[2][5:].decode('gbk').strip()
                if hphm == '无车牌':
                    hphm = 'NA'
                # 处理后图片存放规则：时间/ip/*.jpg
                dest_filename = date + '/' + ip + '/' + jgsj + '_' + fxbh + '_' + cdbh + '_' + hphm + '_1.jpg'
                return dest_filename
        except Exception, e:
            logger.error('parser filename failed: %s' % e.message)
            return None

    @staticmethod
    def test():
        data = []
        info = {}
        info['id'] = '123456'
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
