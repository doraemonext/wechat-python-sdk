# -*- coding: utf-8 -*-

import hashlib
import re
import requests
import json
import random

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
        self.__ticket = None
        self.__ticket_id = None

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
        :raises ValueError: 参数出错, 具体内容有 ``fake id not exist``
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
        except ValueError:
            raise NeedLoginError(r.text)
        try:
            if message['base_resp']['ret'] == -21:
                raise ValueError('fake id not exist')
            if message['base_resp']['ret'] != 0:
                raise NeedLoginError(r.text)
        except KeyError:
            raise NeedLoginError(r.text)

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

    def get_news_list(self, page, pagesize=10):
        """
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

        :param page: 页码 (从 0 开始)
        :param pagesize: 每页数目
        :return: 返回的 JSON 数据
        :raises NeedLoginError: 操作未执行成功, 需要再次尝试登录, 异常内容为服务器返回的错误数据
        """
        begin = page * pagesize
        url = "https://mp.weixin.qq.com/cgi-bin/appmsg?token={token}&lang=zh_CN&type=10&action=list&begin={begin}&count={pagesize}&f=json&random={random}".format(
            token=self.__token,
            begin=begin,
            pagesize=pagesize,
            random=round(random.random(), 3),
        )
        headers = {
            'x-requested-with': 'XMLHttpRequest',
            'referer': 'https://mp.weixin.qq.com/cgi-bin/masssendpage?t=mass/send&token={token}&lang=zh_CN'.format(
                token=self.__token,
            ),
            'cookie': self.__cookies,
        }
        r = requests.get(url, headers=headers)

        try:
            message = json.dumps(json.loads(r.text)['app_msg_info']['item'], ensure_ascii=False)
        except (KeyError, ValueError):
            raise NeedLoginError(r.text)

        return message

    def get_dialog_message(self, fakeid):
        """
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

        :param fakeid: 用户 UID (即 fakeid)
        :return: 返回的 JSON 数据
        :raises NeedLoginError: 操作未执行成功, 需要再次尝试登录, 异常内容为服务器返回的错误数据
        """
        url = 'https://mp.weixin.qq.com/cgi-bin/singlesendpage?t=message/send&action=index&tofakeid={fakeid}&token={token}&lang=zh_CN&f=json&random={random}'.format(
            fakeid=fakeid,
            token=self.__token,
            random=round(random.random(), 3),
        )
        headers = {
            'x-requested-with': 'XMLHttpRequest',
            'referer': 'https://mp.weixin.qq.com/cgi-bin/masssendpage?t=mass/send&token={token}&lang=zh_CN'.format(
                token=self.__token,
            ),
            'cookie': self.__cookies,
        }
        r = requests.get(url, headers=headers)

        try:
            message = json.dumps(json.loads(r.text)['page_info'], ensure_ascii=False)
        except (KeyError, ValueError):
            raise NeedLoginError(r.text)

        return message

    def send_news(self, fakeid, msgid):
        """
        向指定用户发送图文消息 （必须从图文库里选取消息ID传入)
        :param fakeid: 用户的 UID (即 fakeid)
        :param msgid: 图文消息 ID
        :raises NeedLoginError: 操作未执行成功, 需要再次尝试登录, 异常内容为服务器返回的错误数据
        :raises ValueError: 参数出错, 具体内容有 ``fake id not exist`` 及 ``message id not exist``
        """
        url = 'https://mp.weixin.qq.com/cgi-bin/singlesend?t=ajax-response'
        payload = {
            'tofakeid': fakeid,
            'type': 10,
            'token': self.__token,
            'fid': msgid,
            'appmsgid': msgid,
            'error': 'false',
            'ajax': 1,
        }
        headers = {
            'x-requested-with': 'XMLHttpRequest',
            'referer': 'https://mp.weixin.qq.com/cgi-bin/singlemsgpage?fromfakeid={fakeid}&msgid=&source=&count=20&t=wxm-singlechat&lang=zh_CN'.format(
                fakeid=fakeid,
            ),
            'cookie': self.__cookies,
        }
        r = requests.post(url, data=payload, headers=headers)

        try:
            message = json.loads(r.text)
        except ValueError:
            raise NeedLoginError(r.text)
        try:
            if message['base_resp']['ret'] == 10700 or message['base_resp']['ret'] == -21:
                raise ValueError('fake id not exist')
            if message['base_resp']['ret'] == 10705:
                raise ValueError('message id not exist')
            if message['base_resp']['ret'] != 0:
                raise NeedLoginError(r.text)
        except KeyError:
            raise NeedLoginError(r.text)

    def upload_file(self, filepath):
        """
        上传素材 (图片/音频/视频)
        :param filepath: 本地文件路径
        :return: 直接返回上传后的文件 ID (fid)
        :raises NeedLoginError: 操作未执行成功, 需要再次尝试登录, 异常内容为服务器返回的错误数据
        :raises ValueError: 参数出错, 错误原因直接打印异常即可 (常见错误内容: ``file not exist``: 找不到本地文件, ``audio too long``: 音频文件过长, ``file invalid type``: 文件格式不正确, 还有其他错误请自行检查)
        """
        if not self.__ticket:
            self._init_ticket()

        url = 'https://mp.weixin.qq.com/cgi-bin/filetransfer?action=upload_material&f=json&ticket_id={ticket_id}&ticket={ticket}&token={token}&lang=zh_CN'.format(
            ticket_id=self.__ticket_id,
            ticket=self.__ticket,
            token=self.__token,
        )
        try:
            files = {'file': open(filepath, 'rb')}
        except IOError:
            raise ValueError('file not exist')
        payloads = {
            'Filename': filepath,
            'folder': '/cgi-bin/uploads',
            'Upload': 'Submit Query',
        }
        headers = {
            'referer': 'http://mp.weixin.qq.com/cgi-bin/indexpage?t=wxm-upload&lang=zh_CN&type=2&formId=1',
            'cookie': self.__cookies,
        }
        r = requests.post(url, files=files, data=payloads, headers=headers)

        try:
            message = json.loads(r.text)
        except ValueError:
            raise NeedLoginError(r.text)
        try:
            if message['base_resp']['ret'] != 0:
                raise ValueError(message['base_resp']['err_msg'])
        except KeyError:
            raise NeedLoginError(r.text)

        return message['content']

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

    def _init_ticket(self):
        """
        初始化 Ticket 值
        :raises NeedLoginError: 操作未执行成功, 需要再次尝试登录, 异常内容为服务器返回的错误数据
        """
        url = 'https://mp.weixin.qq.com/cgi-bin/home?t=home/index&lang=zh_CN&token={token}'.format(token=self.__token)
        headers = {
            'x-requested-with': 'XMLHttpRequest',
            'referer': 'https://mp.weixin.qq.com',
            'cookie': self.__cookies,
        }
        r = requests.get(url, headers=headers)

        ticket_id = re.search(r'user_name:\"(.*)\"', r.text)
        if not ticket_id:
            raise NeedLoginError(r.text)
        self.__ticket_id = ticket_id.group(1)
        ticket = re.search(r'ticket:\"(.*)\"', r.text)
        if not ticket:
            raise NeedLoginError(r.text)
        self.__ticket = ticket.group(1)
