==============================
 上下文对话支持
==============================

为了实现用户状态的维持与记录， ``wechat-python-sdk`` 实现了上下文对话功能。

**由于作者精力有限，目前仅实现了 Django 下的上下文对话支持，其他方式或其他框架下的上下文对话适配将在后续版本中逐渐完成。如果您有精力、有兴趣，欢迎向本项目贡献代码 :)**

Django
------------------------------

该上下文对话支持功能在 Django 1.6+ 环境下测试通过。

对于一个单独的公众号而言，每个已关注用户都会有一个对该公众号唯一的OpenID，所以，我们可以通过OpenID来确定并记录用户身份、状态等信息。

安装
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

在你的 settings.py 的 ``INSTALLED_APPS`` 中添加 ``wechat_sdk.context.framework.django`` ，如下：

::

   INSTALLED_APPS = (
       # ...
       'wechat_sdk.context.framework.django',
   )

然后执行数据库同步

如果你是 Django 1.7+ 版本，执行：

::

   python manage.py migrate wechat_sdk_django

否则，执行:

::

   python manage.py syncdb wechat_sdk_django

安装完成:)

现在在你的数据库中可以看到， ``wechat-python-sdk`` 在其中新建了一个名为  ``wechat_context`` 的数据表，这就是用来存储微信上下文的地方。

使用说明
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

初始化上下文对话需要传入用户的 OpenID，初始化的过程非常简单，假设存储当前请求用户 OpenID 的变量名称为 ``source`` ，则有如下代码：

::

   from wechat_sdk.context.framework.django import DatabaseContextStore

   context = DatabaseContextStore(openid=source)

如果当前用户尚未存储任何上下文对话数据， ``DatabaseContextStore`` 会自动新建记录，否则会自动取出数据库的已有记录，无需任何干预。

对于我们现在得到的这个 ``context`` 上下文对话，你可以自由读写，并且可以多次编辑其中的内容。

.. py:class:: backends.ContextBase

   这是所有上下文对话的基类。它支持下面这些标准的字典方法：

   .. py:method:: __getitem__(key)

      示例： ``fav_color = context['fav_color']``

   .. py:method:: __setitem__(key, value)

      示例： ``context['fav_color'] = 'blue'``

   .. py:method:: __delitem__(key)

      示例： ``del context['fav_color']``

   .. py:method:: __contains__(key)

      示例： ``'fav_color' in context``

   .. py:method:: get(key, default=None)

      示例： ``fav_color = context.get('fav_color', 'red')``

   .. py:method:: pop(key)

      示例： ``fav_color = context.pop('fav_color')``

   .. py:method:: keys()
   .. py:method:: items()
   .. py:method:: setdefault()
   .. py:method:: clear()

   它还有支持下面这些方法：

   .. py:method:: flush()

      本方法会在数据库中删除该用户的所有信息，执行前请确认不再需要该用户的任何数据。

   .. py:method:: get_expiry_age()

      本方法返回当前上下文对话还有多少秒失效。

      本方法接收两个可选的关键字参数：

      * ``modification``: 该上下文对话的最后修改时间，需要为 ``datetime`` 对象。默认是当前时间。
      * ``expiry``: 该上下文对话的过期时间信息。可以是 ``datetime`` 对象，也可以是 ``int`` ，或者是 ``None`` 。默认为 ``set_expire`` 所设定的过期日期。

   .. py:method:: get_expire_date()

      本方法返回当前上下文对话的过期日期 (``datetime`` 对象)

      本方法接受的两个可选的关键字参数和 ``get_expire_age()`` 相同。

   .. py:method:: set_expiry(value)

      设置当前上下文对话的过期时间。你可以用不同的方式来传入你想要设定的过期时间：

      * 如果 ``value`` 是一个数字，那么当前上下文对话将会在 ``value`` 秒后失效。举例来说，如果你调用了 ``context.set_expire(300)`` ，那么当前上下文对话将会在 5 分钟后失效。
      * 如果 ``value`` 是一个 ``datetime`` 或 ``timedelta`` 对象，那么当前上下文对话将会在该指定的时间失效。
      * 如果 ``value`` 是 ``None`` ，那么当前上下文对话的过期时间将会重置到系统所设定的值(WECHAT_CONTEXT_AGE)。

   .. py:method:: clear_expired()

      本方法会在数据库中清空所有的过期信息，无需手动调用，每次执行 ``save()`` 时会自动进行清理。

   .. py:method:: save()

      **本方法会将所有的当前的上下文对话信息存入数据库。请务必要在代码的结束位置调用本方法，否则所有数据都不会被保存。**

      示例： ``context.save()``

使用准则
~~~~~~~~~~~~~~~~~~~~~~~~

不要尝试直接访问或设置 ``context`` 实例中的除上面提到的方法和属性，仅仅把它当做一个普通的 python 字典就可以了。

使用示例
~~~~~~~~~~~~~~~~~~~~~~~~

这里用一个非常简单的小例子来帮助大家理解并使用上下文对话功能。它的功能很简单，如果我一直朝这个 ``home`` 函数发文字信息的请求，它会记录当前是第多少次对话以及上一次的对话内容是什么。

::

    # -*- coding: utf-8 -*-

    from django.http.response import HttpResponse, HttpResponseBadRequest
    from django.views.decorators.csrf import csrf_exempt
    from wechat_sdk import WechatBasic
    from wechat_sdk.exceptions import ParseError
    from wechat_sdk.messages import TextMessage
    from wechat_sdk.context.framework.django import DatabaseContextStore


    @csrf_exempt
    def home(request):
        # 从 request 中提取基本信息 (signature, timestamp, nonce, xml)
        signature = request.GET.get('signature')
        timestamp = request.GET.get('timestamp')
        nonce = request.GET.get('nonce')
        xml = request.body

        # 实例化 WechatBasic 并检验合法性
        wechat_instance = WechatBasic(token='MY_WECHAT_TOKEN')
        if not wechat_instance.check_signature(signature=signature, timestamp=timestamp, nonce=nonce):
            return HttpResponseBadRequest('Verify Failed')

        # 解析本次请求的 XML 数据
        try:
            wechat_instance.parse_data(data=xml)
        except ParseError:
            return HttpResponseBadRequest('Invalid XML Data')

        message = wechat_instance.get_message()  # 获取解析好的微信请求信息
        context = DatabaseContextStore(openid=message.source)  # 利用本次请求中的用户OpenID来初始化上下文对话

        if isinstance(message, TextMessage):
            step = context.get('step', 1)  # 从上下文对话数据中取出 'step' 所对应的内容(当前对话次数)，如果没有则返回 1
            last_text = context.get('last_text')  # 从上下文对话数据中取出 'last_text' 所对应的内容(上次对话内容)
            # 生成字符串
            now_text = u'这是第 %d 次对话' % step
            if step > 1:
                now_text += u'，上一次对话文字：%s' % last_text
            # 将新的数据存入上下文对话中
            context['step'] = step + 1
            context['last_text'] = message.content
            response = wechat_instance.response_text(content=now_text)
        else:
            response = wechat_instance.response_text(content=u'错误的信息类型')

        context.save()  # 非常重要！请勿忘记！最后需要将所有临时数据保存入数据库！
        return HttpResponse(response)

可用设置项
~~~~~~~~~~~~~~~~~~~~~~~~~~~

``wechat-python-sdk`` 为您提供了设置项，它有自己的默认值，但是您也可以通过修改它来适应自己的需求。

``WECHAT_CONTEXT_AGE = 7200`` 上下文对话默认过期时间(s)

如果需要修改，直接在 settings.py 中加上上面的设置项即可；不需修改则不必在 settings.py 中增加该项。
