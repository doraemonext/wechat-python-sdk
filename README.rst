微信公众平台 Python 开发包
===========================

非官方微信公众平台 Python 开发包，包括官方接口和非官方接口。

* 官方接口依据公众平台开发者文档编写，可以实现公众平台开发者文档中的所有内容，具体不列举，请查看 ``WechatBasic`` 文档；

* 非官方接口采用模拟登陆的方式，可以实现更多高级功能，但也存在相应风险。尤其注意，本开发包不提供群发功能，此功能被微信公众平台明令禁止。

  目前提供的非官方接口功能有：

  * 主动对指定用户发送文本消息
  * 主动对指定用户发送图片消息
  * 主动对指定用户发送语音消息
  * 主动对指定用户发送视频消息
  * 获取指定用户的个人信息
  * 获取用户列表
  * 获取分组列表
  * 获取图文信息列表
  * 获取与指定用户的对话内容
  * 向指定用户发送图文消息(必须从图文库里选取消息ID传入)
  * 上传素材至素材库 (图片/语音/视频)
  * 向特定用户发送媒体文件 (图片/语音/视频)
  * 获取素材库文件列表
  * 获取用户头像
  * 获取新消息的数目
  * 获取最新一条消息
  * 获取消息列表
  * 根据消息ID获取图片消息内容
  * 根据消息ID获取语音消息内容
  * 根据消息ID获取视频消息内容

**请注意：本开发包并不打算提供一个独立的完整微信解决方案，我们更希望这个开发包可以非常融洽的在各个框架中进行集成并使用，对于HTTP请求及响应方面并不涉及，该开发包仅仅接受必要参数，提供各种微信操作的方法，并返回相应的可以响应微信服务器的数据(Response)或操作执行结果。**

文档
----------------------------

`http://wechat-python-sdk.readthedocs.org/ <http://wechat-python-sdk.readthedocs.org/>`_

快速开始
----------------------------

安装
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

    pip install wechat-sdk
    
官方接口调用示例
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**关于字符串中的中文问题，请保证所有在代码中出现的包含汉字的字符串均为 unicode 类型，微信服务器发送过来的 Request Body 不受此限制，请注意下面的代码中关于字符串类型的地方。**

第一个例子(examples/tutorial_official_1.py)，根据用户发送的内容返回用户发送内容的类型文字说明，比如用户发送了一张图片，则返回“图片”，发送了一段文字，则返回“文字”。

这里附加一个操作，当用户发送的是文字并且内容为“wechat”时返回“^_^”笑脸符号。

::

    # -*- coding: utf-8 -*-

    from wechat_sdk import WechatBasic


    # 下面这些变量均假设已由 Request 中提取完毕
    token = 'WECHAT_TOKEN'  # 你的微信 Token
    signature = 'f24649c76c3f3d81b23c033da95a7a30cb7629cc'  # Request 中 GET 参数 signature
    timestamp = '1406799650'  # Request 中 GET 参数 timestamp
    nonce = '1505845280'  # Request 中 GET 参数 nonce
    # 用户的请求内容 (Request 中的 Body)
    # 请更改 body_text 的内容来测试下面代码的执行情况
    body_text = """
    <xml>
    <ToUserName><![CDATA[touser]]></ToUserName>
    <FromUserName><![CDATA[fromuser]]></FromUserName>
    <CreateTime>1405994593</CreateTime>
    <MsgType><![CDATA[text]]></MsgType>
    <Content><![CDATA[wechat]]></Content>
    <MsgId>6038700799783131222</MsgId>
    </xml>
    """

    # 实例化 wechat
    wechat = WechatBasic(token=token)
    # 对签名进行校验
    if wechat.check_signature(signature=signature, timestamp=timestamp, nonce=nonce):
        # 对 XML 数据进行解析 (必要, 否则不可执行 response_text, response_image 等操作)
        wechat.parse_data(body_text)
        # 获得解析结果, message 为 WechatMessage 对象 (wechat_sdk.messages中定义)
        message = wechat.get_message()

        response = None
        if message.type == 'text':
            if message.content == 'wechat':
                response = wechat.response_text(u'^_^')
            else:
                response = wechat.response_text(u'文字')
        elif message.type == 'image':
            response = wechat.response_text(u'图片')
        else:
            response = wechat.response_text(u'未知')

        # 现在直接将 response 变量内容直接作为 HTTP Response 响应微信服务器即可，此处为了演示返回内容，直接将响应进行输出
        print response

第二个例子(examples/tutorial_official_2.py)，假如用户输入“新闻”，则服务器响应一段预设的多图文

::

    # -*- coding: utf-8 -*-

    from wechat_sdk import WechatBasic


    # 下面这些变量均假设已由 Request 中提取完毕
    token = 'WECHAT_TOKEN'  # 你的微信 Token
    signature = 'f24649c76c3f3d81b23c033da95a7a30cb7629cc'  # Request 中 GET 参数 signature
    timestamp = '1406799650'  # Request 中 GET 参数 timestamp
    nonce = '1505845280'  # Request 中 GET 参数 nonce
    # 用户的请求内容 (Request 中的 Body)
    # 请更改 body_text 的内容来测试下面代码的执行情况
    body_text = """
    <xml>
    <ToUserName><![CDATA[touser]]></ToUserName>
    <FromUserName><![CDATA[fromuser]]></FromUserName>
    <CreateTime>1405994593</CreateTime>
    <MsgType><![CDATA[text]]></MsgType>
    <Content><![CDATA[新闻]]></Content>
    <MsgId>6038700799783131222</MsgId>
    </xml>
    """

    # 实例化 wechat
    wechat = WechatBasic(token=token)
    # 对签名进行校验
    if wechat.check_signature(signature=signature, timestamp=timestamp, nonce=nonce):
        # 对 XML 数据进行解析 (必要, 否则不可执行 response_text, response_image 等操作)
        wechat.parse_data(body_text)
        # 获得解析结果, message 为 WechatMessage 对象 (wechat_sdk.messages中定义)
        message = wechat.get_message()

        response = None
        if message.type == 'text' and message.content == u'新闻':
            response = wechat.response_news([
                {
                    'title': u'第一条新闻标题',
                    'description': u'第一条新闻描述，这条新闻没有预览图',
                    'url': u'http://www.google.com.hk/',
                }, {
                    'title': u'第二条新闻标题, 这条新闻无描述',
                    'picurl': u'http://doraemonext.oss-cn-hangzhou.aliyuncs.com/test/wechat-test.jpg',
                    'url': u'http://www.github.com/',
                }, {
                    'title': u'第三条新闻标题',
                    'description': u'第三条新闻描述',
                    'picurl': u'http://doraemonext.oss-cn-hangzhou.aliyuncs.com/test/wechat-test.jpg',
                    'url': u'http://www.v2ex.com/',
                }
            ])

        # 现在直接将 response 变量内容直接作为 HTTP Response 响应微信服务器即可，此处为了演示返回内容，直接将响应进行输出
        print response


非官方接口调用示例
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

第一个例子(examples/tutorial_unofficial_1.py)，展示了几个直接获取信息的函数的用法，至于具体的返回值所包含的内容，请查看 ``WechatExt`` 文档

::

    # -*- coding: utf-8

    import json

    from wechat_sdk import WechatExt


    wechat = WechatExt(username='username', password='password')

    # 获取未分组中所有的用户成员
    user_list = wechat.get_user_list()
    print user_list
    print '==================================='

    # 获取分组列表
    group_list = wechat.get_group_list()
    print group_list
    print '==================================='

    # 获取图文信息列表
    news_list = wechat.get_news_list(page=0, pagesize=15)
    print news_list
    print '==================================='

    # 获取与最新一条消息用户的对话内容
    user_info_json = wechat.get_top_message()
    user_info = json.loads(user_info_json)
    print wechat.get_dialog_message(fakeid=user_info['msg_item'][0]['fakeid'])
