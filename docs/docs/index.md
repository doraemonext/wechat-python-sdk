# 欢迎使用 wechat-python-sdk 开发包

![image](/img/logo.png)
## 概述

wechat-python-sdk 希望能帮你解决微信公众平台开发中的种种不便，让你可以专注于业务逻辑本身，而不是浪费精力在与微信服务器复杂的交互中。

本开发包目前支持订阅号、服务号的官方接口，相信这将会极大的简化你的开发过程。

## 安装

**请注意：本 SDK 在 pypi.python.org 上的软件包名称为 [`wechat-sdk`](https://pypi.python.org/pypi/wechat-sdk)。**

可以通过 pip 进行安装

    pip install wechat-sdk

也可以通过 easy_install 进行安装

    easy_install wechat-sdk

也可以直接在终端下输入下列命令手动安装

    wget https://github.com/wechat-python-sdk/wechat-python-sdk/archive/master.tar.gz
    tar zvxf master.tar.gz
    cd wechat-python-sdk-master
    python setup.py build
    python setup.py install
    
## 下一步
	
如果你是 SDK 的新用户，请点击导航栏上的 **快速入门**。

如果你需要更加全面详细的使用说明，请点击导航栏上的 **官方接口**。

如果你需要 SDK 的所有细节，请点击导航栏上的 **API 文档**。

如果你对 SDK 的使用心存疑问，请点击导航栏上的 **常见问题 FAQ**，如果其中没有你想要的答案，请前往 [wechat-python-sdk Issues](https://github.com/wechat-python-sdk/wechat-python-sdk/issues) 提出你的问题。

如果你对本项目感兴趣，请点击导航栏上的 **关于项目** 和 **关于作者**。

## 许可协议

本项目采用 MIT 许可协议，可放心集成于商业产品中，但请包含本许可声明。

    Copyright (C) 2014-2016 Ace Kwok
    
    Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
    
    The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
    
    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

## 感谢

感谢 [WeRoBot](https://github.com/whtsky/WeRoBot) 和 [wechatpy](https://github.com/jxtech/wechatpy) 项目，本项目中官方接口的许多代码均借鉴于此。

## 版本兼容说明

wechat-python-sdk 于 2016 年 2 月份进行了一次较大规模升级，升级到了 v0.6.0 版本，但会保持向前兼容。请先前版本的用户放心升级使用。

## 更新历史

### v0.6.4

* 修正 Windows 下安装问题(感谢 [jiajunhuang](https://github.com/jiajunhuang))

### v0.6.3

* 增加了回复空消息的功能

### v0.6.2

* 增加了 Python 3 的支持 

### v0.6.1

* 修正了 jsapi_ticket 的获取出错问题
* 代码结构的优化

### v0.6.0

* 重新编写了文档, 添加了快速上手教程
* 添加了 WechatConf 微信配置类
* 增加了对消息加解密的支持
* 对整体进行了较大规模的重构, 优化了代码结构

### v0.5.9

* 修复了 py3 中 只有 str 没有 unicode 的情况(感谢 [hbrls](https://github.com/hbrls))
* 避免 generate_jsapi_signature 刷新 access_token(感谢 [paicha](https://github.com/paicha))
* 增加客服消息转发功能(感谢 [torpedoallen](https://github.com/torpedoallen))

### v0.5.8

* 增加了小视频消息类支持
* 修复了多层级XML解析问题

### v0.5.7

* 修复创建二维码时的传参Bug (感谢 [lvxudong](https://github.com/lvxudong))
* 创建菜单时的 menu_data 可自由使用 str 或 unicode

### v0.5.6

* 添加模板消息的支持

### v0.5.5

* 修复 grant_jsapi_ticket 会时不时出现 invalid credential 的问题 (感谢 [JohnnyZhao](https://github.com/JohnnyZhao))

### v0.5.4

* 在 grant_token 函数调用之后，顺带着覆盖本地的 access_token (感谢 [JohnnyZhao](https://github.com/JohnnyZhao))

### v0.5.3

* 修复 hashlib.sha1 无法 decode unicode 字符串问题 (感谢 [JohnnyZhao](https://github.com/JohnnyZhao))

### v0.5.2

* 官方接口中的 upload_media 方法增加 StringIO 支持

### v0.5.1

* 官方接口增加了 JS-SDK 支持，可对 URL 进行签名 (感谢 [JohnnyZhao](https://github.com/JohnnyZhao))
* 官方接口的文本回复方法增加了是否对内容进行转义的控制参数
* 非官方接口增加了图文分析信息 (感谢 [svcvit](https://github.com/svcvit))

### v0.5.0

* 新增了针对 Django 的上下文对话支持
* 新增了非官方接口下的验证码登录及获取验证码功能
* 新增了在素材库中创建图文消息功能
* 新增了二维码事件的获取
* 修正了编码转换问题
* 修正了自定义菜单跳转事件获取
* 更正了 WechatBasic 中的解释说明链接
* 更新文档，增加了一个快速上手示例
* 增加了FAQ文档

