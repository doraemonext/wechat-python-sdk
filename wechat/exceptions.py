# -*- coding: utf-8 -*-


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