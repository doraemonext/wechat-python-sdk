# -*- coding: utf-8 -*-
# From: https://github.com/whtsky/WeRoBot/blob/develop/werobot/messages.py

from .exceptions import ParseError

MESSAGE_TYPES = {}


def handle_for_type(type):
    def register(f):
        MESSAGE_TYPES[type] = f
        return f
    return register


class WechatMessage(object):
    def __init__(self, message):
        self.id = int(message.pop("MsgId", 0))
        self.target = message.pop("ToUserName", None)
        self.source = message.pop('FromUserName', None)
        self.time = int(message.pop('CreateTime', 0))
        self.__dict__.update(message)


@handle_for_type("text")
class TextMessage(WechatMessage):
    def __init__(self, message):
        self.content = message.pop("Content", "")
        super(TextMessage, self).__init__(message)


@handle_for_type("image")
class ImageMessage(WechatMessage):
    def __init__(self, message):
        try:
            self.picurl = message.pop("PicUrl")
            self.media_id = message.pop('MediaId')
        except KeyError:
            raise ParseError()
        super(ImageMessage, self).__init__(message)


@handle_for_type("video")
class VideoMessage(WechatMessage):
    def __init__(self, message):
        try:
            self.media_id = message.pop('MediaId')
            self.thumb_media_id = message.pop('ThumbMediaId')
        except KeyError:
            raise ParseError()
        super(VideoMessage, self).__init__(message)


@handle_for_type("location")
class LocationMessage(WechatMessage):
    def __init__(self, message):
        try:
            location_x = message.pop('Location_X')
            location_y = message.pop('Location_Y')
            self.location = (float(location_x), float(location_y))
            self.scale = int(message.pop('Scale'))
            self.label = message.pop('Label')
        except KeyError:
            raise ParseError()
        super(LocationMessage, self).__init__(message)


@handle_for_type("link")
class LinkMessage(WechatMessage):
    def __init__(self, message):
        try:
            self.title = message.pop('Title')
            self.description = message.pop('Description')
            self.url = message.pop('Url')
        except KeyError:
            raise ParseError()
        super(LinkMessage, self).__init__(message)


@handle_for_type("event")
class EventMessage(WechatMessage):
    def __init__(self, message):
        message.pop("type")
        try:
            self.type = message.pop("Event").lower()
            if self.type == "click":
                self.key = message.pop('EventKey')
            elif self.type == "location":
                self.latitude = float(message.pop("Latitude"))
                self.longitude = float(message.pop("Longitude"))
                self.precision = float(message.pop("Precision"))
        except KeyError:
            raise ParseError()
        super(EventMessage, self).__init__(message)


@handle_for_type("voice")
class VoiceMessage(WechatMessage):
    def __init__(self, message):
        try:
            self.media_id = message.pop('MediaId')
            self.format = message.pop('Format')
            self.recognition = message.pop('Recognition')
        except KeyError:
            raise ParseError()
        super(VoiceMessage, self).__init__(message)


class UnknownMessage(WechatMessage):
    def __init__(self, message):
        self.type = 'unknown'
        super(UnknownMessage, self).__init__(message)