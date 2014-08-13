# -*- coding: utf-8 -*-

import hashlib
import requests
import time
import json

from xml.dom import minidom
from xml.parsers.expat import ExpatError

from .messages import MESSAGE_TYPES, UnknownMessage
from .exceptions import ParseError, NeedParseError, NeedParamError, OfficialAPIError
from .reply import TextReply, ImageReply, VoiceReply, VideoReply, MusicReply, Article, ArticleReply


class WechatBasic(object):
    """
    微信基本功能类

    仅包含官方 API 中所包含的内容, 如需高级功能支持请移步 ext.py 中的 WechatExt 类
    """
    def __init__(self, token=None, appid=None, appsecret=None, partnerid=None,
                 partnerkey=None, paysignkey=None, access_token=None, access_token_expires_at=None):
        """
        :param token: 微信 Token
        :param appid: App ID
        :param appsecret: App Secret
        :param partnerid: 财付通商户身份标识, 支付权限专用
        :param partnerkey: 财付通商户权限密钥 Key, 支付权限专用
        :param paysignkey: 商户签名密钥 Key, 支付权限专用
        :param access_token: 直接导入的 access_token 值, 该值需要在上一次该类实例化之后手动进行缓存并在此处传入, 如果不传入, 将会在需要时自动重新获取
        :param access_token_expires_at: 直接导入的 access_token 的过期日期，该值需要在上一次该类实例化之后手动进行缓存并在此处传入, 如果不传入, 将会在需要时自动重新获取
        """
        self.__token = token
        self.__appid = appid
        self.__appsecret = appsecret
        self.__partnerid = partnerid
        self.__partnerkey = partnerkey
        self.__paysignkey = paysignkey

        self.__access_token = access_token
        self.__access_token_expires_at = access_token_expires_at
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
        self._check_token()

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
        if type(data) == unicode:
            data = data.encode('utf-8')
        elif type(data) == str:
            pass
        else:
            raise ParseError()

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

    def get_message(self):
        """
        获取解析好的 WechatMessage 对象
        :return: 解析好的 WechatMessage 对象
        """
        self._check_parse()

        return self.__message

    def get_access_token(self):
        """
        获取 Access Token 及 Access Token 过期日期, 仅供缓存使用, 如果希望得到原生的 Access Token 请求数据请使用 :func:`grant_token`
        :return: dict 对象, key 包括 `access_token` 及 `access_token_expires_at`
        """
        self._check_appid_appsecret()

        return {
            'access_token': self.access_token,
            'access_token_expires_at': self.__access_token_expires_at,
        }

    def response_text(self, content):
        """
        将文字信息 content 组装为符合微信服务器要求的响应数据
        :param content: 回复文字
        :return: 符合微信服务器要求的 XML 响应数据
        """
        self._check_parse()

        return TextReply(message=self.__message, content=content).render()

    def response_image(self, media_id):
        """
        将 media_id 所代表的图片组装为符合微信服务器要求的响应数据
        :param media_id: 图片的 MediaID
        :return: 符合微信服务器要求的 XML 响应数据
        """
        self._check_parse()

        return ImageReply(message=self.__message, media_id=media_id).render()

    def response_voice(self, media_id):
        """
        将 media_id 所代表的语音组装为符合微信服务器要求的响应数据
        :param media_id: 语音的 MediaID
        :return: 符合微信服务器要求的 XML 响应数据
        """
        self._check_parse()

        return VoiceReply(message=self.__message, media_id=media_id).render()

    def response_video(self, media_id, title=None, description=None):
        """
        将 media_id 所代表的视频组装为符合微信服务器要求的响应数据
        :param media_id: 视频的 MediaID
        :param title: 视频消息的标题
        :param description: 视频消息的描述
        :return: 符合微信服务器要求的 XML 响应数据
        """
        self._check_parse()

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
        """
        self._check_parse()

        return MusicReply(message=self.__message, title=title, description=description, music_url=music_url,
                          hq_music_url=hq_music_url, thumb_media_id=thumb_media_id).render()

    def response_news(self, articles):
        """
        将新闻信息组装为符合微信服务器要求的响应数据
        :param articles: list 对象, 每个元素为一个 dict 对象, key 包含 `title`, `description`, `picurl`, `url`
        :return: 符合微信服务器要求的 XML 响应数据
        """
        self._check_parse()

        news = ArticleReply(message=self.__message)
        for article in articles:
            article = Article(**article)
            news.add_article(article)
        return news.render()

    def grant_token(self):
        """
        获取 Access Token
        详情请参考 http://mp.weixin.qq.com/wiki/index.php?title=通用接口文档
        :return: 返回的 JSON 数据包
        """
        self._check_appid_appsecret()

        return self._get(
            url="https://api.weixin.qq.com/cgi-bin/token",
            params={
                "grant_type": "client_credential",
                "appid": self.__appid,
                "secret": self.__appsecret,
            }
        )

    def create_menu(self, menu_data):
        """
        创建自定义菜单 ::

            wechat = WechatBasic(appid='appid', appsecret='appsecret')
            wechat.create_menu({
                'button':[
                    {
                        'type':'click',
                        'name':'今日歌曲',
                        'key':'V1001_TODAY_MUSIC'
                    },
                    {
                        'type':'click',
                        'name':'歌手简介',
                        'key':'V1001_TODAY_SINGER'
                    },
                    {
                        'name':'菜单',
                        'sub_button':[
                            {
                                'type':'view',
                                'name':'搜索',
                                'url':'http://www.soso.com/'
                            },
                            {
                                'type':'view',
                                'name':'视频',
                                'url':'http://v.qq.com/'
                            },
                            {
                                'type':'click',
                                'name':'赞一下我们',
                                'key':'V1001_GOOD'
                            }
                        ]
                    }
                ]})

        详情请参考 http://mp.weixin.qq.com/wiki/index.php?title=自定义菜单创建接口
        :param menu_data: Python 字典
        :return: 返回的 JSON 数据包
        """
        self._check_appid_appsecret()

        return self._post(
            url='https://api.weixin.qq.com/cgi-bin/menu/create',
            data=menu_data
        )

    def get_menu(self):
        """
        查询自定义菜单
        详情请参考 http://mp.weixin.qq.com/wiki/index.php?title=自定义菜单查询接口
        :return: 返回的 JSON 数据包
        """
        self._check_appid_appsecret()

        return self._get('https://api.weixin.qq.com/cgi-bin/menu/get')

    def delete_menu(self):
        """
        删除自定义菜单
        详情请参考 http://mp.weixin.qq.com/wiki/index.php?title=自定义菜单删除接口
        :return: 返回的 JSON 数据包
        """
        self._check_appid_appsecret()

        return self._get('https://api.weixin.qq.com/cgi-bin/menu/delete')

    def upload_media(self, media_type, media_file):
        """
        上传多媒体文件
        详情请参考 http://mp.weixin.qq.com/wiki/index.php?title=上传下载多媒体文件
        :param media_type: 媒体文件类型，分别有图片（image）、语音（voice）、视频（video）和缩略图（thumb）
        :param media_file:要上传的文件，一个 File-object
        :return: 返回的 JSON 数据包
        """
        self._check_appid_appsecret()

        return self._post(
            url='http://file.api.weixin.qq.com/cgi-bin/media/upload',
            params={
                'access_token': self.access_token,
                'type': media_type,
            },
            files={
                'media': media_file,
            }
        )

    def download_media(self, media_id):
        """
        下载多媒体文件
        详情请参考 http://mp.weixin.qq.com/wiki/index.php?title=上传下载多媒体文件
        :param media_id: 媒体文件 ID
        :return: requests 的 Response 实例
        """
        self._check_appid_appsecret()

        return requests.get(
            'http://file.api.weixin.qq.com/cgi-bin/media/get',
            params={
                'access_token': self.access_token,
                'media_id': media_id,
            },
            stream=True,
        )

    def create_group(self, name):
        """
        创建分组
        详情请参考 http://mp.weixin.qq.com/wiki/index.php?title=分组管理接口
        :param name: 分组名字（30个字符以内）
        :return: 返回的 JSON 数据包
        """
        self._check_appid_appsecret()

        return self._post(
            url='https://api.weixin.qq.com/cgi-bin/groups/create',
            data={
                'group': {
                    'name': name,
                },
            }
        )

    def get_groups(self):
        """
        查询所有分组
        详情请参考 http://mp.weixin.qq.com/wiki/index.php?title=分组管理接口
        :return: 返回的 JSON 数据包
        """
        self._check_appid_appsecret()

        return self._get('https://api.weixin.qq.com/cgi-bin/groups/get')

    def get_group_by_id(self, openid):
        """
        查询用户所在分组
        详情请参考 http://mp.weixin.qq.com/wiki/index.php?title=分组管理接口
        :param openid: 用户的OpenID
        :return: 返回的 JSON 数据包
        """
        self._check_appid_appsecret()

        return self._post(
            url='https://api.weixin.qq.com/cgi-bin/groups/getid',
            data={
                'openid': openid,
            }
        )

    def update_group(self, group_id, name):
        """
        修改分组名
        详情请参考 http://mp.weixin.qq.com/wiki/index.php?title=分组管理接口
        :param group_id: 分组id，由微信分配
        :param name: 分组名字（30个字符以内）
        :return: 返回的 JSON 数据包
        """
        self._check_appid_appsecret()

        return self._post(
            url='https://api.weixin.qq.com/cgi-bin/groups/update',
            data={
                'group': {
                    'id': int(group_id),
                    'name': name,
                }
            }
        )

    def move_user(self, user_id, group_id):
        """
        移动用户分组
        详情请参考 http://mp.weixin.qq.com/wiki/index.php?title=分组管理接口
        :param user_id: 用户 ID 。 就是你收到的 WechatMessage 的 source
        :param group_id: 分组 ID
        :return: 返回的 JSON 数据包
        """
        self._check_appid_appsecret()

        return self._post(
            url='https://api.weixin.qq.com/cgi-bin/groups/members/update',
            data={
                'openid': user_id,
                'to_groupid': group_id,
            }
        )

    def get_user_info(self, user_id, lang='zh_CN'):
        """
        获取用户基本信息
        详情请参考 http://mp.weixin.qq.com/wiki/index.php?title=获取用户基本信息
        :param user_id: 用户 ID, 就是你收到的 WechatMessage 的 source
        :param lang: 返回国家地区语言版本，zh_CN 简体，zh_TW 繁体，en 英语
        :return: 返回的 JSON 数据包
        """
        self._check_appid_appsecret()

        return self._get(
            url='https://api.weixin.qq.com/cgi-bin/user/info',
            params={
                'access_token': self.access_token,
                'openid': user_id,
                'lang': lang,
            }
        )

    def get_followers(self, first_user_id=None):
        """
        获取关注者列表
        详情请参考 http://mp.weixin.qq.com/wiki/index.php?title=获取关注者列表
        :param first_user_id: 可选。第一个拉取的OPENID，不填默认从头开始拉取
        :return: 返回的 JSON 数据包
        """
        self._check_appid_appsecret()

        params = {
            'access_token': self.access_token,
        }
        if first_user_id:
            params['next_openid'] = first_user_id
        return self._get('https://api.weixin.qq.com/cgi-bin/user/get', params=params)

    def send_text_message(self, user_id, content):
        """
        发送文本消息
        详情请参考 http://mp.weixin.qq.com/wiki/index.php?title=发送客服消息
        :param user_id: 用户 ID, 就是你收到的 WechatMessage 的 source
        :param content: 消息正文
        :return: 返回的 JSON 数据包
        """
        self._check_appid_appsecret()

        return self._post(
            url='https://api.weixin.qq.com/cgi-bin/message/custom/send',
            data={
                'touser': user_id,
                'msgtype': 'text',
                'text': {
                    'content': content,
                },
            }
        )

    def send_image_message(self, user_id, media_id):
        """
        发送图片消息
        详情请参考 http://mp.weixin.qq.com/wiki/index.php?title=发送客服消息
        :param user_id: 用户 ID, 就是你收到的 WechatMessage 的 source
        :param media_id: 图片的媒体ID。 可以通过 :func:`upload_media` 上传。
        :return: 返回的 JSON 数据包
        """
        self._check_appid_appsecret()

        return self._post(
            url='https://api.weixin.qq.com/cgi-bin/message/custom/send',
            data={
                'touser': user_id,
                'msgtype': 'image',
                'image': {
                    'media_id': media_id,
                },
            }
        )

    def send_voice_message(self, user_id, media_id):
        """
        发送语音消息
        详情请参考 http://mp.weixin.qq.com/wiki/index.php?title=发送客服消息
        :param user_id: 用户 ID, 就是你收到的 WechatMessage 的 source
        :param media_id: 发送的语音的媒体ID。 可以通过 :func:`upload_media` 上传。
        :return: 返回的 JSON 数据包
        """
        self._check_appid_appsecret()

        return self._post(
            url='https://api.weixin.qq.com/cgi-bin/message/custom/send',
            data={
                'touser': user_id,
                'msgtype': 'voice',
                'voice': {
                    'media_id': media_id,
                },
            }
        )

    def send_video_message(self, user_id, media_id, title=None, description=None):
        """
        发送视频消息
        详情请参考 http://mp.weixin.qq.com/wiki/index.php?title=发送客服消息
        :param user_id: 用户 ID, 就是你收到的 WechatMessage 的 source
        :param media_id: 发送的视频的媒体ID。 可以通过 :func:`upload_media` 上传。
        :param title: 视频消息的标题
        :param description: 视频消息的描述
        :return: 返回的 JSON 数据包
        """
        self._check_appid_appsecret()

        video_data = {
            'media_id': media_id,
        }
        if title:
            video_data['title'] = title
        if description:
            video_data['description'] = description

        return self._post(
            url='https://api.weixin.qq.com/cgi-bin/message/custom/send',
            data={
                'touser': user_id,
                'msgtype': 'video',
                'video': video_data,
            }
        )

    def send_music_message(self, user_id, url, hq_url, thumb_media_id, title=None, description=None):
        """
        发送音乐消息
        详情请参考 http://mp.weixin.qq.com/wiki/index.php?title=发送客服消息
        :param user_id: 用户 ID, 就是你收到的 WechatMessage 的 source
        :param url: 音乐链接
        :param hq_url: 高品质音乐链接，wifi环境优先使用该链接播放音乐
        :param thumb_media_id: 缩略图的媒体ID。 可以通过 :func:`upload_media` 上传。
        :param title: 音乐标题
        :param description: 音乐描述
        :return: 返回的 JSON 数据包
        """
        self._check_appid_appsecret()

        music_data = {
            'musicurl': url,
            'hqmusicurl': hq_url,
            'thumb_media_id': thumb_media_id,
        }
        if title:
            music_data['title'] = title
        if description:
            music_data['description'] = description

        return self._post(
            url='https://api.weixin.qq.com/cgi-bin/message/custom/send',
            data={
                'touser': user_id,
                'msgtype': 'music',
                'music': music_data,
            }
        )

    def send_article_message(self, user_id, articles):
        """
        发送图文消息
        详情请参考 http://mp.weixin.qq.com/wiki/index.php?title=发送客服消息
        :param user_id: 用户 ID, 就是你收到的 WechatMessage 的 source
        :param articles: list 对象, 每个元素为一个 dict 对象, key 包含 `title`, `description`, `picurl`, `url`
        :return: 返回的 JSON 数据包
        """
        self._check_appid_appsecret()

        articles_data = []
        for article in articles:
            article = Article(**article)
            articles_data.append({
                'title': article.title,
                'description': article.description,
                'url': article.url,
                'picurl': article.picurl,
            })
        return self._post(
            url='https://api.weixin.qq.com/cgi-bin/message/custom/send',
            data={
                'touser': user_id,
                'msgtype': 'news',
                'news': {
                    'articles': articles_data,
                },
            }
        )

    def create_qrcode(self, **data):
        """
        创建二维码
        详情请参考 http://mp.weixin.qq.com/wiki/index.php?title=生成带参数的二维码
        :param data: 你要发送的参数 dict
        :return: 返回的 JSON 数据包
        """
        self._check_appid_appsecret()

        return self._post(
            url='https://api.weixin.qq.com/cgi-bin/qrcode/create',
            data=data
        )

    def show_qrcode(self, ticket):
        """
        通过ticket换取二维码
        详情请参考 http://mp.weixin.qq.com/wiki/index.php?title=生成带参数的二维码
        :param ticket: 二维码 ticket 。可以通过 :func:`create_qrcode` 获取到
        :return: 返回的 Request 对象
        """
        self._check_appid_appsecret()

        return requests.get(
            url='https://mp.weixin.qq.com/cgi-bin/showqrcode',
            params={
                'ticket': ticket
            }
        )

    @property
    def access_token(self):
        self._check_appid_appsecret()

        if self.__access_token:
            now = time.time()
            if self.__access_token_expires_at - now > 60:
                return self.__access_token
        response_json = self.grant_token()
        self.__access_token = response_json['access_token']
        self.__access_token_expires_at = int(time.time()) + response_json['expires_in']
        return self.__access_token

    def _check_token(self):
        """
        检查 Token 是否存在
        :raises NeedParamError: Token 参数没有在初始化的时候提供
        """
        if not self.__token:
            raise NeedParamError('Please provide Token parameter in the construction of class.')

    def _check_appid_appsecret(self):
        """
        检查 AppID 和 AppSecret 是否存在
        :raises NeedParamError: AppID 或 AppSecret 参数没有在初始化的时候完整提供
        """
        if not self.__appid or not self.__appsecret:
            raise NeedParamError('Please provide app_id and app_secret parameters in the construction of class.')

    def _check_parse(self):
        """
        检查是否成功解析微信服务器传来的数据
        :raises NeedParseError: 需要解析微信服务器传来的数据
        """
        if not self.__is_parse:
            raise NeedParseError()

    def _check_official_error(self, json_data):
        """
        检测微信公众平台返回值中是否包含错误的返回码
        :raises OfficialAPIError: 如果返回码提示有错误，抛出异常；否则返回 True
        """
        if "errcode" in json_data and json_data["errcode"] != 0:
            raise OfficialAPIError("{}: {}".format(json_data["errcode"], json_data["errmsg"]))

    def _request(self, method, url, **kwargs):
        """
        向微信服务器发送请求
        :param method: 请求方法
        :param url: 请求地址
        :param kwargs: 附加数据
        :return: 微信服务器响应的 json 数据
        """
        if "params" not in kwargs:
            kwargs["params"] = {
                "access_token": self.access_token,
            }
        if isinstance(kwargs.get("data", ""), dict):
            body = json.dumps(kwargs["data"], ensure_ascii=False)
            body = body.encode('utf8')
            kwargs["data"] = body

        r = requests.request(
            method=method,
            url=url,
            **kwargs
        )
        r.raise_for_status()
        response_json = r.json()
        self._check_official_error(response_json)
        return response_json

    def _get(self, url, **kwargs):
        """
        使用 GET 方法向微信服务器发出请求
        :param url: 请求地址
        :param kwargs: 附加数据
        :return: 微信服务器响应的 json 数据
        """
        return self._request(
            method="get",
            url=url,
            **kwargs
        )

    def _post(self, url, **kwargs):
        """
        使用 POST 方法向微信服务器发出请求
        :param url: 请求地址
        :param kwargs: 附加数据
        :return: 微信服务器响应的 json 数据
        """
        return self._request(
            method="post",
            url=url,
            **kwargs
        )