# -*- coding: utf-8 -*-

import base64
import time

import six
import xmltodict

from wechat_sdk.exceptions import ParseError
from wechat_sdk.lib.crypto.base import BaseCrypto
from wechat_sdk.lib.crypto.utils import get_sha1_signature
from wechat_sdk.lib.crypto.exceptions import ValidateSignatureError, ValidateAESKeyError, DecryptAESError
from wechat_sdk.utils import to_binary, to_text


class WechatBaseCrypto(object):
    """微信加密解密基类"""

    def __init__(self, token, encoding_aes_key, _id):
        """构造函数

        :param token: 公众平台上，开发者设置的Token
        :param encoding_aes_key: 公众平台上，开发者设置的EncodingAESKey
        :param _id: 公众号的 appid 或企业号的 corpid
        """
        self.__key = base64.b64decode(to_binary(encoding_aes_key) + to_binary('='))
        if len(self.__key) != 32:
            raise ValidateAESKeyError(encoding_aes_key)
        self.__token = to_binary(token)
        self.__id = to_binary(_id)
        self.__pc = BaseCrypto(self.__key)

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
        try:
            return self.__pc.decrypt(echostr, self.__id)
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
        nonce = to_binary(nonce)
        timestamp = to_binary(timestamp) or to_binary(int(time.time()))
        encrypt = self.__pc.encrypt(to_text(msg), self.__id)
        # 生成安全签名
        signature = get_sha1_signature(self.__token, timestamp, nonce, encrypt)
        return to_text(xml.format(
            encrypt=to_text(encrypt),
            signature=to_text(signature),
            timestamp=to_text(timestamp),
            nonce=to_text(nonce)
        ))

    def _decrypt_message(self, msg, msg_signature, timestamp, nonce):
        """检验消息的真实性，并且获取解密后的明文

        :param msg: 密文，对应POST请求的数据
        :param msg_signature: 签名串，对应URL参数的msg_signature
        :param timestamp: 时间戳，对应URL参数的timestamp
        :param nonce: 随机串，对应URL参数的nonce
        :return: 解密后的原文
        """
        timestamp = to_binary(timestamp)
        nonce = to_binary(nonce)
        if isinstance(msg, six.string_types):
            try:
                msg = xmltodict.parse(to_text(msg))['xml']
            except Exception as e:
                raise ParseError(e)

        encrypt = msg['Encrypt']
        signature = get_sha1_signature(self.__token, timestamp, nonce, encrypt)
        if signature != msg_signature:
            raise ValidateSignatureError()
        return self.__pc.decrypt(encrypt, self.__id)


class BasicCrypto(WechatBaseCrypto):
    """微信普通公众号(订阅/服务号)加密解密类"""

    def __init__(self, token, encoding_aes_key, app_id):
        super(BasicCrypto, self).__init__(token, encoding_aes_key, app_id)
        self.__app_id = app_id

    def encrypt_message(self, msg, nonce, timestamp=None):
        return self._encrypt_message(msg, nonce, timestamp)

    def decrypt_message(self, msg, msg_signature, timestamp, nonce):
        return self._decrypt_message(msg, msg_signature, timestamp, nonce)


class CorpCrypto(WechatBaseCrypto):
    """微信企业号加密解密类"""

    def __init__(self, token, encoding_aes_key, corp_id):
        super(CorpCrypto, self).__init__(token, encoding_aes_key, corp_id)
        self.__corp_id = corp_id

    def check_signature(self, msg_signature, timestamp, nonce, echostr):
        return self._check_signature(msg_signature, timestamp, nonce, echostr)

    def encrypt_message(self, msg, nonce, timestamp=None):
        return self._encrypt_message(msg, nonce, timestamp)

    def decrypt_message(self, msg, msg_signature, timestamp, nonce):
        return self._decrypt_message(msg, msg_signature, timestamp, nonce)
