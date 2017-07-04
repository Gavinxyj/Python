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
    def parser_format(arrayData, mapData):
        data = []
        for item in arrayData:
            info = {}
            path = os.path.split(item)[0]
            fileName = os.path.split(item)[1]

            values = fileName.split('_')

            if values[len(values) - 1] != '1.jpg':
                continue

            if len(values) < 12:
                logger.error('this file is illegal, this file name is ' % fileName)

            # id
            info['id'] = ''

            # 车辆品牌
            info['clpp'] = ''

            # 抓拍方向
            info['zpfx'] = ''

            # 设备编号
            info['sbbh'] = values[0]

            # 卡口编号
            info['kkbh'] = values[0][:-3] + '000'

            if info['kkbh'] in mapData.keys():
                info['kkbh'] = mapData[info['kkbh']]
            else:
                continue

            # 车辆通过时间
            info['tgsj'] = TimeUtils.convert_time_format(values[1], '%Y%m%d%H%M%S', '%Y-%m-%d %H:%M:%S')
            # 号牌号码
            if values[2] == '-':
                info['hphm'] = '未识别'
            else:
                info['hphm'] = values[2]

            # 车辆通行状态
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
            strjson = json.dumps(info, ensure_ascii=False, sort_keys=True)

            data.append(strjson)
        return data

    @staticmethod
    def dest_dir_format(filename):
        try:
            if filename:
                values = filename.split('_')
                date = values[1][:8]
                kkbh = values[0][:-3] + '000'
                xsfx = values[7]
                cphm = values[2]
                if cphm == '-':
                    cphm = '000'
                else:
                    for item in cphm[::-1]:
                        if item.isdigit():
                            cphm = item
                            break

                # 处理后图片存放规则：日期 / 卡口 / 方向 / 号牌最后一位 / 号牌种类_号牌号码_通过时间_1（ or 2）.jpg
                dest_filename = values[4] + "_" + values[2] + "_" + values[1] + "_" + values[len(values) - 1]
                dest_dir = date + '/' + kkbh + '/' + xsfx + '/' + cphm + '/' + dest_filename 

                return dest_dir
        except Exception, e:
            logger.error('parser filename failed: %s' % e.message)
            return None
