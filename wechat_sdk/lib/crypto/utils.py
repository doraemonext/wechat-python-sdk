# -*- coding: utf-8 -*-

import hashlib

from wechat_sdk.lib.crypto.exceptions import CryptoComputeSignatureError
from wechat_sdk.utils import to_binary


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
        sortlist = [token, timestamp, nonce, to_binary(encrypt)]
        sortlist.sort()
        sha = hashlib.sha1()
        sha.update(to_binary("").join(sortlist))
        return sha.hexdigest()
    except Exception as e:
        raise CryptoComputeSignatureError(e)
