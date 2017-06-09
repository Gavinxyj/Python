#!/usr/bin/env python
# @author   youjiang xie
# @E-mail   xie_youjiang@163.com
# @time     2017/6/7 0007 11:38
# @project  Python
# @file     KafkaOperatorImpl

from kafka import KafkaProducer


class KafkaImpl(object):

    def __init__(self, args):
        self.producer = KafkaProducer(bootstrap_servers=args['url'])
        self.topic = args['topic']

    def set_message(self, msg):
        self.producer.send(self.topic, msg)
        self.producer.flush()
