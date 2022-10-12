#!/usr/bin/env python
# -*- coding:utf-8 -*-

import logging
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
            for msg in self.kafka_client:
                print(msg)
        except KafkaError as e:
            logger.error(f'核心通信: Rabbitmq server midway chain break => {e} username: {self.rmq_client.user} \r\n'
                         f'准备重连 ......')
            self.kafka_client._conn()
            self.handle()
        except Exception as e:
            logger.error(f'Rabbitmq server Abnormal connection {e}')
            self.kafka_client._conn()
            self.handle()

    def set_rmq_client(self):
        for key, params_dic in self.bind_option.items():
            self.rmq_client._exchange_declare(exchange=params_dic['exchange'])
            self.rmq_client._queue_declare(queue=params_dic['queue'], durable=params_dic['durable'])
            self.rmq_client._queue_bind(exchange=params_dic['exchange'], binding_key=params_dic['bind_key'])
            self.rmq_client._basic_consume(on_message_callback=self.callback, auto_ack=True)

    def callback(self, ch, method, properties, body):
        routing_key = method.routing_key
        pb_structure = routing_key.split('.')[4]
        if not pb_structure: return
        server_name = self.rmq_client.user
        bind_config = self.bind_option.get(pb_structure)
        callback_agent = bind_config.get('callback_agent')
        consumer_mode = bind_config.get('consumer_mode')
        callback_data = dict(
            sender=server_name,
            ch=ch,
            method=method,
            properties=properties,
            body=body
        )
        if consumer_mode.get('agent'):
            getattr(self.signal_agent, callback_agent).send(data=callback_data)

        if consumer_mode.get('queue'):
            if self.consumer_queue.full():
                logger.error(f'Serious warning ⚠ \r\n'
                             f' The queue cache has reached the maximum limit ?_？\r\n'
                             f'Check queue consumption application！！！！！')
                self.consumer_queue.get()
            self.consumer_queue.put(callback_data)

    def push_data(self, inter_pb, routing_key, data):
        exchange = self.bind_option.get(inter_pb).get('exchange')
        queue = self.bind_option.get(inter_pb).get('queue')
        self.rmq_client.publish_msg(
            data=data,
            exchange=exchange,
            queue=queue,
            routing_key=routing_key,
        )
