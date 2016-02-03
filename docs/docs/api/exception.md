# 异常类 

所有异常类均处于 `wechat_sdk.exceptions` 中，可按需导入。

## WechatException()

wechat-python-sdk 异常基类

导入方式：`from wechat_sdk.exceptions import WechatException`

继承自：`Exception`

## WechatAPIException()

官方 API 错误异常（包含错误码及错误信息）

导入方式：`from wechat_sdk.exceptions import WechatAPIException`

继承自：`WechatException`

### 属性

* `.errcode`：错误代码
* `.errmsg`：错误信息

## WechatSDKException()

SDK 错误异常（仅包含错误内容描述）

导入方式：`from wechat_sdk.exceptions import WechatSDKException`

继承自：`WechatException`

### 属性

* `.message`：错误信息

## NeedParamError()

构造参数提供不全异常

导入方式：`from wechat_sdk.exceptions import NeedParamError`

继承自：`WechatSDKException`

### 属性

* `.message`：错误信息

## ParseError()

解析微信服务器数据异常

导入方式：`from wechat_sdk.exceptions import ParseError`

继承自：`WechatSDKException`

### 属性

* `.message`：错误信息

## NeedParseError()

尚未解析微信服务器请求数据异常

导入方式：`from wechat_sdk.exceptions import NeedParseError`

继承自：`WechatSDKException`

### 属性

* `.message`：错误信息

## OfficialAPIError()

微信官方API请求出错异常

导入方式：`from wechat_sdk.exceptions import OfficialAPIError`

继承自：`WechatAPIException`

### 属性

* `.errcode`：错误代码
* `.errmsg`：错误信息

## UnOfficialAPIError()

微信非官方API请求出错异常

导入方式：`from wechat_sdk.exceptions import UnOfficialAPIError`

继承自：`WechatSDKException`

### 属性

* `.message`：错误信息

## NeedLoginError()

微信非官方API请求出错异常 - 需要登录

导入方式：`from wechat_sdk.exceptions import NeedLoginError`

继承自：`UnOfficialAPIError`

### 属性

* `.message`：错误信息

## LoginError()

微信非官方API请求出错异常 - 登录出错

导入方式：`from wechat_sdk.exceptions import LoginError`

继承自：`UnOfficialAPIError`

### 属性

* `.message`：错误信息

## LoginVerifyCodeError()

微信非官方API请求出错异常 - 登录出错 - 验证码错误

导入方式：`from wechat_sdk.exceptions import LoginVerifyCodeError`

继承自：`LoginError`

### 属性

* `.message`：错误信息


