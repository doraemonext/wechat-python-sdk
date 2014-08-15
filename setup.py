# -*- coding: utf-8 -*-
#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name = 'wechat-sdk',
    version = '0.3.4',
    keywords = ('wechat', 'sdk', 'wechat sdk'),
    description = u'微信公众平台Python开发包',
    long_description = open("README.rst").read(),
    license = 'BSD License',

    url = 'https://github.com/doraemonext/wechat-python-sdk',
    author = 'doraemonext',
    author_email = 'doraemonext@gmail.com',

    packages = find_packages(),
    include_package_data = True,
    platforms = 'any',
    install_requires=open("requirements.txt").readlines(),
)