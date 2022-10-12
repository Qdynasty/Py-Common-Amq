#!/usr/bin/env python
# -*- coding:utf-8 -*-

import logging

logger = logging.getLogger()


class MqSect(object):

    def __init__(self, signal_agent, mqtt_client, interface_bind, consumer_queue):
        self.signal_agent = signal_agent
        self.mqtt_client = mqtt_client
        self.bind_option = interface_bind.get('interface_bind')
        self.consumer_queue = consumer_queue
        self.mqtt_client.client.on_connect = self.mqtt_on_connect
        self.mqtt_client.client.on_message = self.mqtt_on_message
        self.mqtt_client.client.on_disconnect = self.mqtt_on_disconnect

    def handle(self):
        self.mqtt_client.client.loop_forever()

    def mqtt_on_disconnect(self, client, user_data, rc):
        """MQTT 断开事件"""
        logger.error('mqtt disconnect rc=%s' % rc)

    def mqtt_on_connect(self, client, user_data, flags, rc):
        """MQTT 链接事件"""
        topic_qos_list = [
            (topic_qos.get('topic'), topic_qos.get('qos'),)
            for topic_qos in list(self.bind_option.values())
        ]
        logger.info('Listening topic : {}'.format(topic_qos_list))
        self.mqtt_client.client.subscribe(topic_qos_list)

    def mqtt_on_message(self, client, user_data, msg):
        """消息接收"""
        topic = msg.topic
        payload = msg.payload.decode()
        qos = msg.qos
        pb_structure = topic.split('/')[-2]
        if not pb_structure:
            return
        server_name = self.mqtt_client.user
        bind_config = self.bind_option.get(pb_structure)
        callback_agent = bind_config.get('callback_agent')

        consumer_mode = bind_config.get('consumer_mode')
        callback_data = dict(
            sender=server_name,
            topic=topic,
            msg=msg,
            user_data=user_data,
        )
        if consumer_mode.get('agent'):
            getattr(self.signal_agent, callback_agent).send(data=callback_data)

        if consumer_mode.get('queue'):
            if self.consumer_queue.full():
                logger.error(f'Serious warning ⚠ \r\n'
                             f'The queue cache has reached the maximum limit ?_？\r\n'
                             f'Check queue consumption application！')
                self.consumer_queue.get()
            self.consumer_queue.put(callback_data)
