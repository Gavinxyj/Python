#!/usr/bin/env python
# @author   youjiang xie
# @E-mail   xie_youjiang@163.com
# @time     2017/6/7 0007 11:38
# @project  Python
# @file     KafkaOperatorImpl
import logging
from kafka import KafkaProducer
logger = logging.getLogger("kakou.database")

class KafkaImpl(object):

    def __init__(self, args):
        self.producer = KafkaProducer(bootstrap_servers=args['url'])
        self.topic = args['topic']

    def send_message(self, msg):
        try:
            if msg:
                self.producer.send(self.topic, bytes(msg))
        except Exception, e:
            logger.error('kafka send msg error, msg : %s error: %s' % (msg, e.message))

    def close(self):
        self.producer.close()
