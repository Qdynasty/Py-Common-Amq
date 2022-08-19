#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Date: 2022/2/22

import os
import re
import setuptools


with open('README.md', 'r') as fd:
    long_description = fd.read()


def get_version(package):
    """
    Return package version as listed in `__version__` in `init.py`.
    """
    init_py = open(os.path.join(package, 'version.py')).read()
    return re.search("__version__ = ['\"]([^'\"]+)['\"]", init_py).group(1)


version = get_version('pydp_amq')


setuptools.setup(
    name='pydp-amq',
    version=version,
    author='Wang Chao',
    author_email='wangchao@trunk.tech',
    description='Python Data Process',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='http://git-rd.trunk.tech/wangchao2/cm.git',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=[
        'click==7.1.2',
        'arrow==1.0.3',
        'pika==1.2.0',
        'PyYAML==5.4.1',
        'cython==0.29.23',
        'kafka-python==2.0.2',
        'paho-mqtt>=1.5.1',
        'mergedict',
    ]
)
