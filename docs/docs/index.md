# 欢迎使用 wechat-python-sdk 开发包

![image](/img/logo.png)

## 概述

wechat-python-sdk 希望能帮你解决微信公众平台开发中的种种不便，让你可以专注于业务逻辑本身，而不是浪费精力在与微信服务器复杂的交互中。

本开发包目前支持订阅号、服务号的官方接口，以及额外添加了扩展功能接口（扩展功能将会直接模拟登陆腾讯官方公众平台去进行相应操作），相信这将会极大的简化你的开发过程。

## 安装

**请注意：本 SDK 在 pypi.python.org 上的软件包名称为 [`wechat-sdk`](https://pypi.python.org/pypi/wechat-sdk)。**

可以通过 pip 进行安装

    pip install wechat-sdk

也可以通过 easy_install 进行安装

    easy_install wechat-sdk

也可以直接在终端下输入下列命令手动安装

    wget https://github.com/doraemonext/wechat-python-sdk/archive/master.tar.gz
    tar zvxf master.tar.gz
    cd wechat-python-sdk-master
    python setup.py build
    python setup.py install
    
## 下一步
	
如果你是 SDK 的新用户，请点击导航栏上的 **快速入门**。

如果你需要更加全面详细的使用说明，请点击导航栏上的 **官方接口** 和 **扩展功能**。

如果你需要 SDK 的所有细节，请点击导航栏上的 **API 文档**。

如果你对 SDK 的使用心存疑问，请点击导航栏上的 **常见问题 FAQ**，如果其中没有你想要的答案，请前往 [wechat-python-sdk Issues](https://github.com/wechat-python-sdk/wechat-python-sdk/issues) 提出你的问题。

如果你对 SDK 的开发进度感兴趣，请点击导航栏上的 **功能完成度**。

如果你发现 SDK 满足不了你的要求，而且你也有兴趣、有能力开发该功能，请点击导航栏上的 **贡献代码指南**。

如果你对本项目感兴趣，请点击导航栏上的 **关于**。

## 许可协议

本项目采用 MIT 许可协议，可放心集成于商业产品中，但请包含本许可声明。

    Copyright (C) 2014-2016 Ace Kwok
    
    Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
    
    The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
    
    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

## 感谢

感谢 [WeRoBot](https://github.com/whtsky/WeRoBot) 和 [wechatpy](https://github.com/jxtech/wechatpy) 项目，本项目中官方接口的许多代码均借鉴于此。

## 版本兼容说明

wechat-python-sdk 于 2016 年 2 月份进行了一次较大规模升级，升级到了 v0.6.0 版本，更正了部分类中的方法名称，但会保持向前兼容。请先前版本的用户放心升级使用。

