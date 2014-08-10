# -*- coding: utf-8 -*-
#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name = 'wechat-sdk',
    version = '0.2',
    keywords = ('wechat', 'sdk', 'wechat sdk'),
    description = u'微信公众平台Python开发包',
    long_description = u"""
https://github.com/doraemonext/wechat-python-sdk

当前进度正在开发中，非官方接口功能尚未开发完成，文档正在完善中，仅供测试使用，请耐心等待。

非官方微信公众平台 Python 开发包，包括官方接口和非官方接口。

官方接口依据公众平台开发者文档编写，可以实现公众平台开发者文档中的所有内容；

非官方接口采用模拟登陆的方式，可以实现更多高级功能，但也存在相应风险。尤其注意，本开发包不提供群发功能，此功能被微信公众平台明令禁止。
    """,
    license = 'BSD License',

    url = 'https://github.com/doraemonext/wechat-python-sdk',
    author = 'doraemonext',
    author_email = 'doraemonext@gmail.com',


    packages = find_packages(),
    include_package_data = True,
    platforms = 'any',
    install_requires = ['requests'],
)