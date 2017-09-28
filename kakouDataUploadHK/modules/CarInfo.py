#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @author   youjiang xie
# @E-mail   xie_youjiang@163.com
# @time     2017/6/7 0007 18:45
# @project  Python
# @file     CarInfo

import os, os.path
import json
import time
import logging
from utils.TimeUtils import TimeUtils

logger = logging.getLogger("kakou.modules")


class CarInfo(object):
    
    @staticmethod
    def parser_format(item, mapData):
        try:
            info = {}
            values = None

            if item[-3:] != 'ini':
                    return None
            with open(item, 'r') as file_object:
                items = [line.strip('\r\n') for line in file_object.readlines()]
                values = items
            if values:
                # id
                info['id'] = ''
                # 车辆品牌
                info['clpp'] = ''
                # 抓拍方向
                info['zpfx'] = ''
                # 设备编号
                info['sbbh'] = values[0][5:]
                # 卡口编号
                info['kkbh'] = values[0][5:][:-3] + '000'
                if info['kkbh'] in mapData.keys():
                    info['kkbh'] = mapData[info['kkbh']]
                else:
                    logger.error('kkbh map failed, filename = ' % item)
                    return None
                # 车辆通过时间
                info['tgsj'] = TimeUtils.convert_time_format(values[1][5:], '%Y%m%d%H%M%S', '%Y-%m-%d %H:%M:%S')
                # 号牌号码
                if values[2][5:].decode('gbk').strip() == '无车牌':
                    info['hphm'] = '未识别'
                else:
                    info['hphm'] = values[2][5:].decode('gbk')
                # 车辆通行状态               
                info['cltxzt'] = '1'
               
                # 号牌种类
                info['hpzl'] = '02'
                # 行驶速度
                info['xssd'] = values[6][5:]
                # 车道编号
                info['cdbh'] = '%02d' % int(values[5][5:])
                # 车行方向
                info['cxfx'] = values[7][5:].decode('gbk').strip()
                if info['cxfx'] == '由东向西':
                    info['cxfx'] = '01'
                elif info['cxfx'] == '由西向东':
                    info['cxfx'] = '02'
                elif info['cxfx'] == '由南向北':
                    info['cxfx'] = '03'
                elif info['cxfx'] == '由北向南':
                    info['cxfx'] = '04'
                # 车身颜色q

                info['csys'] = values[9][5:]
                # 车辆特征图像1
                info['tplj1'] = ''
                # 车辆特征图像2
                info['tplj2'] = ''
                # 车辆特征图像3
                info['tplj3'] = ''
                strjson = json.dumps(info, ensure_ascii=False, sort_keys=True)
                logger.debug('strjson = %s' % strjson)
                return strjson
        except Exception as e:
            logger.error('parser_format is failed filename: ' % item)
            

    @staticmethod
    def dest_dir_format(str_json):
        try:
            date= TimeUtils.convert_time_format(str_json['tgsj'],'%Y-%m-%d %H:%M:%S', '%Y%m%d%H%M%S', True)[:8]
            kkbh= str_json['sbbh'][:-3] + '000'
            xsfx= '%d' % int(str_json['cxfx'])
            cphm = str_json['hphm']
            if cphm == '未识别':
                cphm = '000'
            else:
                for item in cphm[::-1]:
                    if item.isdigit():
                        cphm = item
                        break

            # 处理后图片存放规则：日期 / 卡口 / 方向 / 号牌最后一位 / 号牌种类_号牌号码_通过时间_1（ or 2）.jpg
            dest_filename = '2' + "_" + str_json['hphm'] + "_" + \
                            TimeUtils.convert_time_format(str_json['tgsj'],'%Y-%m-%d %H:%M:%S', '%Y%m%d%H%M%S', True) + "_" + '1.jpg'
            dest_dir = date + '/' + kkbh + '/' + xsfx + '/' + cphm + '/' + dest_filename 

            return dest_dir
        except Exception, e:
            logger.error('parser filename failed: %s' % e.message)
            return None