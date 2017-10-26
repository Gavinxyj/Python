#!/usr/bin/python
# -*- coding:utf-8 -*-

from kafka import KafkaProducer
import random

msg = ['{"cdbh": "01", "clpp": "", "cltxzt": "1", "csys": "H", "cxfx": "02", "hphm": "冀BTB401", "hpzl": "02", "id": "", "kkbh": "123", "sbbh": "735051002035", "tgsj": "2017-10-25 10:15:29 600", "tplj1": "", "tplj2": "", "tplj3": "", "xssd": "1", "zpfx": ""}',
       '{"cdbh": "02", "clpp": "", "cltxzt": "1", "csys": "H", "cxfx": "04", "hphm": "冀BTB780", "hpzl": "02", "id": "", "kkbh": "125", "sbbh": "835081001023", "tgsj": "2017-10-25 10:15:18 858", "tplj1": "", "tplj2": "", "tplj3": "", "xssd": "116", "zpfx": ""}',
       '{"cdbh": "01", "clpp": "", "cltxzt": "1", "csys": "H", "cxfx": "04", "hphm": "冀BTB894", "hpzl": "02", "id": "", "kkbh": "125", "sbbh": "835081001023", "tgsj": "2017-10-25 10:15:20 061", "tplj1": "", "tplj2": "", "tplj3": "", "xssd": "92", "zpfx": ""}',
       '{"cdbh": "02", "clpp": "", "cltxzt": "1", "csys": "Z", "cxfx": "02", "hphm": "未识别", "hpzl": "01", "id": "", "kkbh": "125", "sbbh": "835081001022", "tgsj": "2017-10-25 10:14:56 013", "tplj1": "", "tplj2": "", "tplj3": "", "xssd": "5", "zpfx": ""}',
       '{"cdbh": "01", "clpp": "", "cltxzt": "1", "csys": "B", "cxfx": "01", "hphm": "冀BWY277", "hpzl": "02", "id": "", "kkbh": "127", "sbbh": "635121018038", "tgsj": "2017-10-25 10:15:29 991", "tplj1": "", "tplj2": "", "tplj3": "", "xssd": "50", "zpfx": ""}' ]

class KafkaImpl(object):

    def __init__(self, args):
        self.producer = KafkaProducer(bootstrap_servers=args['url'])
        self.topic = args['topic']
        


    def handle(self):
        try:
            while True:
                print random.choice(msg)
                self.producer.send(self.topic, bytes(random.choice(msg)))
                self.producer.flush()
        except Exception as e:
            print e

    def close(self):
        self.producer.close()