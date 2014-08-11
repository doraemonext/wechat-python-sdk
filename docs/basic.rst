微信官方接口操作
==========================

.. py:class:: WechatBasic(token=None, appid=None, appsecret=None, partnerid=None, partnerkey=None, paysignkey=None, access_token=None, access_token_expires_at=None)

    微信基本功能类

    :param str token: 微信 Token
    :param str appid: App ID
    :param str appsecret: App Secret
    :param str partnerid: 财付通商户身份标识, 支付权限专用
    :param str partnerkey: 财付通商户权限密钥 Key, 支付权限专用
    :param str paysignkey: 商户签名密钥 Key, 支付权限专用
    :param str access_token: 直接导入的 ``access_token`` 值, 该值需要在上一次该类实例化之后手动进行缓存并在此处传入, 如果不传入, 将会在需要时自动重新获取
    :param str access_token_expires_at: 直接导入的 ``access_token`` 的过期日期，该值需要在上一次该类实例化之后手动进行缓存并在此处传入, 如果不传入, 将会在需要时自动重新获取

    **实例化说明：**

    1. 当实例化 WechatBasic 时，你可以传递上述参数说明中任意多个参数进去，但是传递参数不足将会在使用部分功能时引发对应的异常，下面列举使用场景和应该传递哪些参数：

     - **订阅号(未认证)** ：仅传入 ``token`` 参数

     - **其他(认证订阅号, 未认证服务号, 认证服务号)** ：传入 ``token``, ``appid``, ``appsecret``, ``access_token``, ``access_token_expires_at`` 参数，如果已经开通支付权限，请传入 ``partnerid``, ``partnerkey``, ``paysignkey`` 参数

     **虽然认证订阅号、未认证服务号拥有 appid 及 appsecret，但不代表其能调用高级接口** ，这两种类型的账号仅能进行自定义菜单操作，进行其他权限外操作仍然会抛出异常 ``OfficialAPIError``

    2. **详细说明一下 access_token 及 access_token_expires_at 参数的传入问题：**

     因为此开发包并不打算以服务器的方式常驻，所以，每次请求均会重新实例化 ``WechatBasic`` ，而微信的 ``access_token`` 有效期为 7200 秒，不可能每次实例化的时候去重新获取，所以需要你以你自己的方式去保存上一次请求中实例化后的 ``WechatBasic`` 中 ``access_token`` 及 ``access_token_expires_at`` 参数，并在下一次的实例化的过程中传入，以此来保证 ``access_token`` 的持久性。

     获取 ``access_token`` 及 ``access_token_expires_at`` 的方式为调用 :func:`get_access_token` 方法

     下一版本将会考虑更为简单通用的方法，在新版本发布之前，请用你自己的方式把得到的 ``access_token`` 及 ``access_token_expires_at`` 保存起来，不管是文件，缓存还是数据库都可以，获取 ``access_token`` 和 ``access_token_expires_at`` 的时间可以非常自由，不管是刚刚实例化完成还是得到响应结果之后都没有问题，在调用 :func:`get_access_token` 时如果没有 ``access_token`` 会自动获取的 :)

    .. py:method:: check_signature(signature, timestamp, nonce)

        验证微信消息真实性

        :param str signature: 微信加密签名
        :param str timestamp: 时间戳
        :param str nonce: 随机数
        :return: 通过验证返回 ``True``, 未通过验证返回 ``False``

    .. py:method:: parse_data(data)

        解析微信服务器发送过来的数据并保存类中

        :param str data: HTTP Request 的 Body 数据
        :raises: ParseError 解析微信服务器数据错误, 数据不合法

    .. py:method:: get_message()

        获取解析好的 WechatMessage 对象

        :return: 解析好的 WechatMessage 对象

    .. py:method:: get_access_token()

        获取 Access Token 及 Access Token 过期日期

        :return: dict 对象, key 包括 ``access_token`` 及 ``access_token_expires_at``

    .. py:method:: response_text(content)

        将文字信息 content 组装为符合微信服务器要求的响应数据

        :param str content: 回复文字
        :return: 符合微信服务器要求的 XML 响应数据

    .. py:method:: response_image(media_id)

        将 media_id 所代表的图片组装为符合微信服务器要求的响应数据

        :param str media_id: 图片的 MediaID
        :return: 符合微信服务器要求的 XML 响应数据

    .. py:method:: response_voice(media_id)

        将 media_id 所代表的语音组装为符合微信服务器要求的响应数据

        :param str media_id: 语音的 MediaID
        :return: 符合微信服务器要求的 XML 响应数据

    .. py:method:: response_video(media_id [, title=None, description=None])

        将 media_id 所代表的视频组装为符合微信服务器要求的响应数据

        :param str media_id: 视频的 MediaID
        :param str title: 视频消息的标题
        :param str description: 视频消息的描述
        :return: 符合微信服务器要求的 XML 响应数据

    .. py:method:: response_music(music_url [, title=None, description=None, hq_music_url=None, thumb_media_id=None])

        将音乐信息组装为符合微信服务器要求的响应数据

        :param str music_url: 音乐链接
        :param str title: 音乐标题
        :param str description: 音乐描述
        :param str hq_music_url: 高质量音乐链接, WIFI环境优先使用该链接播放音乐
        :param str thumb_media_id: 缩略图的 MediaID
        :return: 符合微信服务器要求的 XML 响应数据

    .. py:method:: response_news(articles)

        将新闻信息组装为符合微信服务器要求的响应数据

        :param list articles: list 对象, 每个元素为一个 dict 对象, key 包含 ``title``, ``description``, ``picurl``, ``url``
        :return: 符合微信服务器要求的 XML 响应数据

    未完待续……请耐心等待……