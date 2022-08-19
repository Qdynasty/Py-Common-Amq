#!/usr/bin/env python
# -*- coding:utf-8 -*-

import threading
import json
import logging
from kafka import KafkaConsumer, KafkaProducer
from kafka.errors import KafkaError


local = threading.local()
logger = logging.getLogger()


class Service(object):

    def __init__(self, **option):
        self.servers = option.get('servers')
        self.sub_topics = option.get('sub_topics')
        self.pub_topic = option.get('pub_topics')
        self.retry_count = option.get('retry_count')
        self.current_count = 0

    def link(self):
        return self

    #############################################
    #  Kafka
    #############################################
    @property
    def consumer(self):
        _consumer = KafkaConsumer(
            bootstrap_servers=self.servers,
            # client_id='trunk',
            # group_id='trunk_prod',
            # earliest :当各分区下有已提交的offset时,从提交的offset开始消费;无提交的offset时,从头开始消费
            # latest：当各分区下有已提交的offset时,从提交的offset开始消费;无提交的offset时,消费新产生的该分区下的数据
            # none:topic各分区都存在已提交的offset时,从offset后开始消费;只要有一个分区不存在已提交的offset,则抛出异常
            auto_offset_reset='latest',
            # 接收json数据
            value_deserializer=lambda m: json.loads(m.decode('utf-8'))
        )
        _consumer.subscribe(self.sub_topics)
        return _consumer

    @property
    def producer(self):
        return KafkaProducer(
            bootstrap_servers=self.servers,
            # 每条消息的最大大小
            max_request_size=1024 * 1024 * 1,
            # 重试次数item_resource_index_test
            retries=self.retry_count,
            # 发送json数据z
            value_serializer=lambda m: json.dumps(m).encode('utf-8')
        )

    def publish_msg(self, msg, pub_topic, partition=None, times=0):
        if times > 3:
            logging.error(f'this {self.pub_topic}, msg: {msg}, lost...')
            return False

        try:
            # 发送到指定的消息主题（异步，不阻塞）
            self.producer.send(
                pub_topic, value=msg, partition=partition
            ).add_callback(self.on_send_success).add_errback(self.on_send_error)
            # 获取发送结果（阻塞），超时时间为空则一直等待
            # record_metadata = record_metadata.get(timeout=60)
            self.producer.flush()
        except KafkaError as e:
            logging.error(f'send msg ext has error, {e}')

            # 重试机制
            return self.producer.send(msg, times + 1)

    # 发送成功的回调函数
    def on_send_success(self, record_metadata):
        pass

    # 发送失败的回调函数
    def on_send_error(self, excp):
        logging.error(f'send msg: {excp}')

    def close(self):
        self.consumer.close()
        self.producer.close()


