微信非官方接口操作 WechatExt
============================

.. py:class:: wechat_sdk.ext.WechatExt(username, password [, token=None, cookies=None, ifencodepwd=False])

    微信扩展功能类

    :param str username: 你的微信公众平台账户用户名
    :param str password: 你的微信公众平台账户密码
    :param str token: 直接导入的 ``token`` 值, 该值需要在上一次该类实例化之后手动进行缓存并在此传入, 如果不传入, 将会在实例化的时候自动获取
    :param str cookies: 直接导入的 ``cookies`` 值, 该值需要在上一次该类实例化之后手动进行缓存并在此传入, 如果不传入, 将会在实例化的时候自动获取
    :param str ifencodepwd: 密码是否已经经过编码, 如果密码已经经过加密, 此处为 ``True`` , 如果传入的密码为明文, 此处为 ``False``

    **实例化说明：**

    1. 当实例化 WechatExt 时，你必须传入 ``username`` 和 ``password`` ，对于 ``token`` 和 ``cookies`` 参数，如果传入，将会自动省略登录过程，但请保证你的代码中会捕获 ``NeedLoginError`` 异常，一旦发生此异常，你需要重新调用 :func:`login` 方法登录来获取新的 ``token`` 及 ``cookies``。

    2. **详细说明一下 token 及 cookies 参数的传入问题：**

     因为此开发包并不打算以服务器的方式常驻，所以，每次请求均会重新实例化 ``WechatExt`` ，所以需要你以你自己的方式去保存上一次请求中实例化后的 ``WechatExt`` 中 ``token`` 及 ``cookies`` 参数，并在下一次的实例化的过程中传入，以此来保证不会频繁登录。

     获取 ``token`` 及 ``cookies`` 的方式为调用 :func:`get_token_cookies` 方法

     下一版本将会考虑更为简单通用的方法，在新版本发布之前，请用你自己的方式把得到的 ``token`` 及 ``cookies`` 保存起来，不管是文件，缓存还是数据库都可以，只要在实例化后，你可以在任何时间调用 :func:`get_token_cookes` 方法。

    .. py:method:: login()

        登录微信公众平台

        注意在实例化 ``WechatExt`` 的时候，如果没有传入 ``token`` 及 ``cookies`` ，将会自动调用该方法，无需手动调用

        当且仅当捕获到 ``NeedLoginError`` 异常时才需要调用此方法进行登录重试

        :raises: LoginError 登录出错异常，异常内容为微信服务器响应的内容，可作为日志记录下来

    .. py:method:: get_token_cookies()

        获取当前 token 及 cookies, 供手动缓存使用

        返回 dict 示例::

            {
                'cookies': 'bizuin=3086177907;data_bizuin=3086177907;data_ticket=AgWTXTpLL+FV+bnc9yLbb3V8;slave_sid=TERlMEJ1bWFCbTlmVnRLX0lLdUpRV0pyN2k1eVkzbWhiY0NfTHVjNFRZQk1DRDRfal82UzZKWTczR3I5TFpUYjRXUDBtN1h1cmJMRTkzS3hianBHOGpHaFM0eXJiNGp6cDFWUGpqbFNyMFlyQ05GWGpseVg2T2s2Sk5DRWpnRlE=;slave_user=gh_1b2959761a7d;',
                'token': 373179898
            }

        :return: 一个 dict 对象, key 为 ``token`` 和 ``cookies``

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

        :param page: 页码 (从 0 开始)
        :param pagesize: 每页大小
        :param groupid: 分组 ID
        :return: 返回的 JSON 数据
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

    .. py:method:: get_dialog_message(fakeid)

        获取与指定用户的对话内容

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

        :param str fakeid: 用户 UID (即 fakeid)
        :return: 返回的 JSON 数据
        :raises: NeedLoginError 操作未执行成功, 需要再次尝试登录, 异常内容为服务器返回的错误数据

    .. py:method:: send_news(fakeid, msgid)

        向指定用户发送图文消息 （必须从图文库里选取消息ID传入)

        :param str fakeid: 用户的 UID (即 fakeid)
        :param str msgid: 图文消息 ID
        :raises: NeedLoginError 操作未执行成功, 需要再次尝试登录, 异常内容为服务器返回的错误数据
        :raises: ValueError 参数出错, 具体内容有 ``fake id not exist`` 及 ``message id not exist``

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
                        "size": "53.7	K"
                    },
                    {
                        "update_time": 1408722328,
                        "name": "Doraemonext.png",
                        "play_length": 0,
                        "file_id": 206470809,
                        "type": 2,
                        "size": "53.7	K"
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