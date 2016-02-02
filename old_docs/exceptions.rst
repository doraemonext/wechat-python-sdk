异常类
=====================

.. py:class:: wechat_sdk.exceptions.NeedParamError()

   构造参数提供不全异常

.. py:class:: wechat_sdk.exceptions.ParseError()

   解析微信服务器数据异常

.. py:class:: wechat_sdk.exceptions.NeedParseError()

   尚未解析微信服务器请求数据异常

.. py:class:: wechat_sdk.exceptions.OfficialAPIError()

   微信官方 API 请求出错异常

.. py:class:: wechat_sdk.exceptions.UnOfficialAPIError()

   微信非官方 API 请求出错异常

.. py:class:: wechat_sdk.exceptions.NeedLoginError()

   微信非官方API请求出错异常 - 需要登录

   该类为 ``wechat_sdk.exceptions.UnOfficialAPIError`` 的子类

.. py:class:: wechat_sdk.exceptions.LoginError()

   微信非官方API请求出错异常 - 登录出错

   该类为 ``wechat_sdk.exceptions.UnOfficialAPIError`` 的子类

.. py:class:: wechat_sdk.exceptions.LoginVerifyCodeError()

   微信非官方API请求出错异常 - 登录出错 - 验证码错误

   该类为 ``wechat_sdk.exceptions.LoginError`` 的子类
