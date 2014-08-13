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