# 快速上手 - SDK 快速介绍

本节将快速向你介绍 wechat-python-sdk 的整体脉络及注意事项，为后续文档的阅读打下基础。下文假设你已经安装了 ``wechat-sdk`` 。如果还没有，请返回 [安装](/#_2) 一节进行安装。

## 注意事项

**请注意：本开发包并不打算提供一个独立的完整微信解决方案，我们更希望这个开发包可以非常融洽的在各个框架中进行集成并使用，对于HTTP请求及响应方面并不涉及，该开发包仅仅接受必要参数，提供各种微信操作的方法，并返回相应的可以响应微信服务器的数据(Response)或操作执行结果。**

## 主要组件说明

wechat-python-sdk 有两个主要组件，分别是 `WechatConf`，`WechatBasic`，下面来一一介绍它们的作用。

* `WechatConf` 是 **微信配置类**，你需要将在公众平台开发者选项中的 Token/AppID/AppSecret/EncodingAESKey 等信息传入其中，之后该类将会自行维护相关配置信息（access_token/jsapi_ticket）的有效性，支持分布式。
* `WechatBasic` 是 **官方接口类**，与官方公众平台开发者文档（[http://mp.weixin.qq.com/wiki](http://mp.weixin.qq.com/wiki)）对应，是对该文档所有接口的二次封装，方便调用。该类需要传入 `WechatConf` 的有效实例。

## 异常说明

wechat-python-sdk 在操作失败时会根据错误原因抛出对应异常。这里介绍最通用的两种异常类型 `WechatAPIException` 和 `WechatSDKException`，它们可以应对大部分的开发需求。其他类型异常均从这两类异常继承而来，具体信息请参考 [异常类 API](/api/exception) 。

* `WechatAPIException`：**官方公众平台接口错误异常**，包含属性 `errcode` 和 `errmsg`，分别对应于错误代码和错误信息。`errcode` 的对应解释请参照 [官方文档](http://mp.weixin.qq.com/wiki/10/6380dc743053a91c544ffd2b7c959166.html)。
* `WechatSDKException`：**SDK自身错误异常**，包含属性 `message`，对应于错误信息。

后续文档的每个操作都会描述当运行出错时所抛出的异常信息。

## 下一步

你现在已经快速了解了 wechat-python-sdk 的整体脉络及注意事项，接下来请阅读 [快速上手 - 官方接口](/quickstart/official) 来学习如何使用官方接口进行开发， 


