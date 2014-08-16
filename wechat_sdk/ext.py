# -*- coding: utf-8 -*-

import hashlib
import re
import requests

from .exceptions import UnOfficialAPIError, NeedLoginError, LoginError


class WechatExt(object):
    """
    微信扩展功能类

    通过模拟登陆的方式实现更多的高级功能, 请注意使用本类有风险, 请自行承担
    """
    def __init__(self, account, pwd, token=None, cookies=None, ifencodepwd=False):
        """
        :param account: 账户名称(用户名)
        :param pwd: 密码
        :param token: token
        :param cookies: cookie
        :param ifencodepwd: 密码是否已加密
        :return:
        """
        self.account = account
        if ifencodepwd:
            self.pwd = pwd
        else:
            self.pwd = hashlib.md5(pwd).hexdigest()
        self.wx_cookies = cookies
        self.lastmsgid = 0
        self.token = token

        if not self.token or not self.wx_cookies:
            self.token = ''
            self.wx_cookies = ''
            self.login()

    def login(self):
        """
        模拟登陆微信公众平台
        :raises LoginError: 登录出错
        """
        url = 'https://mp.weixin.qq.com/cgi-bin/login?lang=zh_CN'
        payload = {
            'username': self.account,
            'imgcode': '',
            'f': 'json',
            'pwd': self.pwd,
        }
        headers = {
            'x-requested-with': 'XMLHttpRequest',
            'referer': 'https://mp.weixin.qq.com/cgi-bin/loginpage?t=wxm2-login&lang=zh_CN',
        }
        r = requests.post(url, data=payload, headers=headers)

        s = re.search(r'token=(\d+)', r.text)
        if not s:
            raise LoginError()
        self.token = int(s.group(1))

        self.wx_cookies = ''
        for cookie in r.cookies:
            self.wx_cookies += cookie.name + '=' + cookie.value + ';'

    def get_message_list(self):
        """
        获取消息列表
        :return: 返回的 JSON 数据
        :raises NeedLoginError: 需要再次尝试登录
        """
        url = 'https://mp.weixin.qq.com/cgi-bin/message?t=message/list&token=%s&count=20&day=7' % self.token
        payload = {
            't': 'message/list',
            'token': self.token,
            'count': 20,
            'day': 7,
        }
        headers = {
            'x-requested-with': 'XMLHttpRequest',
            'referer': 'https://mp.weixin.qq.com/cgi-bin/loginpage?t=wxm2-login&lang=zh_CN',
            'cookie': self.wx_cookies,
        }

        r = requests.get(url, data=payload, headers=headers)

        c = "".join(r.text.split())
        s = re.search(r'list:\((.*)\).msg_item', c)
        if not s:
            raise NeedLoginError()
        else:
            msg_list = s.group(1)
        return msg_list

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