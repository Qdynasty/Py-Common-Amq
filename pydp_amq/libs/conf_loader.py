#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
from .config_file import ConfigFile
from .registry import Registry

"""全局路径"""
service_root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

"""初始化配置"""
GlobalConfigFile = ConfigFile(os.path.join(service_root_path, 'configs'))

"""app 配置"""
app_options = Registry(GlobalConfigFile.load_app('app'))

"""rmq 配置"""
rmq_options = Registry(GlobalConfigFile.load_app('rmq'))

"""server 配置"""
server_options = Registry(GlobalConfigFile.load_app('server'))
