#!/usr/bin/env python
# -*- coding:utf-8 -*-

from pydp_amq.libs import signal


class SignalAgent:

    def __init__(self, server_options):
        self.generate(server_options)

    def generate(self, server_option):
        """生成指定链接器 signal"""
        # todo 回调书对象显式说明
        rmq_providing_args = {'sender', 'ch', 'method', 'properties', 'body'}
        mqtt_providing_args = {'sender', 'topic', 'msg'}
        for alias, bind_config in server_option.items():
            interface_option = bind_config.get('interface_bind') or {}
            for interface, options in interface_option.items():
                callback_agent = options.get('callback_agent')

                if alias.startswith('rmq'):
                    setattr(
                        self, callback_agent,
                        signal.Signal(
                            name=callback_agent,
                            providing_args=rmq_providing_args
                        )
                    )

                elif alias.startswith('mqtt'):
                    setattr(
                        self, callback_agent,
                        signal.Signal(
                            name=callback_agent,
                            providing_args=mqtt_providing_args
                        )
                    )
