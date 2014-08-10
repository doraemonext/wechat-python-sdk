# -*- coding: utf-8 -*-


class NeedParamError(Exception):
    """
    构造参数提供不全异常
    """
    pass


class ParseError(Exception):
    """
    解析微信服务器数据异常
    """
    pass


class NeedParseError(Exception):
    """
    尚未解析微信服务器请求数据异常
    """
    pass


class OfficialAPIError(Exception):
    """
    微信官方API请求出错异常
    """
    pass