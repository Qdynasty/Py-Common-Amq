#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Intro: Component connector
# Author: Q.dynasty
# Version: 1.0.0

from types import SimpleNamespace

from pydp_amq.libs.excepts import ExceptionWarning
from pydp_amq.libs.mods import DirMods


class ManageConnector(object):

    def __init__(self):
        self.server_register = None
        self.handler_register = None

    def register_connector(self, server_switch):
        """
        @describe 注册连接器
            @param server_switch:  链接服务开关
        """
        dir_mods = DirMods('pydp_amq.apps.connectors')
        connector_parsers = {name_path.split('.')[-1][:-7]: mod for name_path, mod in dir_mods.mods.items()}
        registers = dict()
        for server_alias in server_switch:
            registers[server_alias] = getattr(
                connector_parsers[server_alias.split('_')[0]], 'Service'
            )
        if registers:
            self.server_register = SimpleNamespace(**registers)

    def register_handler(self, server_switch):
        """
        @describe 注册处理器
            @param server_switch:  链接服务开关
        """
        dir_mods = DirMods('pydp_amq.apps.handlers')
        handler_parsers = {name_path.split('.')[-1]: mod for name_path, mod in dir_mods.mods.items()}
        registers = dict()
        for server_alias in server_switch:
            registers[server_alias] = getattr(
                handler_parsers[server_alias.split('_')[0]], 'MqSect'
            )
        if registers:
            self.handler_register = SimpleNamespace(**registers)

    def conn_server(self, server_alias, server_options):
        """
        @note 服务链接
            服务别名：链接器
        @param server_alias:
        @param server_options:
        @return:
        """
        if not server_alias:
            raise ExceptionWarning('Please add a linked data source.')
        service = getattr(self.server_register, server_alias)
        return service(**server_options.get('server'))

    def handler_dispatch(self, signal_agent, client, callback_queue, server_options, server_alias):
        """
        处理器调运
        @return:
        """
        if not server_alias:
            raise ExceptionWarning('Please add a linked data source.')
        handler = getattr(self.handler_register, server_alias)
        return handler(
            signal_agent,
            client,
            server_options.get(server_alias),
            callback_queue
        )
