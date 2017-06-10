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
import logging.config
from utils.TimeUtils import TimeUtils

logging.config.fileConfig('config/logging.conf')
logger = logging.getLogger("kakou")


class CarInfo(object):

    @staticmethod
    def parser_format(arrayData, mapData):
        data = []
        for item in arrayData:
            info = {}
            path = os.path.split(item)[0]
            fileName = os.path.split(item)[1]

            values = fileName.split('_')

            if len(values) < 12:
                logger.error('this file is illegal, this file name is ' % fileName)
            # 卡口编号
            info['kkbh'] = values[0]

            if values[0] in mapData.keys():
                info['kkbh'] = mapData[values[0]]
            else:
                continue

            # 车辆通过时间
            info['tgsj'] = TimeUtils.convert_time_format(values[1], '%Y%m%d%H%M%S', '%Y-%m-%d %H:%M:%S')
            # 号牌号码
            if values[2] == '-':
                info['hphm'] = '未识别'
            else:
                info['hphm'] = values[2]

            #车辆通行状态
            if values[8] == '0':
                info['cltxzt'] = '1'
            else:
                info['cltxzt'] = '2'

            # 号牌种类
            info['hpzl'] = '%02d' % int(values[4])
            # 行驶速度
            info['xssd'] = values[6]
            # 车道编号
            info['cdbh'] = '%02d' % int(values[5])
            # 车行方向
            info['cxfx'] = '%02d' % int(values[7])
            # 车身颜色
            info['csys'] = values[9]
            # 车辆特征图像1
            info['tplj1'] = ''
            # 车辆特征图像2
            info['tplj2'] = ''
            # 车辆特征图像3
            info['tplj3'] = ''
            strjson = json.dumps(info, ensure_ascii=False)
            data.append(strjson)
        return data
