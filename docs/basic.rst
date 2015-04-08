微信官方接口操作 WechatBasic
=================================

.. py:class:: wechat_sdk.basic.WechatBasic(token=None, appid=None, appsecret=None, partnerid=None, partnerkey=None, paysignkey=None, access_token=None, access_token_expires_at=None, jsapi_ticket=None, jsapi_ticket_expires_at=None, checkssl=False)

    微信基本功能类

    :param str token: 微信 Token
    :param str appid: App ID
    :param str appsecret: App Secret
    :param str partnerid: 财付通商户身份标识, 支付权限专用
    :param str partnerkey: 财付通商户权限密钥 Key, 支付权限专用
    :param str paysignkey: 商户签名密钥 Key, 支付权限专用
    :param str access_token: 直接导入的 ``access_token`` 值, 该值需要在上一次该类实例化之后手动进行缓存并在此处传入, 如果不传入, 将会在需要时自动重新获取
    :param str access_token_expires_at: 直接导入的 ``access_token`` 的过期日期，该值需要在上一次该类实例化之后手动进行缓存并在此处传入, 如果不传入, 将会在需要时自动重新获取
    :param str jsapi_ticket: 直接导入的 ``jsapi_ticket`` 值, 该值需要在上一次该类实例化之后手动进行缓存并在此处传入, 如果不传入, 将会在需要时自动重新获取
    :param str jsapi_ticket_expires_at: 直接导入的 ``jsapi_ticket`` 的过期日期，该值需要在上一次该类实例化之后手动进行缓存并在此处传入, 如果不传入, 将会在需要时自动重新获取
    :param boolean checkssl: 是否检查 SSL, 默认为 False, 可避免 urllib3 的 InsecurePlatformWarning 警告

    **实例化说明：**

    1. 当实例化 WechatBasic 时，你可以传递上述参数说明中任意多个参数进去，但是传递参数不足将会在使用部分功能时引发对应的异常。

     **虽然认证订阅号、未认证服务号拥有 appid 及 appsecret，但不代表其能调用高级接口** ，这两种类型的账号仅能进行自定义菜单及JS相关操作，进行其他权限外操作仍然会抛出异常 ``OfficialAPIError``

    2. **详细说明一下 access_token, access_token_expires_at, jsapi_ticket, jsapi_ticket_expires_at 参数的传入问题：**

     因为此开发包并不打算以服务器的方式常驻，所以，每次请求均会重新实例化 ``WechatBasic`` ，而微信的 ``access_token`` 和 ``jsapi_ticket`` 的有效期为 7200 秒，不可能每次实例化的时候去重新获取，所以需要你以你自己的方式去保存上一次请求中实例化后的 ``WechatBasic`` 中 ``access_token``, ``access_token_expires_at``, ``jsapi_ticket``, ``jsapi_ticket_expires_at`` 参数，并在下一次的实例化的过程中传入，以此来保证 ``access_token`` 及 ``jsapi_ticket`` 的持久性。

     获取 ``access_token`` 及 ``access_token_expires_at`` 的方式为调用 :func:`get_access_token` 方法

     获取 ``jsapi_ticket`` 及 ``jsapi_ticket_expires_at`` 的方式为调用 :func:`get_jsapi_ticket` 方法

     下一版本将会考虑更为简单通用的方法，在新版本发布之前，请用你自己的方式把得到的 ``access_token``, ``access_token_expires_at``, ``jsapi_ticket``, ``jsapi_ticket_expires_at`` 保存起来，不管是文件，缓存还是数据库都可以，获取它们的时间可以非常自由，不管是刚刚实例化完成还是得到响应结果之后都没有问题，在调用对应函数时如果没有 ``access_token`` 或 ``jsapi_ticket`` 的话会自动获取的 :)

    .. py:method:: check_signature(signature, timestamp, nonce)

        验证微信消息真实性

        运行时检查：``token``

        可用公众号类型：认证/未认证订阅号, 认证/未认证服务号

        :param str signature: 微信加密签名
        :param str timestamp: 时间戳
        :param str nonce: 随机数
        :return: 通过验证返回 ``True``, 未通过验证返回 ``False``

    .. py:method:: generate_jsapi_signature(timestamp, noncestr, url, jsapi_ticket=None)

        使用 jsapi_ticket 对 url 进行签名

        当未提供 ``jsapi_ticket`` 参数时检查：``appid``, ``appsecret``

        可用公众号类型：认证/未认证订阅号，认证/未认证服务号

        :param str timestamp: 时间戳
        :param str noncestr: 随机数
        :param str url: 要签名的 url，不包含 # 及其后面部分
        :param str jsapi_ticket: (可选参数) jsapi_ticket 值 (如不提供将自动通过 appid 和 appsecret 获取)
        :return: 返回 sha1 签名的 hexdigest 值

    .. py:method:: parse_data(data)

        解析微信服务器发送过来的数据并保存类中

        运行时检查：无

        可用公众号类型：认证/未认证订阅号, 认证/未认证服务号

        :param str data: HTTP Request 的 Body 数据
        :raises: ParseError 解析微信服务器数据错误, 数据不合法

    .. py:method:: get_message()

        获取解析好的 :class:`WechatMessage` 对象

        运行时检查：是否已调用 :func:`parse_data` 进行解析

        可用公众号类型：认证/未认证订阅号, 认证/未认证服务号

        :return: 解析好的 WechatMessage 对象

    .. py:method:: get_access_token()

        获取 Access Token 及 Access Token 过期日期, 仅供缓存使用, 如果希望得到原生的 Access Token 请求数据请使用 :func:`grant_token`

        运行时检查：``appid``, ``appsecret``

        可用公众号类型：认证订阅号, 认证/未认证服务号

        :return: dict 对象, key 包括 ``access_token`` 及 ``access_token_expires_at``

    .. py:method:: get_jsapi_ticket()

        获取 Jsapi Ticket 及 Jsapi Ticket 过期日期, 仅供缓存使用, 如果希望得到原生的 Jsapi Ticket 请求数据请使用 :func:`grant_jsapi_ticket`

        运行时检查：``appid``, ``appsecret``

        可用公众号类型：认证/未认证订阅号, 认证/未认证服务号

        :return: dict 对象, key 包括 `jsapi_ticket` 及 `jsapi_ticket_expires_at`

    .. py:method:: response_text(content, escape=False)

        将文字信息 content 组装为符合微信服务器要求的响应数据

        运行时检查：是否已调用 :func:`parse_data` 进行解析

        可用公众号类型：认证/未认证订阅号, 认证/未认证服务号

        :param str content: 回复文字
        :param boolean escape: 是否转义该文本内容 (默认不转义)
        :return: 符合微信服务器要求的 XML 响应数据

    .. py:method:: response_image(media_id)

        将 media_id 所代表的图片组装为符合微信服务器要求的响应数据

        运行时检查：是否已调用 :func:`parse_data` 进行解析

        可用公众号类型：认证/未认证订阅号, 认证/未认证服务号

        :param str media_id: 图片的 MediaID
        :return: 符合微信服务器要求的 XML 响应数据

    .. py:method:: response_voice(media_id)

        将 media_id 所代表的语音组装为符合微信服务器要求的响应数据

        运行时检查：是否已调用 :func:`parse_data` 进行解析

        可用公众号类型：认证/未认证订阅号, 认证/未认证服务号

        :param str media_id: 语音的 MediaID
        :return: 符合微信服务器要求的 XML 响应数据

    .. py:method:: response_video(media_id [, title=None, description=None])

        将 media_id 所代表的视频组装为符合微信服务器要求的响应数据

        运行时检查：是否已调用 :func:`parse_data` 进行解析

        可用公众号类型：认证/未认证订阅号, 认证/未认证服务号

        :param str media_id: 视频的 MediaID
        :param str title: 视频消息的标题
        :param str description: 视频消息的描述
        :return: 符合微信服务器要求的 XML 响应数据

    .. py:method:: response_music(music_url [, title=None, description=None, hq_music_url=None, thumb_media_id=None])

        将音乐信息组装为符合微信服务器要求的响应数据

        运行时检查：是否已调用 :func:`parse_data` 进行解析

        可用公众号类型：认证/未认证订阅号, 认证/未认证服务号

        :param str music_url: 音乐链接
        :param str title: 音乐标题
        :param str description: 音乐描述
        :param str hq_music_url: 高质量音乐链接, WIFI环境优先使用该链接播放音乐
        :param str thumb_media_id: 缩略图的 MediaID
        :return: 符合微信服务器要求的 XML 响应数据

    .. py:method:: response_news(articles)

        将新闻信息组装为符合微信服务器要求的响应数据

        运行时检查：是否已调用 :func:`parse_data` 进行解析

        可用公众号类型：认证/未认证订阅号, 认证/未认证服务号

        :param list articles: list 对象, 每个元素为一个 dict 对象, key 包含 ``title``, ``description``, ``picurl``, ``url``
        :return: 符合微信服务器要求的 XML 响应数据

    .. py:method:: grant_token(override=True)

        获取 Access Token

        运行时检查：``appid``, ``appsecret``

        可用公众号类型：认证订阅号, 认证/未认证服务号

        详情请参考 `<http://mp.weixin.qq.com/wiki/11/0e4b294685f817b95cbed85ba5e82b8f.html>`_

        :param boolean override: 是否在获取的同时覆盖已有 access_token (默认为True)
        :return: 返回的 JSON 数据包

    .. py:method:: grant_jsapi_ticket(override=True)

        获取 Jsapi Ticket

        运行时检查：``appid``, ``appsecret``

        可用公众号类型：认证/未认证订阅号, 认证/未认证服务号

        详情请参考 http://mp.weixin.qq.com/wiki/7/aaa137b55fb2e0456bf8dd9148dd613f.html#.E9.99.84.E5.BD.951-JS-SDK.E4.BD.BF.E7.94.A8.E6.9D.83.E9.99.90.E7.AD.BE.E5.90.8D.E7.AE.97.E6.B3.95

        :param boolean override: 是否在获取的同时覆盖已有 jsapi_ticket (默认为True)
        :return: 返回的 JSON 数据包

    .. py:method:: create_menu(menu_data)

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

        详情请参考 `<http://mp.weixin.qq.com/wiki/13/43de8269be54a0a6f64413e4dfa94f39.html>`_

        请注意中文请使用 unicode 形式, 如上面的示例

        运行时检查：``appid``, ``appsecret``

        可用公众号类型：认证订阅号, 认证/未认证服务号

        :param dict menu_data: Python 字典
        :return: 返回的 JSON 数据包

    .. py:method:: get_menu()

        查询自定义菜单

        详情请参考 `<http://mp.weixin.qq.com/wiki/16/ff9b7b85220e1396ffa16794a9d95adc.html>`_

        运行时检查：``appid``, ``appsecret``

        可用公众号类型：认证订阅号, 认证/未认证服务号

        :return: 返回的 JSON 数据包

    .. py:method:: delete_menu()

        删除自定义菜单

        详情请参考 `<http://mp.weixin.qq.com/wiki/16/8ed41ba931e4845844ad6d1eeb8060c8.html>`_

        运行时检查：``appid``, ``appsecret``

        可用公众号类型：认证订阅号, 认证/未认证服务号

        :return: 返回的 JSON 数据包

    .. py:method:: upload_media(media_type, media_file, extension='')

        上传多媒体文件

        详情请参考 `<http://mp.weixin.qq.com/wiki/10/78b15308b053286e2a66b33f0f0f5fb6.html>`_

        运行时检查：``appid``, ``appsecret``

        可用公众号类型：认证服务号

        :param str media_type: 媒体文件类型，分别有图片（image）、语音（voice）、视频（video）和缩略图（thumb）
        :param object media_file: 要上传的文件，一个 File object 或 StringIO object
        :param str extension: 如果 media_file 传入的为 StringIO object，那么必须传入 extension 显示指明该媒体文件扩展名，如 ``mp3``, ``amr``；如果 media_file 传入的为 File object，那么该参数请留空
        :return: 返回的 JSON 数据包

    .. py:method:: download_media(media_id)

        下载多媒体文件

        如果希望将返回的多媒体文件以文件的形式进行保存，提供一个代码示例::

            wechat = WechatBasic(appid='appid', appsecret='appsecret')
            response = wechat.download_media('your media id')
            with open('yourfilename', 'wb') as fd:
                for chunk in response.iter_content(1024):
                    fd.write(chunk)

        详情请参考 `<http://mp.weixin.qq.com/wiki/10/78b15308b053286e2a66b33f0f0f5fb6.html>`_

        运行时检查：``appid``, ``appsecret``

        可用公众号类型：认证服务号

        :param str media_id: 媒体文件 ID
        :return: requests 的 Response 实例 (具体请参考 `<http://docs.python-requests.org/en/latest/>`_)

    .. py:method:: create_group(name)

        创建分组

        详情请参考 `<http://mp.weixin.qq.com/wiki/13/be5272dc4930300ba561d927aead2569.html>`_

        运行时检查：``appid``, ``appsecret``

        可用公众号类型：认证服务号

        :param str name: 分组名字（30个字符以内）
        :return: 返回的 JSON 数据包

    .. py:method:: get_groups()

        查询所有分组

        详情请参考 `<http://mp.weixin.qq.com/wiki/13/be5272dc4930300ba561d927aead2569.html>`_

        运行时检查：``appid``, ``appsecret``

        可用公众号类型：认证服务号

        :return: 返回的 JSON 数据包

    .. py:method:: get_group_by_id(openid)

        查询用户所在分组

        详情请参考 `<http://mp.weixin.qq.com/wiki/13/be5272dc4930300ba561d927aead2569.html>`_

        运行时检查：``appid``, ``appsecret``

        可用公众号类型：认证服务号

        :param str openid: 用户的OpenID
        :return: 返回的 JSON 数据包

    .. py:method:: update_group(group_id, name)

        修改分组名

        详情请参考 `<http://mp.weixin.qq.com/wiki/13/be5272dc4930300ba561d927aead2569.html>`_

        运行时检查：``appid``, ``appsecret``

        可用公众号类型：认证服务号

        :param integer group_id: 分组id，由微信分配
        :param str name: 分组名字（30个字符以内）
        :return: 返回的 JSON 数据包

    .. py:method:: move_user(user_id, group_id)

        移动用户分组

        详情请参考 `<http://mp.weixin.qq.com/wiki/13/be5272dc4930300ba561d927aead2569.html>`_

        运行时检查：``appid``, ``appsecret``

        可用公众号类型：认证服务号

        :param str user_id: 用户 ID, 就是你收到的 WechatMessage 的 source
        :param str group_id: 分组 ID
        :return: 返回的 JSON 数据包

    .. py:method:: get_user_info(user_id [, lang='zh_CN'])

        获取用户基本信息

        详情请参考 `<http://mp.weixin.qq.com/wiki/14/bb5031008f1494a59c6f71fa0f319c66.html>`_

        运行时检查：``appid``, ``appsecret``

        可用公众号类型：认证服务号

        :param str user_id: 用户 ID, 就是你收到的 WechatMessage 的 source
        :param str lang: 返回国家地区语言版本，zh_CN 简体，zh_TW 繁体，en 英语
        :return: 返回的 JSON 数据包

    .. py:method:: get_followers(first_user_id=None)

        获取关注者列表

        详情请参考 `<http://mp.weixin.qq.com/wiki/3/17e6919a39c1c53555185907acf70093.html>`_

        运行时检查：``appid``, ``appsecret``

        可用公众号类型：认证服务号

        :param str first_user_id: 可选。第一个拉取的OPENID，不填默认从头开始拉取
        :return: 返回的 JSON 数据包

    .. py:method:: send_text_message(user_id, content)

        发送文本消息

        详情请参考 `<http://mp.weixin.qq.com/wiki/7/12a5a320ae96fecdf0e15cb06123de9f.html>`_

        运行时检查：``appid``, ``appsecret``

        可用公众号类型：认证服务号

        :param str user_id: 用户 ID, 就是你收到的 WechatMessage 的 source
        :param str content: 消息正文
        :return: 返回的 JSON 数据包

    .. py:method:: send_image_message(user_id, media_id)

        发送图片消息

        详情请参考 `<http://mp.weixin.qq.com/wiki/7/12a5a320ae96fecdf0e15cb06123de9f.html>`_

        运行时检查：``appid``, ``appsecret``

        可用公众号类型：认证服务号

        :param str user_id: 用户 ID, 就是你收到的 WechatMessage 的 source
        :param str media_id: 图片的媒体ID。 可以通过 :func:`upload_media` 上传。
        :return: 返回的 JSON 数据包

    .. py:method:: send_voice_message(user_id, media_id)

        发送语音消息

        详情请参考 `<http://mp.weixin.qq.com/wiki/7/12a5a320ae96fecdf0e15cb06123de9f.html>`_

        运行时检查：``appid``, ``appsecret``

        可用公众号类型：认证服务号

        :param str user_id: 用户 ID, 就是你收到的 WechatMessage 的 source
        :param str media_id: 发送的语音的媒体ID。 可以通过 :func:`upload_media` 上传。
        :return: 返回的 JSON 数据包

    .. py:method:: send_video_message(user_id, media_id [, title=None, description=None)

        发送视频消息

        详情请参考 `<http://mp.weixin.qq.com/wiki/7/12a5a320ae96fecdf0e15cb06123de9f.html>`_

        运行时检查：``appid``, ``appsecret``

        可用公众号类型：认证服务号

        :param str user_id: 用户 ID, 就是你收到的 WechatMessage 的 source
        :param str media_id: 发送的视频的媒体ID。 可以通过 :func:`upload_media` 上传。
        :param str title: 视频消息的标题
        :param str description: 视频消息的描述
        :return: 返回的 JSON 数据包

    .. py:method:: send_music_message(user_id, url, hq_url, thumb_media_id [, title=None, description=None])

        发送音乐消息

        详情请参考 `<http://mp.weixin.qq.com/wiki/7/12a5a320ae96fecdf0e15cb06123de9f.html>`_

        运行时检查：``appid``, ``appsecret``

        可用公众号类型：认证服务号

        :param str user_id: 用户 ID, 就是你收到的 WechatMessage 的 source
        :param str url: 音乐链接
        :param str hq_url: 高品质音乐链接，wifi环境优先使用该链接播放音乐
        :param str thumb_media_id: 缩略图的媒体ID。 可以通过 :func:`upload_media` 上传。
        :param str title: 音乐标题
        :param str description: 音乐描述
        :return: 返回的 JSON 数据包

    .. py:method:: send_article_message(user_id, articles)

        发送图文消息

        详情请参考 `<http://mp.weixin.qq.com/wiki/7/12a5a320ae96fecdf0e15cb06123de9f.html>`_

        运行时检查：``appid``, ``appsecret``

        可用公众号类型：认证服务号

        :param str user_id: 用户 ID, 就是你收到的 WechatMessage 的 source
        :param list articles: list 对象, 每个元素为一个 dict 对象, key 包含 ``title``, ``description``, ``picurl``, ``url``
        :return: 返回的 JSON 数据包

    .. py:method:: create_qrcode(**data)

        创建二维码

        详情请参考 `<http://mp.weixin.qq.com/wiki/18/28fc21e7ed87bec960651f0ce873ef8a.html>`_

        运行时检查：``appid``, ``appsecret``

        可用公众号类型：认证服务号

        :param dict data: 你要发送的参数 dict
        :return: 返回的 JSON 数据包

    .. py:method:: show_qrcode(ticket)

        通过ticket换取二维码

        详情请参考 `<http://mp.weixin.qq.com/wiki/18/28fc21e7ed87bec960651f0ce873ef8a.html>`_

        运行时检查：``appid``, ``appsecret``

        可用公众号类型：认证服务号

        :param str ticket: 二维码 ticket 。可以通过 :func:`create_qrcode` 获取到
        :return: 返回的 Request 对象

    .. py:method:: set_template_industry(industry_id1, industry_id2)

        设置所属行业

        详情请参考 http://mp.weixin.qq.com/wiki/17/304c1885ea66dbedf7dc170d84999a9d.html

        运行时检查：``appid``, ``appsecret``

        可用公众号类型：认证服务号

        :param str industry_id1: 主营行业代码
        :param str industry_id2: 副营行业代码
        :return: 返回的 JSON 数据包

    .. py:method:: get_template_id(template_id_short):

        获得模板ID

        详情请参考 http://mp.weixin.qq.com/wiki/17/304c1885ea66dbedf7dc170d84999a9d.html

        运行时检查：``appid``, ``appsecret``

        可用公众号类型：认证服务号

        :param str template_id_short: 模板库中模板的编号，有“TM**”和“OPENTMTM**”等形式
        :return: 返回的 JSON 数据包

    .. py:method:: send_template_message(user_id, template_id, data, url='', topcolor='#FF0000')

        发送模版消息

        详情请参考 http://mp.weixin.qq.com/wiki/17/304c1885ea66dbedf7dc170d84999a9d.html

        运行时检查：``appid``, ``appsecret``

        可用公众号类型：认证服务号

        注意参数中的 data 示例如下(请提供dict形式而不是字符串形式)：::

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

        :param str user_id: 用户 ID, 就是你收到的 WechatMessage 的 source (OpenID)
        :param str template_id: 模板ID
        :param dict data: 模板消息数据，示例如上
        :param str url: 跳转地址 (默认为空)
        :param str topcolor: 顶部颜色RGB值 (默认 ``#FF0000`` )
        :return: 返回的 JSON 数据包
