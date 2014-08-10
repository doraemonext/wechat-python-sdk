# 微信公众平台 Python 开发包

**当前进度正在开发中，请勿在生产环境使用。**

非官方微信公众平台 Python 开发包，包括官方接口和非官方接口。

* 官方接口依据公众平台开发者文档编写，可以实现公众平台开发者文档中的所有内容；

* 非官方接口采用模拟登陆的方式，可以实现更多高级功能，但也存在相应风险。尤其注意，本开发包不提供群发功能，此功能被微信公众平台明令禁止。

## 文档

[http://wechat-python-sdk.readthedocs.org/](http://wechat-python-sdk.readthedocs.org/)

## 快速开始

### 安装

    pip install wechat-sdk
    
### 官方接口调用示例

    # -*- coding: utf-8 -*-
    
    from wechat_sdk import WechatBasic
    
    
    # 初始化
    wechat = WechatBasic(token='WECHAT_TOKEN',             # 微信 Token
                         appid='wechat_app_id',            # App ID (可选)
                         appsecret='wechat_app_secret',    # App Secret (可选)
                         partnerid='wechat_partner_id',    # 财付通商户身份标识, 支付权限专用 (可选)
                         partnerkey='wechat_partner_key',  # 财付通商户权限密钥 Key, 支付权限专用 (可选)
                         paysignkey='wechat_paysign_key')  # 商户签名密钥 Key, 支付权限专用 (可选)
    
    # 对签名进行校验                     
    if wechat.check_signature(signature='114f72fa8893172d9d68970c2b7621bb84acda84',
                              timestamp='1406799649',
                              nonce='1000166642'):
        # 解析微信服务器的请求数据                      
        wechat.parse_data("""
        <xml>
        <ToUserName><![CDATA[gh_6091f3b083e7]]></ToUserName>
        <FromUserName><![CDATA[oPGltuJSbiK6HkOSOGyVSCy0hRoU]]></FromUserName>
        <CreateTime>1405994594</CreateTime>
        <MsgType><![CDATA[text]]></MsgType>
        <Content><![CDATA[文字信息]]></Content>
        <MsgId>6038700799783131746</MsgId>
        </xml>
        """)

		# 得到可以响应微信服务器的文字回复信息的 XML
        response_text = wechat.response_text('测试回复文字信息')
        # 得到可以响应微信服务器的音乐回复信息的 XML
        response_music = wechat.response_music(music_url='music_url',
                                               title='music_title',             # (可选)
                                               description='music_description', # (可选)
                                               hq_music_url='hq_music_url')     # (可选)

        # 接下来便可以将response_text或response_music直接作为HTTP Response响应微信服务器
        # print response_text
        # print response_music