# -*- coding: utf-8 -*-

from wechat_sdk.exceptions import WechatSDKException


class CryptoException(WechatSDKException):
    """加密解密异常基类"""
    pass


class CryptoComputeSignatureError(CryptoException):
    """签名计算错误"""
    pass


class EncryptAESError(CryptoException):
    """AES加密错误"""
    pass


class DecryptAESError(CryptoException):
    """AES解密错误"""
    pass


class IllegalBuffer(CryptoException):
    """不合法的缓冲区"""
    pass


class ValidateAppIDError(CryptoException):
    """验证AppID错误"""
    pass


class ValidateSignatureError(CryptoException):
    """验证签名错误"""
    pass


class ValidateAESKeyError(CryptoException):
    """验证AES Key错误"""
    pass
