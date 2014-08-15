# -*- coding: utf-8 -*-

import time

from .messages import WechatMessage


class WechatReply(object):
    def __init__(self, message=None, **kwargs):
        if 'source' not in kwargs and isinstance(message, WechatMessage):
            kwargs['source'] = message.target
        if 'target' not in kwargs and isinstance(message, WechatMessage):
            kwargs['target'] = message.source
        if 'time' not in kwargs:
            kwargs['time'] = int(time.time())

        self._args = dict()
        for k, v in kwargs.items():
            self._args[k] = v

    def render(self):
        raise NotImplementedError()


class TextReply(WechatReply):
    """
    回复文字消息
    """
    TEMPLATE = u"""
    <xml>
    <ToUserName><![CDATA[{target}]]></ToUserName>
    <FromUserName><![CDATA[{source}]]></FromUserName>
    <CreateTime>{time}</CreateTime>
    <MsgType><![CDATA[text]]></MsgType>
    <Content><![CDATA[{content}]]></Content>
    </xml>
    """

    def __init__(self, message, content):
        """
        :param message: WechatMessage 对象
        :param content: 文字回复内容
        """
        super(TextReply, self).__init__(message=message, content=content)

    def render(self):
        return TextReply.TEMPLATE.format(**self._args)


class ImageReply(WechatReply):
    """
    回复图片消息
    """
    TEMPLATE = u"""
    <xml>
    <ToUserName><![CDATA[{target}]]></ToUserName>
    <FromUserName><![CDATA[{source}]]></FromUserName>
    <CreateTime>{time}</CreateTime>
    <MsgType><![CDATA[image]]></MsgType>
    <Image>
    <MediaId><![CDATA[{media_id}]]></MediaId>
    </Image>
    </xml>
    """

    def __init__(self, message, media_id):
        """
        :param message: WechatMessage 对象
        :param media_id: 图片的 MediaID
        """
        super(ImageReply, self).__init__(message=message, media_id=media_id)

    def render(self):
        return ImageReply.TEMPLATE.format(**self._args)


class VoiceReply(WechatReply):
    """
    回复语音消息
    """
    TEMPLATE = u"""
    <xml>
    <ToUserName><![CDATA[{target}]]></ToUserName>
    <FromUserName><![CDATA[{source}]]></FromUserName>
    <CreateTime>{time}</CreateTime>
    <MsgType><![CDATA[voice]]></MsgType>
    <Voice>
    <MediaId><![CDATA[{media_id}]]></MediaId>
    </Voice>
    </xml>
    """

    def __init__(self, message, media_id):
        """
        :param message: WechatMessage 对象
        :param media_id: 语音的 MediaID
        """
        super(VoiceReply, self).__init__(message=message, media_id=media_id)

    def render(self):
        return VoiceReply.TEMPLATE.format(**self._args)


class VideoReply(WechatReply):
    """
    回复视频消息
    """
    TEMPLATE = u"""
    <xml>
    <ToUserName><![CDATA[{target}]]></ToUserName>
    <FromUserName><![CDATA[{source}]]></FromUserName>
    <CreateTime>{time}</CreateTime>
    <MsgType><![CDATA[video]]></MsgType>
    <Video>
    <MediaId><![CDATA[{media_id}]]></MediaId>
    <Title><![CDATA[{title}]]></Title>
    <Description><![CDATA[{description}]]></Description>
    </Video>
    </xml>
    """

    def __init__(self, message, media_id, title=None, description=None):
        """
        :param message: WechatMessage对象
        :param media_id: 视频的 MediaID
        :param title: 视频消息的标题
        :param description: 视频消息的描述
        """
        title = title or ''
        description = description or ''
        super(VideoReply, self).__init__(message=message, media_id=media_id, title=title, description=description)

    def render(self):
        return VideoReply.TEMPLATE.format(**self._args)


class MusicReply(WechatReply):
    """
    回复音乐消息
    """
    TEMPLATE_THUMB = u"""
    <xml>
    <ToUserName><![CDATA[{target}]]></ToUserName>
    <FromUserName><![CDATA[{source}]]></FromUserName>
    <CreateTime>{time}</CreateTime>
    <MsgType><![CDATA[music]]></MsgType>
    <Music>
    <Title><![CDATA[{title}]]></Title>
    <Description><![CDATA[{description}]]></Description>
    <MusicUrl><![CDATA[{music_url}]]></MusicUrl>
    <HQMusicUrl><![CDATA[{hq_music_url}]]></HQMusicUrl>
    <ThumbMediaId><![CDATA[{thumb_media_id}]]></ThumbMediaId>
    </Music>
    </xml>
    """

    TEMPLATE_NOTHUMB = u"""
    <xml>
    <ToUserName><![CDATA[{target}]]></ToUserName>
    <FromUserName><![CDATA[{source}]]></FromUserName>
    <CreateTime>{time}</CreateTime>
    <MsgType><![CDATA[music]]></MsgType>
    <Music>
    <Title><![CDATA[{title}]]></Title>
    <Description><![CDATA[{description}]]></Description>
    <MusicUrl><![CDATA[{music_url}]]></MusicUrl>
    <HQMusicUrl><![CDATA[{hq_music_url}]]></HQMusicUrl>
    </Music>
    </xml>
    """

    def __init__(self, message, title='', description='', music_url='', hq_music_url='', thumb_media_id=None):
        title = title or ''
        description = description or ''
        music_url = music_url or ''
        hq_music_url = hq_music_url or music_url
        super(MusicReply, self).__init__(message=message, title=title, description=description,
                                         music_url=music_url, hq_music_url=hq_music_url, thumb_media_id=thumb_media_id)

    def render(self):
        if self._args['thumb_media_id']:
            return MusicReply.TEMPLATE_THUMB.format(**self._args)
        else:
            return MusicReply.TEMPLATE_NOTHUMB.format(**self._args)


class Article(object):
    def __init__(self, title=None, description=None, picurl=None, url=None):
        self.title = title or ''
        self.description = description or ''
        self.picurl = picurl or ''
        self.url = url or ''


class ArticleReply(WechatReply):
    TEMPLATE = u"""
    <xml>
    <ToUserName><![CDATA[{target}]]></ToUserName>
    <FromUserName><![CDATA[{source}]]></FromUserName>
    <CreateTime>{time}</CreateTime>
    <MsgType><![CDATA[news]]></MsgType>
    <ArticleCount>{count}</ArticleCount>
    <Articles>{items}</Articles>
    </xml>
    """

    ITEM_TEMPLATE = u"""
    <item>
    <Title><![CDATA[{title}]]></Title>
    <Description><![CDATA[{description}]]></Description>
    <PicUrl><![CDATA[{picurl}]]></PicUrl>
    <Url><![CDATA[{url}]]></Url>
    </item>
    """

    def __init__(self, message, **kwargs):
        super(ArticleReply, self).__init__(message, **kwargs)
        self._articles = []

    def add_article(self, article):
        if len(self._articles) >= 10:
            raise AttributeError("Can't add more than 10 articles in an ArticleReply")
        else:
            self._articles.append(article)

    def render(self):
        items = []
        for article in self._articles:
            items.append(ArticleReply.ITEM_TEMPLATE.format(
                title=article.title,
                description=article.description,
                picurl=article.picurl,
                url=article.url,
            ))
        self._args["items"] = ''.join(items)
        self._args["count"] = len(items)
        return ArticleReply.TEMPLATE.format(**self._args)