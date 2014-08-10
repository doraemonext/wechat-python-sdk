# -*- coding: utf-8 -*-

import hashlib

from xml.dom import minidom
from xml.parsers.expat import ExpatError

from .messages import MESSAGE_TYPES, UnknownMessage
from .exceptions import ParseError, NeedParseError
from .reply import TextReply, ImageReply, VoiceReply, VideoReply, MusicReply, Article, ArticleReply


class WechatBasic(object):
    """
    微信基本功能类

    仅包含官方 API 中所包含的内容, 如需高级功能支持请移步 ext.py 中的 WechatExt 类
    """
    def __init__(self, token, appid=None, appsecret=None, partnerid=None,
                 partnerkey=None, paysignkey=None, debug=False):
        """
        :param token: 微信 Token
        :param appid: App ID
        :param appsecret: App Secret
        :param partnerid: 财付通商户身份标识, 支付权限专用
        :param partnerkey: 财付通商户权限密钥 Key, 支付权限专用
        :param paysignkey: 商户签名密钥 Key, 支付权限专用
        :param debug: 是否进入 Debug 模式, 开启 Debug 模式将会向控制台输出所有运行记录
        """
        self.__token = token
        self.__appid = appid
        self.__appsecret = appsecret
        self.__partnerid = partnerid
        self.__partnerkey = partnerkey
        self.__paysignkey = paysignkey
        self.__debug = debug

        self.__is_parse = False
        self.__message = None

    def check_signature(self, signature, timestamp, nonce):
        """
        验证微信消息真实性
        :param signature: 微信加密签名
        :param timestamp: 时间戳
        :param nonce: 随机数
        :return: 通过验证返回 True, 未通过验证返回 False
        """
        tmp_list = [self.__token, timestamp, nonce]
        tmp_list.sort()
        tmp_str = ''.join(tmp_list)
        if signature == hashlib.sha1(tmp_str).hexdigest():
            return True
        else:
            return False

    def parse_data(self, data):
        """
        解析微信服务器发送过来的数据并保存类中
        :param data: HTTP Request 的 Body 数据
        :raises ParseError: 解析微信服务器数据错误, 数据不合法
        """
        result = {}

        try:
            doc = minidom.parseString(data)
        except ExpatError:
            raise ParseError()

        params = [ele for ele in doc.childNodes[0].childNodes
                  if isinstance(ele, minidom.Element)]

        for param in params:
            if param.childNodes:
                text = param.childNodes[0]
                result[param.tagName] = text.data
        result['raw'] = data
        result['type'] = result.pop('MsgType').lower()

        message_type = MESSAGE_TYPES.get(result['type'], UnknownMessage)
        self.__message = message_type(result)
        self.__is_parse = True

    def response_text(self, content):
        """
        将文字信息 content 组装为符合微信服务器要求的响应数据
        :param content: 回复文字
        :return: 符合微信服务器要求的 XML 响应数据
        :raises NeedParseError: 没有解析数据就调用本函数, 调用错误
        """
        if not self.__is_parse:
            raise NeedParseError()

        return TextReply(message=self.__message, content=content).render()

    def response_image(self, media_id):
        """
        将 media_id 所代表的图片组装为符合微信服务器要求的响应数据
        :param media_id: 图片的 MediaID
        :return: 符合微信服务器要求的 XML 响应数据
        :raises NeedParseError: 没有解析数据就调用本函数, 调用错误
        """
        if not self.__is_parse:
            raise NeedParseError()

        return ImageReply(message=self.__message, media_id=media_id).render()

    def response_voice(self, media_id):
        """
        将 media_id 所代表的语音组装为符合微信服务器要求的响应数据
        :param media_id: 语音的 MediaID
        :return: 符合微信服务器要求的 XML 响应数据
        :raises NeedParseError: 没有解析数据就调用本函数, 调用错误
        """
        if not self.__is_parse:
            raise NeedParseError()

        return VoiceReply(message=self.__message, media_id=media_id).render()

    def response_video(self, media_id, title=None, description=None):
        """
        将 media_id 所代表的视频组装为符合微信服务器要求的响应数据
        :param media_id: 视频的 MediaID
        :param title: 视频消息的标题
        :param description: 视频消息的描述
        :return: 符合微信服务器要求的 XML 响应数据
        :raises NeedParseError: 没有解析数据就调用本函数, 调用错误
        """
        if not self.__is_parse:
            raise NeedParseError()

        return VideoReply(message=self.__message, media_id=media_id, title=title, description=description).render()

    def response_music(self, music_url, title=None, description=None, hq_music_url=None, thumb_media_id=None):
        """
        将音乐信息组装为符合微信服务器要求的响应数据
        :param music_url: 音乐链接
        :param title: 音乐标题
        :param description: 音乐描述
        :param hq_music_url: 高质量音乐链接, WIFI环境优先使用该链接播放音乐
        :param thumb_media_id: 缩略图的 MediaID
        :return: 符合微信服务器要求的 XML 响应数据
        :raises NeedParseError: 没有解析数据就调用本函数, 调用错误
        """
        if not self.__is_parse:
            raise NeedParseError()

        return MusicReply(message=self.__message, title=title, description=description, music_url=music_url,
                          hq_music_url=hq_music_url, thumb_media_id=thumb_media_id).render()

    def response_news(self, articles):
        """
        将新闻信息组装为符合微信服务器要求的响应数据
        :param articles: list 对象, 每个元素为一个 dict 对象, key 包含 `title`, `description`, `picurl`, `url`
        :return: 符合微信服务器要求的 XML 响应数据
        :raises NeedParseError: 没有解析数据就调用本函数, 调用错误
        """
        if not self.__is_parse:
            raise NeedParseError()

        news = ArticleReply(message=self.__message)
        for article in articles:
            article = Article(**article)
            news.add_article(article)
        return news.render()