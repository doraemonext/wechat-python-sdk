# -*- coding: utf-8 -*-

import base64
import time

import six
import xmltodict

from wechat_sdk.exceptions import ParseError
from wechat_sdk.crypto.base import BaseCrypto
from wechat_sdk.crypto.utils import get_sha1_signature
from wechat_sdk.crypto.exceptions import ValidateSignatureError, ValidateAESKeyError, DecryptAESError
from wechat_sdk.utils import to_binary, to_text


class WechatBaseCrypto(object):
    """微信加密解密基类"""

    def __init__(self, token, encoding_aes_key, _id):
        """构造函数

        :param token: 公众平台上，开发者设置的Token
        :param encoding_aes_key: 公众平台上，开发者设置的EncodingAESKey
        :param _id: 公众号的 appid 或企业号的 corpid
        """
        self.__key = base64.b64decode(encoding_aes_key + '=')
        if len(self.__key) != 32:
            raise ValidateAESKeyError(self.__key)
        self.__token = token
        self.__id = _id

    def _check_signature(self, msg_signature, timestamp, nonce, echostr):
        """验证签名有效性

        :param msg_signature: 签名串，对应URL参数的msg_signature
        :param timestamp: 时间戳，对应URL参数的timestamp
        :param nonce: 随机串，对应URL参数的nonce
        :param echostr: 随机串，对应URL参数的echostr
        :return: 解密之后的echostr
        :raise ValidateSignatureError: 签名无效异常
        """
        signature = get_sha1_signature(self.__token, timestamp, nonce, echostr)
        if not signature == msg_signature:
            raise ValidateSignatureError()
        pc = BaseCrypto(self.__key)
        try:
            return pc.decrypt(echostr, self.__id)
        except DecryptAESError as e:
            raise ValidateSignatureError(e)

    def _encrypt_message(self, msg, nonce, timestamp=None):
        """将公众号回复用户的消息加密打包

        :param msg: 待回复用户的消息，xml格式的字符串
        :param nonce: 随机串，可以自己生成，也可以用URL参数的nonce
        :param timestamp: 时间戳，可以自己生成，也可以用URL参数的timestamp,如为None则自动用当前时间
        :return: 加密后的可以直接回复用户的密文，包括msg_signature, timestamp, nonce, encrypt的xml格式的字符串
        """
        xml = """<xml>
<Encrypt><![CDATA[{encrypt}]]></Encrypt>
<MsgSignature><![CDATA[{signature}]]></MsgSignature>
<TimeStamp>{timestamp}</TimeStamp>
<Nonce><![CDATA[{nonce}]]></Nonce>
</xml>"""
        timestamp = timestamp or to_binary(int(time.time()))
        pc = BaseCrypto(self.__key)
        encrypt = pc.encrypt(msg, self.__id)
        # 生成安全签名
        signature = get_sha1_signature(self.__token, timestamp, nonce, encrypt)
        return to_text(xml.format(
            encrypt=encrypt,
            signature=signature,
            timestamp=timestamp,
            nonce=nonce
        ))

    def _decrypt_message(self, msg, msg_signature, timestamp, nonce):
        """检验消息的真实性，并且获取解密后的明文

        :param msg: 密文，对应POST请求的数据
        :param msg_signature: 签名串，对应URL参数的msg_signature
        :param timestamp: 时间戳，对应URL参数的timestamp
        :param nonce: 随机串，对应URL参数的nonce
        :return: 解密后的原文
        """
        if isinstance(msg, six.string_types):
            try:
                msg = xmltodict.parse(to_text(msg))['xml']
            except Exception as e:
                raise ParseError(e)

        encrypt = msg['Encrypt']
        signature = get_sha1_signature(self.__token, timestamp, nonce, encrypt)
        if signature != msg_signature:
            raise ValidateSignatureError()
        pc = BaseCrypto(self.__key)
        return pc.decrypt(encrypt, self.__id)


class WechatCrypto(WechatBaseCrypto):
    """微信普通公众号(订阅/服务号)加密解密类"""

    def __init__(self, token, encoding_aes_key, app_id):
        super(WechatCrypto, self).__init__(token, encoding_aes_key, app_id)
        self.__app_id = app_id

    def encrypt_message(self, msg, nonce, timestamp=None):
        return self._encrypt_message(msg, nonce, timestamp)

    def decrypt_message(self, msg, msg_signature, timestamp, nonce):
        return self._decrypt_message(msg, msg_signature, timestamp, nonce)


class WechatCorpCrypto(WechatBaseCrypto):
    """微信企业号加密解密类"""

    def __init__(self, token, encoding_aes_key, corp_id):
        super(WechatCorpCrypto, self).__init__(token, encoding_aes_key, corp_id)
        self.__corp_id = corp_id

    def check_signature(self, msg_signature, timestamp, nonce, echostr):
        return self._check_signature(msg_signature, timestamp, nonce, echostr)

    def encrypt_message(self, msg, nonce, timestamp=None):
        return self._encrypt_message(msg, nonce, timestamp)

    def decrypt_message(self, msg, msg_signature, timestamp, nonce):
        return self._decrypt_message(msg, msg_signature, timestamp, nonce)
