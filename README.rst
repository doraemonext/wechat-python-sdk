微信公众平台 Python 开发包
===========================

**当前代码还未完成全部功能，非官方接口功能尚不能使用，请耐心等待代码及文档的完善。**

非官方微信公众平台 Python 开发包，包括官方接口和非官方接口。

* 官方接口依据公众平台开发者文档编写，可以实现公众平台开发者文档中的所有内容；

* 非官方接口采用模拟登陆的方式，可以实现更多高级功能，但也存在相应风险。尤其注意，本开发包不提供群发功能，此功能被微信公众平台明令禁止。

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
                response = wechat.response_text('^_^')
            else:
                response = wechat.response_text('文字')
        elif message.type == 'image':
            response = wechat.response_text('图片')
        else:
            response = wechat.response_text('未知')
    
        # 现在直接将 response 变量内容直接作为 HTTP Response 响应微信服务器即可，此处为了演示返回内容，直接将响应进行输出
        print response