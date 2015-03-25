==============================
 微信非官方接口操作 WechatExt
==============================

.. py:class:: wechat_sdk.ext.WechatExt(username, password [, token=None, cookies=None, appid=None, plugin_token=None, ifencodepwd=False, login=True, checkssl=False])

   微信扩展功能类

   :param str username: 你的微信公众平台账户用户名
   :param str password: 你的微信公众平台账户密码
   :param str token: 直接导入的 ``token`` 值, 该值需要在上一次该类实例化之后手动进行缓存并在此传入, 如果不传入, 将会在实例化的时候自动获取
   :param str cookies: 直接导入的 ``cookies`` 值, 该值需要在上一次该类实例化之后手动进行缓存并在此传入, 如果不传入, 将会在实例化的时候自动获取
   :param str appid: 直接导入的 ``appid`` 值, 该值需要在上一次该类实例化之后手动进行缓存并在此传入, 如果不传入, 将会在调用 ``stat_`` 开头的方法(统计分析类)时自动获取
   :param str plugin_token: 直接导入的 ``plugin_token`` 值, 该值需要在上一次该类实例化之后手动进行缓存并在此传入, 如果不传入, 将会在调用 ``stat_`` 开头的方法(统计分析类)时自动获取
   :param boolean ifencodepwd: 密码是否已经经过编码, 如果密码已经经过加密, 此处为 ``True`` , 如果传入的密码为明文, 此处为 ``False``
   :param boolean login: **是否在实例化过程中尝试登录 (推荐此处设置为 False, 然后手动执行登录以方便进行识别验证码等操作, 此处默认值为 True 为兼容历史版本**
   :param boolean checkssl: 是否检查 SSL, 默认为 False, 可避免 urllib3 的 InsecurePlatformWarning 警告

   **实例化说明：**

   1. 请注意实例化时的 ``login`` 参数，它的默认值为 ``True`` ，但这仅仅是为了兼容历史版本（v0.4.2及以前），在新版本中，强烈推荐将该参数设置为 ``False`` ，然后手动执行 :func:`login` 以有效应对可能出现的验证码问题。

   2. 当实例化 WechatExt 时，你必须传入 ``username`` 和 ``password`` ，对于 ``token`` 和 ``cookies`` 参数，如果传入了它们，将会自动省略登录过程（无论 ``login`` 参数被设置为了 ``True`` 还是 ``False`` ）。

   3. 请保证你的代码中会捕获 ``NeedLoginError`` 异常，一旦发生此异常，你需要重新调用 :func:`login` 方法登录来获取新的 ``token`` 及 ``cookies`` 。

   4. **详细说明一下 token 及 cookies 参数的传入问题：**

      因为此开发包并不打算以服务器的方式常驻，所以，每次请求均会重新实例化 ``WechatExt`` ，所以需要你以你自己的方式去保存上一次请求中实例化后的 ``WechatExt`` 中 ``token`` 及 ``cookies`` 参数，并在下一次的实例化的过程中传入，以此来保证不会频繁登录。

      获取 ``token`` 及 ``cookies`` 的方式为调用 :func:`get_token_cookies` 方法

      下一版本将会考虑更为简单通用的方法，在新版本发布之前，请用你自己的方式把得到的 ``token`` 及 ``cookies`` 保存起来，不管是文件，缓存还是数据库都可以，只要在实例化后，你可以在任何时间调用 :func:`get_token_cookies` 方法。

   5. ``appid`` 及 ``plugin_token`` 参数是用于统计分析类的方法的(以 ``stat_`` 开头)，如果不需要调用这些方法，可以无需理会这两个参数。

      它们和 ``token`` 及 ``cookies`` 一样，可由开发者自行缓存，获取它们的方式为调用 :func:`get_plugin_token_appid` 方法。唯一需要注意的是，如果传入了 ``appid`` 及 ``plugin_token`` 参数，那么也必须要传入 ``token`` 和 ``cookies`` 参数，否则无效。

   .. py:method:: login(verify_code='')

        登录微信公众平台

        当你刚刚实例化 ``WechatExt`` 完或者捕获到 ``NeedLoginError`` 异常时，需要调用此方法进行登录或登录重试。

        **如何应对登录时的验证码：**

        默认情况下，如果微信服务器认为你的账号正常，那么直接调用一次 :func:`login` 就可以完成登录操作，但如果不幸出现了验证码，本方法会抛出 ``LoginVerifyCodeError`` 异常，这时你需要通过下面的 :func:`get_verify_code` 方法来获取验证码图片，然后通过你自己的方式识别这张图片并得出结果，并将验证码识别结果作为本方法的 ``verify_code`` 参数值来重新调用本方法，可多次尝试。

        **如何识别验证码：**

        鉴于腾讯的验证码基本无法通过机器进行识别，所以推荐网络上的人工识别验证码服务。因为 ``token`` 和 ``cookies`` 都有一定时间的有效期，所以一次验证码识别可以使用不短的时间，响应时间和价格完全可以承受。

        :param str verify_code: 验证码, 不传入则为无验证码
        :raises: LoginVerifyCodeError 需要验证码或验证码出错，该异常为 ``LoginError`` 的子类
        :raises: LoginError 登录出错，异常内容为微信服务器响应的内容，可作为日志记录下来


   .. py:method:: get_verify_code(file_path)

        获取登录验证码并存储到本地路径

        :param str file_path: 将验证码图片保存的文件路径

   .. py:method:: get_token_cookies()

        获取当前 token 及 cookies, 供手动缓存使用

        返回 dict 示例::

            {
                'cookies': 'bizuin=3086177907;data_bizuin=3086177907;data_ticket=AgWTXTpLL+FV+bnc9yLbb3V8;slave_sid=TERlMEJ1bWFCbTlmVnRLX0lLdUpRV0pyN2k1eVkzbWhiY0NfTHVjNFRZQk1DRDRfal82UzZKWTczR3I5TFpUYjRXUDBtN1h1cmJMRTkzS3hianBHOGpHaFM0eXJiNGp6cDFWUGpqbFNyMFlyQ05GWGpseVg2T2s2Sk5DRWpnRlE=;slave_user=gh_1b2959761a7d;',
                'token': 373179898
            }

        :return: 一个 dict 对象, key 为 ``token`` 和 ``cookies``

   .. py:method:: get_plugin_token_appid()

        获取当前 plugin_token 及 appid, 供手动缓存使用

        返回 dict 示例::

            {
                'plugin_token': 'll1D85fGDCTr4AAxC_RrFIsfaM1eajMksOjZN_eXodroIeT77QkrMfckyYdG0qj8CnvWGUPp7-mpBOs07dbuG-iwULOcyjoEvlTsghm1K34C0oj3AI8egAxGqixxhRs8',
                'appid': 'wxd0c09648a48b3798'
            }

        :return: 一个 dict 对象, key 为 ``plugin_token`` 和 ``appid``

   .. py:method:: send_message(fakeid, content)

        主动发送文本消息

        :param str fakeid: 用户的 UID (即 fakeid )
        :param str content: 发送的内容
        :raises: NeedLoginError 操作未执行成功, 需要再次尝试登录, 异常内容为服务器返回的错误数据
        :raises: ValueError 参数出错, 具体内容有 ``fake id not exist``

   .. py:method:: get_user_list(page=0, pagesize=10, groupid=0)

        获取用户列表

        返回JSON示例 ::

            {
                "contacts": [
                    {
                        "id": 2431798261,
                        "nick_name": "Doraemonext",
                        "remark_name": "",
                        "group_id": 0
                    },
                    {
                        "id": 896229760,
                        "nick_name": "微信昵称",
                        "remark_name": "",
                        "group_id": 0
                    }
                ]
            }

        :param integer page: 页码 (从 0 开始)
        :param integer pagesize: 每页大小
        :param integer groupid: 分组 ID
        :return: 返回的 JSON 数据
        :raises: NeedLoginError 操作未执行成功, 需要再次尝试登录, 异常内容为服务器返回的错误数据

   .. py:method:: stat_article_detail_list(page=1, start_date=str(date.today()+timedelta(days=-30)), end_date=str(date.today()))

        获取图文分析数据

        返回JSON示例 ::

            {
                "hasMore": true,  // 说明是否可以增加 page 页码来获取数据
                "data": [
                    {
                        "index": [
                            "20,816",  // 送达人数
                            "1,944",  // 图文页阅读人数
                            "2,554",  // 图文页阅读次数
                            "9.34%",  // (图文页阅读人数 / 送达人数)
                            "0",  // 原文页阅读人数
                            "0",  // 原文页阅读次数
                            "0%",  // （原文页阅读人数 / 图文页阅读人数)
                            "47",  // 分享转发人数
                            "61",  // 分享转发次数
                            "1"  // 微信收藏人数
                        ],
                        "time": "2015-01-21",
                        "table_data": "{\"fields\":{\"TargetUser\":{\"thText\":\"\\u9001\\u8fbe\\u4eba\\u6570\",\"number\":false,\"colAlign\":\"center\",\"needOrder\":false,\"precision\":0},\"IntPageReadUser\":{\"thText\":\"\\u4eba\\u6570\",\"number\":true,\"colAlign\":\"right\",\"needOrder\":false,\"precision\":0},\"IntPageReadCount\":{\"thText\":\"\\u6b21\\u6570\",\"number\":true,\"colAlign\":\"right\",\"needOrder\":false,\"precision\":0},\"PageConversion\":{\"thText\":\"\\u56fe\\u6587\\u8f6c\\u5316\\u7387\",\"number\":true,\"colAlign\":\"right\",\"needOrder\":false,\"precision\":\"2\"},\"OriPageReadUser\":{\"thText\":\"\\u4eba\\u6570\",\"number\":true,\"colAlign\":\"right\",\"needOrder\":false,\"precision\":0},\"OriPageReadCount\":{\"thText\":\"\\u6b21\\u6570\",\"number\":true,\"colAlign\":\"right\",\"needOrder\":false,\"precision\":0},\"Conversion\":{\"thText\":\"\\u539f\\u6587\\u8f6c\\u5316\\u7387\",\"number\":true,\"colAlign\":\"right\",\"needOrder\":false,\"precision\":\"2\"},\"ShareUser\":{\"thText\":\"\\u4eba\\u6570\",\"number\":true,\"colAlign\":\"right\",\"needOrder\":false,\"precision\":0},\"ShareCount\":{\"thText\":\"\\u6b21\\u6570\",\"number\":true,\"colAlign\":\"right\",\"needOrder\":false,\"precision\":0},\"AddToFavUser\":{\"thText\":\"\\u5fae\\u4fe1\\u6536\\u85cf\\u4eba\\u6570\",\"number\":true,\"colAlign\":\"right\",\"needOrder\":false,\"precision\":0}},\"data\":[{\"MsgId\":\"205104027_1\",\"Title\":\"\\u56de\\u5bb6\\u5927\\u4f5c\\u6218 | \\u5feb\\u6765\\u5e26\\u6211\\u56de\\u5bb6\",\"RefDate\":\"20150121\",\"TargetUser\":\"20,816\",\"IntPageReadUser\":\"1,944\",\"IntPageReadCount\":\"2,554\",\"OriPageReadUser\":\"0\",\"OriPageReadCount\":\"0\",\"ShareUser\":\"47\",\"ShareCount\":\"61\",\"AddToFavUser\":\"1\",\"Conversion\":\"0%\",\"PageConversion\":\"9.34%\"}],\"fixedRow\":false,\"cssSetting\":{\"\":\"\"},\"complexHeader\":[[{\"field\":\"TargetUser\",\"thText\":\"\\u9001\\u8fbe\\u4eba\\u6570\",\"rowSpan\":2,\"colSpan\":1},{\"thText\":\"\\u56fe\\u6587\\u9875\\u9605\\u8bfb\",\"colSpan\":3},{\"thText\":\"\\u539f\\u6587\\u9875\\u9605\\u8bfb\",\"colSpan\":3},{\"thText\":\"\\u5206\\u4eab\\u8f6c\\u53d1\",\"colSpan\":2},{\"field\":\"AddToFavUser\",\"thText\":\"\\u5fae\\u4fe1\\u6536\\u85cf\\u4eba\\u6570\",\"rowSpan\":2,\"enable\":true}],[{\"field\":\"IntPageReadUser\",\"thText\":\"\\u4eba\\u6570\"},{\"field\":\"IntPageReadCount\",\"thText\":\"\\u6b21\\u6570\"},{\"field\":\"PageConversion\",\"thText\":\"\\u56fe\\u6587\\u8f6c\\u5316\\u7387\"},{\"field\":\"OriPageReadUser\",\"thText\":\"\\u4eba\\u6570\"},{\"field\":\"OriPageReadCount\",\"thText\":\"\\u6b21\\u6570\"},{\"field\":\"Conversion\",\"thText\":\"\\u539f\\u6587\\u8f6c\\u5316\\u7387\"},{\"field\":\"ShareUser\",\"thText\":\"\\u4eba\\u6570\"},{\"field\":\"ShareCount\",\"thText\":\"\\u6b21\\u6570\"}]]}",
                        "id": "205104027_1",
                        "title": "回家大作战 | 快来带我回家"
                    },
                    {
                        "index": [
                            "20,786",  // 送达人数
                            "2,598",  // 图文页阅读人数
                            "3,368",  // 图文页阅读次数
                            "12.5%",  // (图文页阅读人数 / 送达人数)
                            "0",  // 原文页阅读人数
                            "0",  // 原文页阅读次数
                            "0%",  // （原文页阅读人数 / 图文页阅读人数)
                            "73",  // 分享转发人数
                            "98",  // 分享转发次数
                            "1"  // 微信收藏人数
                        ],
                        "time": "2015-01-20",
                        "table_data": "{\"fields\":{\"TargetUser\":{\"thText\":\"\\u9001\\u8fbe\\u4eba\\u6570\",\"number\":false,\"colAlign\":\"center\",\"needOrder\":false,\"precision\":0},\"IntPageReadUser\":{\"thText\":\"\\u4eba\\u6570\",\"number\":true,\"colAlign\":\"right\",\"needOrder\":false,\"precision\":0},\"IntPageReadCount\":{\"thText\":\"\\u6b21\\u6570\",\"number\":true,\"colAlign\":\"right\",\"needOrder\":false,\"precision\":0},\"PageConversion\":{\"thText\":\"\\u56fe\\u6587\\u8f6c\\u5316\\u7387\",\"number\":true,\"colAlign\":\"right\",\"needOrder\":false,\"precision\":\"2\"},\"OriPageReadUser\":{\"thText\":\"\\u4eba\\u6570\",\"number\":true,\"colAlign\":\"right\",\"needOrder\":false,\"precision\":0},\"OriPageReadCount\":{\"thText\":\"\\u6b21\\u6570\",\"number\":true,\"colAlign\":\"right\",\"needOrder\":false,\"precision\":0},\"Conversion\":{\"thText\":\"\\u539f\\u6587\\u8f6c\\u5316\\u7387\",\"number\":true,\"colAlign\":\"right\",\"needOrder\":false,\"precision\":\"2\"},\"ShareUser\":{\"thText\":\"\\u4eba\\u6570\",\"number\":true,\"colAlign\":\"right\",\"needOrder\":false,\"precision\":0},\"ShareCount\":{\"thText\":\"\\u6b21\\u6570\",\"number\":true,\"colAlign\":\"right\",\"needOrder\":false,\"precision\":0},\"AddToFavUser\":{\"thText\":\"\\u5fae\\u4fe1\\u6536\\u85cf\\u4eba\\u6570\",\"number\":true,\"colAlign\":\"right\",\"needOrder\":false,\"precision\":0}},\"data\":[{\"MsgId\":\"205066833_1\",\"Title\":\"\\u56de\\u5bb6\\u5927\\u4f5c\\u6218 | \\u5982\\u4f55\\u4f18\\u96c5\\u5730\\u53bb\\u5f80\\u8f66\\u7ad9\\u548c\\u673a\\u573a\",\"RefDate\":\"20150120\",\"TargetUser\":\"20,786\",\"IntPageReadUser\":\"2,598\",\"IntPageReadCount\":\"3,368\",\"OriPageReadUser\":\"0\",\"OriPageReadCount\":\"0\",\"ShareUser\":\"73\",\"ShareCount\":\"98\",\"AddToFavUser\":\"1\",\"Conversion\":\"0%\",\"PageConversion\":\"12.5%\"}],\"fixedRow\":false,\"cssSetting\":{\"\":\"\"},\"complexHeader\":[[{\"field\":\"TargetUser\",\"thText\":\"\\u9001\\u8fbe\\u4eba\\u6570\",\"rowSpan\":2,\"colSpan\":1},{\"thText\":\"\\u56fe\\u6587\\u9875\\u9605\\u8bfb\",\"colSpan\":3},{\"thText\":\"\\u539f\\u6587\\u9875\\u9605\\u8bfb\",\"colSpan\":3},{\"thText\":\"\\u5206\\u4eab\\u8f6c\\u53d1\",\"colSpan\":2},{\"field\":\"AddToFavUser\",\"thText\":\"\\u5fae\\u4fe1\\u6536\\u85cf\\u4eba\\u6570\",\"rowSpan\":2,\"enable\":true}],[{\"field\":\"IntPageReadUser\",\"thText\":\"\\u4eba\\u6570\"},{\"field\":\"IntPageReadCount\",\"thText\":\"\\u6b21\\u6570\"},{\"field\":\"PageConversion\",\"thText\":\"\\u56fe\\u6587\\u8f6c\\u5316\\u7387\"},{\"field\":\"OriPageReadUser\",\"thText\":\"\\u4eba\\u6570\"},{\"field\":\"OriPageReadCount\",\"thText\":\"\\u6b21\\u6570\"},{\"field\":\"Conversion\",\"thText\":\"\\u539f\\u6587\\u8f6c\\u5316\\u7387\"},{\"field\":\"ShareUser\",\"thText\":\"\\u4eba\\u6570\"},{\"field\":\"ShareCount\",\"thText\":\"\\u6b21\\u6570\"}]]}",
                        "id": "205066833_1",
                        "title": "回家大作战 | 如何优雅地去往车站和机场"
                    },
                    {
                        "index": [
                            "20,745",  // 送达人数
                            "1,355",  // 图文页阅读人数
                            "1,839",  // 图文页阅读次数
                            "6.53%",  // (图文页阅读人数 / 送达人数)
                            "145",  // 原文页阅读人数
                            "184",  // 原文页阅读次数
                            "10.7%",  // （原文页阅读人数 / 图文页阅读人数)
                            "48",  // 分享转发人数
                            "64",  // 分享转发次数
                            "5"  // 微信收藏人数
                        ],
                        "time": "2015-01-19",
                        "table_data": "{\"fields\":{\"TargetUser\":{\"thText\":\"\\u9001\\u8fbe\\u4eba\\u6570\",\"number\":false,\"colAlign\":\"center\",\"needOrder\":false,\"precision\":0},\"IntPageReadUser\":{\"thText\":\"\\u4eba\\u6570\",\"number\":true,\"colAlign\":\"right\",\"needOrder\":false,\"precision\":0},\"IntPageReadCount\":{\"thText\":\"\\u6b21\\u6570\",\"number\":true,\"colAlign\":\"right\",\"needOrder\":false,\"precision\":0},\"PageConversion\":{\"thText\":\"\\u56fe\\u6587\\u8f6c\\u5316\\u7387\",\"number\":true,\"colAlign\":\"right\",\"needOrder\":false,\"precision\":\"2\"},\"OriPageReadUser\":{\"thText\":\"\\u4eba\\u6570\",\"number\":true,\"colAlign\":\"right\",\"needOrder\":false,\"precision\":0},\"OriPageReadCount\":{\"thText\":\"\\u6b21\\u6570\",\"number\":true,\"colAlign\":\"right\",\"needOrder\":false,\"precision\":0},\"Conversion\":{\"thText\":\"\\u539f\\u6587\\u8f6c\\u5316\\u7387\",\"number\":true,\"colAlign\":\"right\",\"needOrder\":false,\"precision\":\"2\"},\"ShareUser\":{\"thText\":\"\\u4eba\\u6570\",\"number\":true,\"colAlign\":\"right\",\"needOrder\":false,\"precision\":0},\"ShareCount\":{\"thText\":\"\\u6b21\\u6570\",\"number\":true,\"colAlign\":\"right\",\"needOrder\":false,\"precision\":0},\"AddToFavUser\":{\"thText\":\"\\u5fae\\u4fe1\\u6536\\u85cf\\u4eba\\u6570\",\"number\":true,\"colAlign\":\"right\",\"needOrder\":false,\"precision\":0}},\"data\":[{\"MsgId\":\"205028693_1\",\"Title\":\"\\u5145\\u7535\\u65f6\\u95f4 | \\u542c\\u542c\\u7535\\u53f0\\uff0c\\u4f18\\u96c5\\u5730\\u63d0\\u5347\\u5b66\\u4e60\\u6548\\u7387\",\"RefDate\":\"20150119\",\"TargetUser\":\"20,745\",\"IntPageReadUser\":\"1,355\",\"IntPageReadCount\":\"1,839\",\"OriPageReadUser\":\"145\",\"OriPageReadCount\":\"184\",\"ShareUser\":\"48\",\"ShareCount\":\"64\",\"AddToFavUser\":\"5\",\"Conversion\":\"10.7%\",\"PageConversion\":\"6.53%\"}],\"fixedRow\":false,\"cssSetting\":{\"\":\"\"},\"complexHeader\":[[{\"field\":\"TargetUser\",\"thText\":\"\\u9001\\u8fbe\\u4eba\\u6570\",\"rowSpan\":2,\"colSpan\":1},{\"thText\":\"\\u56fe\\u6587\\u9875\\u9605\\u8bfb\",\"colSpan\":3},{\"thText\":\"\\u539f\\u6587\\u9875\\u9605\\u8bfb\",\"colSpan\":3},{\"thText\":\"\\u5206\\u4eab\\u8f6c\\u53d1\",\"colSpan\":2},{\"field\":\"AddToFavUser\",\"thText\":\"\\u5fae\\u4fe1\\u6536\\u85cf\\u4eba\\u6570\",\"rowSpan\":2,\"enable\":true}],[{\"field\":\"IntPageReadUser\",\"thText\":\"\\u4eba\\u6570\"},{\"field\":\"IntPageReadCount\",\"thText\":\"\\u6b21\\u6570\"},{\"field\":\"PageConversion\",\"thText\":\"\\u56fe\\u6587\\u8f6c\\u5316\\u7387\"},{\"field\":\"OriPageReadUser\",\"thText\":\"\\u4eba\\u6570\"},{\"field\":\"OriPageReadCount\",\"thText\":\"\\u6b21\\u6570\"},{\"field\":\"Conversion\",\"thText\":\"\\u539f\\u6587\\u8f6c\\u5316\\u7387\"},{\"field\":\"ShareUser\",\"thText\":\"\\u4eba\\u6570\"},{\"field\":\"ShareCount\",\"thText\":\"\\u6b21\\u6570\"}]]}",
                        "id": "205028693_1",
                        "title": "充电时间 | 听听电台，优雅地提升学习效率"
                    }
                ]
            }

        :param integer page: 页码 (由于腾讯接口限制，page 从 1 开始，3 条数据为 1 页)
        :param str start_date: 开始时间，默认是今天-30天 (类型: str 格式示例: "2015-01-15")
        :param str end_date: 结束时间，默认是今天 (类型: str 格式示例: "2015-02-01")
        :return: 返回的 JSON 数据，具体的各项内容解释参见上面的 JSON 返回示例
        :raises: NeedLoginError 操作未执行成功, 需要再次尝试登录, 异常内容为服务器返回的错误数据

   .. py:method:: get_group_list()

        获取分组列表

        返回JSON示例::

            {
                "groups": [
                    {
                        "cnt": 8,
                        "id": 0,
                        "name": "未分组"
                    },
                    {
                        "cnt": 0,
                        "id": 1,
                        "name": "黑名单"
                    },
                    {
                        "cnt": 0,
                        "id": 2,
                        "name": "星标组"
                    }
                ]
            }

        :return: 返回的 JSON 数据
        :raises: NeedLoginError 操作未执行成功, 需要再次尝试登录, 异常内容为服务器返回的错误数据

   .. py:method:: get_news_list(page, pagesize=10)

        获取图文信息列表

        返回JSON示例::

            [
                {
                    "multi_item": [
                        {
                            "seq": 0,
                            "title": "98路公交线路",
                            "show_cover_pic": 1,
                            "author": "",
                            "cover": "https://mmbiz.qlogo.cn/mmbiz/D2pflbZwStFibz2Sb1kWOuHrxtDMPKJic3GQgcgkDSoEm668gClFVDt3BR8GGQ5eB8HoL4vDezzKtSblIjckOf7A/0",
                            "content_url": "http://mp.weixin.qq.com/s?__biz=MjM5MTA2ODcwOA==&mid=204884970&idx=1&sn=bf25c51f07260d4ed38305a1cbc0ce0f#rd",
                            "source_url": "",
                            "file_id": 204884939,
                            "digest": "98路线路1.农大- 2.金阳小区- 3.市客运司- 4.市制药厂- 5.新农大- 6.独山子酒店- 7.三"
                        }
                    ],
                    "seq": 0,
                    "title": "98路公交线路",
                    "show_cover_pic": 1,
                    "author": "",
                    "app_id": 204884970,
                    "content_url": "http://mp.weixin.qq.com/s?__biz=MjM5MTA2ODcwOA==&mid=204884970&idx=1&sn=bf25c51f07260d4ed38305a1cbc0ce0f#rd",
                    "create_time": "1405237966",
                    "file_id": 204884939,
                    "img_url": "https://mmbiz.qlogo.cn/mmbiz/D2pflbZwStFibz2Sb1kWOuHrxtDMPKJic3GQgcgkDSoEm668gClFVDt3BR8GGQ5eB8HoL4vDezzKtSblIjckOf7A/0",
                    "digest": "98路线路1.农大- 2.金阳小区- 3.市客运司- 4.市制药厂- 5.新农大- 6.独山子酒店- 7.三"
                },
                {
                    "multi_item": [
                        {
                            "seq": 0,
                            "title": "2013年新疆软件园大事记",
                            "show_cover_pic": 0,
                            "author": "",
                            "cover": "https://mmbiz.qlogo.cn/mmbiz/D2pflbZwStFibz2Sb1kWOuHrxtDMPKJic3icvFgkxZRyIrkLbic9I5ZKLa3XB8UqNlkT8CYibByHuraSvVoeSzdTRLQ/0",
                            "content_url": "http://mp.weixin.qq.com/s?__biz=MjM5MTA2ODcwOA==&mid=204883415&idx=1&sn=68d62215052d29ece3f2664e9c4e8cab#rd",
                            "source_url": "",
                            "file_id": 204883412,
                            "digest": "1月1．新疆软件园展厅设计方案汇报会2013年1月15日在维泰大厦4楼9号会议室召开新疆软件园展厅设计工作完"
                        },
                        {
                            "seq": 1,
                            "title": "2012年新疆软件园大事记",
                            "show_cover_pic": 0,
                            "author": "",
                            "cover": "https://mmbiz.qlogo.cn/mmbiz/D2pflbZwStFibz2Sb1kWOuHrxtDMPKJic3oErGEhSicRQc82icibxZOZ2YAGNgiaGYfOFYppmPzOOS0v1xfZ1nvyT58g/0",
                            "content_url": "http://mp.weixin.qq.com/s?__biz=MjM5MTA2ODcwOA==&mid=204883415&idx=2&sn=e7db9b30d770c85c61008d2f523b8610#rd",
                            "source_url": "",
                            "file_id": 204883398,
                            "digest": "1月1．新疆软件园环评顺利通过专家会评审2012年1月30日，新疆软件园环境影响评价顺利通过专家会评审，与会"
                        },
                        {
                            "seq": 2,
                            "title": "2011年新疆软件园大事记",
                            "show_cover_pic": 0,
                            "author": "",
                            "cover": "https://mmbiz.qlogo.cn/mmbiz/D2pflbZwStFibz2Sb1kWOuHrxtDMPKJic3qA7tEN8GvkgDwnOfKsGsicJeQ6PxQSgWuJXfQaXkpM4VNlQicOWJM4Tg/0",
                            "content_url": "http://mp.weixin.qq.com/s?__biz=MjM5MTA2ODcwOA==&mid=204883415&idx=3&sn=4cb1c6d25cbe6dfeff37f52a62532bd0#rd",
                            "source_url": "",
                            "file_id": 204883393,
                            "digest": "6月1．软件园召开第一次建设领导小组会议2011年6月7日，第一次软件园建设领导小组会议召开，会议认为，新疆"
                        },
                        {
                            "seq": 3,
                            "title": "2010年新疆软件园大事记",
                            "show_cover_pic": 0,
                            "author": "",
                            "cover": "https://mmbiz.qlogo.cn/mmbiz/D2pflbZwStFibz2Sb1kWOuHrxtDMPKJic3YG4sSuf9X9ecMPjDRju842IbIvpFWK7tuZs0Po4kZCz4URzOBj5rnQ/0",
                            "content_url": "http://mp.weixin.qq.com/s?__biz=MjM5MTA2ODcwOA==&mid=204883415&idx=4&sn=4319f7f051f36ed972e2f05a221738ec#rd",
                            "source_url": "",
                            "file_id": 204884043,
                            "digest": "5月1．新疆软件园与开发区（头屯河区）管委会、经信委签署《新疆软件园建设战略合作协议》2010年5月12日，"
                        }
                    ],
                    "seq": 1,
                    "title": "2013年新疆软件园大事记",
                    "show_cover_pic": 0,
                    "author": "",
                    "app_id": 204883415,
                    "content_url": "http://mp.weixin.qq.com/s?__biz=MjM5MTA2ODcwOA==&mid=204883415&idx=1&sn=68d62215052d29ece3f2664e9c4e8cab#rd",
                    "create_time": "1405232974",
                    "file_id": 204883412,
                    "img_url": "https://mmbiz.qlogo.cn/mmbiz/D2pflbZwStFibz2Sb1kWOuHrxtDMPKJic3icvFgkxZRyIrkLbic9I5ZKLa3XB8UqNlkT8CYibByHuraSvVoeSzdTRLQ/0",
                    "digest": "1月1．新疆软件园展厅设计方案汇报会2013年1月15日在维泰大厦4楼9号会议室召开新疆软件园展厅设计工作完"
                }
            ]

        :param integer page: 页码 (从 0 开始)
        :param integer pagesize: 每页数目
        :return: 返回的 JSON 数据
        :raises: NeedLoginError 操作未执行成功, 需要再次尝试登录, 异常内容为服务器返回的错误数据

   .. py:method:: get_dialog_message(fakeid [, last_msgid=0, create_time=0])

        获取与指定用户的对话内容, 获取的内容由 ``last_msgid`` (需要获取的对话中时间最早的 **公众号发送给用户** 的消息ID) 和 ``create_time`` (需要获取的对话中时间最早的消息时间戳) 进行过滤

        消息过滤规则:

        1. 首先按照 ``last_msgid`` 过滤 (不需要按照 ``last_msgid`` 过滤则不需要传入此参数)

            a. ``fakeid`` 为用户 UID
            b. 通过 ``last_msgid`` 去匹配公众号过去发送给用户的某一条消息
            c. 如果匹配成功, 则返回这条消息之后与这个用户相关的所有消息内容 (包括发送的消息和接收的)
            d. 如果匹配失败 (没有找到), 则返回与这个用户相关的所有消息 (包括发送的消息和接收的)

        2. 第一条规则返回的消息内容接着按照 ``create_time`` 进行过滤, 返回 ``create_time`` 时间戳之时及之后的所有消息 (不需要按照 ``create_time`` 过滤则不需要传入此参数)

        返回JSON示例::

            {
                "to_nick_name": "Doraemonext",
                "msg_items": {
                    "msg_item": [
                        {
                            "date_time": 1408671873,
                            "has_reply": 0,
                            "multi_item": [ ],
                            "msg_status": 4,
                            "nick_name": "Doraemonext",
                            "to_uin": 2391068708,
                            "content": "你呢",
                            "source": "",
                            "fakeid": "844735403",
                            "send_stat": {
                                "fail": 0,
                                "succ": 0,
                                "total": 0
                            },
                            "refuse_reason": "",
                            "type": 1,
                            "id": 206439567
                        },
                        {
                            "date_time": 1408529750,
                            "send_stat": {
                                "fail": 0,
                                "succ": 0,
                                "total": 0
                            },
                            "app_sub_type": 3,
                            "multi_item": [
                                {
                                    "seq": 0,
                                    "title": "软件企业有望拎包入住新疆软件园",
                                    "show_cover_pic": 1,
                                    "author": "",
                                    "cover": "https://mmbiz.qlogo.cn/mmbiz/D2pflbZwStFibz2Sb1kWOuHrxtDMPKJic3oErGEhSicRQc82icibxZOZ2YAGNgiaGYfOFYppmPzOOS0v1xfZ1nvyT58g/0",
                                    "content_url": "http://mp.weixin.qq.com/s?__biz=MjM5MTA2ODcwOA==&mid=204885255&idx=1&sn=40e07d236a497e36d2d3e9711dfe090a#rd",
                                    "source_url": "",
                                    "content": "",
                                    "file_id": 204885252,
                                    "vote_id": [ ],
                                    "digest": "12月8日，国家软件公共服务平台新疆分平台在乌鲁木齐经济技术开发区（头屯河区）揭牌。这意味着，软件企业有"
                                }
                            ],
                            "msg_status": 2,
                            "title": "软件企业有望拎包入住新疆软件园",
                            "nick_name": "Doraemonext",
                            "to_uin": 844735403,
                            "content_url": "http://mp.weixin.qq.com/s?__biz=MjM5MTA2ODcwOA==&mid=204885255&idx=1&sn=40e07d236a497e36d2d3e9711dfe090a#rd",
                            "show_type": 1,
                            "content": "",
                            "source": "biz",
                            "fakeid": "2391068708",
                            "file_id": 204885252,
                            "has_reply": 0,
                            "refuse_reason": "",
                            "type": 6,
                            "id": 206379033,
                            "desc": "12月8日，国家软件公共服务平台新疆分平台在乌鲁木齐经济技术开发区（头屯河区）揭牌。这意味着，软件企业有"
                        }
                    ]
                }
            }

        :param str fakeid: 用户 UID (即 fakeid )
        :param str last_msgid: 公众号之前发送给用户(fakeid)的消息 ID, 为 0 则表示全部消息
        :param str create_time: 获取这个时间戳之时及之后的消息，为 0 则表示全部消息
        :return: 返回的 JSON 数据
        :raises: NeedLoginError 操作未执行成功, 需要再次尝试登录, 异常内容为服务器返回的错误数据

   .. py:method:: send_news(fakeid, msgid)

        向指定用户发送图文消息 （必须从图文库里选取消息ID传入)

        :param str fakeid: 用户的 UID (即 fakeid)
        :param str msgid: 图文消息 ID
        :raises: NeedLoginError 操作未执行成功, 需要再次尝试登录, 异常内容为服务器返回的错误数据
        :raises: ValueError 参数出错, 具体内容有 ``fake id not exist`` 及 ``message id not exist``

   .. py:method:: add_news(news)

        在素材库中创建图文消息

        :param list news: list 对象, 其中的每个元素为一个 dict 对象, 代表一条图文, key 值分别为 ``title``, ``author``, ``summary``, ``content``, ``picture_id``, ``from_url``, 对应内容为标题, 作者, 摘要, 内容, 素材库里的图片ID(可通过 ``upload_file`` 函数上传获取), 来源链接。

                          其中必须提供的 key 值为 ``title`` 和 ``content``

                          示例::

                              [
                                  {
                                      'title': '图文标题',
                                      'author': '图文作者',
                                      'summary': '图文摘要',
                                      'content': '图文内容',
                                      'picture_id': '23412341',
                                      'from_url': 'http://www.baidu.com',
                                  },
                                  {
                                      'title': '最少图文标题',
                                      'content': '图文内容',
                                  }
                              ]
        :raises: ValueError 参数提供错误时抛出
        :raises: NeedLoginError 操作未执行成功, 需要再次尝试登录, 异常内容为服务器返回的错误数据

   .. py:method:: upload_file(filepath)

        上传素材 (图片/音频/视频)

        :param str filepath: 本地文件路径
        :return: 直接返回上传后的文件 ID (fid)
        :raises: NeedLoginError 操作未执行成功, 需要再次尝试登录, 异常内容为服务器返回的错误数据
        :raises: ValueError 参数出错, 错误原因直接打印异常即可 (常见错误内容: ``file not exist``: 找不到本地文件, ``audio too long``: 音频文件过长, ``file invalid type``: 文件格式不正确, 还有其他错误请自行检查)

   .. py:method:: send_file(fakeid, fid, type)

        向特定用户发送媒体文件

        :param str fakeid: 用户 UID (即 fakeid)
        :param str fid: 文件 ID
        :param integer type: 文件类型 (2: 图片, 3: 音频, 4: 视频)
        :raises: NeedLoginError 操作未执行成功, 需要再次尝试登录, 异常内容为服务器返回的错误数据
        :raises: ValueError 参数出错, 错误原因直接打印异常即可 (常见错误内容: ``system error`` 或 ``can not send this type of msg``: 文件类型不匹配, ``user not exist``: 用户 fakeid 不存在, ``file not exist``: 文件 fid 不存在, 还有其他错误请自行检查)

   .. py:method:: get_file_list(type, page [, count=10])

        获取素材库文件列表

        返回JSON示例::

            {
                "type": 2,
                "file_item": [
                    {
                        "update_time": 1408723089,
                        "name": "Doraemonext.png",
                        "play_length": 0,
                        "file_id": 206471048,
                        "type": 2,
                        "size": "53.7 K"
                    },
                    {
                        "update_time": 1408722328,
                        "name": "Doraemonext.png",
                        "play_length": 0,
                        "file_id": 206470809,
                        "type": 2,
                        "size": "53.7 K"
                    }
                ],
                "file_cnt": {
                    "voice_cnt": 1,
                    "app_msg_cnt": 10,
                    "commondity_msg_cnt": 0,
                    "video_cnt": 0,
                    "img_cnt": 29,
                    "video_msg_cnt": 0,
                    "total": 40
                }
            }

        :param integer type: 文件类型 (2: 图片, 3: 音频, 4: 视频)
        :param integer page: 页码 (从 0 开始)
        :param integer count: 每页大小
        :return: 返回的 JSON 数据
        :raises: NeedLoginError 操作未执行成功, 需要再次尝试登录, 异常内容为服务器返回的错误数据

   .. py:method:: send_image(fakeid, fid)

        给指定用户 fakeid 发送图片信息

        :param str fakeid: 用户的 UID (即 fakeid)
        :param str fid: 文件 ID
        :raises: NeedLoginError 操作未执行成功, 需要再次尝试登录, 异常内容为服务器返回的错误数据
        :raises: ValueError 参数出错, 错误原因直接打印异常即可 (常见错误内容: ``system error`` 或 ``can not send this type of msg``: 文件类型不匹配, ``user not exist``: 用户 fakeid 不存在, ``file not exist``: 文件 fid 不存在, 还有其他错误请自行检查)

   .. py:method:: send_audio(fakeid, fid)

        给指定用户 fakeid 发送语音信息

        :param str fakeid: 用户的 UID (即 fakeid)
        :param str fid: 文件 ID
        :raises: NeedLoginError 操作未执行成功, 需要再次尝试登录, 异常内容为服务器返回的错误数据
        :raises: ValueError 参数出错, 错误原因直接打印异常即可 (常见错误内容: ``system error`` 或 ``can not send this type of msg``: 文件类型不匹配, ``user not exist``: 用户 fakeid 不存在, ``file not exist``: 文件 fid 不存在, 还有其他错误请自行检查)

   .. py:method:: send_video(fakeid, fid)

        给指定用户 fakeid 发送视频消息

        :param str fakeid: 用户的 UID (即 fakeid)
        :param str fid: 文件 ID
        :raises: NeedLoginError 操作未执行成功, 需要再次尝试登录, 异常内容为服务器返回的错误数据
        :raises: ValueError 参数出错, 错误原因直接打印异常即可 (常见错误内容: ``system error`` 或 ``can not send this type of msg``: 文件类型不匹配, ``user not exist``: 用户 fakeid 不存在, ``file not exist``: 文件 fid 不存在, 还有其他错误请自行检查)

   .. py:method:: get_user_info(fakeid)

        获取指定用户的个人信息

        返回JSON示例::

            {
                "province": "湖北",
                "city": "武汉",
                "gender": 1,
                "nick_name": "Doraemonext",
                "country": "中国",
                "remark_name": "",
                "fake_id": 844735403,
                "signature": "",
                "group_id": 0,
                "user_name": ""
            }

        :param str fakeid: 用户的 UID (即 fakeid)
        :return: 返回的 JSON 数据
        :raises: NeedLoginError 操作未执行成功, 需要再次尝试登录, 异常内容为服务器返回的错误数据

   .. py:method:: get_avatar(fakeid)

        获取用户头像信息

        :param str fakeid: 用户的 UID (即 fakeid)
        :return: 二进制 JPG 数据字符串, 可直接作为 File Object 中 write 的参数
        :raises: NeedLoginError 操作未执行成功, 需要再次尝试登录, 异常内容为服务器返回的错误数据

   .. py:method:: get_new_message_num(lastid=0)

        获取新消息的数目

        :param lastid: 最近获取的消息 ID, 为 0 时获取总消息数目
        :return: 消息数目
        :rtype: int

   .. py:method:: get_top_message()

        获取最新一条消息

        返回JSON示例::

            {
                "msg_item": [
                    {
                        "id": 206448489,
                        "type": 2,
                        "fakeid": "844735403",
                        "nick_name": "Doraemonext",
                        "date_time": 1408696938,
                        "source": "",
                        "msg_status": 4,
                        "has_reply": 0,
                        "refuse_reason": "",
                        "multi_item": [ ],
                        "to_uin": 2391068708,
                        "send_stat": {
                            "total": 0,
                            "succ": 0,
                            "fail": 0
                        }
                    }
                ]
            }

        :return: 返回的 JSON 数据
        :raises: NeedLoginError 操作未执行成功, 需要再次尝试登录, 异常内容为服务器返回的错误数据

   .. py:method:: get_message_list(lastid=0, offset=0, count=20, day=7, star=False)

        获取消息列表

        返回JSON示例 ::

            {
                "msg_item": [
                    {
                        "id": 206439583,
                        "type": 1,
                        "fakeid": "844735403",
                        "nick_name": "Doraemonext",
                        "date_time": 1408671892,
                        "content": "测试消息",
                        "source": "",
                        "msg_status": 4,
                        "has_reply": 0,
                        "refuse_reason": "",
                        "multi_item": [ ],
                        "to_uin": 2391068708,
                        "send_stat": {
                            "total": 0,
                            "succ": 0,
                            "fail": 0
                        }
                    },
                    {
                        "id": 206439579,
                        "type": 1,
                        "fakeid": "844735403",
                        "nick_name": "Doraemonext",
                        "date_time": 1408671889,
                        "content": "wechat-python-sdk",
                        "source": "",
                        "msg_status": 4,
                        "has_reply": 0,
                        "refuse_reason": "",
                        "multi_item": [ ],
                        "to_uin": 2391068708,
                        "send_stat": {
                            "total": 0,
                            "succ": 0,
                            "fail": 0
                        }
                    }
                ]
            }

        :param integer lastid: 传入最后的消息 id 编号, 为 0 则从最新一条起倒序获取
        :param integer offset: lastid 起算第一条的偏移量
        :param integer count: 获取数目
        :param integer day: 最近几天消息 (0: 今天, 1: 昨天, 2: 前天, 3: 更早, 7: 全部), 这里的全部仅有5天
        :param boolean star: 是否只获取星标消息
        :return: 返回的 JSON 数据
        :raises: NeedLoginError 操作未执行成功, 需要再次尝试登录, 异常内容为服务器返回的错误数据

   .. py:method:: get_message_image(msgid, mode='large')

        根据消息 ID 获取图片消息内容

        :param str msgid: 消息 ID
        :param str mode: 图片尺寸 ('large'或'small')
        :return: 二进制 JPG 图片字符串, 可直接作为 File Object 中 write 的参数
        :raises: NeedLoginError 操作未执行成功, 需要再次尝试登录, 异常内容为服务器返回的错误数据
        :raises: ValueError 参数出错, 错误原因直接打印异常即可, 错误内容: ``image message not exist``: msg参数无效, ``mode error``: mode参数无效

   .. py:method:: get_message_voice(msgid)

        根据消息 ID 获取语音消息内容

        :param str msgid: 消息 ID
        :return: 二进制 MP3 音频字符串, 可直接作为 File Object 中 write 的参数
        :raises: NeedLoginError 操作未执行成功, 需要再次尝试登录, 异常内容为服务器返回的错误数据
        :raises: ValueError 参数出错, 错误原因直接打印异常即可, 错误内容: ``voice message not exist``: msg参数无效

   .. py:method:: get_message_video(msgid)

        根据消息 ID 获取视频消息内容

        :param str msgid: 消息 ID
        :return: 二进制 MP4 视频字符串, 可直接作为 File Object 中 write 的参数
        :raises: NeedLoginError 操作未执行成功, 需要再次尝试登录, 异常内容为服务器返回的错误数据
        :raises: ValueError 参数出错, 错误原因直接打印异常即可, 错误内容: ``video message not exist``: msg参数无效
