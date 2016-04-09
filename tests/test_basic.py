# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import os
import json
import unittest

import xmltodict
from httmock import urlmatch, HTTMock, response

from wechat_sdk import WechatBasic
from wechat_sdk.exceptions import NeedParamError, ParseError, OfficialAPIError
from wechat_sdk.messages import (
    TextMessage, ImageMessage, VoiceMessage, VideoMessage, ShortVideoMessage, LinkMessage,
    LocationMessage, EventMessage, UnknownMessage
)


TESTS_PATH = os.path.abspath(os.path.dirname(__file__))
FIXTURE_PATH = os.path.join(TESTS_PATH, 'fixtures')


@urlmatch(netloc=r'(.*\.)?api\.weixin\.qq\.com$')
def wechat_api_mock(url, request):
    path = url.path.replace('/cgi-bin/', '').replace('/', '_')
    if path.startswith('_'):
        path = path[1:]
    res_file = os.path.join(FIXTURE_PATH, '%s.json' % path)
    content = {
        'errcode': 99999,
        'errmsg': 'can not find fixture %s' % res_file,
    }
    headers = {
        'Content-Type': 'application/json'
    }
    try:
        with open(res_file, 'rb') as f:
            content = json.loads(f.read().decode('utf-8'))
    except (IOError, ValueError) as e:
        print(e)
    return response(200, content, headers, request=request)


class WechatBasicTestCase(unittest.TestCase):
    token = 'test_token'
    appid = 'wxn5rg4orc9ajgq0yb'
    appsecret = 'y5tjcmn76i4mrsdcyebxzkdv0h1qjefk'

    fixtures_access_token = 'HoVFaIslbrofqJgkR0Svcx2d4za0RJKa3H6A_NjzhBbm96Wtg_a3ifUYQvOfJmV76QTcCpNubcsnOLmDopu2hjWfFeQSCE4c8QrsxwE_N3w'
    fixtures_jsapi_ticket = 'bxLdikRXVbTPdHSM05e5u5sUoXNKd8-41ZO3MhKoyN5OfkWITDGgnr2fwJ0m9E8NYzWKVZvdVtaUgWvsdshFKA'

    test_message = """<xml>
<ToUserName><![CDATA[toUser]]></ToUserName>
<FromUserName><![CDATA[fromUser]]></FromUserName>
<CreateTime>1348831860</CreateTime>
<MsgType><![CDATA[text]]></MsgType>
<Content><![CDATA[测试信息]]></Content>
<MsgId>1234567890123456</MsgId>
</xml>"""

    def test_check_signature(self):
        signature = '41f929117dd6231a953f632cfb3be174b8e3ef08'
        timestamp = '1434295379'
        nonce = 'ueivlkyhvdng46da0qxr52qzcjabjmo7'

        # 测试无 Token 初始化
        wechat = WechatBasic()
        with self.assertRaises(NeedParamError):
            wechat.check_signature(signature=signature, timestamp=timestamp, nonce=nonce)

        # 测试有 Token 初始化
        wechat = WechatBasic(token=self.token)
        self.assertTrue(wechat.check_signature(signature=signature, timestamp=timestamp, nonce=nonce))
        self.assertFalse(wechat.check_signature(signature=signature, timestamp=timestamp+'2', nonce=nonce))

    def test_grant_token(self):
        # 测试无 appid 和 appsecret 初始化
        wechat = WechatBasic()
        with self.assertRaises(NeedParamError):
            wechat.grant_token()

        # 测试有 appid 和 appsecret 初始化（覆盖已有 access_token，默认override=True即覆盖）
        wechat = WechatBasic(appid=self.appid, appsecret=self.appsecret)
        with HTTMock(wechat_api_mock):
            resp = wechat.grant_token()
            self.assertEqual(resp['access_token'], self.fixtures_access_token)
            self.assertEqual(resp['expires_in'], 7200)
            self.assertEqual(wechat.conf.access_token, self.fixtures_access_token)

    def test_grant_jsapi_ticket(self):
        # 测试无 appid 和 appsecret 初始化
        wechat = WechatBasic()
        with self.assertRaises(NeedParamError):
            wechat.grant_jsapi_ticket()

        # 测试有 appid 和 appsecret 初始化（覆盖已有 jsapi_ticket，默认override=True即覆盖）
        wechat = WechatBasic(appid=self.appid, appsecret=self.appsecret)
        with HTTMock(wechat_api_mock):
            resp = wechat.grant_jsapi_ticket()
            self.assertEqual(resp['errcode'], 0)
            self.assertEqual(resp['errmsg'], 'ok')
            self.assertEqual(resp['ticket'], self.fixtures_jsapi_ticket)
            self.assertEqual(resp['expires_in'], 7200)
            self.assertEqual(wechat.conf.jsapi_ticket, self.fixtures_jsapi_ticket)

    def test_access_token(self):
        # 测试无 appid 和 appsecret 初始化
        wechat = WechatBasic()
        with self.assertRaises(NeedParamError):
            print(wechat.conf.access_token)

        # 测试有 appid 和 appsecret 初始化
        wechat = WechatBasic(appid=self.appid, appsecret=self.appsecret)
        with HTTMock(wechat_api_mock):
            access_token = wechat.conf.access_token
            self.assertEqual(access_token, self.fixtures_access_token)

    def test_jsapi_ticket(self):
        # 测试无 appid 和 appsecret 初始化
        wechat = WechatBasic()
        with self.assertRaises(NeedParamError):
            print(wechat.conf.jsapi_ticket)

        # 测试有 appid 和 appsecret 初始化
        wechat = WechatBasic(appid=self.appid, appsecret=self.appsecret)
        with HTTMock(wechat_api_mock):
            jsapi_ticket = wechat.conf.jsapi_ticket
            self.assertEqual(jsapi_ticket, self.fixtures_jsapi_ticket)

    def test_generate_jsapi_signature(self):
        noncestr = 'Wm3WZYTPz0wzccnW'
        jsapi_ticket = 'sM4AOVdWfPE4DxkXGEs8VMCPGGVi4C3VM0P37wVUCFvkVAy_90u5h9nbSlYy3-Sl-HhTdfl2fzFy1AOcHKP7qg'  # NOQA
        timestamp = 1414587457
        url = 'http://mp.weixin.qq.com?params=value'

        # 测试无 appid 和 appsecret 初始化
        wechat = WechatBasic()
        with self.assertRaises(NeedParamError):
            wechat.generate_jsapi_signature(timestamp=timestamp, noncestr=noncestr, url=url)

        # 测试有 appid 和 appsecret 初始化
        wechat = WechatBasic(appid=self.appid, appsecret=self.appsecret)
        with HTTMock(wechat_api_mock):
            signature = wechat.generate_jsapi_signature(timestamp=timestamp, noncestr=noncestr, url=url, jsapi_ticket=jsapi_ticket)
            self.assertEqual(signature, '0f9de62fce790f9a083d5c99e95740ceb90c27ed')

    def test_parse_data_bad_message(self):
        bad_message = 'xml>a2341'
        wechat = WechatBasic()
        with self.assertRaises(ParseError):
            wechat.parse_data(data=bad_message)

    def test_parse_data_text_message(self):
        message = """<xml>
<ToUserName><![CDATA[toUser]]></ToUserName>
<FromUserName><![CDATA[fromUser]]></FromUserName>
<CreateTime>1348831860</CreateTime>
<MsgType><![CDATA[text]]></MsgType>
<Content><![CDATA[this is a test]]></Content>
<MsgId>1234567890123456</MsgId>
</xml>"""

        wechat = WechatBasic()
        wechat.parse_data(data=message)
        message = wechat.message

        self.assertIsInstance(message, TextMessage)
        self.assertEqual(message.id, 1234567890123456)
        self.assertEqual(message.target, 'toUser')
        self.assertEqual(message.source, 'fromUser')
        self.assertEqual(message.time, 1348831860)
        self.assertEqual(message.type, 'text')
        self.assertEqual(message.content, 'this is a test')

    def test_parse_data_image_message(self):
        message = """<xml>
<ToUserName><![CDATA[toUser]]></ToUserName>
<FromUserName><![CDATA[fromUser]]></FromUserName>
<CreateTime>1348831860</CreateTime>
<MsgType><![CDATA[image]]></MsgType>
<PicUrl><![CDATA[this is a url]]></PicUrl>
<MediaId><![CDATA[media_id]]></MediaId>
<MsgId>1234567890123456</MsgId>
</xml>"""

        wechat = WechatBasic()
        wechat.parse_data(data=message)
        message = wechat.message

        self.assertIsInstance(message, ImageMessage)
        self.assertEqual(message.id, 1234567890123456)
        self.assertEqual(message.target, 'toUser')
        self.assertEqual(message.source, 'fromUser')
        self.assertEqual(message.time, 1348831860)
        self.assertEqual(message.type, 'image')
        self.assertEqual(message.media_id, 'media_id')

    def test_parse_data_voice_message(self):
        message = """<xml>
<ToUserName><![CDATA[toUser]]></ToUserName>
<FromUserName><![CDATA[fromUser]]></FromUserName>
<CreateTime>1357290913</CreateTime>
<MsgType><![CDATA[voice]]></MsgType>
<MediaId><![CDATA[media_id]]></MediaId>
<Format><![CDATA[Format]]></Format>
<MsgId>1234567890123456</MsgId>
</xml>"""

        wechat = WechatBasic()
        wechat.parse_data(data=message)
        message = wechat.message

        self.assertIsInstance(message, VoiceMessage)
        self.assertEqual(message.id, 1234567890123456)
        self.assertEqual(message.target, 'toUser')
        self.assertEqual(message.source, 'fromUser')
        self.assertEqual(message.time, 1357290913)
        self.assertEqual(message.type, 'voice')
        self.assertEqual(message.media_id, 'media_id')
        self.assertEqual(message.format, 'Format')
        self.assertIsNone(message.recognition)

    def test_parse_data_voice_recognition(self):
        message = """<xml>
<ToUserName><![CDATA[toUser]]></ToUserName>
<FromUserName><![CDATA[fromUser]]></FromUserName>
<CreateTime>1357290913</CreateTime>
<MsgType><![CDATA[voice]]></MsgType>
<MediaId><![CDATA[media_id]]></MediaId>
<Format><![CDATA[Format]]></Format>
<Recognition><![CDATA[腾讯微信团队]]></Recognition>
<MsgId>1234567890123456</MsgId>
</xml>"""

        wechat = WechatBasic()
        wechat.parse_data(data=message)
        message = wechat.message

        self.assertIsInstance(message, VoiceMessage)
        self.assertEqual(message.id, 1234567890123456)
        self.assertEqual(message.target, 'toUser')
        self.assertEqual(message.source, 'fromUser')
        self.assertEqual(message.time, 1357290913)
        self.assertEqual(message.type, 'voice')
        self.assertEqual(message.media_id, 'media_id')
        self.assertEqual(message.format, 'Format')
        self.assertEqual(message.recognition, '腾讯微信团队')

    def test_parse_data_video_message(self):
        message = """<xml>
<ToUserName><![CDATA[toUser]]></ToUserName>
<FromUserName><![CDATA[fromUser]]></FromUserName>
<CreateTime>1357290913</CreateTime>
<MsgType><![CDATA[video]]></MsgType>
<MediaId><![CDATA[media_id]]></MediaId>
<ThumbMediaId><![CDATA[thumb_media_id]]></ThumbMediaId>
<MsgId>1234567890123456</MsgId>
</xml>"""

        wechat = WechatBasic()
        wechat.parse_data(data=message)
        message = wechat.message

        self.assertIsInstance(message, VideoMessage)
        self.assertEqual(message.id, 1234567890123456)
        self.assertEqual(message.target, 'toUser')
        self.assertEqual(message.source, 'fromUser')
        self.assertEqual(message.time, 1357290913)
        self.assertEqual(message.type, 'video')
        self.assertEqual(message.media_id, 'media_id')
        self.assertEqual(message.thumb_media_id, 'thumb_media_id')

    def test_parse_data_short_video_message(self):
        message = """<xml>
<ToUserName><![CDATA[toUser]]></ToUserName>
<FromUserName><![CDATA[fromUser]]></FromUserName>
<CreateTime>1357290913</CreateTime>
<MsgType><![CDATA[shortvideo]]></MsgType>
<MediaId><![CDATA[media_id]]></MediaId>
<ThumbMediaId><![CDATA[thumb_media_id]]></ThumbMediaId>
<MsgId>1234567890123456</MsgId>
</xml>"""

        wechat = WechatBasic()
        wechat.parse_data(data=message)
        message = wechat.message

        self.assertIsInstance(message, ShortVideoMessage)
        self.assertEqual(message.id, 1234567890123456)
        self.assertEqual(message.target, 'toUser')
        self.assertEqual(message.source, 'fromUser')
        self.assertEqual(message.time, 1357290913)
        self.assertEqual(message.type, 'shortvideo')
        self.assertEqual(message.media_id, 'media_id')
        self.assertEqual(message.thumb_media_id, 'thumb_media_id')

    def test_parse_data_location_message(self):
        message = """<xml>
<ToUserName><![CDATA[toUser]]></ToUserName>
<FromUserName><![CDATA[fromUser]]></FromUserName>
<CreateTime>1351776360</CreateTime>
<MsgType><![CDATA[location]]></MsgType>
<Location_X>23.134521</Location_X>
<Location_Y>113.358803</Location_Y>
<Scale>20</Scale>
<Label><![CDATA[位置信息]]></Label>
<MsgId>1234567890123456</MsgId>
</xml>"""

        wechat = WechatBasic()
        wechat.parse_data(data=message)
        message = wechat.message

        self.assertIsInstance(message, LocationMessage)
        self.assertEqual(message.id, 1234567890123456)
        self.assertEqual(message.target, 'toUser')
        self.assertEqual(message.source, 'fromUser')
        self.assertEqual(message.time, 1351776360)
        self.assertEqual(message.type, 'location')
        self.assertEqual(message.location, (23.134521, 113.358803))
        self.assertEqual(message.scale, 20)
        self.assertEqual(message.label, '位置信息')

    def test_parse_data_link_message(self):
        message = """<xml>
<ToUserName><![CDATA[toUser]]></ToUserName>
<FromUserName><![CDATA[fromUser]]></FromUserName>
<CreateTime>1351776360</CreateTime>
<MsgType><![CDATA[link]]></MsgType>
<Title><![CDATA[公众平台官网链接]]></Title>
<Description><![CDATA[公众平台官网链接]]></Description>
<Url><![CDATA[url]]></Url>
<MsgId>1234567890123456</MsgId>
</xml>"""

        wechat = WechatBasic()
        wechat.parse_data(data=message)
        message = wechat.message

        self.assertIsInstance(message, LinkMessage)
        self.assertEqual(message.id, 1234567890123456)
        self.assertEqual(message.target, 'toUser')
        self.assertEqual(message.source, 'fromUser')
        self.assertEqual(message.time, 1351776360)
        self.assertEqual(message.type, 'link')
        self.assertEqual(message.title, '公众平台官网链接')
        self.assertEqual(message.description, '公众平台官网链接')
        self.assertEqual(message.url, 'url')

    def test_parse_data_subscribe_event(self):
        message = """<xml>
<ToUserName><![CDATA[toUser]]></ToUserName>
<FromUserName><![CDATA[FromUser]]></FromUserName>
<CreateTime>123456789</CreateTime>
<MsgType><![CDATA[event]]></MsgType>
<Event><![CDATA[subscribe]]></Event>
</xml>"""

        wechat = WechatBasic()
        wechat.parse_data(data=message)
        message = wechat.message

        self.assertIsInstance(message, EventMessage)
        self.assertEqual(message.type, 'subscribe')
        self.assertEqual(message.target, 'toUser')
        self.assertEqual(message.source, 'FromUser')
        self.assertEqual(message.time, 123456789)
        self.assertIsNone(message.ticket)
        self.assertIsNone(message.key)

    def test_parse_data_unsubscribe_event(self):
        message = """<xml>
<ToUserName><![CDATA[toUser]]></ToUserName>
<FromUserName><![CDATA[FromUser]]></FromUserName>
<CreateTime>123456789</CreateTime>
<MsgType><![CDATA[event]]></MsgType>
<Event><![CDATA[unsubscribe]]></Event>
</xml>"""

        wechat = WechatBasic()
        wechat.parse_data(data=message)
        message = wechat.message

        self.assertIsInstance(message, EventMessage)
        self.assertEqual(message.type, 'unsubscribe')
        self.assertEqual(message.target, 'toUser')
        self.assertEqual(message.source, 'FromUser')
        self.assertEqual(message.time, 123456789)

    def test_parse_data_subscribe_qrscene_event(self):
        message = """<xml>
<ToUserName><![CDATA[toUser]]></ToUserName>
<FromUserName><![CDATA[FromUser]]></FromUserName>
<CreateTime>123456789</CreateTime>
<MsgType><![CDATA[event]]></MsgType>
<Event><![CDATA[subscribe]]></Event>
<EventKey><![CDATA[qrscene_123123]]></EventKey>
<Ticket><![CDATA[TICKET]]></Ticket>
</xml>"""

        wechat = WechatBasic()
        wechat.parse_data(data=message)
        message = wechat.message

        self.assertIsInstance(message, EventMessage)
        self.assertEqual(message.type, 'subscribe')
        self.assertEqual(message.target, 'toUser')
        self.assertEqual(message.source, 'FromUser')
        self.assertEqual(message.time, 123456789)
        self.assertEqual(message.key, 'qrscene_123123')
        self.assertEqual(message.ticket, 'TICKET')

    def test_parse_data_scan_event(self):
        message = """<xml>
<ToUserName><![CDATA[toUser]]></ToUserName>
<FromUserName><![CDATA[FromUser]]></FromUserName>
<CreateTime>123456789</CreateTime>
<MsgType><![CDATA[event]]></MsgType>
<Event><![CDATA[SCAN]]></Event>
<EventKey><![CDATA[SCENE_VALUE]]></EventKey>
<Ticket><![CDATA[TICKET]]></Ticket>
</xml>"""

        wechat = WechatBasic()
        wechat.parse_data(data=message)
        message = wechat.message

        self.assertIsInstance(message, EventMessage)
        self.assertEqual(message.type, 'scan')
        self.assertEqual(message.target, 'toUser')
        self.assertEqual(message.source, 'FromUser')
        self.assertEqual(message.time, 123456789)
        self.assertEqual(message.key, 'SCENE_VALUE')
        self.assertEqual(message.ticket, 'TICKET')

    def test_parse_data_location_event(self):
        message = """<xml>
<ToUserName><![CDATA[toUser]]></ToUserName>
<FromUserName><![CDATA[fromUser]]></FromUserName>
<CreateTime>123456789</CreateTime>
<MsgType><![CDATA[event]]></MsgType>
<Event><![CDATA[LOCATION]]></Event>
<Latitude>23.137466</Latitude>
<Longitude>113.352425</Longitude>
<Precision>119.385040</Precision>
</xml>"""

        wechat = WechatBasic()
        wechat.parse_data(data=message)
        message = wechat.message

        self.assertIsInstance(message, EventMessage)
        self.assertEqual(message.type, 'location')
        self.assertEqual(message.target, 'toUser')
        self.assertEqual(message.source, 'fromUser')
        self.assertEqual(message.time, 123456789)
        self.assertEqual(message.latitude, 23.137466)
        self.assertEqual(message.longitude, 113.352425)
        self.assertEqual(message.precision, 119.385040)

    def test_parse_data_click_event(self):
        message = """<xml>
<ToUserName><![CDATA[toUser]]></ToUserName>
<FromUserName><![CDATA[FromUser]]></FromUserName>
<CreateTime>123456789</CreateTime>
<MsgType><![CDATA[event]]></MsgType>
<Event><![CDATA[CLICK]]></Event>
<EventKey><![CDATA[EVENTKEY]]></EventKey>
</xml>"""

        wechat = WechatBasic()
        wechat.parse_data(data=message)
        message = wechat.message

        self.assertIsInstance(message, EventMessage)
        self.assertEqual(message.type, 'click')
        self.assertEqual(message.target, 'toUser')
        self.assertEqual(message.source, 'FromUser')
        self.assertEqual(message.time, 123456789)
        self.assertEqual(message.key, 'EVENTKEY')

    def test_parse_data_view_event(self):
        message = """<xml>
<ToUserName><![CDATA[toUser]]></ToUserName>
<FromUserName><![CDATA[FromUser]]></FromUserName>
<CreateTime>123456789</CreateTime>
<MsgType><![CDATA[event]]></MsgType>
<Event><![CDATA[VIEW]]></Event>
<EventKey><![CDATA[www.qq.com]]></EventKey>
</xml>"""

        wechat = WechatBasic()
        wechat.parse_data(data=message)
        message = wechat.message

        self.assertIsInstance(message, EventMessage)
        self.assertEqual(message.type, 'view')
        self.assertEqual(message.target, 'toUser')
        self.assertEqual(message.source, 'FromUser')
        self.assertEqual(message.time, 123456789)
        self.assertEqual(message.key, 'www.qq.com')

    def test_response_text(self):
        wechat = WechatBasic()
        wechat.parse_data(data=self.test_message)

        response_xml_1 = wechat.response_text('test message')
        response_xml_2 = wechat.response_text('测试文本')
        response_xml_3 = wechat.response_text(u'测试文本')
        response_xml_4 = wechat.response_text('<h1>你好</h1>')
        response_xml_5 = wechat.response_text('<h1>你好</h1>', escape=True)
        response_1 = xmltodict.parse(response_xml_1)
        response_2 = xmltodict.parse(response_xml_2)
        response_3 = xmltodict.parse(response_xml_3)
        response_4 = xmltodict.parse(response_xml_4)
        response_5 = xmltodict.parse(response_xml_5)

        self.assertEqual(response_1['xml']['ToUserName'], 'fromUser')
        self.assertEqual(response_1['xml']['FromUserName'], 'toUser')
        self.assertEqual(response_1['xml']['MsgType'], 'text')

        self.assertEqual(response_1['xml']['Content'], 'test message')
        self.assertEqual(response_2['xml']['Content'], '测试文本')
        self.assertEqual(response_3['xml']['Content'], '测试文本')
        self.assertEqual(response_4['xml']['Content'], '<h1>你好</h1>')
        self.assertEqual(response_5['xml']['Content'], '&lt;h1&gt;你好&lt;/h1&gt;')

    def test_response_image(self):
        wechat = WechatBasic()
        wechat.parse_data(data=self.test_message)

        resp_xml = wechat.response_image(media_id='xurkvi9gl')
        resp = xmltodict.parse(resp_xml)

        self.assertEqual(resp['xml']['ToUserName'], 'fromUser')
        self.assertEqual(resp['xml']['FromUserName'], 'toUser')
        self.assertEqual(resp['xml']['MsgType'], 'image')
        self.assertEqual(resp['xml']['Image']['MediaId'], 'xurkvi9gl')

    def test_response_voice(self):
        wechat = WechatBasic()
        wechat.parse_data(data=self.test_message)

        resp_xml = wechat.response_voice(media_id='xurkvi9gl')
        resp = xmltodict.parse(resp_xml)

        self.assertEqual(resp['xml']['ToUserName'], 'fromUser')
        self.assertEqual(resp['xml']['FromUserName'], 'toUser')
        self.assertEqual(resp['xml']['MsgType'], 'voice')
        self.assertEqual(resp['xml']['Voice']['MediaId'], 'xurkvi9gl')

    def test_response_video(self):
        wechat = WechatBasic()
        wechat.parse_data(data=self.test_message)

        resp_xml = wechat.response_video(
            media_id='xurkvi9gl',
            title='测试视频',
            description='测试描述',
        )
        resp = xmltodict.parse(resp_xml)

        self.assertEqual(resp['xml']['ToUserName'], 'fromUser')
        self.assertEqual(resp['xml']['FromUserName'], 'toUser')
        self.assertEqual(resp['xml']['MsgType'], 'video')
        self.assertEqual(resp['xml']['Video']['MediaId'], 'xurkvi9gl')
        self.assertEqual(resp['xml']['Video']['Title'], '测试视频')
        self.assertEqual(resp['xml']['Video']['Description'], '测试描述')

    def test_response_music(self):
        wechat = WechatBasic()
        wechat.parse_data(data=self.test_message)

        resp_xml = wechat.response_music(
            music_url='http://mp3.baidu.com',
            title='测试音乐',
            description='测试描述',
            hq_music_url='http://baidu.com/',
        )
        resp = xmltodict.parse(resp_xml)

        self.assertEqual(resp['xml']['ToUserName'], 'fromUser')
        self.assertEqual(resp['xml']['FromUserName'], 'toUser')
        self.assertEqual(resp['xml']['MsgType'], 'music')
        self.assertEqual(resp['xml']['Music']['Title'], '测试音乐')
        self.assertEqual(resp['xml']['Music']['Description'], '测试描述')
        self.assertEqual(resp['xml']['Music']['MusicUrl'], 'http://mp3.baidu.com')
        self.assertEqual(resp['xml']['Music']['HQMusicUrl'], 'http://baidu.com/')

    def test_response_news(self):
        wechat = WechatBasic()
        wechat.parse_data(data=self.test_message)

        resp_xml = wechat.response_news(articles=[
            {
                'title': '第一条新闻标题',
                'description': '第一条新闻描述，这条新闻没有预览图',
                'url': 'http://www.google.com.hk/',
            }, {
                'title': '第二条新闻标题, 这条新闻无描述',
                'picurl': 'http://doraemonext.oss-cn-hangzhou.aliyuncs.com/test/wechat-test.jpg',
                'url': 'http://www.github.com/',
            }, {
                'title': '第三条新闻标题',
                'description': '第三条新闻描述',
                'picurl': 'http://doraemonext.oss-cn-hangzhou.aliyuncs.com/test/wechat-test.jpg',
                'url': 'http://www.v2ex.com/',
            }
        ])
        resp = xmltodict.parse(resp_xml)

        self.assertEqual(resp['xml']['ToUserName'], 'fromUser')
        self.assertEqual(resp['xml']['FromUserName'], 'toUser')
        self.assertEqual(resp['xml']['MsgType'], 'news')
        self.assertEqual(resp['xml']['ArticleCount'], '3')

        self.assertEqual(resp['xml']['Articles']['item'][0]['Title'], '第一条新闻标题')
        self.assertEqual(resp['xml']['Articles']['item'][0]['Description'], '第一条新闻描述，这条新闻没有预览图')
        self.assertEqual(resp['xml']['Articles']['item'][0]['Url'], 'http://www.google.com.hk/')
        self.assertIsNone(resp['xml']['Articles']['item'][0]['PicUrl'])

        self.assertEqual(resp['xml']['Articles']['item'][1]['Title'], '第二条新闻标题, 这条新闻无描述')
        self.assertIsNone(resp['xml']['Articles']['item'][1]['Description'])
        self.assertEqual(resp['xml']['Articles']['item'][1]['Url'], 'http://www.github.com/')
        self.assertEqual(resp['xml']['Articles']['item'][1]['PicUrl'], 'http://doraemonext.oss-cn-hangzhou.aliyuncs.com/test/wechat-test.jpg')

        self.assertEqual(resp['xml']['Articles']['item'][2]['Title'], '第三条新闻标题')
        self.assertEqual(resp['xml']['Articles']['item'][2]['Description'], '第三条新闻描述')
        self.assertEqual(resp['xml']['Articles']['item'][2]['Url'], 'http://www.v2ex.com/')
        self.assertEqual(resp['xml']['Articles']['item'][2]['PicUrl'], 'http://doraemonext.oss-cn-hangzhou.aliyuncs.com/test/wechat-test.jpg')

    def test_group_transfer_message(self):
        wechat = WechatBasic()
        wechat.parse_data(data=self.test_message)
        resp_xml = wechat.group_transfer_message()
        resp = xmltodict.parse(resp_xml)

        self.assertEqual(resp['xml']['ToUserName'], 'fromUser')
        self.assertEqual(resp['xml']['FromUserName'], 'toUser')
        self.assertEqual(resp['xml']['MsgType'], 'transfer_customer_service')

    def test_create_menu(self):
        menu_info = {
            'button': [
                {
                    'type': 'click',
                    'name': '今日歌曲',
                    'key': 'V1001_TODAY_MUSIC'
                },
                {
                    'type': 'click',
                    'name': '歌手简介',
                    'key': 'V1001_TODAY_SINGER'
                },
                {
                    'name': '菜单',
                    'sub_button': [
                        {
                            'type': 'view',
                            'name': '搜索',
                            'url': 'http://www.soso.com/'
                        },
                        {
                            'type': 'view',
                            'name': '视频',
                            'url': 'http://v.qq.com/'
                        },
                        {
                            'type': 'click',
                            'name': '赞一下我们',
                            'key': 'V1001_GOOD'
                        }
                    ]
                }
            ]
        }

        # 测试无 appid 和 appsecret 初始化
        wechat = WechatBasic()
        with self.assertRaises(NeedParamError):
            wechat.create_menu(menu_info)

        # 测试有 appid 和 appsecret 初始化
        wechat = WechatBasic(appid=self.appid, appsecret=self.appsecret)
        with HTTMock(wechat_api_mock):
            resp = wechat.create_menu(menu_info)
            self.assertEqual(resp['errcode'], 0)
            self.assertEqual(resp['errmsg'], 'ok')

    def test_get_menu(self):
        # 测试无 appid 和 appsecret 初始化
        wechat = WechatBasic()
        with self.assertRaises(NeedParamError):
            wechat.get_menu()

        # 测试有 appid 和 appsecret 初始化
        wechat = WechatBasic(appid=self.appid, appsecret=self.appsecret)
        with HTTMock(wechat_api_mock):
            resp = wechat.get_menu()
            self.assertEqual(resp['menu'], {
                "button": [
                    {
                        "type": "click",
                        "name": "今日歌曲",
                        "key": "V1001_TODAY_MUSIC",
                        "sub_button": []
                    },
                    {
                        "type": "click",
                        "name": "歌手简介",
                        "key": "V1001_TODAY_SINGER",
                        "sub_button": []
                    },
                    {
                        "name": "菜单",
                        "sub_button": [
                            {
                                "type": "view",
                                "name": "搜索",
                                "url": "http://www.soso.com/",
                                "sub_button": []
                            },
                            {
                                "type": "view",
                                "name": "视频",
                                "url": "http://v.qq.com/",
                                "sub_button": []
                            },
                            {
                                "type": "click",
                                "name": "赞一下我们",
                                "key": "V1001_GOOD",
                                "sub_button": []
                            }
                        ]
                    }
                ]
            })

    def test_delete_menu(self):
        # 测试无 appid 和 appsecret 初始化
        wechat = WechatBasic()
        with self.assertRaises(NeedParamError):
            wechat.delete_menu()

        # 测试有 appid 和 appsecret 初始化
        wechat = WechatBasic(appid=self.appid, appsecret=self.appsecret)
        with HTTMock(wechat_api_mock):
            resp = wechat.delete_menu()
            self.assertEqual(resp['errcode'], 0)
            self.assertEqual(resp['errmsg'], 'ok')

    def test_create_group(self):
        # 测试无 appid 和 appsecret 初始化
        wechat = WechatBasic()
        with self.assertRaises(NeedParamError):
            wechat.create_group('测试组')

        # 测试有 appid 和 appsecret 初始化
        wechat = WechatBasic(appid=self.appid, appsecret=self.appsecret)
        with HTTMock(wechat_api_mock):
            resp = wechat.create_group('测试组')
            self.assertEqual(resp['group']['id'], 107)
            self.assertEqual(resp['group']['name'], 'test')

    def test_get_group(self):
        # 测试无 appid 和 appsecret 初始化
        wechat = WechatBasic()
        with self.assertRaises(NeedParamError):
            wechat.get_groups()

        # 测试有 appid 和 appsecret 初始化
        wechat = WechatBasic(appid=self.appid, appsecret=self.appsecret)
        with HTTMock(wechat_api_mock):
            resp = wechat.get_groups()
            self.assertEqual(resp['groups'][0]['id'], 0)
            self.assertEqual(resp['groups'][0]['name'], '未分组')
            self.assertEqual(resp['groups'][0]['count'], 72596)
            self.assertEqual(resp['groups'][1]['id'], 1)
            self.assertEqual(resp['groups'][1]['name'], '黑名单')
            self.assertEqual(resp['groups'][1]['count'], 36)
            self.assertEqual(resp['groups'][2]['id'], 2)
            self.assertEqual(resp['groups'][2]['name'], '星标组')
            self.assertEqual(resp['groups'][2]['count'], 8)
            self.assertEqual(resp['groups'][3]['id'], 104)
            self.assertEqual(resp['groups'][3]['name'], '华东媒')
            self.assertEqual(resp['groups'][3]['count'], 4)
            self.assertEqual(resp['groups'][4]['id'], 106)
            self.assertEqual(resp['groups'][4]['name'], '★不测试组★')
            self.assertEqual(resp['groups'][4]['count'], 1)

    def test_get_group_by_id(self):
        # 测试无 appid 和 appsecret 初始化
        wechat = WechatBasic()
        with self.assertRaises(NeedParamError):
            wechat.get_group_by_id('13441123412341')

        # 测试有 appid 和 appsecret 初始化
        wechat = WechatBasic(appid=self.appid, appsecret=self.appsecret)
        with HTTMock(wechat_api_mock):
            resp = wechat.get_group_by_id('12554647777')
            self.assertEqual(resp['groupid'], 102)

    def test_update_group(self):
        # 测试无 appid 和 appsecret 初始化
        wechat = WechatBasic()
        with self.assertRaises(NeedParamError):
            wechat.update_group(23, 'asfff')

        # 测试有 appid 和 appsecret 初始化
        wechat = WechatBasic(appid=self.appid, appsecret=self.appsecret)
        with HTTMock(wechat_api_mock):
            resp = wechat.update_group(11, '113444')
            self.assertEqual(resp['errcode'], 0)
            self.assertEqual(resp['errmsg'], 'ok')

    def test_move_user(self):
        # 测试无 appid 和 appsecret 初始化
        wechat = WechatBasic()
        with self.assertRaises(NeedParamError):
            wechat.move_user("123412", 1241234)

        # 测试有 appid 和 appsecret 初始化
        wechat = WechatBasic(appid=self.appid, appsecret=self.appsecret)
        with HTTMock(wechat_api_mock):
            resp = wechat.update_group("21341", 12341234)
            self.assertEqual(resp['errcode'], 0)
            self.assertEqual(resp['errmsg'], 'ok')

    def test_get_user_info(self):
        # 测试无 appid 和 appsecret 初始化
        wechat = WechatBasic()
        with self.assertRaises(NeedParamError):
            wechat.get_user_info('123412412341234')

        # 测试有 appid 和 appsecret 初始化
        wechat = WechatBasic(appid=self.appid, appsecret=self.appsecret)
        with HTTMock(wechat_api_mock):
            resp = wechat.get_user_info('3253634563425234')
            self.assertEqual(resp['subscribe'], 1)
            self.assertEqual(resp['openid'], 'o6_bmjrPTlm6_2sgVt7hMZOPfL2M')
            self.assertEqual(resp['nickname'], 'Band')
            self.assertEqual(resp['sex'], 1)
            self.assertEqual(resp['language'], 'zh_CN')
            self.assertEqual(resp['city'], '广州')
            self.assertEqual(resp['province'], '广东')
            self.assertEqual(resp['country'], '中国')
            self.assertEqual(resp['headimgurl'], 'http://wx.qlogo.cn/mmopen/g3MonUZtNHkdmzicIlibx6iaFqAc56vxLSUfpb6n5WKSYVY0ChQKkiaJSgQ1dZuTOgvLLrhJbERQQ4eMsv84eavHiaiceqxibJxCfHe/0')
            self.assertEqual(resp['subscribe_time'], 1382694957)
            self.assertEqual(resp['unionid'], 'o6_bmasdasdsad6_2sgVt7hMZOPfL')
            self.assertEqual(resp['remark'], '')
            self.assertEqual(resp['groupid'], 0)

    def test_get_followers(self):
        # 测试无 appid 和 appsecret 初始化
        wechat = WechatBasic()
        with self.assertRaises(NeedParamError):
            wechat.get_followers()

        # 测试有 appid 和 appsecret 初始化
        wechat = WechatBasic(appid=self.appid, appsecret=self.appsecret)
        with HTTMock(wechat_api_mock):
            resp = wechat.get_followers()
            self.assertEqual(resp['total'], 2)
            self.assertEqual(resp['count'], 2)
            self.assertEqual(resp['data'], {
                'openid': ['', 'OPENID1', 'OPENID2']
            })
            self.assertEqual(resp['next_openid'], 'NEXT_OPENID')

    def test_send_text_message(self):
        # 测试无 appid 和 appsecret 初始化
        wechat = WechatBasic()
        with self.assertRaises(NeedParamError):
            wechat.send_text_message('asdfasdfdf', 'asdadsfd')

        # 测试有 appid 和 appsecret 初始化
        wechat = WechatBasic(appid=self.appid, appsecret=self.appsecret)
        with HTTMock(wechat_api_mock):
            resp = wechat.send_text_message('13412412341234242', '测试')
            self.assertEqual(resp['errcode'], 0)
            self.assertEqual(resp['errmsg'], 'ok')

    def test_send_image_message(self):
        # 测试无 appid 和 appsecret 初始化
        wechat = WechatBasic()
        with self.assertRaises(NeedParamError):
            wechat.send_image_message('afasdfadsf', 'asfdadfsadfsdfas')

        # 测试有 appid 和 appsecret 初始化
        wechat = WechatBasic(appid=self.appid, appsecret=self.appsecret)
        with HTTMock(wechat_api_mock):
            resp = wechat.send_image_message('asdfasdfdfas', '12342341234')
            self.assertEqual(resp['errcode'], 0)
            self.assertEqual(resp['errmsg'], 'ok')

    def test_send_voice_message(self):
        # 测试无 appid 和 appsecret 初始化
        wechat = WechatBasic()
        with self.assertRaises(NeedParamError):
            wechat.send_voice_message('asdfasdf', 'safddsafasddfsaadsf')

        # 测试有 appid 和 appsecret 初始化
        wechat = WechatBasic(appid=self.appid, appsecret=self.appsecret)
        with HTTMock(wechat_api_mock):
            resp = wechat.send_voice_message('safasf', '123412343423241')
            self.assertEqual(resp['errcode'], 0)
            self.assertEqual(resp['errmsg'], 'ok')

    def test_send_video_message(self):
        # 测试无 appid 和 appsecret 初始化
        wechat = WechatBasic()
        with self.assertRaises(NeedParamError):
            wechat.send_video_message('asfasdfadsf', '123412342134')

        # 测试有 appid 和 appsecret 初始化
        wechat = WechatBasic(appid=self.appid, appsecret=self.appsecret)
        with HTTMock(wechat_api_mock):
            resp = wechat.send_video_message('safasf', '123412343423241')
            self.assertEqual(resp['errcode'], 0)
            self.assertEqual(resp['errmsg'], 'ok')

    def test_send_music_message(self):
        # 测试无 appid 和 appsecret 初始化
        wechat = WechatBasic()
        with self.assertRaises(NeedParamError):
            wechat.send_music_message('231412341234', 'http://www.baidu.com', 'http://www.google.com', '12341234')

        # 测试有 appid 和 appsecret 初始化
        wechat = WechatBasic(appid=self.appid, appsecret=self.appsecret)
        with HTTMock(wechat_api_mock):
            resp = wechat.send_music_message('231412341234', 'http://www.baidu.com', 'http://www.google.com', '12341234')
            self.assertEqual(resp['errcode'], 0)
            self.assertEqual(resp['errmsg'], 'ok')

    def test_send_article_message(self):
        article_info = [
            {
                'title': '第一条新闻标题',
                'description': '第一条新闻描述，这条新闻没有预览图',
                'url': 'http://www.google.com.hk/',
            }, {
                'title': '第二条新闻标题, 这条新闻无描述',
                'picurl': 'http://doraemonext.oss-cn-hangzhou.aliyuncs.com/test/wechat-test.jpg',
                'url': 'http://www.github.com/',
            }, {
                'title': '第三条新闻标题',
                'description': '第三条新闻描述',
                'picurl': 'http://doraemonext.oss-cn-hangzhou.aliyuncs.com/test/wechat-test.jpg',
                'url': 'http://www.v2ex.com/',
            }
        ]

        # 测试无 appid 和 appsecret 初始化
        wechat = WechatBasic()
        with self.assertRaises(NeedParamError):
            wechat.send_article_message('12341234234', article_info)

        # 测试有 appid 和 appsecret 初始化
        wechat = WechatBasic(appid=self.appid, appsecret=self.appsecret)
        with HTTMock(wechat_api_mock):
            resp = wechat.send_article_message('safasf', article_info)
            self.assertEqual(resp['errcode'], 0)
            self.assertEqual(resp['errmsg'], 'ok')

    def test_create_qrcode(self):
        data = {"action_name": "QR_LIMIT_STR_SCENE", "action_info": {"scene": {"scene_str": "123"}}}

        # 测试无 appid 和 appsecret 初始化
        wechat = WechatBasic()
        with self.assertRaises(NeedParamError):
            wechat.create_qrcode(data)

        # 测试有 appid 和 appsecret 初始化
        wechat = WechatBasic(appid=self.appid, appsecret=self.appsecret)
        with HTTMock(wechat_api_mock):
            resp = wechat.create_qrcode(data)
            self.assertEqual(resp['ticket'], 'gQH47joAAAAAAAAAASxodHRwOi8vd2VpeGluLnFxLmNvbS9xL2taZ2Z3TVRtNzJXV1Brb3ZhYmJJAAIEZ23sUwMEmm3sUw==')
            self.assertEqual(resp['expire_seconds'], 60)
            self.assertEqual(resp['url'], 'http://weixin.qq.com/q/kZgfwMTm72WWPkovabbI')

    def test_get_template_id(self):
        # 测试无 appid 和 appsecret 初始化
        wechat = WechatBasic()
        with self.assertRaises(NeedParamError):
            wechat.get_template_id('aafeewr')

        # 测试有 appid 和 appsecret 初始化
        wechat = WechatBasic(appid=self.appid, appsecret=self.appsecret)
        with HTTMock(wechat_api_mock):
            resp = wechat.get_template_id('123412431234')
            self.assertEqual(resp['errcode'], 0)
            self.assertEqual(resp['errmsg'], 'ok')
            self.assertEqual(resp['template_id'], 'Doclyl5uP7Aciu-qZ7mJNPtWkbkYnWBWVja26EGbNyk')

    def test_send_template_message(self):
        data = {
            "first": {
                "value": "恭喜你购买成功！",
                "color": "#173177"
            },
            "keynote1": {
                "value": "巧克力",
                "color": "#173177"
            },
            "keynote2": {
                "value": "39.8元",
                "color": "#173177"
            },
            "keynote3": {
                "value": "2014年9月16日",
                "color": "#173177"
            },
            "remark": {
                "value": "欢迎再次购买！",
                "color": "#173177"
            }
        }

        # 测试无 appid 和 appsecret 初始化
        wechat = WechatBasic()
        with self.assertRaises(NeedParamError):
            wechat.send_template_message('12341234', '123412341234', data)

        # 测试有 appid 和 appsecret 初始化
        wechat = WechatBasic(appid=self.appid, appsecret=self.appsecret)
        with HTTMock(wechat_api_mock):
            resp = wechat.send_template_message('12341234', '123412341', data)
            self.assertEqual(resp['errcode'], 0)
            self.assertEqual(resp['errmsg'], 'ok')
            self.assertEqual(resp['msgid'], 200228332)

    def test_check_official_error(self):
        wechat = WechatBasic()

        data = {
            'errcode': 10001,
            'errmsg': 'test error message'
        }
        with self.assertRaises(OfficialAPIError) as exc:
            wechat._check_official_error(data)
        self.assertEqual(exc.exception.errcode, 10001)
        self.assertEqual(exc.exception.errmsg, 'test error message')
        self.assertEqual(exc.exception.__str__(), '10001: test error message')

        data = {'errcode': 10000}
        with self.assertRaises(OfficialAPIError) as exc:
            wechat._check_official_error(data)
        self.assertEqual(exc.exception.errcode, 10000)
        self.assertEqual(exc.exception.errmsg, '')
        self.assertEqual(exc.exception.__str__(), '10000: ')
