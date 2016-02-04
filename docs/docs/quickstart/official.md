# 快速上手 - 官方接口

本页内容提供了一些可以快速上手的短小示例代码，并假设你已经安装了 wechat-python-sdk 。如果还没有，请返回 [安装](/#_2) 一节遵循提示进行安装。

在开始之前，请准备好你的：

* Token（可选）
* App ID / App Secret (可选)
* EncodingAESKey (可选)

你没有看错，他们都是可选项，但如果你什么都不提供，那执行方法的时候就会抛出一堆无法执行操作的异常了 :)

## 实例化 WechatConf 微信配置类

这里给出一个简单的 `WechatConf` 实例化代码：

```python
from wechat_sdk import WechatConf
conf = WechatConf(
    token='your_token', 
    appid='your_appid', 
    appsecret='your_appsecret', 
    encrypt_mode='safe',  # 可选项：normal/compatible/safe，分别对应于 明文/兼容/安全 模式
    encoding_aes_key='your_encoding_aes_key'  # 如果传入此值则必须保证同时传入 token, appid
)
```

上面所有的参数都是可选的，请按需传入即可。

**下面的所有代码会始终假设变量 `conf` 已经通过上述方式实例化完毕，将会直接使用而不再进行详细说明。**

## 实例化 WechatBasic 官方接口类

`WechatBasic` 的实例化只需要将已经实例化好的 `conf` 传入即可，如下：

```python
from wechat_sdk import WechatBasic
wechat = WechatBasic(conf=conf)
```

接下来，你就可以使用 `wechat` 变量来完成你所需要的所有功能。

**下面的所有代码会始终假设变量 `wechat` 已经通过上述方式实例化完毕，将会直接使用而不再进行详细说明。**

## 验证服务器请求有效性

首先假设你已经自行从微信服务器发送的 Request 中提取出了 `signature`, `timestamp`, `nonce` 参数，下面将直接使用这三个变量：

```python
if wechat.check_signature(signature, timestamp, nonce):
    print 'Accept'
else:
    print 'Wrong'
```

Tips: 该方法在执行前会检查 `conf` 中是否传入了 `token` 参数，如果没有传入则抛出 `NeedParamError` 异常（该异常继承自 `WechatSDKException`）。

## 解析接收到的 XML 消息

首先假设你已经自行从微信服务器发送的 Request 中提取出了 `body_text`（也就是 Request 中的 body），下面将直接使用该变量：

```python
from wechat_sdk.exceptions import ParseError
try:
    wechat.parse_data(body_text)
except ParseError:
    print 'Invalid Body Text'
```

这里的 `ParseError` 异常继承自 `WechatSDKException`，当解析数据出错时被抛出。

如果解析成功，将不会有任何返回信息，也不会有异常抛出。

## 获取解析后的信息

当解析成功后，你可以直接获取解析后的具体信息：

### 公共信息获取

```python
id = wechat.message.id          # 对应于 XML 中的 MsgId
target = wechat.message.target  # 对应于 XML 中的 ToUserName
source = wechat.message.source  # 对应于 XML 中的 FromUserName
time = wechat.message.time      # 对应于 XML 中的 CreateTime
type = wechat.message.type      # 对应于 XML 中的 MsgType
raw = wechat.message.raw        # 原始 XML 文本，方便进行其他分析
```

### 私有信息获取

当 `isinstance(wechat.message, TextMessage)` 时，有：

```python
content = wechat.message.content                   # 对应于 XML 中的 Content
```

当 `isinstance(wechat.message, ImageMessage)` 时，有：

```python
picurl = wechat.message.picurl                     # 对应于 XML 中的 PicUrl
media_id = wechat.message.media_id                 # 对应于 XML 中的 MediaId
```

当 `isinstance(wechat.message, VoiceMessage)` 时，有：

```python
media_id = wechat.message.media_id                 # 对应于 XML 中的 MediaId
format = wechat.message.format                     # 对应于 XML 中的 Format
recognition = wechat.message.recognition           # 对应于 XML 中的 Recognition
```

当 `isintance(wechat.message, VideoMessage)` 或 `isinstance(wechat.message, ShortVideoMessage)` 时，有：

```python
media_id = wechat.message.media_id                 # 对应于 XML 中的 MediaId
thumb_media_id = wechat.message.thumb_media_id     # 对应于 XML 中的 ThumbMediaId
```

当 `isinstance(wechat.message, LocationMessage)` 时，有：

```python
location = wechat.message.location                 # Tuple(X, Y)，对应于 XML 中的 (Location_X, Location_Y)
scale = wechat.message.scale                       # 对应于 XML 中的 Scale
label = wechat.message.label                       # 对应于 XML 中的 Label
```

当 `isinstance(wechat.message, LinkMessage)` 时，有：

```python
title = wechat.message.title                       # 对应于 XML 中的 Title
description = wechat.message.description           # 对应于 XML 中的 Description
url = wechat.message.url                           # 对应于 XML 中的 Url
```

当 `isinstance(wechat.message, EventMessage)` 时，有：

```python
if wechat.message.type == 'subscribe':  # 关注事件(包括普通关注事件和扫描二维码造成的关注事件)
    key = wechat.message.key                        # 对应于 XML 中的 EventKey (普通关注事件时此值为 None)
    ticket = wechat.message.ticket                  # 对应于 XML 中的 Ticket (普通关注事件时此值为 None)
elif wechat.message.type == 'unsubscribe':  # 取消关注事件（无可用私有信息）
    pass
elif wechat.message.type == 'scan':  # 用户已关注时的二维码扫描事件
    key = wechat.message.key                        # 对应于 XML 中的 EventKey
    ticket = wechat.message.ticket                  # 对应于 XML 中的 Ticket
elif wechat.message.type == 'location':  # 上报地理位置事件
    latitude = wechat.message.latitude              # 对应于 XML 中的 Latitude
    longitude = wechat.message.longitude            # 对应于 XML 中的 Longitude
    precision = wechat.message.precision            # 对应于 XML 中的 Precision
elif wechat.message.type == 'click':  # 自定义菜单点击事件
    key = wechat.message.key                        # 对应于 XML 中的 EventKey
elif wechat.message.type == 'view':  # 自定义菜单跳转链接事件
    key = wechat.message.key                        # 对应于 XML 中的 EventKey
elif wechat.message.type == 'templatesendjobfinish':  # 模板消息事件
    status = wechat.message.status                  # 对应于 XML 中的 Status
elif wechat.message.type in ['scancode_push', 'scancode_waitmsg', 'pic_sysphoto', 
                             'pic_photo_or_album', 'pic_weixin', 'location_select']:  # 其他事件
    key = wechat.message.key                        # 对应于 XML 中的 EventKey
```

## 回复消息

**回复消息要求必须已经成功调用过 `.parse_data()` 方法。**

另外以下 `response_` 系列函数仅返回处理好的 XML 字符串，你还需要将它通过你自己的框架封装为 HTTP Response 返回微信服务器。

### 回复文本消息

```python
xml = wechat.response_text(content='文本回复')
```

如果需要转义文本，可以传入参数 `escape=True`：

```python
xml = wechat.response_text(content='文本回复', escape=True)
```

### 回复图片消息

```python
xml = wechat.response_image(media_id='media_id')
```

### 回复语音消息

```python
xml = wechat.response_voice(media_id='media_id')
```

### 回复视频消息

```python
xml = wechat.response_video(media_id='media_id', title='video_title', description='video_description')
```

以上参数中 `title` 和 `description` 均为可选项。

### 回复音乐消息

```python
xml = wechat.response_music(
    music_url='your_music_url',
    title='music_title',
    description='music_description',
    hq_music_url='your_hq_music_url',
    thumb_media_id='your_thumb_media_id',
)
```

以上参数中 `title`、`description`、`hq_music_url`、`thumb_media_id` 均为可选项。

### 回复图文消息

```python
xml = wechat.response_news([
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
```

## 总结

通过上面的文档你应该已经掌握了如何使用 wechat-python-sdk 进行基本的：

* **验证服务器请求有效性**
* **解析接收到的 XML 消息**
* **获取解析后的信息**
* **回复消息** 

等操作，通过它们，你可以快速搭建一个最简单的服务来应对微信服务器的请求。

## 下一步

接下来请阅读 [**快速上手 - WechatConf 详解**](/quickstart/wechatconf) 来了解如何使用 WechatConf 维护配置信息，可以说，它将是官方接口使用过程中最重要的一环。


