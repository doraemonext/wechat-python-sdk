# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import os
import json
import time
import unittest

import xmltodict
from httmock import urlmatch, HTTMock, response

from wechat_sdk.core.conf import WechatConf
from wechat_sdk.exceptions import NeedParamError
from wechat_sdk.lib.crypto.base import BaseCrypto
from wechat_sdk.utils import to_binary
from tests.utils import api_weixin_mock


class TestBaseCrypto(BaseCrypto):

    def get_random_str(self):
        return to_binary('doraemonext')


class CoreConfTestCase(unittest.TestCase):
    token = 'test_token'
    appid = 'wx9354b770fe837911'
    appsecret = 'c994da14dca2047bb51caaedaf16f249'
    encoding_aes_key = 'hXMHI0zd8S4Hc14NRoSKvX8lw8jQhJ02N4bEXKh9tJc'

    fixtures_access_token = 'HoVFaIslbrofqJgkR0Svcx2d4za0RJKa3H6A_NjzhBbm96Wtg_a3ifUYQvOfJmV76QTcCpNubcsnOLmDopu2hjWfFeQSCE4c8QrsxwE_N3w'
    fixtures_jsapi_ticket = 'bxLdikRXVbTPdHSM05e5u5sUoXNKd8-41ZO3MhKoyN5OfkWITDGgnr2fwJ0m9E8NYzWKVZvdVtaUgWvsdshFKA'

    normal_request_message = """<xml>
    <ToUserName><![CDATA[gh_1b2959761a7d]]></ToUserName>
    <FromUserName><![CDATA[oJNCEjt3uIphaC1DrpB030QxMV_w]]></FromUserName>
    <CreateTime>1442129896</CreateTime>
    <MsgType><![CDATA[text]]></MsgType>
    <Content><![CDATA[xxx]]></Content>
    <MsgId>6193900740131666054</MsgId>
    </xml>"""
    compatible_request_message = """<xml>
    <ToUserName><![CDATA[gh_1b2959761a7d]]></ToUserName>
    <FromUserName><![CDATA[oJNCEjt3uIphaC1DrpB030QxMV_w]]></FromUserName>
    <CreateTime>1442129896</CreateTime>
    <MsgType><![CDATA[text]]></MsgType>
    <Content><![CDATA[xxx]]></Content>
    <MsgId>6193900740131666054</MsgId>
    <Encrypt><![CDATA[JCqIUfe7GJ84SQdp7M4y2xrnsqUp9ihcNZrAErcA8KSc5ewTAYCX1CtAiZqntANyYmFdQqwNAQXMU3vQGbJms/rXSjz4vN77kc9SbIDphNKRYXyaEI5P8iuQHlAjyfUE2kXnWjusYEPnKaB5RLkanwbNwhWVzgYbV4OVst9hSMepv3WpVzOBZlj8CpqhklqwHJuOda4X7unQzwRWyLA8M/lzPDCdN3rcRqz2wH9SlEc0JfjKXKk1RmBFYhHbJ2boeLFc7dIg0Sc3JNMCBw7MU4tBWAEuD+wedUSy45zZ0u1HeQSe13d6QSlVOoC9Ta0InwnlL28VpngEMru4YGeDGoyRKgDOYbDr71dI0sp/kInAKwPXWbOcqd0LFQ9P9Y+BxW4z5BNkYo9LFubXbilnO/VzU8++zuAhFSED11baYFs=]]></Encrypt>
    </xml>"""
    safe_request_message = """<xml>
    <ToUserName><![CDATA[gh_1b2959761a7d]]></ToUserName>
    <Encrypt><![CDATA[JCqIUfe7GJ84SQdp7M4y2xrnsqUp9ihcNZrAErcA8KSc5ewTAYCX1CtAiZqntANyYmFdQqwNAQXMU3vQGbJms/rXSjz4vN77kc9SbIDphNKRYXyaEI5P8iuQHlAjyfUE2kXnWjusYEPnKaB5RLkanwbNwhWVzgYbV4OVst9hSMepv3WpVzOBZlj8CpqhklqwHJuOda4X7unQzwRWyLA8M/lzPDCdN3rcRqz2wH9SlEc0JfjKXKk1RmBFYhHbJ2boeLFc7dIg0Sc3JNMCBw7MU4tBWAEuD+wedUSy45zZ0u1HeQSe13d6QSlVOoC9Ta0InwnlL28VpngEMru4YGeDGoyRKgDOYbDr71dI0sp/kInAKwPXWbOcqd0LFQ9P9Y+BxW4z5BNkYo9LFubXbilnO/VzU8++zuAhFSED11baYFs=]]></Encrypt>
    </xml>"""

    response_message = """<xml>
    <ToUserName><![CDATA[gh_1b2959761a7d]]></ToUserName>
    <FromUserName><![CDATA[oJNCEjt3uIphaC1DrpB030QxMV_w]]></FromUserName>
    <CreateTime>1442129896</CreateTime>
    <MsgType><![CDATA[text]]></MsgType>
    <Content><![CDATA[测试消息]]></Content>
    <MsgId>6193900740131666054</MsgId>
    </xml>"""
    response_encrypted_message = """<xml>
    <Encrypt><![CDATA[manHcaGm3P7cOzkyWaigw1nNiIohhn3S7xogsE0ftGFIWncP56fLoI8oVv5HS8D44X5EuQjS+/0rGMNDblrdiiflGzrTjv1CtyT0jEYsgSdPCPFvGf/pOv+timCn+YAQDby0vSxzdJ3WKQB7kubElnxVrQUTIKfe4YKSxaGuhr4m6O7C6YH2uEGaZYQyUeuq5GVPcd9ZS45YOFzAxOyK8mWp7tCkuItqt5hElZ6dMaFOnp6cEGN7113ONtPSS2US7thd9u0+EVuiNEvuF5ErqJtc0saBK18LL/PeZ1xH1ZI6ZQZiQiX3uSeQ7SUDzOCNPV0BZ9NCdOnhHwKGS/F5PkU/sG0LsZVkobeBYApOTS0MY3Da/UVR3Zznr0Enab4YM4VjGdNBclBdkbukT/t/cYQaha0zGrYpOpzqNOQpxSuM5jB/lSQo6B+niT/PftLCR6J+hmRAXPbeVRZx1pJcUQ==]]></Encrypt>
    <MsgSignature><![CDATA[e458c417d5aee4c3a9abed78da4020404e9b6cf9]]></MsgSignature>
    <TimeStamp>1442129896</TimeStamp>
    <Nonce><![CDATA[1641605039]]></Nonce>
    </xml>
    """
    signature = 'cc7c1221903889730bee4e92aba106a7bdb382f8'
    timestamp = 1442129896
    nonce = 1641605039
    encrypt_type = 'aes'
    msg_signature = 'd4e1e604ec9c7f88aeb0faea11ebb83d6f6f20a0'

    def test_init_with_token(self):
        """ 测试只有 Token 的初始化 """
        conf = WechatConf(token=self.token)
        self.assertEqual(conf.token, self.token)
        self.assertIsNone(conf.appid)
        self.assertIsNone(conf.appsecret)
        self.assertIsNone(conf.encoding_aes_key)
        self.assertIsNone(conf.crypto)
        with self.assertRaises(NeedParamError):
            getattr(conf, 'access_token')
        with self.assertRaises(NeedParamError):
            getattr(conf, 'jsapi_ticket')

    def test_init_with_token_and_appid_appsecret(self):
        """ 测试 Token AppID AppSecret 的初始化 """
        conf = WechatConf(token=self.token, appid=self.appid, appsecret=self.appsecret)
        self.assertEqual(conf.token, self.token)
        self.assertEqual(conf.appid, self.appid)
        self.assertEqual(conf.appsecret, self.appsecret)
        self.assertIsNone(conf.encoding_aes_key)
        self.assertIsNone(conf.crypto)
        with HTTMock(api_weixin_mock):
            access_token = conf.access_token
            access_token_expires_at = int(time.time()) + 7200
            self.assertEqual(access_token, self.fixtures_access_token)
            self.assertEqual(conf._WechatConf__access_token, self.fixtures_access_token)
            self.assertIn(conf._WechatConf__access_token_expires_at,
                          range(access_token_expires_at-10, access_token_expires_at+11))

            jsapi_ticket = conf.jsapi_ticket
            jsapi_ticket_expires_at = int(time.time()) + 7200
            self.assertEqual(jsapi_ticket, self.fixtures_jsapi_ticket)
            self.assertEqual(conf._WechatConf__jsapi_ticket, self.fixtures_jsapi_ticket)
            self.assertIn(conf._WechatConf__access_token_expires_at,
                          range(jsapi_ticket_expires_at-10, jsapi_ticket_expires_at+11))

    def test_init_with_normal_encrypt_mode(self):
        """ 测试明文模式下的初始化 """
        conf = WechatConf(token=self.token, appid=self.appid, appsecret=self.appsecret, encrypt_mode='normal')
        self.assertEqual(conf.token, self.token)
        self.assertEqual(conf.appid, self.appid)
        self.assertEqual(conf.appsecret, self.appsecret)
        self.assertIsNone(conf.encoding_aes_key)
        self.assertIsNone(conf.crypto)

    def test_init_with_compatible_encrypt_mode(self):
        """ 测试兼容模式下的初始化 """
        conf = WechatConf(token=self.token, appid=self.appid, appsecret=self.appsecret,
                          encrypt_mode='compatible', encoding_aes_key=self.encoding_aes_key)
        self.assertEqual(conf.token, self.token)
        self.assertEqual(conf.appid, self.appid)
        self.assertEqual(conf.appsecret, self.appsecret)
        self.assertEqual(conf.encoding_aes_key, self.encoding_aes_key)
        self.assertIsNotNone(conf.crypto)

        # 测试解密微信服务器的请求消息
        req = conf.crypto.decrypt_message(msg=self.compatible_request_message, msg_signature=self.msg_signature,
                                          timestamp=self.timestamp, nonce=self.nonce)
        self.assertEqual(xmltodict.parse(req), xmltodict.parse(self.normal_request_message))

        # 测试加密返回信息
        origin_crypto = conf.crypto._WechatBaseCrypto__pc
        conf.crypto._WechatBaseCrypto__pc = TestBaseCrypto(key=conf.crypto._WechatBaseCrypto__key)
        resp = conf.crypto.encrypt_message(msg=self.response_message, nonce=self.nonce, timestamp=self.timestamp)
        self.assertEqual(xmltodict.parse(resp), xmltodict.parse(self.response_encrypted_message))
        conf.crypto._WechatBaseCrypto__pc = origin_crypto

    def test_init_with_safe_encrypt_mode(self):
        """ 测试安全模式下的初始化 """
        conf = WechatConf(token=self.token, appid=self.appid, appsecret=self.appsecret,
                          encrypt_mode='safe', encoding_aes_key=self.encoding_aes_key)
        self.assertEqual(conf.token, self.token)
        self.assertEqual(conf.appid, self.appid)
        self.assertEqual(conf.appsecret, self.appsecret)
        self.assertEqual(conf.encoding_aes_key, self.encoding_aes_key)
        self.assertIsNotNone(conf.crypto)

        # 测试解密微信服务器的请求消息
        req = conf.crypto.decrypt_message(msg=self.safe_request_message, msg_signature=self.msg_signature,
                                          timestamp=self.timestamp, nonce=self.nonce)
        self.assertEqual(xmltodict.parse(req), xmltodict.parse(self.normal_request_message))

        # 测试加密返回信息
        origin_crypto = conf.crypto._WechatBaseCrypto__pc
        conf.crypto._WechatBaseCrypto__pc = TestBaseCrypto(key=conf.crypto._WechatBaseCrypto__key)
        resp = conf.crypto.encrypt_message(msg=self.response_message, nonce=self.nonce, timestamp=self.timestamp)
        self.assertEqual(xmltodict.parse(resp), xmltodict.parse(self.response_encrypted_message))
        conf.crypto._WechatBaseCrypto__pc = origin_crypto

