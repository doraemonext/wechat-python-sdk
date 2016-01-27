# -*- coding: utf-8 -*-

import hashlib
import re
import requests
import json
import random
import time
from datetime import timedelta, date

from .base import WechatBase
from .exceptions import UnOfficialAPIError, NeedLoginError, LoginError, LoginVerifyCodeError
from .utils import disable_urllib3_warning


class WechatExt(WechatBase):
    """
    微信扩展功能类

    通过模拟登陆的方式实现更多的高级功能, 请注意使用本类有风险, 请自行承担
    """
    def __init__(self, username, password, token=None, cookies=None, appid=None, plugin_token=None, ifencodepwd=False,
                 login=True, checkssl=False):
        """
        :param username: 你的微信公众平台账户用户名
        :param password: 你的微信公众平台账户密码
        :param token: 直接导入的 ``token`` 值, 该值需要在上一次该类实例化之后手动进行缓存并在此传入, 如果不传入, 将会在实例化的时候自动获取
        :param cookies: 直接导入的 ``cookies`` 值, 该值需要在上一次该类实例化之后手动进行缓存并在此传入, 如果不传入, 将会在实例化的时候自动获取
        :param appid: 直接导入的 ``appid`` 值, 该值需要在上一次该类实例化之后手动进行缓存并在此传入, 如果不传入, 将会在调用 stat_ 开头的方法(统计分析类)时自动获取
        :param plugin_token: 直接导入的 ``plugin_token`` 值, 该值需要在上一次该类实例化之后手动进行缓存并在此传入, 如果不传入, 将会在调用 stat_ 开头的方法(统计分析类)时自动获取
        :param ifencodepwd: 密码是否已经经过编码, 如果密码已经经过加密, 此处为 ``True`` , 如果传入的密码为明文, 此处为 ``False``
        :param login: 是否在初始化过程中尝试登录 (推荐此处设置为 ``False``, 然后手动执行登录以方便进行识别验证码等操作, 此处默认值为 ``True`` 为兼容历史版本
        :param checkssl: 是否检查 SSL, 默认为 False, 可避免 urllib3 的 InsecurePlatformWarning 警告
        """
        if not checkssl:
            disable_urllib3_warning()  # 可解决 InsecurePlatformWarning 警告

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
        self.__fakeid = None

        self.__appid = appid
        self.__plugin_token = plugin_token

        if not self.__token or not self.__cookies:
            self.__token = ''
            self.__cookies = ''
            self.__appid = ''
            self.__plugin_token = ''
            if login:
                self.login()

    def login(self, verify_code=''):
        """
        登录微信公众平台
        注意在实例化 ``WechatExt`` 的时候，如果没有传入 ``token`` 及 ``cookies`` ，将会自动调用该方法，无需手动调用
        当且仅当捕获到 ``NeedLoginError`` 异常时才需要调用此方法进行登录重试
        :param verify_code: 验证码, 不传入则为无验证码
        :raises LoginVerifyCodeError: 需要验证码或验证码出错，该异常为 ``LoginError`` 的子类
        :raises LoginError: 登录出错异常，异常内容为微信服务器响应的内容，可作为日志记录下来
        """
        url = 'https://mp.weixin.qq.com/cgi-bin/login'
        payload = {
            'username': self.__username,
            'pwd': self.__password,
            'imgcode': verify_code,
            'f': 'json',
        }
        headers = {
            'x-requested-with': 'XMLHttpRequest',
            'referer': 'https://mp.weixin.qq.com/cgi-bin/loginpage?t=wxm2-login&lang=zh_CN',
            'Cookie': self.__cookies,
        }
        r = requests.post(url, data=payload, headers=headers)

        s = re.search(r'token=(\d+)', r.text)
        if not s:
            try:
                error_code = json.loads(r.text)['base_resp']['ret']
            except (KeyError, ValueError):
                raise LoginError(r.text)

            if error_code in [-8, -27]:
                raise LoginVerifyCodeError(r.text)
            elif re.search(r'readtemplate', r.text):
                raise LoginError('You need to turn off the safety protection of wechat.')
            else:
                raise LoginError(r.text)
        self.__token = int(s.group(1))

        self.__cookies = ''
        for cookie in r.cookies:
            self.__cookies += cookie.name + '=' + cookie.value + ';'

    def get_verify_code(self, file_path):
        """
        获取登录验证码并存储
        :param file_path: 将验证码图片保存的文件路径
        """
        url = 'https://mp.weixin.qq.com/cgi-bin/verifycode'
        payload = {
            'username': self.__username,
            'r': int(random.random() * 10000000000000),
        }
        headers = {
            'referer': 'https://mp.weixin.qq.com/',
        }
        r = requests.get(url, data=payload, headers=headers, stream=True)

        self.__cookies = ''
        for cookie in r.cookies:
            self.__cookies += cookie.name + '=' + cookie.value + ';'

        with open(file_path, 'wb') as fd:
            for chunk in r.iter_content(1024):
                fd.write(chunk)

    def get_token_cookies(self):
        """
        获取当前 token 及 cookies, 供手动缓存使用

        返回 dict 示例::

            {
                'cookies': 'bizuin=3086177907;data_bizuin=3086177907;data_ticket=AgWTXTpLL+FV+bnc9yLbb3V8;slave_sid=TERlMEJ1bWFCbTlmVnRLX0lLdUpRV0pyN2k1eVkzbWhiY0NfTHVjNFRZQk1DRDRfal82UzZKWTczR3I5TFpUYjRXUDBtN1h1cmJMRTkzS3hianBHOGpHaFM0eXJiNGp6cDFWUGpqbFNyMFlyQ05GWGpseVg2T2s2Sk5DRWpnRlE=;slave_user=gh_1b2959761a7d;',
                'token': 373179898
            }

        :return: 一个 dict 对象, key 为 ``token`` 和 ``cookies``
        """
        return {
            'token': self.__token,
            'cookies': self.__cookies,
        }

    def get_plugin_token_appid(self):
        """
        获取当前 plugin_token 及 appid, 供手动缓存使用

        返回 dict 示例::

            {
                'plugin_token': 'll1D85fGDCTr4AAxC_RrFIsfaM1eajMksOjZN_eXodroIeT77QkrMfckyYdG0qj8CnvWGUPp7-mpBOs07dbuG-iwULOcyjoEvlTsghm1K34C0oj3AI8egAxGqixxhRs8',
                'appid': 'wxd0c09648a48b3798'
            }

        :return: 一个 dict 对象, key 为 ``plugin_token`` 和 ``appid``
        """
        self._init_plugin_token_appid()

        return {
            'plugin_token': self.__plugin_token,
            'appid': self.__appid,
        }

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

    def stat_article_detail_list(self, page=1, start_date=str(date.today()+timedelta(days=-30)), end_date=str(date.today())):
        """
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

        :param page: 页码 (由于腾讯接口限制，page 从 1 开始，3 条数据为 1 页)
        :param start_date: 开始时间，默认是今天-30天 (类型: str 格式示例: "2015-01-15")
        :param end_date: 结束时间，默认是今天 (类型: str 格式示例: "2015-02-01")
        :return: 返回的 JSON 数据，具体的各项内容解释参见上面的 JSON 返回示例
        :raises NeedLoginError: 操作未执行成功, 需要再次尝试登录, 异常内容为服务器返回的错误数据
        """
        self._init_plugin_token_appid()

        url = 'http://mta.qq.com/mta/wechat/ctr_article_detail/get_list?sort=RefDate%20desc&keyword=&page={page}&appid={appid}&pluginid=luopan&token={token}&from=&src=false&devtype=3&time_type=day&start_date={start_date}&end_date={end_date}&need_compare=0&app_id=&rnd={rnd}&ajax=1'.format(
            page=page,
            appid=self.__appid,
            token=self.__plugin_token,
            rnd=int(time.time()),
            start_date=start_date,
            end_date=end_date,
        )
        headers = {
            'x-requested-with': 'XMLHttpRequest',
            'referer': 'http://mta.qq.com/mta/wechat/ctr_article_detail/get_list?sort=RefDate%20desc&keyword=&page={page}&appid={appid}&pluginid=luopan&token={token}&from=&src=false&devtype=3&time_type=day&start_date={start_date}&end_date={end_date}&need_compare=0&app_id=&rnd={rnd}&ajax=1'.format(
                page=page,
                appid=self.__appid,
                token=self.__plugin_token,
                rnd=int(time.time()),
                start_date=start_date,
                end_date=end_date,
            ),
            'cookie': self.__cookies,
        }
        r = requests.get(url, headers=headers)

        if not re.search(r'wechat_token', self.__cookies):
            for cookie in r.cookies:
                self.__cookies += cookie.name + '=' + cookie.value + ';'

        try:
            data = json.loads(r.text)
            if data.get('is_session_expire'):
                raise NeedLoginError(r.text)
            message = json.dumps(data, ensure_ascii=False)
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

    def get_dialog_message(self, fakeid, last_msgid=0, create_time=0):
        """
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

        :param fakeid: 用户 UID (即 fakeid )
        :param last_msgid: 公众号之前发送给用户(fakeid)的消息 ID, 为 0 则表示全部消息
        :param create_time: 获取这个时间戳之时及之后的消息，为 0 则表示全部消息
        :return: 返回的 JSON 数据
        :raises NeedLoginError: 操作未执行成功, 需要再次尝试登录, 异常内容为服务器返回的错误数据
        """
        self._init_fakeid()

        url = 'https://mp.weixin.qq.com/cgi-bin/singlesendpage?tofakeid={fakeid}&action=sync&lastmsgfromfakeid={fromfakeid}&lastmsgid={last_msgid}&createtime={create_time}&token={token}&lang=zh_CN&f=json&ajax=1'.format(
            fakeid=fakeid,
            fromfakeid=self.__fakeid,
            last_msgid=last_msgid,
            create_time=create_time,
            token=self.__token,
        )

        headers = {
            'x-requested-with': 'XMLHttpRequest',
            'referer': 'https://mp.weixin.qq.com/cgi-bin/message?t=message/list&count=20&day=7&token={token}&lang=zh_CN'.format(token=self.__token),
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
            'lang': 'zh_CN',
            'f': 'json',
            'tofakeid': fakeid,
            'type': 10,
            'token': self.__token,
            'appmsgid': msgid,
            'app_id': msgid,
            'error': 'false',
            'ajax': 1,
            'random': random.random(),
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

    def add_news(self, news):
        """
        在素材库中创建图文消息

        :param news: list 对象, 其中的每个元素为一个 dict 对象, 代表一条图文, key 值分别为 ``title``, ``author``, ``summary``,
                     ``content``, ``picture_id``, ``from_url``, 对应内容为标题, 作者, 摘要, 内容, 素材库里的
                     图片ID(可通过 ``upload_file`` 函数上传获取), 来源链接。

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
        :raises ValueError: 参数提供错误时抛出
        :raises NeedLoginError: 操作未执行成功, 需要再次尝试登录, 异常内容为服务器返回的错误数据
        """
        if not news:
            raise ValueError('The news cannot be empty')
        for item in news:
            if 'title' not in item or 'content' not in item:
                raise ValueError('The news item needs to provide at least two arguments: title, content')

        url = 'https://mp.weixin.qq.com/cgi-bin/operate_appmsg?lang=zh_CN&t=ajax-response&sub=create&token={token}'.format(
            token=self.__token,
        )
        payload = {
            'token': self.__token,
            'type': 10,
            'lang': 'zh_CN',
            'sub': 'create',
            'ajax': 1,
            'AppMsgId': '',
            'error': 'false',
        }
        headers = {
            'referer': 'https://mp.weixin.qq.com/cgi-bin/operate_appmsg?lang=zh_CN&sub=edit&t=wxm-appmsgs-edit-new&type=10&subtype=3&token={token}'.format(
                token=self.__token
            ),
            'cookie': self.__cookies,
        }
        i = 0
        for item in news:
            payload['title'+str(i)] = item.get('title')
            payload['author'+str(i)] = item.get('author')
            payload['digest'+str(i)] = item.get('summary')
            payload['content'+str(i)] = item.get('content')
            payload['fileid'+str(i)] = item.get('picture_id')
            payload['sourceurl'+str(i)] = item.get('from_url')
            i += 1
        payload['count'] = i
        r = requests.post(url, data=payload, headers=headers)

        try:
            message = json.loads(r.text)
        except ValueError:
            raise NeedLoginError(r.text)
        try:
            if message['ret'] != '0':
                raise ValueError(r.text)
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

    def send_file(self, fakeid, fid, type):
        """
        向特定用户发送媒体文件
        :param fakeid: 用户 UID (即 fakeid)
        :param fid: 文件 ID
        :param type: 文件类型 (2: 图片, 3: 音频, 15: 视频)
        :raises NeedLoginError: 操作未执行成功, 需要再次尝试登录, 异常内容为服务器返回的错误数据
        :raises ValueError: 参数出错, 错误原因直接打印异常即可 (常见错误内容: ``system error`` 或 ``can not send this type of msg``: 文件类型不匹配, ``user not exist``: 用户 fakeid 不存在, ``file not exist``: 文件 fid 不存在, 还有其他错误请自行检查)
        """
        if type == 4:  # 此处判断为兼容历史版本, 微信官方已经将视频类型修改为 15
            type = 15

        url = 'https://mp.weixin.qq.com/cgi-bin/singlesend?t=ajax-response&f=json&token={token}&lang=zh_CN'.format(
            token=self.__token,
        )
        payloads = {}
        if type == 2 or type == 3:  # 如果文件类型是图片或者音频
            payloads = {
                'token': self.__token,
                'lang': 'zh_CN',
                'f': 'json',
                'ajax': 1,
                'random': random.random(),
                'type': type,
                'file_id': fid,
                'tofakeid': fakeid,
                'fileid': fid,
                'imgcode': '',
            }
        elif type == 15:  # 如果文件类型是视频
            payloads = {
                'token': self.__token,
                'lang': 'zh_CN',
                'f': 'json',
                'ajax': 1,
                'random': random.random(),
                'type': type,
                'app_id': fid,
                'tofakeid': fakeid,
                'appmsgid': fid,
                'imgcode': '',
            }
        headers = {
            'referer': 'https://mp.weixin.qq.com/cgi-bin/singlesendpage?tofakeid={fakeid}&t=message/send&action=index&token={token}&lang=zh_CN'.format(
                fakeid=fakeid,
                token=self.__token,
            ),
            'cookie': self.__cookies,
            'x-requested-with': 'XMLHttpRequest',
        }
        r = requests.post(url, data=payloads, headers=headers)

        try:
            message = json.loads(r.text)
        except ValueError:
            raise NeedLoginError(r.text)
        try:
            if message['base_resp']['ret'] != 0:
                raise ValueError(message['base_resp']['err_msg'])
        except KeyError:
            raise NeedLoginError(r.text)

    def get_file_list(self, type, page, count=10):
        """
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

        :param type: 文件类型 (2: 图片, 3: 音频, 4: 视频)
        :param page: 页码 (从 0 开始)
        :param count: 每页大小
        :return: 返回的 JSON 数据
        :raises NeedLoginError: 操作未执行成功, 需要再次尝试登录, 异常内容为服务器返回的错误数据
        """
        url = 'https://mp.weixin.qq.com/cgi-bin/filepage?token={token}&lang=zh_CN&type={type}&random={random}&begin={begin}&count={count}&f=json'.format(
            token=self.__token,
            type=type,
            random=round(random.random(), 3),
            begin=page*count,
            count=count,
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

    def send_image(self, fakeid, fid):
        """
        给指定用户 fakeid 发送图片信息
        :param fakeid: 用户的 UID (即 fakeid)
        :param fid: 文件 ID
        :raises NeedLoginError: 操作未执行成功, 需要再次尝试登录, 异常内容为服务器返回的错误数据
        :raises ValueError: 参数出错, 错误原因直接打印异常即可 (常见错误内容: ``system error`` 或 ``can not send this type of msg``: 文件类型不匹配, ``user not exist``: 用户 fakeid 不存在, ``file not exist``: 文件 fid 不存在, 还有其他错误请自行检查)
        """
        return self.send_file(fakeid, fid, 2)

    def send_audio(self, fakeid, fid):
        """
        给指定用户 fakeid 发送语音信息
        :param fakeid: 用户的 UID (即 fakeid)
        :param fid: 文件 ID
        :raises NeedLoginError: 操作未执行成功, 需要再次尝试登录, 异常内容为服务器返回的错误数据
        :raises ValueError: 参数出错, 错误原因直接打印异常即可 (常见错误内容: ``system error`` 或 ``can not send this type of msg``: 文件类型不匹配, ``user not exist``: 用户 fakeid 不存在, ``file not exist``: 文件 fid 不存在, 还有其他错误请自行检查)
        """
        return self.send_file(fakeid, fid, 3)

    def send_video(self, fakeid, fid):
        """
        给指定用户 fakeid 发送视频消息
        :param fakeid: 用户的 UID (即 fakeid)
        :param fid: 文件 ID
        :raises NeedLoginError: 操作未执行成功, 需要再次尝试登录, 异常内容为服务器返回的错误数据
        :raises ValueError: 参数出错, 错误原因直接打印异常即可 (常见错误内容: ``system error`` 或 ``can not send this type of msg``: 文件类型不匹配, ``user not exist``: 用户 fakeid 不存在, ``file not exist``: 文件 fid 不存在, 还有其他错误请自行检查)
        """
        return self.send_file(fakeid, fid, 15)

    def get_user_info(self, fakeid):
        """
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

        :param fakeid: 用户的 UID (即 fakeid)
        :return: 返回的 JSON 数据
        :raises NeedLoginError: 操作未执行成功, 需要再次尝试登录, 异常内容为服务器返回的错误数据
        """
        url = 'https://mp.weixin.qq.com/cgi-bin/getcontactinfo'
        payloads = {
            'ajax': 1,
            'lang': 'zh_CN',
            'random': round(random.random(), 3),
            'token': self.__token,
            't': 'ajax-getcontactinfo',
            'fakeid': fakeid,
        }
        headers = {
            'x-requested-with': 'XMLHttpRequest',
            'referer': 'https://mp.weixin.qq.com/cgi-bin/getmessage?t=wxm-message&lang=zh_CN&count=50&token={token}'.format(
                token=self.__token,
            ),
            'cookie': self.__cookies,
        }
        r = requests.post(url, data=payloads, headers=headers)

        try:
            message = json.dumps(json.loads(r.text)['contact_info'], ensure_ascii=False)
        except (KeyError, ValueError):
            raise NeedLoginError(r.text)

        return message

    def get_avatar(self, fakeid):
        """
        获取用户头像信息
        :param fakeid: 用户的 UID (即 fakeid)
        :return: 二进制 JPG 数据字符串, 可直接作为 File Object 中 write 的参数
        :raises NeedLoginError: 操作未执行成功, 需要再次尝试登录, 异常内容为服务器返回的错误数据
        """
        url = 'https://mp.weixin.qq.com/misc/getheadimg?fakeid={fakeid}&token={token}&lang=zh_CN'.format(
            fakeid=fakeid,
            token=self.__token,
        )
        headers = {
            'x-requested-with': 'XMLHttpRequest',
            'referer': 'https://mp.weixin.qq.com/cgi-bin/getmessage?t=wxm-message&lang=zh_CN&count=50&token={token}'.format(
                token=self.__token,
            ),
            'cookie': self.__cookies,
        }
        r = requests.get(url, headers=headers, stream=True)

        return r.raw.data

    def get_new_message_num(self, lastid=0):
        """
        获取新消息的数目
        :param lastid: 最近获取的消息 ID, 为 0 时获取总消息数目
        :return: 消息数目
        """
        url = 'https://mp.weixin.qq.com/cgi-bin/getnewmsgnum?f=json&t=ajax-getmsgnum&lastmsgid={lastid}&token={token}&lang=zh_CN'.format(
            lastid=lastid,
            token=self.__token,
        )
        payloads = {
            'ajax': 1,
            'f': 'json',
            'random': random.random(),
            'lang': 'zh_CN',
            'token': self.__token,
        }
        headers = {
            'x-requested-with': 'XMLHttpRequest',
            'referer': 'https://mp.weixin.qq.com/cgi-bin/message?t=message/list&count=20&day=7&token={token}&lang=zh_CN'.format(
                token=self.__token,
            ),
            'cookie': self.__cookies,
        }
        r = requests.get(url, data=payloads, headers=headers)

        try:
            return int(json.loads(r.text)['newTotalMsgCount'])
        except (KeyError, ValueError):
            raise NeedLoginError(r.text)

    def get_top_message(self):
        """
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
        :raises NeedLoginError: 操作未执行成功, 需要再次尝试登录, 异常内容为服务器返回的错误数据
        """
        return self.get_message_list(count=1)

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

    def get_message_image(self, msgid, mode='large'):
        """
        根据消息 ID 获取图片消息内容
        :param msgid: 消息 ID
        :param mode: 图片尺寸 ('large'或'small')
        :return: 二进制 JPG 图片字符串, 可直接作为 File Object 中 write 的参数
        :raises NeedLoginError: 操作未执行成功, 需要再次尝试登录, 异常内容为服务器返回的错误数据
        :raises ValueError: 参数出错, 错误原因直接打印异常即可, 错误内容: ``image message not exist``: msg参数无效, ``mode error``: mode参数无效
        """
        if mode != 'large' and mode != 'small':
            raise ValueError('mode error')

        url = 'https://mp.weixin.qq.com/cgi-bin/getimgdata?token={token}&msgid={msgid}&mode={mode}&source=&fileId=0'.format(
            msgid=msgid,
            token=self.__token,
            mode=mode,
        )
        headers = {
            'x-requested-with': 'XMLHttpRequest',
            'referer': 'https://mp.weixin.qq.com/cgi-bin/message?t=message/list&token={token}&count=20&day=7'.format(
                token=self.__token,
            ),
            'cookie': self.__cookies,
        }
        r = requests.get(url, headers=headers, stream=True)

        # 检测会话是否超时
        if r.headers.get('content-type', None) == 'text/html; charset=UTF-8':
            raise NeedLoginError(r.text)
        # 检测图片是否存在
        if not r.raw.data:
            raise ValueError('image message not exist')

        return r.raw.data

    def get_message_voice(self, msgid):
        """
        根据消息 ID 获取语音消息内容
        :param msgid: 消息 ID
        :return: 二进制 MP3 音频字符串, 可直接作为 File Object 中 write 的参数
        :raises NeedLoginError: 操作未执行成功, 需要再次尝试登录, 异常内容为服务器返回的错误数据
        :raises ValueError: 参数出错, 错误原因直接打印异常即可, 错误内容: ``voice message not exist``: msg参数无效
        """
        url = 'https://mp.weixin.qq.com/cgi-bin/getvoicedata?msgid={msgid}&fileid=&token={token}&lang=zh_CN'.format(
            msgid=msgid,
            token=self.__token,
        )
        headers = {
            'x-requested-with': 'XMLHttpRequest',
            'referer': 'https://mp.weixin.qq.com/cgi-bin/message?t=message/list&token={token}&count=20&day=7'.format(
                token=self.__token,
            ),
            'cookie': self.__cookies,
        }
        r = requests.get(url, headers=headers, stream=True)

        # 检测会话是否超时
        if r.headers.get('content-type', None) == 'text/html; charset=UTF-8':
            raise NeedLoginError(r.text)
        # 检测语音是否存在
        if not r.raw.data:
            raise ValueError('voice message not exist')

        return r.raw.data

    def get_message_video(self, msgid):
        """
        根据消息 ID 获取视频消息内容
        :param msgid: 消息 ID
        :return: 二进制 MP4 视频字符串, 可直接作为 File Object 中 write 的参数
        :raises NeedLoginError: 操作未执行成功, 需要再次尝试登录, 异常内容为服务器返回的错误数据
        :raises ValueError: 参数出错, 错误原因直接打印异常即可, 错误内容: ``video message not exist``: msg参数无效
        """
        url = 'https://mp.weixin.qq.com/cgi-bin/getvideodata?msgid={msgid}&fileid=&token={token}'.format(
            msgid=msgid,
            token=self.__token,
        )
        headers = {
            'x-requested-with': 'XMLHttpRequest',
            'referer': 'https://mp.weixin.qq.com/cgi-bin/message?t=message/list&token={token}&count=20&day=7'.format(
                token=self.__token,
            ),
            'cookie': self.__cookies,
        }
        r = requests.get(url, headers=headers, stream=True)

        # 检测会话是否超时
        if r.headers.get('content-type', None) == 'text/html; charset=UTF-8':
            raise NeedLoginError(r.text)
        # 检测视频是否存在
        if not r.raw.data:
            raise ValueError('video message not exist')

        return r.raw.data

    def _init_fakeid(self):
        """
        初始化公众号自身的 ``fakeid`` 值
        :raises NeedLoginError: 操作未执行成功, 需要再次尝试登录, 异常内容为服务器返回的错误数据
        """
        if not self.__fakeid:
            self._init_self_information()

    def _init_ticket(self):
        """
        初始化公众号自身的 ``ticket`` 及 ``ticket_id`` 值
        :raises NeedLoginError: 操作未执行成功, 需要再次尝试登录, 异常内容为服务器返回的错误数据
        """
        if not self.__ticket:
            self._init_self_information()

    def _init_self_information(self):
        """
        初始化公众号自身的属性值 (目前包括 ``Ticket`` 值 及 公众号自身的 ``fakeid`` 值)
        :raises NeedLoginError: 操作未执行成功, 需要再次尝试登录, 异常内容为服务器返回的错误数据
        """
        url = 'https://mp.weixin.qq.com/cgi-bin/home?t=home/index&lang=zh_CN&token={token}'.format(token=self.__token)
        headers = {
            'x-requested-with': 'XMLHttpRequest',
            'referer': 'https://mp.weixin.qq.com',
            'cookie': self.__cookies,
        }
        r = requests.get(url, headers=headers)

        # 获取 Ticket ID 值
        ticket_id = re.search(r'user_name:\"(.*)\"', r.text)
        if not ticket_id:
            raise NeedLoginError(r.text)
        self.__ticket_id = ticket_id.group(1)

        # 获取 Ticket 值
        ticket = re.search(r'ticket:\"(.*)\"', r.text)
        if not ticket:
            raise NeedLoginError(r.text)
        self.__ticket = ticket.group(1)

        # 获取公众号自身的 fakeid 值
        fakeid = re.search(r'uin:\"(.*)\"', r.text)
        if not fakeid:
            raise NeedLoginError(r.text)
        self.__fakeid = fakeid.group(1)

    def _init_appid(self):
        """
        初始化公众号自身的 ``appid`` 值
        :raises NeedLoginError: 操作未执行成功, 需要再次尝试登录, 异常内容为服务器返回的错误数据
        """
        if not self.__appid:
            self._init_plugin_token_appid()

    def _init_plugin_token(self):
        """
        初始化公众号自身的 ``PluginToken`` 值
        :raises NeedLoginError: 操作未执行成功, 需要再次尝试登录, 异常内容为服务器返回的错误数据
        """
        if not self.__plugin_token:
            self._init_plugin_token_appid()

    def _init_plugin_token_appid(self):
        """
        初始化公众号的 ``PluginToken`` 值及公众号自身的 ``appid`` 值
        :raises NeedLoginError: 操作未执行成功, 需要再次尝试登录, 异常内容为服务器返回的错误数据
        """
        if not self.__plugin_token or not self.__appid:
            url = 'https://mp.weixin.qq.com/misc/pluginloginpage?action=stat_article_detail&pluginid=luopan&t=statistics/index&token={token}&lang=zh_CN'.format(
                token=self.__token,
            )
            headers = {
                'x-requested-with': 'XMLHttpRequest',
                'referer': 'https://mp.weixin.qq.com/misc/pluginloginpage?action=stat_article_detail&pluginid=luopan&t=statistics/index&token={token}&lang=zh_CN'.format(
                    token=self.__token,
                ),
                'cookie': self.__cookies,
            }
            r = requests.get(url, headers=headers)

            plugin_token = re.search(r"pluginToken : '(\S+)',", r.text)
            if not plugin_token:
                raise NeedLoginError(r.text)
            self.__plugin_token = plugin_token.group(1)

            appid = re.search(r"appid : '(\S+)',", r.text)
            if not appid:
                raise NeedLoginError(r.text)
            self.__appid = appid.group(1)