# -*- coding: utf-8 -*-

__all__ = ['WechatBasic', 'WechatExt']

try:
    from wechat_sdk.basic import WechatBasic
    from wechat_sdk.ext import WechatExt
except ImportError:
    pass