#!/usr/bin/env python
# -*- coding:utf-8 -*-

import logging
import traceback

from kafka.errors import KafkaError

logger = logging.getLogger()


class MqSect(object):

    def __init__(self, signal_agent, kafka_client, interface_bind, consumer_queue):
        self.signal_agent = signal_agent
        self.kafka_client = kafka_client
        self.bind_option = interface_bind.get('interface_bind')
        self.consumer_queue = consumer_queue

    def handle(self):
        try:
            for msg in self.kafka_client.consumer:
                self.callback(msg)
        except KafkaError as e:
            logger.error(f'核心通信: Kafka server midway chain break => {e} username: {self.kafka_client.servers} \r\n'
                         f'准备重连 ......')
            self.kafka_client.link()
            self.handle()
        except Exception as e:
            logger.error(f'Kafka server Abnormal connection {e}')
            self.kafka_client._conn()
            self.handle()

    def callback(self, msg):
        try:
            routing_key = msg.topic
            pb_structure = routing_key.split('.')[4]
            if not pb_structure: return
            server_name = self.kafka_client.servers
            bind_config = self.bind_option.get(pb_structure)
            callback_agent = bind_config.get('callback_agent')
            consumer_mode = bind_config.get('consumer_mode')
            callback_data = dict(sender=server_name, data=msg)
            if consumer_mode.get('agent'):
                getattr(self.signal_agent, callback_agent).send(data=callback_data)

            if consumer_mode.get('queue'):
                if self.consumer_queue.full():
                    logger.error(f'Serious warning ⚠ \r\n'
                                 f' The queue cache has reached the maximum limit ?_？\r\n'
                                 f'Check queue consumption application！！！！！')
                    self.consumer_queue.get()
                self.consumer_queue.put(callback_data)
        except AttributeError as e:
            logger.error(f"⚠️ config->interface_bind:{self.bind_option} not exist {pb_structure}"
                         f"\n error:{traceback.format_exc()}")
