# -*- coding: utf-8 -*-

import io
import hashlib
import requests
import cgi
import six

from .base import WechatBase
from .core.conf import WechatConf
from .messages import MESSAGE_TYPES, UnknownMessage
from .exceptions import (
    ParseError, NeedParseError, NeedParamError, OfficialAPIError)
from .reply import (
    TextReply, ImageReply, VoiceReply, VideoReply, MusicReply, Article,
    ArticleReply, GroupTransferReply)
from .lib.parser import XMLStore
from .lib.request import WechatRequest
from .utils import to_binary, to_text, generate_nonce, generate_timestamp, convert_ext_to_mime, is_allowed_extension


class WechatBasic(WechatBase):
    """微信基本功能类

    仅包含官方 API 中所包含的内容, 如需高级功能支持请移步 ext.py 中的 WechatExt 类
    """
    def __init__(self, token=None, appid=None, appsecret=None, partnerid=None,
                 partnerkey=None, paysignkey=None, access_token=None, access_token_expires_at=None,
                 jsapi_ticket=None, jsapi_ticket_expires_at=None, checkssl=False, conf=None):
        """
        :param token: 微信 Token
        :param appid: App ID
        :param appsecret: App Secret
        :param partnerid: 财付通商户身份标识, 支付权限专用
        :param partnerkey: 财付通商户权限密钥 Key, 支付权限专用
        :param paysignkey: 商户签名密钥 Key, 支付权限专用
        :param access_token: 直接导入的 access_token 值, 该值需要在上一次该类实例化之后手动进行缓存并在此处传入, 如果不传入, 将会在需要时自动重新获取
        :param access_token_expires_at: 直接导入的 access_token 的过期日期，该值需要在上一次该类实例化之后手动进行缓存并在此处传入, 如果不传入, 将会在需要时自动重新获取
        :param jsapi_ticket: 直接导入的 jsapi_ticket 值, 该值需要在上一次该类实例化之后手动进行缓存并在此处传入, 如果不传入, 将会在需要时自动重新获取
        :param jsapi_ticket_expires_at: 直接导入的 jsapi_ticket 的过期日期，该值需要在上一次该类实例化之后手动进行缓存并在此处传入, 如果不传入, 将会在需要时自动重新获取
        :param checkssl: 是否检查 SSL, 默认为 False, 可避免 urllib3 的 InsecurePlatformWarning 警告
        :param conf: WechatConf 配置类, 提供此参数将默认忽略其他所有参数, 所有数据均从此配置类中获取
        """
        if conf is not None:
            self.__conf = conf
        elif isinstance(token, WechatConf):  # 针对将 WechatConf 实例作为第一个参数传入的容错处理
            self.__conf = token
        else:  # 仅为兼容 v0.6.0 以前的初始化操作, 不再进行更新维护
            self.__conf = WechatConf(
                token=token,
                appid=appid,
                appsecret=appsecret,

                access_token=access_token,
                access_token_expires_at=access_token_expires_at,
                jsapi_ticket=jsapi_ticket,
                jsapi_ticket_expires_at=jsapi_ticket_expires_at,

                encrypt_mode='normal',

                partnerid=partnerid,
                partnerkey=partnerkey,
                paysignkey=paysignkey,
                checkssl=checkssl,
            )

        self.__request = WechatRequest(conf=self.__conf)
        self.__is_parse = False
        self.__message = None

    @property
    def conf(self):
        """ 获取当前 WechatConf 配置实例 """
        return self.__conf

    @conf.setter
    def conf(self, conf):
        """ 设置当前 WechatConf 实例  """
        self.__conf = conf
        self.__request = WechatRequest(conf=self.__conf)

    @property
    def request(self):
        """ 获取当前 WechatConf 配置实例 """
        return self.__request

    @request.setter
    def request(self, request):
        """ 设置当前 WechatConf 实例  """
        self.__request = request

    def check_signature(self, signature, timestamp, nonce):
        """
        验证微信消息真实性
        :param signature: 微信加密签名
        :param timestamp: 时间戳
        :param nonce: 随机数
        :return: 通过验证返回 True, 未通过验证返回 False
        """
        if not signature or not timestamp or not nonce:
            return False

        tmp_list = [self.conf.token, timestamp, nonce]
        tmp_list.sort()
        tmp_str = ''.join(tmp_list)
        if signature != hashlib.sha1(tmp_str.encode('utf-8')).hexdigest():
            return False

        return True

    def generate_jsapi_signature(self, timestamp, noncestr, url, jsapi_ticket=None):
        """
        使用 jsapi_ticket 对 url 进行签名
        :param timestamp: 时间戳
        :param noncestr: 随机数
        :param url: 要签名的 url，不包含 # 及其后面部分
        :param jsapi_ticket: (可选参数) jsapi_ticket 值 (如不提供将自动通过 appid 和 appsecret 获取)
        :return: 返回sha1签名的hexdigest值
        """
        if not jsapi_ticket:
            jsapi_ticket = self.conf.jsapi_ticket
        data = {
            'jsapi_ticket': jsapi_ticket,
            'noncestr': noncestr,
            'timestamp': timestamp,
            'url': url,
        }
        keys = list(data.keys())
        keys.sort()
        data_str = '&'.join(['%s=%s' % (key, data[key]) for key in keys])
        signature = hashlib.sha1(data_str.encode('utf-8')).hexdigest()
        return signature

    def parse_data(self, data, msg_signature=None, timestamp=None, nonce=None):
        """
        解析微信服务器发送过来的数据并保存类中
        :param data: HTTP Request 的 Body 数据
        :param msg_signature: EncodingAESKey 的 msg_signature
        :param timestamp: EncodingAESKey 用时间戳
        :param nonce: EncodingAESKey 用随机数
        :raises ParseError: 解析微信服务器数据错误, 数据不合法
        """
        result = {}
        if isinstance(data, six.text_type):  # unicode to str(PY2), str to bytes(PY3)
            data = data.encode('utf-8')

        if self.conf.encrypt_mode == 'safe':
            if not (msg_signature and timestamp and nonce):
                raise ParseError('must provide msg_signature/timestamp/nonce in safe encrypt mode')

            data = self.conf.crypto.decrypt_message(
                msg=data,
                msg_signature=msg_signature,
                timestamp=timestamp,
                nonce=nonce,
            )
        try:
            xml = XMLStore(xmlstring=data)
        except Exception:
            raise ParseError()

        result = xml.xml2dict
        result['raw'] = data
        result['type'] = result.pop('MsgType').lower()

        message_type = MESSAGE_TYPES.get(result['type'], UnknownMessage)
        self.__message = message_type(result)
        self.__is_parse = True

    @property
    def message(self):
        return self.get_message()

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
        **仅为兼容 v0.6.0 以前版本使用, 自行维护 access_token 请使用 access_token_setfunc 和 access_token_getfunc 进行操作**
        :return: dict 对象, key 包括 `access_token` 及 `access_token_expires_at`
        """
        return self.conf.get_access_token()

    def get_jsapi_ticket(self):
        """
        获取 Jsapi Ticket 及 Jsapi Ticket 过期日期, 仅供缓存使用, 如果希望得到原生的 Jsapi Ticket 请求数据请使用 :func:`grant_jsapi_ticket`
        **仅为兼容 v0.6.0 以前版本使用, 自行维护 jsapi_ticket 请使用 jsapi_ticket_setfunc 和 jsapi_ticket_getfunc 进行操作**
        :return: dict 对象, key 包括 `jsapi_ticket` 及 `jsapi_ticket_expires_at`
        """
        return self.conf.get_jsapi_ticket()

    def response_none(self):
        """
        回复空消息
        :return: 符合微信服务器要求的空消息
        """
        self._check_parse()
        return self._encrypt_response('success')

    def response_text(self, content, escape=False):
        """
        将文字信息 content 组装为符合微信服务器要求的响应数据
        :param content: 回复文字
        :param escape: 是否转义该文本内容 (默认不转义)
        :return: 符合微信服务器要求的 XML 响应数据
        """
        self._check_parse()
        content = self._transcoding(content)
        if escape:
            if six.PY2:
                content = cgi.escape(content)
            else:
                import html
                content = html.escape(content)

        response = TextReply(message=self.__message, content=content).render()
        return self._encrypt_response(response)

    def response_image(self, media_id):
        """
        将 media_id 所代表的图片组装为符合微信服务器要求的响应数据
        :param media_id: 图片的 MediaID
        :return: 符合微信服务器要求的 XML 响应数据
        """
        self._check_parse()

        response = ImageReply(message=self.__message, media_id=media_id).render()
        return self._encrypt_response(response)

    def response_voice(self, media_id):
        """
        将 media_id 所代表的语音组装为符合微信服务器要求的响应数据
        :param media_id: 语音的 MediaID
        :return: 符合微信服务器要求的 XML 响应数据
        """
        self._check_parse()

        response = VoiceReply(message=self.__message, media_id=media_id).render()
        return self._encrypt_response(response)

    def response_video(self, media_id, title=None, description=None):
        """
        将 media_id 所代表的视频组装为符合微信服务器要求的响应数据
        :param media_id: 视频的 MediaID
        :param title: 视频消息的标题
        :param description: 视频消息的描述
        :return: 符合微信服务器要求的 XML 响应数据
        """
        self._check_parse()
        title = self._transcoding(title)
        description = self._transcoding(description)

        response = VideoReply(message=self.__message, media_id=media_id, title=title, description=description).render()
        return self._encrypt_response(response)

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
        music_url = self._transcoding(music_url)
        title = self._transcoding(title)
        description = self._transcoding(description)
        hq_music_url = self._transcoding(hq_music_url)

        response = MusicReply(message=self.__message, title=title, description=description, music_url=music_url,
                              hq_music_url=hq_music_url, thumb_media_id=thumb_media_id).render()
        return self._encrypt_response(response)

    def response_news(self, articles):
        """
        将新闻信息组装为符合微信服务器要求的响应数据
        :param articles: list 对象, 每个元素为一个 dict 对象, key 包含 `title`, `description`, `picurl`, `url`
        :return: 符合微信服务器要求的 XML 响应数据
        """
        self._check_parse()
        for article in articles:
            if article.get('title'):
                article['title'] = self._transcoding(article['title'])
            if article.get('description'):
                article['description'] = self._transcoding(article['description'])
            if article.get('picurl'):
                article['picurl'] = self._transcoding(article['picurl'])
            if article.get('url'):
                article['url'] = self._transcoding(article['url'])

        news = ArticleReply(message=self.__message)
        for article in articles:
            article = Article(**article)
            news.add_article(article)
        response = news.render()
        return self._encrypt_response(response)

    def group_transfer_message(self):
        """
        将 message 群发到多客服系统
        :return: 符合微信服务器要求的 XML 响应数据
        """
        self._check_parse()
        response = GroupTransferReply(message=self.__message).render()
        return self._encrypt_response(response)

    def grant_token(self, **kwargs):
        """
        获取 Access Token
        详情请参考 http://mp.weixin.qq.com/wiki/11/0e4b294685f817b95cbed85ba5e82b8f.html
        :return: 返回的 JSON 数据包
        """
        return self.conf.grant_access_token()

    def grant_jsapi_ticket(self, **kwargs):
        """
        获取 Jsapi Ticket
        详情请参考 http://mp.weixin.qq.com/wiki/7/aaa137b55fb2e0456bf8dd9148dd613f.html#.E9.99.84.E5.BD.951-JS-SDK.E4.BD.BF.E7.94.A8.E6.9D.83.E9.99.90.E7.AD.BE.E5.90.8D.E7.AE.97.E6.B3.95
        :return: 返回的 JSON 数据包
        """
        return self.conf.grant_jsapi_ticket()

    def create_menu(self, menu_data):
        """
        创建自定义菜单 ::

            # -*- coding: utf-8 -*-
            wechat = WechatBasic(appid='appid', appsecret='appsecret')
            wechat.create_menu({
                'button':[
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
                ]})

        详情请参考 http://mp.weixin.qq.com/wiki/13/43de8269be54a0a6f64413e4dfa94f39.html
        :param menu_data: Python 字典
        :return: 返回的 JSON 数据包
        """
        menu_data = self._transcoding_dict(menu_data)
        return self.request.post(
            url='https://api.weixin.qq.com/cgi-bin/menu/create',
            data=menu_data
        )

    def get_menu(self):
        """
        查询自定义菜单
        详情请参考 http://mp.weixin.qq.com/wiki/16/ff9b7b85220e1396ffa16794a9d95adc.html
        :return: 返回的 JSON 数据包
        """
        return self.request.get('https://api.weixin.qq.com/cgi-bin/menu/get')

    def delete_menu(self):
        """
        删除自定义菜单
        详情请参考 http://mp.weixin.qq.com/wiki/16/8ed41ba931e4845844ad6d1eeb8060c8.html
        :return: 返回的 JSON 数据包
        """
        return self.request.get('https://api.weixin.qq.com/cgi-bin/menu/delete')

    def upload_media(self, media_type, media_file, extension=''):
        """
        上传多媒体文件
        详情请参考 http://mp.weixin.qq.com/wiki/10/78b15308b053286e2a66b33f0f0f5fb6.html
        :param media_type: 媒体文件类型，分别有图片（image）、语音（voice）、视频（video）和缩略图（thumb）
        :param media_file: 要上传的文件，一个 File object 或 StringIO object
        :param extension: 如果 media_file 传入的为 StringIO object，那么必须传入 extension 显示指明该媒体文件扩展名，如 ``mp3``, ``amr``；如果 media_file 传入的为 File object，那么该参数请留空
        :return: 返回的 JSON 数据包
        """
        if six.PY2:
            return self._upload_media_py2(media_type, media_file, extension)
        else:
            return self._upload_media_py3(media_type, media_file, extension)

    def _upload_media_py2(self, media_type, media_file, extension=''):
        if not isinstance(media_file, file) and not isinstance(media_file, six.StringIO):
            raise ValueError('Parameter media_file must be file object or StringIO.StringIO object.')
        if isinstance(media_file, six.StringIO) and not is_allowed_extension(extension.lower()):
            raise ValueError('Please provide \'extension\' parameters when the type of \'media_file\' is \'StringIO.StringIO\'.')

        if isinstance(media_file, file):
            extension = media_file.name.split('.')[-1].lower()
            if not is_allowed_extension(extension):
                raise ValueError('Invalid file type.')
            filename = media_file.name
        else:
            extension = extension.lower()
            filename = 'temp.' + extension

        return self.request.post(
            url='https://api.weixin.qq.com/cgi-bin/media/upload',
            params={
                'type': media_type,
            },
            files={
                'media': (filename, media_file, convert_ext_to_mime(extension))
            }
        )

    def _upload_media_py3(self, media_type, media_file, extension=''):
        if isinstance(media_file, io.IOBase) and hasattr(media_file, 'name'):
            extension = media_file.name.split('.')[-1].lower()
            if not is_allowed_extension(extension):
                raise ValueError('Invalid file type.')
            filename = media_file.name
        elif isinstance(media_file, io.BytesIO):
            extension = extension.lower()
            if not is_allowed_extension(extension):
                raise ValueError('Please provide \'extension\' parameters when the type of \'media_file\' is \'io.BytesIO\'.')
            filename = 'temp.' + extension
        else:
            raise ValueError('Parameter media_file must be io.BufferedIOBase(open a file with \'rb\') or io.BytesIO object.')

        return self.request.post(
            url='https://api.weixin.qq.com/cgi-bin/media/upload',
            params={
                'type': media_type,
            },
            files={
                'media': (filename, media_file, convert_ext_to_mime(extension))
            }
        )

    def download_media(self, media_id):
        """
        下载多媒体文件
        详情请参考 http://mp.weixin.qq.com/wiki/10/78b15308b053286e2a66b33f0f0f5fb6.html
        :param media_id: 媒体文件 ID
        :return: requests 的 Response 实例
        """
        return self.request.get(
            'https://api.weixin.qq.com/cgi-bin/media/get',
            params={
                'media_id': media_id,
            },
            stream=True,
        )

    def create_group(self, name):
        """
        创建分组
        详情请参考 http://mp.weixin.qq.com/wiki/13/be5272dc4930300ba561d927aead2569.html
        :param name: 分组名字（30个字符以内）
        :return: 返回的 JSON 数据包
        :raise HTTPError: 微信api http 请求失败
        """
        return self.request.post(
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
        详情请参考 http://mp.weixin.qq.com/wiki/13/be5272dc4930300ba561d927aead2569.html
        :return: 返回的 JSON 数据包
        """
        return self.request.get('https://api.weixin.qq.com/cgi-bin/groups/get')

    def get_group_by_id(self, openid):
        """
        查询用户所在分组
        详情请参考 http://mp.weixin.qq.com/wiki/13/be5272dc4930300ba561d927aead2569.html
        :param openid: 用户的OpenID
        :return: 返回的 JSON 数据包
        """
        return self.request.post(
            url='https://api.weixin.qq.com/cgi-bin/groups/getid',
            data={
                'openid': openid,
            }
        )

    def update_group(self, group_id, name):
        """
        修改分组名
        详情请参考 http://mp.weixin.qq.com/wiki/13/be5272dc4930300ba561d927aead2569.html
        :param group_id: 分组id，由微信分配
        :param name: 分组名字（30个字符以内）
        :return: 返回的 JSON 数据包
        """
        return self.request.post(
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
        详情请参考 http://mp.weixin.qq.com/wiki/13/be5272dc4930300ba561d927aead2569.html
        :param user_id: 用户 ID 。 就是你收到的 WechatMessage 的 source
        :param group_id: 分组 ID
        :return: 返回的 JSON 数据包
        """
        return self.request.post(
            url='https://api.weixin.qq.com/cgi-bin/groups/members/update',
            data={
                'openid': user_id,
                'to_groupid': group_id,
            }
        )

    def get_user_info(self, user_id, lang='zh_CN'):
        """
        获取用户基本信息
        详情请参考 http://mp.weixin.qq.com/wiki/14/bb5031008f1494a59c6f71fa0f319c66.html
        :param user_id: 用户 ID, 就是你收到的 WechatMessage 的 source
        :param lang: 返回国家地区语言版本，zh_CN 简体，zh_TW 繁体，en 英语
        :return: 返回的 JSON 数据包
        """
        return self.request.get(
            url='https://api.weixin.qq.com/cgi-bin/user/info',
            params={
                'openid': user_id,
                'lang': lang,
            }
        )

    def get_followers(self, first_user_id=None):
        """
        获取关注者列表
        详情请参考 http://mp.weixin.qq.com/wiki/3/17e6919a39c1c53555185907acf70093.html
        :param first_user_id: 可选。第一个拉取的OPENID，不填默认从头开始拉取
        :return: 返回的 JSON 数据包
        """
        params = dict()
        if first_user_id:
            params['next_openid'] = first_user_id
        return self.request.get('https://api.weixin.qq.com/cgi-bin/user/get', params=params)

    def send_text_message(self, user_id, content):
        """
        发送文本消息
        详情请参考 http://mp.weixin.qq.com/wiki/7/12a5a320ae96fecdf0e15cb06123de9f.html
        :param user_id: 用户 ID, 就是你收到的 WechatMessage 的 source
        :param content: 消息正文
        :return: 返回的 JSON 数据包
        """
        return self.request.post(
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
        详情请参考 http://mp.weixin.qq.com/wiki/7/12a5a320ae96fecdf0e15cb06123de9f.html
        :param user_id: 用户 ID, 就是你收到的 WechatMessage 的 source
        :param media_id: 图片的媒体ID。 可以通过 :func:`upload_media` 上传。
        :return: 返回的 JSON 数据包
        """
        return self.request.post(
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
        详情请参考 http://mp.weixin.qq.com/wiki/7/12a5a320ae96fecdf0e15cb06123de9f.html
        :param user_id: 用户 ID, 就是你收到的 WechatMessage 的 source
        :param media_id: 发送的语音的媒体ID。 可以通过 :func:`upload_media` 上传。
        :return: 返回的 JSON 数据包
        """
        return self.request.post(
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
        详情请参考 http://mp.weixin.qq.com/wiki/7/12a5a320ae96fecdf0e15cb06123de9f.html
        :param user_id: 用户 ID, 就是你收到的 WechatMessage 的 source
        :param media_id: 发送的视频的媒体ID。 可以通过 :func:`upload_media` 上传。
        :param title: 视频消息的标题
        :param description: 视频消息的描述
        :return: 返回的 JSON 数据包
        """
        video_data = {
            'media_id': media_id,
        }
        if title:
            video_data['title'] = title
        if description:
            video_data['description'] = description

        return self.request.post(
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
        详情请参考 http://mp.weixin.qq.com/wiki/7/12a5a320ae96fecdf0e15cb06123de9f.html
        :param user_id: 用户 ID, 就是你收到的 WechatMessage 的 source
        :param url: 音乐链接
        :param hq_url: 高品质音乐链接，wifi环境优先使用该链接播放音乐
        :param thumb_media_id: 缩略图的媒体ID。 可以通过 :func:`upload_media` 上传。
        :param title: 音乐标题
        :param description: 音乐描述
        :return: 返回的 JSON 数据包
        """
        music_data = {
            'musicurl': url,
            'hqmusicurl': hq_url,
            'thumb_media_id': thumb_media_id,
        }
        if title:
            music_data['title'] = title
        if description:
            music_data['description'] = description

        return self.request.post(
            url='https://api.weixin.qq.com/cgi-bin/message/custom/send',
            data={
                'touser': user_id,
                'msgtype': 'music',
                'music': music_data,
            }
        )

    def send_article_message(self, user_id, articles=None, media_id=None):
        """
        发送图文消息
        详情请参考 http://mp.weixin.qq.com/wiki/7/12a5a320ae96fecdf0e15cb06123de9f.html
        :param user_id: 用户 ID, 就是你收到的 WechatMessage 的 source
        :param articles: list 对象, 每个元素为一个 dict 对象, key 包含 `title`, `description`, `picurl`, `url`
        :param media_id: 待发送的图文 Media ID
        :return: 返回的 JSON 数据包
        """
        # neither 'articles' nor 'media_id' is specified
        if articles is None and media_id is None:
            raise TypeError('must provide one parameter in "articles" and "media_id"')

        # articles specified
        if articles:
            articles_data = []
            for article in articles:
                article = Article(**article)
                articles_data.append({
                    'title': article.title,
                    'description': article.description,
                    'url': article.url,
                    'picurl': article.picurl,
                })
            return self.request.post(
                url='https://api.weixin.qq.com/cgi-bin/message/custom/send',
                data={
                    'touser': user_id,
                    'msgtype': 'news',
                    'news': {
                        'articles': articles_data,
                    },
                }
            )

        # media_id specified
        return self.request.post(
            url='https://api.weixin.qq.com/cgi-bin/message/custom/send',
            data={
                'touser': user_id,
                'msgtype': 'mpnews',
                'mpnews': {
                    'media_id': media_id,
                },
            }
        )

    def create_qrcode(self, data):
        """
        创建二维码
        详情请参考 http://mp.weixin.qq.com/wiki/18/28fc21e7ed87bec960651f0ce873ef8a.html
        :param data: 你要发送的参数 dict
        :return: 返回的 JSON 数据包
        """
        data = self._transcoding_dict(data)
        return self.request.post(
            url='https://api.weixin.qq.com/cgi-bin/qrcode/create',
            data=data
        )

    def show_qrcode(self, ticket):
        """
        通过ticket换取二维码
        详情请参考 http://mp.weixin.qq.com/wiki/18/28fc21e7ed87bec960651f0ce873ef8a.html
        :param ticket: 二维码 ticket 。可以通过 :func:`create_qrcode` 获取到
        :return: 返回的 Request 对象
        """
        return requests.get(
            url='https://mp.weixin.qq.com/cgi-bin/showqrcode',
            params={
                'ticket': ticket
            }
        )

    def set_template_industry(self, industry_id1, industry_id2):
        """
        设置所属行业
        详情请参考 http://mp.weixin.qq.com/wiki/17/304c1885ea66dbedf7dc170d84999a9d.html
        :param industry_id1: 主营行业代码
        :param industry_id2: 副营行业代码
        :return: 返回的 JSON 数据包
        """
        return self.request.post(
            url='https://api.weixin.qq.com/cgi-bin/template/api_set_industry',
            data={
                'industry_id1': str(industry_id1),
                'industry_id2': str(industry_id2),
            }
        )

    def get_template_id(self, template_id_short):
        """
        获得模板ID
        详情请参考 http://mp.weixin.qq.com/wiki/17/304c1885ea66dbedf7dc170d84999a9d.html
        :param template_id_short: 模板库中模板的编号，有“TM**”和“OPENTMTM**”等形式
        :return: 返回的 JSON 数据包
        """
        return self.request.post(
            url='https://api.weixin.qq.com/cgi-bin/template/api_add_template',
            data={
                'template_id_short': str(template_id_short),
            }
        )

    def send_template_message(self, user_id, template_id, data, url='', topcolor='#FF0000'):
        """
        发送模版消息
        详情请参考 http://mp.weixin.qq.com/wiki/17/304c1885ea66dbedf7dc170d84999a9d.html
        :param user_id: 用户 ID, 就是你收到的 WechatMessage 的 source (OpenID)
        :param template_id: 模板ID
        :param data: 模板消息数据 (dict形式)，示例如下：
        {
            "first": {
               "value": "恭喜你购买成功！",
               "color": "#173177"
            },
            "keynote1":{
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
            "remark":{
               "value": "欢迎再次购买！",
               "color": "#173177"
            }
        }
        :param url: 跳转地址 (默认为空)
        :param topcolor: 顶部颜色RGB值 (默认 '#FF0000' )
        :return: 返回的 JSON 数据包
        """
        unicode_data = {}
        if data:
            unicode_data = self._transcoding_dict(data)

        return self.request.post(
            url='https://api.weixin.qq.com/cgi-bin/message/template/send',
            data={
                'touser': user_id,
                "template_id": template_id,
                "url": url,
                "topcolor": topcolor,
                "data": unicode_data
            }
        )

    @property
    def access_token(self):
        return self.conf.access_token

    @property
    def jsapi_ticket(self):
        return self.conf.jsapi_ticket

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
            raise OfficialAPIError(errcode=json_data.get('errcode'), errmsg=json_data.get('errmsg', ''))

    def _encrypt_response(self, response):
        if self.conf.encrypt_mode == 'safe':
            return self.conf.crypto.encrypt_message(
                msg=to_binary(response),
                nonce=generate_nonce(),
                timestamp=generate_timestamp(),
            )
        return response
