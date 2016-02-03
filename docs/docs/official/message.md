# 官方接口 - 消息管理

## 消息管理 - 解析接收到的 XML 消息

**调用方法：**

`.parse_data(data, msg_signature=None, timestamp=None, nonce=None)`

**参数说明：**

* `data`: 需要解析的 XML 字符串数据
* `msg_signature`: 消息解密专用 - 签名
* `timestamp`: 消息解密专用 - 时间戳
* `nonce`: 消息解密专用 - 随机数

**调用前检查：**

* `Token`

**适用范围：**

所有公众号

**返回值：**

`None`

**异常：**

* 当解析 XML 失败时抛出 `exceptions.ParseError` 异常。

**对应官方文档：**

* [接收普通消息](http://mp.weixin.qq.com/wiki/17/f298879f8fb29ab98b2f2971d42552fd.html)
* [接收事件推送](http://mp.weixin.qq.com/wiki/7/9f89d962eba4c5924ed95b513ba69d9b.html)

## 消息管理 - 被动回复消息

## 消息管理 - 客服消息

## 消息管理 - 群发接口

## 消息管理 - 模板消息

## 消息管理 - 公众号自动回复配置



