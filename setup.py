#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name = 'wechat-sdk',
    version = '0.1',
    keywords = ('wechat', 'sdk'),
    description = 'A Python SDK for WeChat.',
    license = 'BSD License',

    url = 'http://oott.me',
    author = 'doraemonext',
    author_email = 'doraemonext@gmail.com',

    packages = find_packages(),
    include_package_data = True,
    platforms = 'any',
    install_requires = [],
)