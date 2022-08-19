#!/usr/bin/env python
# -*- coding:utf-8 -*-

import time
import logging
import paho.mqtt.client as mqtt

logger = logging.getLogger()


class Service(object):

    def __init__(self, **option):
        self.client_id = option.get('client_id')
        self.host = option.get('host')
        self.port = option.get('port')
        self.keep_alive = option.get('keep_alive', 60)
        self.user = option.get('user')
        self.password = option.get('password')
        self.retry_count = option.get('retry_count')
        self.clean_session = option.get('clean_session', False)

    def link(self):
        self.auth()
        self._conn()

    def auth(self):
        # Set a username and optionally a password for broker authentication.
        self.client = mqtt.Client(client_id=self.client_id)
        self.client.username_pw_set(
            username=self.user,
            password=self.password
        )

    def _start_consuming(self):
        self.client.loop_forever()

    def _conn(self):
        current_count = 0
        try:
            # create connection & channel
            self.client.connect(
                host=self.host,
                port=self.port,
                keepalive=self.keep_alive,
            )
            logger.info('MQTT server connection successful (p≧w≦q) ')
        except Exception as e:
            logger.error(f' 核心通信: MQTT server Not available => {e} username: {self.user} \r\n'
                         f' 准备重连 ......')
            time.sleep(2)
            current_count += 1
            if current_count <= self.retry_count:
                self._conn()

    def publish_msg(self, topic, qos, payload):
        self.client.publish(
            topic, payload=payload, qos=qos or 0, retain=False, properties=None
        )

    def _get_ack(self):
        pass

    def heart_beat(fn):
        """
        MQTT 连接心跳检测, 所有执行MQTT操作的动作需要加该装饰器
        :param fn:
        :return:
        """

        def wrapper(cls, *args, **kwargs):
            if not cls.connection or not cls.connection.is_open:
                connection = cls.conn()
                if not connection:
                    logger.error('Can not connect to the MQTT server, abort')
                    return False

            return fn(cls, *args, **kwargs)

        return wrapper
