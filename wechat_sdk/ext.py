# -*- coding: utf-8 -*-

import hashlib
import re
import requests
import json

from .exceptions import UnOfficialAPIError, NeedLoginError, LoginError


class WechatExt(object):
    """
    微信扩展功能类

    通过模拟登陆的方式实现更多的高级功能, 请注意使用本类有风险, 请自行承担
    """
    def __init__(self, username, password, token=None, cookies=None, ifencodepwd=False):
        """
        :param username: 你的微信公众平台账户用户名
        :param password: 你的微信公众平台账户密码
        :param token: 直接导入的 ``token`` 值, 该值需要在上一次该类实例化之后手动进行缓存并在此传入, 如果不传入, 将会在实例化的时候自动获取
        :param cookies: 直接导入的 ``cookies`` 值, 该值需要在上一次该类实例化之后手动进行缓存并在此传入, 如果不传入, 将会在实例化的时候自动获取
        :param ifencodepwd: 密码是否已经经过编码, 如果密码已经经过加密, 此处为 ``True`` , 如果传入的密码为明文, 此处为 ``False``
        :return:
        """
        self.__username = username
        if ifencodepwd:
            self.__password = password
        else:
            self.__password = hashlib.md5(password).hexdigest()
        self.__cookies = cookies
        self.__lastmsgid = 0
        self.__token = token

        if not self.__token or not self.__cookies:
            self.__token = ''
            self.__cookies = ''
            self.login()

    def login(self):
        """
        登录微信公众平台
        注意在实例化 ``WechatExt`` 的时候，如果没有传入 ``token`` 及 ``cookies`` ，将会自动调用该方法，无需手动调用
        当且仅当捕获到 ``NeedLoginError`` 异常时才需要调用此方法进行登录重试
        :raises LoginError: 登录出错异常，异常内容为微信服务器响应的内容，可作为日志记录下来
        """
        url = 'https://mp.weixin.qq.com/cgi-bin/login?lang=zh_CN'
        payload = {
            'username': self.__username,
            'imgcode': '',
            'f': 'json',
            'pwd': self.__password,
        }
        headers = {
            'x-requested-with': 'XMLHttpRequest',
            'referer': 'https://mp.weixin.qq.com/cgi-bin/loginpage?t=wxm2-login&lang=zh_CN',
        }
        r = requests.post(url, data=payload, headers=headers)

        s = re.search(r'token=(\d+)', r.text)
        if not s:
            raise LoginError(r.text)
        self.__token = int(s.group(1))

        self.__cookies = ''
        for cookie in r.cookies:
            self.__cookies += cookie.name + '=' + cookie.value + ';'

    def send_message(self, fakeid, content):
        """
        主动发送文本消息
        :param fakeid: 用户的 UID (即 fakeid )
        :param content: 发送的内容
        :raises NeedLoginError: 操作未执行成功, 需要再次尝试登录, 异常内容为服务器返回的错误数据
        """
        url = 'https://mp.weixin.qq.com/cgi-bin/singlesend?t=ajax-response'
        payload = {
            'tofakeid': fakeid,
            'type': 1,
            'token': self.__token,
            'content': content,
            'ajax': 1,
        }
        headers = {
            'x-requested-with': 'XMLHttpRequest',
            'referer': 'https://mp.weixin.qq.com/cgi-bin/singlesendpage?t=message/send&action=index&tofakeid={fakeid}&token={token}&lang=zh_CN'.format(
                fakeid=fakeid,
                token=self.__token,
            ),
            'cookie': self.__cookies,
        }
        r = requests.post(url, data=payload, headers=headers)

        try:
            message = json.loads(r.text)
            if message['base_resp']['ret'] != 0:
                raise NeedLoginError(r.text)
        except (KeyError, ValueError):
            raise NeedLoginError(r.text)

        return message

    def get_user_list(self, page=0, pagesize=10, groupid=0):
        """
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
        :raises NeedLoginError: 操作未执行成功, 需要再次尝试登录, 异常内容为服务器返回的错误数据
        """
        url = 'https://mp.weixin.qq.com/cgi-bin/contactmanage?t=user/index&pagesize={pagesize}&pageidx={page}&type=0&groupid={groupid}&lang=zh_CN&f=json&token={token}'.format(
            pagesize=pagesize,
            page=page,
            groupid=groupid,
            token=self.__token,
        )
        headers = {
            'x-requested-with': 'XMLHttpRequest',
            'referer': 'https://mp.weixin.qq.com/cgi-bin/contactmanage?t=user/index&pagesize={pagesize}&pageidx={page}&type=0&groupid=0&lang=zh_CN&token={token}'.format(
                pagesize=pagesize,
                page=page,
                token=self.__token,
            ),
            'cookie': self.__cookies,
        }
        r = requests.get(url, headers=headers)

        try:
            message = json.loads(r.text)['contact_list']
        except (KeyError, ValueError):
            raise NeedLoginError(r.text)

        return message

    def get_group_list(self):
        """
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
        :raises NeedLoginError: 操作未执行成功, 需要再次尝试登录, 异常内容为服务器返回的错误数据
        """
        url = 'https://mp.weixin.qq.com/cgi-bin/contactmanage?t=user/index&pagesize=10&pageidx=0&type=0&groupid=0&lang=zh_CN&f=json&token={token}'.format(
            token=self.__token,
        )
        headers = {
            'x-requested-with': 'XMLHttpRequest',
            'referer': 'https://mp.weixin.qq.com/cgi-bin/contactmanage?t=user/index&pagesize=10&pageidx=0&type=0&groupid=0&lang=zh_CN&token='.format(
                token=self.__token,
            ),
            'cookie': self.__cookies,
        }
        r = requests.get(url, headers=headers)

        try:
            message = json.loads(r.text)['group_list']
        except (KeyError, ValueError):
            raise NeedLoginError(r.text)

        return message

    def get_message_list(self, lastid=0, offset=0, count=20, day=7, star=False):
        """
        获取消息列表

        返回JSON示例::
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

        :param lastid: 传入最后的消息 id 编号, 为 0 则从最新一条起倒序获取
        :param offset: lastid 起算第一条的偏移量
        :param count: 获取数目
        :param day: 最近几天消息 (0: 今天, 1: 昨天, 2: 前天, 3: 更早, 7: 全部), 这里的全部仅有5天
        :param star: 是否只获取星标消息
        :return: 返回的 JSON 数据
        :raises NeedLoginError: 操作未执行成功, 需要再次尝试登录, 异常内容为服务器返回的错误数据
        """
        if star:
            star_param = '&action=star'
        else:
            star_param = ''
        if lastid == 0:
            lastid = ''

        url = 'https://mp.weixin.qq.com/cgi-bin/message?t=message/list&f=json&lang=zh_CN{star}&count={count}&day={day}&frommsgid={lastid}&offset={offset}&token={token}'.format(
            star=star_param,
            count=count,
            day=day,
            lastid=lastid,
            offset=offset,
            token=self.__token,
        )
        headers = {
            'x-requested-with': 'XMLHttpRequest',
            'referer': 'https://mp.weixin.qq.com/cgi-bin/message?t=message/list&count=20&day=7&token={token}&lang=zh_CN'.format(token=self.__token),
            'cookie': self.__cookies,
        }
        r = requests.get(url, headers=headers)

        try:
            message = json.loads(r.text)['msg_items']
        except (KeyError, ValueError):
            raise NeedLoginError(r.text)

        return message

    # def get_news_list(self):
    #     url = 'https://mp.weixin.qq.com/cgi-bin/appmsg?token=%s&lang=zh_CN&type=10&action=list&begin=0&count=10&f=json&random=0.122' % self.token
    #     payload = {
    #         't': 'mass/send',
    #         'token': self.token,
    #     }
    #     headers = {v
    #         'x-requested-with': 'XMLHttpRequest',
    #         'referer': 'https://mp.weixin.qq.com/cgi-bin/masssendpage?t=mass/send&token=%s&lang=zh_CN' % self.token,
    #         'cookie': self.wx_cookies,
    #     }
    #
    #     r = requests.get(url, data=payload, headers=headers)