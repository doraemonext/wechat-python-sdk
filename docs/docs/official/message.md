# 官方接口 - 消息管理

## 解析接收到的 XML 消息

**调用方法：**`.parse_data(data, msg_signature=None, timestamp=None, nonce=None)`

**参数说明：**

* `data`: 需要解析的 XML 字符串数据
* `msg_signature`: 消息解密专用 - 签名
* `timestamp`: 消息解密专用 - 时间戳
* `nonce`: 消息解密专用 - 随机数

**调用前检查：**Token

**返回值：**`None`

**异常：**当解析 XML 失败时抛出 [`exceptions.ParseError`](/api/exception.md#parseerror) 异常。

**说明：**如果在实例化 WechatConf 时传入了 `encrypt_mode='safe'`，那么在调用本方法进行解析消息时必须传入 `msg_signature` / `timestamp` / `nonce` 三个参数，否则会无法解密消息。

如果 `encrypt_mode='normal'` 或 `encrypt_mode='compatible'`，则无需传入后面三个参数。

**对应官方文档：**[接收普通消息](http://mp.weixin.qq.com/wiki/17/f298879f8fb29ab98b2f2971d42552fd.html) / [接收事件推送](http://mp.weixin.qq.com/wiki/7/9f89d962eba4c5924ed95b513ba69d9b.html)

## 获取解析后的信息 

当调用 [`.parse_data()`](#xml) 方法解析成功后，你可以直接获取解析后的具体信息：

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

## 被动回复消息 - 文本消息

将文字信息组装为符合微信服务器要求的响应数据

**调用方法：**`.response_text(content, escape=False)`

**参数说明：**

* `content`: 回复文字
* `escape`: 是否转义该文本内容 (默认不转义)

**调用前检查：**必须已经成功调用过 [`.parse_data()`](#xml) 方法。

**返回值：**组装好的 XML 字符串，可直接回复微信服务器。

**说明：**该方法会根据 WechatConf 实例化时的 `encrypt_mode` 参数自动组装普通消息或加密消息，无需干预。

**对应官方文档：**[回复文本消息](http://mp.weixin.qq.com/wiki/1/6239b44c206cab9145b1d52c67e6c551.html#.E5.9B.9E.E5.A4.8D.E6.96.87.E6.9C.AC.E6.B6.88.E6.81.AF)

## 被动回复消息 - 图片消息

将 media_id 所代表的图片组装为符合微信服务器要求的响应数据

**调用方法：**`.response_image(media_id)`

**参数说明：**

* `media_id`: 图片的 Media ID

**调用前检查：**必须已经成功调用过 [`.parse_data()`](#xml) 方法。

**返回值：**组装好的 XML 字符串，可直接回复微信服务器。

**说明：**该方法会根据 WechatConf 实例化时的 `encrypt_mode` 参数自动组装普通消息或加密消息，无需干预。

**对应官方文档：**[回复图片消息](http://mp.weixin.qq.com/wiki/1/6239b44c206cab9145b1d52c67e6c551.html#.E5.9B.9E.E5.A4.8D.E5.9B.BE.E7.89.87.E6.B6.88.E6.81.AF)

## 被动回复消息 - 语音消息

将 media_id 所代表的语音组装为符合微信服务器要求的响应数据

**调用方法：**`.response_voice(media_id)`

**参数说明：**

* `media_id`: 语音的 Media ID

**调用前检查：**必须已经成功调用过 [`.parse_data()`](#xml) 方法。

**返回值：**组装好的 XML 字符串，可直接回复微信服务器。

**说明：**该方法会根据 WechatConf 实例化时的 `encrypt_mode` 参数自动组装普通消息或加密消息，无需干预。

**对应官方文档：**[回复语音消息](http://mp.weixin.qq.com/wiki/1/6239b44c206cab9145b1d52c67e6c551.html#.E5.9B.9E.E5.A4.8D.E8.AF.AD.E9.9F.B3.E6.B6.88.E6.81.AF)

## 被动回复消息 - 视频消息

将 media_id 所代表的视频组装为符合微信服务器要求的响应数据

**调用方法：**`.response_video(media_id, title=None, description=None)`

**参数说明：**

* `media_id`: 视频的 Media ID
* `title`: 视频消息的标题
* `description`: 视频消息的描述

**调用前检查：**必须已经成功调用过 [`.parse_data()`](#xml) 方法。

**返回值：**组装好的 XML 字符串，可直接回复微信服务器。

**说明：**该方法会根据 WechatConf 实例化时的 `encrypt_mode` 参数自动组装普通消息或加密消息，无需干预。

**对应官方文档：**[回复视频消息](http://mp.weixin.qq.com/wiki/1/6239b44c206cab9145b1d52c67e6c551.html#.E5.9B.9E.E5.A4.8D.E8.A7.86.E9.A2.91.E6.B6.88.E6.81.AF)

## 被动回复消息 - 音乐消息

将音乐信息组装为符合微信服务器要求的响应数据

**调用方法：**`.response_music(music_url, title=None, description=None, hq_music_url=None, thumb_media_id=None)`

**参数说明：**

* `music_url`: 音乐链接
* `title`: 音乐标题
* `description`: 音乐描述
* `hq_music_url`: 高质量音乐链接, WIFI环境优先使用该链接播放音乐
* `thumb_media_id`: 缩略图的 MediaID

**调用前检查：**必须已经成功调用过 [`.parse_data()`](#xml) 方法。

**返回值：**组装好的 XML 字符串，可直接回复微信服务器。

**说明：**该方法会根据 WechatConf 实例化时的 `encrypt_mode` 参数自动组装普通消息或加密消息，无需干预。

**对应官方文档：**[回复音乐消息](http://mp.weixin.qq.com/wiki/1/6239b44c206cab9145b1d52c67e6c551.html#.E5.9B.9E.E5.A4.8D.E9.9F.B3.E4.B9.90.E6.B6.88.E6.81.AF)

## 被动回复消息 - 图文消息

将图文信息组装为符合微信服务器要求的响应数据

**调用方法：**`.response_news(articles)`

**参数说明：**

* `articles`: list 对象, 每个元素为一个 dict 对象, key 包含 `title`, `description`, `picurl`, `url`，示例如下：

        [{
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
        }]

**调用前检查：**必须已经成功调用过 [`.parse_data()`](#xml) 方法。

**返回值：**组装好的 XML 字符串，可直接回复微信服务器。

**说明：**该方法会根据 WechatConf 实例化时的 `encrypt_mode` 参数自动组装普通消息或加密消息，无需干预。

**对应官方文档：**[回复图文消息](http://mp.weixin.qq.com/wiki/1/6239b44c206cab9145b1d52c67e6c551.html#.E5.9B.9E.E5.A4.8D.E5.9B.BE.E6.96.87.E6.B6.88.E6.81.AF)

## 被动回复消息 - 空消息

假如服务器无法保证在五秒内处理并回复，必须调用该接口，这样微信服务器才不会对此作任何处理，并且不会发起重试（这种情况下，可以使用客服消息接口进行异步回复），否则，将出现严重的错误提示。

**调用方法：**`.response_none()`

**调用前检查：**必须已经成功调用过 [`.parse_data()`](#xml) 方法。

**返回值：**组装好的 XML 字符串，可直接回复微信服务器。

**对应官方文档：**[回复空消息](http://mp.weixin.qq.com/wiki/1/6239b44c206cab9145b1d52c67e6c551.html)

## 客服消息

### 发送文本消息

**调用方法：**`.send_text_message(user_id, content)`

**参数说明：**

* `user_id`: 用户 ID（OpenID）
* `content`: 消息正文

**调用前检查：**App ID / App Secret

**返回值：**正常返回官方接口的 JSON 数据：`{"errcode": 0, "errmsg": "ok"}`，一般无需理会该返回值，发送失败会抛出异常，捕获异常即可。

**异常：**当发生失败时抛出 [`exceptions.OfficialAPIError`](/api/exception.md#officialapierror) 异常，该异常包含了错误的代号与原因信息。

**对应官方文档：**[客服接口](http://mp.weixin.qq.com/wiki/11/c88c270ae8935291626538f9c64bd123.html)

### 发送图片消息

**调用方法：**`.send_image_message(user_id, media_id)`

**参数说明：**

* `user_id`: 用户 ID（OpenID）
* `media_id`: 图片的 Media ID，可通过 `.upload_media()` 方法上传

**调用前检查：**App ID / App Secret

**返回值：**正常返回官方接口的 JSON 数据：`{"errcode": 0, "errmsg": "ok"}`，一般无需理会该返回值，发送失败会抛出异常，捕获异常即可。

**异常：**当发生失败时抛出 [`exceptions.OfficialAPIError`](/api/exception.md#officialapierror) 异常，该异常包含了错误的代号与原因信息。

**对应官方文档：**[客服接口](http://mp.weixin.qq.com/wiki/11/c88c270ae8935291626538f9c64bd123.html)

### 发送语音消息 

**调用方法：**`.send_voice_message(user_id, media_id)`

**参数说明：**

* `user_id`: 用户 ID（OpenID）
* `media_id`: 语音的 Media ID，可通过 `.upload_media()` 方法上传

**调用前检查：**App ID / App Secret

**返回值：**正常返回官方接口的 JSON 数据：`{"errcode": 0, "errmsg": "ok"}`，一般无需理会该返回值，发送失败会抛出异常，捕获异常即可。

**异常：**当发生失败时抛出 [`exceptions.OfficialAPIError`](/api/exception.md#officialapierror) 异常，该异常包含了错误的代号与原因信息。

**对应官方文档：**[客服接口](http://mp.weixin.qq.com/wiki/11/c88c270ae8935291626538f9c64bd123.html)

### 发送视频消息

**调用方法：**`.send_video_message(user_id, media_id, title=None, description=None)`

**参数说明：**

* `user_id`: 用户 ID（OpenID）
* `media_id`: 视频的 Media ID，可通过 `.upload_media()` 方法上传
* `title`: 视频消息的标题
* `description`: 视频消息的描述

**调用前检查：**App ID / App Secret

**返回值：**正常返回官方接口的 JSON 数据：`{"errcode": 0, "errmsg": "ok"}`，一般无需理会该返回值，发送失败会抛出异常，捕获异常即可。

**异常：**当发生失败时抛出 [`exceptions.OfficialAPIError`](/api/exception.md#officialapierror) 异常，该异常包含了错误的代号与原因信息。

**对应官方文档：**[客服接口](http://mp.weixin.qq.com/wiki/11/c88c270ae8935291626538f9c64bd123.html)

### 发送音乐消息 

**调用方法：**`.send_music_message(user_id, url, hq_url, thumb_media_id, title=None, description=None)`

**参数说明：**

* `user_id`: 用户 ID（OpenID）
* `url`: 音乐链接
* `hq_url`: 高品质音乐链接，wifi环境优先使用该链接播放音乐
* `thumb_media_id`: 缩略图的 Media ID，可以通过 `.upload_media()` 方法上传
* `title`: 音乐标题
* `description`: 音乐描述

**调用前检查：**App ID / App Secret

**返回值：**正常返回官方接口的 JSON 数据：`{"errcode": 0, "errmsg": "ok"}`，一般无需理会该返回值，发送失败会抛出异常，捕获异常即可。

**异常：**当发生失败时抛出 [`exceptions.OfficialAPIError`](/api/exception.md#officialapierror) 异常，该异常包含了错误的代号与原因信息。

**对应官方文档：**[客服接口](http://mp.weixin.qq.com/wiki/11/c88c270ae8935291626538f9c64bd123.html)

### 发送图文消息

**调用方法：**`.send_article_message(self, user_id, articles=None, media_id=None)`

**参数说明：**

* `user_id`: 用户 ID（OpenID）
* `articles`: list 对象, 每个元素为一个 dict 对象, key 包含 `title`, `description`, `picurl`, `url` （示例同 [被动回复消息 - 图文消息](#-_6)）
* `media_id`: 待发送的图文 Media ID

注意 `articles` 和 `media_id` 参数只能传递任意一个。同时传递两个将优先使用 `articles` 进行发送。

**调用前检查：**App ID / App Secret

**返回值：**正常返回官方接口的 JSON 数据：`{"errcode": 0, "errmsg": "ok"}`，一般无需理会该返回值，发送失败会抛出异常，捕获异常即可。

**异常：**当发生失败时抛出 [`exceptions.OfficialAPIError`](/api/exception.md#officialapierror) 异常，该异常包含了错误的代号与原因信息。

**对应官方文档：**[客服接口](http://mp.weixin.qq.com/wiki/11/c88c270ae8935291626538f9c64bd123.html)

### 发送卡券

待开发

## 群发接口

待开发

## 模板消息

### 设置所属行业

**调用方法：**`.set_template_industry(industry_id1, industry_id2)`

**参数说明：**

* `industry_id1`: 主营行业代码
* `industry_id2`: 副营行业代码

**调用前检查：**App ID / App Secret

**返回值：**正常返回官方接口的 JSON 数据：`{"errcode": 0, "errmsg": "ok"}`，一般无需理会该返回值，设置失败会抛出异常，捕获异常即可。

**异常：**当发生失败时抛出 [`exceptions.OfficialAPIError`](/api/exception.md#officialapierror) 异常，该异常包含了错误的代号与原因信息。

**对应官方文档：**[设置所属行业](http://mp.weixin.qq.com/wiki/5/6dde9eaa909f83354e0094dc3ad99e05.html#.E8.AE.BE.E7.BD.AE.E6.89.80.E5.B1.9E.E8.A1.8C.E4.B8.9A)

### 获取设置的行业信息

待开发

### 获得模板 ID

**调用方法：**`.get_template_id(template_id_short)`

**参数说明：**

* `template_id_short`: 模板库中模板的编号，有“TM\*\*”和“OPENTMTM\*\*”等形式

**调用前检查：**App ID / App Secret

**返回值：**正常返回官方接口的 JSON 数据，示例：

```json
{
    "errcode": 0,
    "errmsg": "ok",
    "template_id": "Doclyl5uP7Aciu-qZ7mJNPtWkbkYnWBWVja26EGbNyk"
}
```

**异常：**当发生失败时抛出 [`exceptions.OfficialAPIError`](/api/exception.md#officialapierror) 异常，该异常包含了错误的代号与原因信息。

**对应官方文档：**[获得模板ID](http://mp.weixin.qq.com/wiki/5/6dde9eaa909f83354e0094dc3ad99e05.html#.E8.8E.B7.E5.BE.97.E6.A8.A1.E6.9D.BFID)

### 获取模板列表

待开发

### 删除模板

待开发

### 发送模板消息

**调用方法：**`.send_template_message(user_id, template_id, data, url='', topcolor='#FF0000')`

**参数说明：**

* `user_id`: 用户 ID（OpenID）
* `template_id`: 模板ID
* `data`: 模板消息数据 (dict形式)，示例如下：

        {
            "first": {
                "value": "恭喜你购买成功！",
                "color": "#173177"
            },
            "keyword1":{
                "value": "巧克力",
                "color": "#173177"
            },
            "keyword2": {
                "value": "39.8元",
                "color": "#173177"
            },
            "keyword3": {
                "value": "2014年9月16日",
                "color": "#173177"
            },
            "remark":{
                "value": "欢迎再次购买！",
                "color": "#173177"
            }
        }
        
* `url`: 跳转地址 (默认为空)
* `topcolor`: 顶部颜色RGB值 (默认 '#FF0000')

**调用前检查：**App ID / App Secret

**返回值：**正常返回官方接口的 JSON 数据，示例：

```json
{
    "errcode": 0,
    "errmsg": "ok",
    "msgid": 200228332
}
```

**异常：**当发生失败时抛出 [`exceptions.OfficialAPIError`](/api/exception.md#officialapierror) 异常，该异常包含了错误的代号与原因信息。

**对应官方文档：**[发送模板消息](http://mp.weixin.qq.com/wiki/5/6dde9eaa909f83354e0094dc3ad99e05.html#.E5.8F.91.E9.80.81.E6.A8.A1.E6.9D.BF.E6.B6.88.E6.81.AF)

### 模板消息事件推送

当模板消息事件推送 XML 到达并经过 [`.parse_data()`](#xml) 解析后，你可以通过下面的方式获取状态信息。

首先要确定该消息是模板消息的事件推送：

```python
from wechat_sdk.messages import EventMessage
if isinstance(wechat.message, EventMessage) and wechat.message.type == 'templatesendjobfinish':
```

然后就可以根据 `wechat.message.status` 的情况进行判断了：

1. 当送达成功时，`wechat.message.status == 'success'`
2. 当送达失败，原因为用户拒收（用户设置拒绝接收公众号消息）时，`wechat.message.status == 'failed:user block'`
3. 当送达失败，其他原因时，`wechat.message.status == 'failed:system failed'`

## 公众号自动回复配置

待开发


