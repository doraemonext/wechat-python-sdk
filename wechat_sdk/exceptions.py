# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals
import six

from wechat_sdk.utils import to_binary, to_text


class WechatException(Exception):
    """wechat-python-sdk 异常基类"""
    pass


class WechatAPIException(WechatException):
    """官方 API 错误异常（必须包含错误码及错误信息）"""
    def __init__(self, errcode, errmsg):
        """
        :param errcode: 错误代码
        :param errmsg: 错误信息
        """
        self.errcode = errcode
        self.errmsg = errmsg

    def __str__(self):
        if six.PY2:
            return to_binary('{code}: {msg}'.format(code=self.errcode, msg=self.errmsg))
        else:
            return to_text('{code}: {msg}'.format(code=self.errcode, msg=self.errmsg))


class WechatSDKException(WechatException):
    """SDK 错误异常（仅包含错误内容描述）"""
    def __init__(self, message=''):
        """
        :param message: 错误内容描述，可选
        """
        self.message = message

    def __str__(self):
        if six.PY2:
            return to_binary(self.message)
        else:
            return to_text(self.message)


class NeedParamError(WechatSDKException):
    """构造参数提供不全异常"""
    pass


class ParseError(WechatSDKException):
    """解析微信服务器数据异常"""
    pass


class NeedParseError(WechatSDKException):
    """尚未解析微信服务器请求数据异常"""
    pass


class OfficialAPIError(WechatAPIException):
    """微信官方API请求出错异常"""
    def __init__(self, errcode, errmsg=None):
        if errmsg is None:  # 对旧版本 OfficialAPIError 的兼容代码
            super(OfficialAPIError, self).__init__(99999, errmsg=errcode)
            return
        super(OfficialAPIError, self).__init__(errcode, errmsg)


class UnOfficialAPIError(WechatSDKException):
    """微信非官方API请求出错异常"""
    pass


class NeedLoginError(UnOfficialAPIError):
    """微信非官方API请求出错异常 - 需要登录"""
    pass


class LoginError(UnOfficialAPIError):
    """微信非官方API请求出错异常 - 登录出错"""
    pass


class LoginVerifyCodeError(LoginError):
    """微信非官方API请求出错异常 - 登录出错 - 验证码错误"""
    pass



