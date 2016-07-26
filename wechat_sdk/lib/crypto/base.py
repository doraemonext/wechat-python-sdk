# -*- coding: utf-8 -*-

import base64
import string
import random
import struct
import socket
import six
from Crypto.Cipher import AES

from wechat_sdk.lib.crypto.pkcs7 import PKCS7Encoder
from wechat_sdk.lib.crypto.exceptions import EncryptAESError, DecryptAESError, IllegalBuffer, ValidateAppIDError
from wechat_sdk.utils import to_text, to_binary


class BaseCrypto(object):
    """提供接收和推送给公众平台消息的加解密接口"""

    def __init__(self, key):
        # self.key = base64.b64decode(key+"=")
        self.key = key
        # 设置加解密模式为AES的CBC模式
        self.mode = AES.MODE_CBC

    def encrypt(self, text, appid):
        """对明文进行加密

        @param text: 需要加密的明文
        @return: 加密得到的字符串
        """
        # 16位随机字符串添加到明文开头
        text = self.get_random_str() + struct.pack("I", socket.htonl(len(text))) + to_binary(text) + appid
        # 使用自定义的填充方式对明文进行补位填充
        pkcs7 = PKCS7Encoder()
        text = pkcs7.encode(text)
        # 加密
        cryptor = AES.new(self.key, self.mode, self.key[:16])
        try:
            ciphertext = cryptor.encrypt(text)
            # 使用BASE64对加密后的字符串进行编码
            return base64.b64encode(ciphertext)
        except Exception as e:
            raise EncryptAESError(e)

    def decrypt(self, text, appid):
        """对解密后的明文进行补位删除

        @param text: 密文
        @return: 删除填充补位后的明文
        """
        try:
            cryptor = AES.new(self.key, self.mode, self.key[:16])
            # 使用BASE64对密文进行解码，然后AES-CBC解密
            plain_text = cryptor.decrypt(base64.b64decode(text))
        except Exception as e:
            raise DecryptAESError(e)

        try:
            if six.PY2:
                pad = ord(plain_text[-1])
            else:
                pad = plain_text[-1]
            # 去掉补位字符串
            # pkcs7 = PKCS7Encoder()
            # plain_text = pkcs7.encode(plain_text)
            # 去除16位随机字符串
            content = plain_text[16:-pad]
            xml_len = socket.ntohl(struct.unpack("I", content[: 4])[0])
            xml_content = content[4: xml_len + 4]
            from_appid = content[xml_len + 4:]
        except Exception as e:
            raise IllegalBuffer(e)
        if from_appid != appid:
            raise ValidateAppIDError()
        return xml_content

    def get_random_str(self):
        """ 随机生成16位字符串

        @return: 16位字符串
        """
        rule = string.ascii_letters + string.digits
        return "".join(random.sample(rule, 16))
