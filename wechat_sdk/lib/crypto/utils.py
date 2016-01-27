# -*- coding: utf-8 -*-

import hashlib

from wechat_sdk.crypto.exceptions import CryptoComputeSignatureError


def get_sha1_signature(token, timestamp, nonce, encrypt):
    """
    用 SHA1 算法生成安全签名
    @param token: 票据
    @param timestamp: 时间戳
    @param encrypt: 密文
    @param nonce: 随机字符串
    @return: 安全签名
    """
    try:
        sortlist = [token, timestamp, nonce, encrypt]
        sortlist.sort()
        sha = hashlib.sha1()
        sha.update("".join(sortlist))
        return sha.hexdigest()
    except Exception as e:
        raise CryptoComputeSignatureError(e)
