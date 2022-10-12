#!/usr/bin/env python
# -*- coding:utf-8 -*-
import threading
import logging
from typing import List
from queue import Queue

from pydp_amq.apps.core import signals
from pydp_amq.apps.core.signals import SignalAgent
from pydp_amq.apps.managers import ManageConnector
from pydp_amq.libs.config_file import ConfigFile
from pydp_amq.libs.registry import Registry

logger = logging.getLogger(__name__)

ServerAlias = List[str]


class AMQSection(object):

    def __init__(self, config_dir, maxsize, server_params=None):
        """
        配置参数 ：
        @param config_dir :  配置目录
        @param server_params: 服务连接参数
        @param maxsize :  最大队列容量
        @warning: 队列容量更具实际需求配置默认 1000*60
        """
        self.server_options = dict()  # 服务别名映射服务配置
        self.server_params = server_params
        self.load_config(config_dir)
        self.manger = ManageConnector()
        self.signal_agent = SignalAgent(self.server_options)
        self.callback_queue = Queue(maxsize=maxsize or 1000 * 60)

        self.manger.register_connector(server_switch=self.server_switch)
        self.manger.register_handler(server_switch=self.server_switch)

    def load_config(self, config_dir):
        """配置加载"""
        config_file = ConfigFile(config_dir)
        server_options = Registry(config_file.load_app('server'))  # 别名开关
        self.server_switch = {
            server: value
            for server, value in server_options.get('server_switch').items()
            if value
        }
        for server_alias in self.server_switch:
            config = config_file.load_app(server_alias)
            if self.server_params is not None:
                config['server'] = self.server_params[server_alias]
            self.server_options[server_alias] = Registry(config)

    def listening(self, server_alias: ServerAlias):
        """
        被动触发惰性链接
        @server_alias: 启动链接服务别名
        @return:
        """
        for alias in server_alias:
            client = self.get_client(alias)
            client.link()

            # fixme 优化连接池 待确认
            # self.thread_pool.submit(fn=self.handler_consuming,
            #                         **{
            #                             "signal_agent": self.signal_agent,
            #                             "client": client,
            #                             "callback_queue": self.callback_queue,
            #                             "server_options": self.server_options,
            #                             "server_alias": alias
            #                         }
            #                         )

            thread = threading.Thread(target=self.handler_consuming,
                                      args=(
                                          self.signal_agent,
                                          client,
                                          self.callback_queue,
                                          self.server_options,
                                          alias)
                                      )
            thread.setDaemon(True)
            thread.start()

    def get_client(self, server_alias):
        return self.manger.conn_server(
            server_alias=server_alias,
            server_options=self.server_options.get(server_alias)
        )

    def handler_consuming(self, signal_agent, client, callback_queue, server_options, server_alias):
        handler = self.manger.handler_dispatch(
            signal_agent=signal_agent,
            client=client,
            callback_queue=callback_queue,
            server_options=server_options,
            server_alias=server_alias
        )
        handler.handle()

    def disconnect(self):
        # fixme 优化连接池 待确认
        # self.thread_pool.shutdown(wait=False)
        logger.warning("AMQSection Thread pool shutdown ！！！！！ ")
        import sys
        sys.exit()
