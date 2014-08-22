微信非官方接口操作 WechatExt
============================

.. py:class:: wechat_sdk.ext.WechatExt(username, password [, token=None, cookies=None, ifencodepwd=False])

    微信扩展功能类

    :param str username: 你的微信公众平台账户用户名
    :param str password: 你的微信公众平台账户密码
    :param str token: 直接导入的 ``token`` 值, 该值需要在上一次该类实例化之后手动进行缓存并在此传入, 如果不传入, 将会在实例化的时候自动获取
    :param str cookies: 直接导入的 ``cookies`` 值, 该值需要在上一次该类实例化之后手动进行缓存并在此传入, 如果不传入, 将会在实例化的时候自动获取
    :param str ifencodepwd: 密码是否已经经过编码, 如果密码已经经过加密, 此处为 ``True`` , 如果传入的密码为明文, 此处为 ``False``

    .. py:method:: login()

        登录微信公众平台

        注意在实例化 ``WechatExt`` 的时候，如果没有传入 ``token`` 及 ``cookies`` ，将会自动调用该方法，无需手动调用

        当且仅当捕获到 ``NeedLoginError`` 异常时才需要调用此方法进行登录重试

        :raises: LoginError 登录出错异常，异常内容为微信服务器响应的内容，可作为日志记录下来

    .. py:method:: send_message(fakeid, content)

        主动发送文本消息

        :param str fakeid: 用户的 UID (即 fakeid )
        :param str content: 发送的内容
        :raises: NeedLoginError 操作未执行成功, 需要再次尝试登录, 异常内容为服务器返回的错误数据

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