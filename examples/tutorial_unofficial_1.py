# -*- coding: utf-8

import json

from wechat_sdk import WechatExt


wechat = WechatExt(username='username', password='password')

# 获取未分组中所有的用户成员
user_list = wechat.get_user_list()
print user_list
print '==================================='

# 获取分组列表
group_list = wechat.get_group_list()
print group_list
print '==================================='

# 获取图文信息列表
news_list = wechat.get_news_list(page=0, pagesize=15)
print news_list
print '==================================='

# 获取与最新一条消息用户的对话内容
user_info_json = wechat.get_top_message()
user_info = json.loads(user_info_json)
print wechat.get_dialog_message(fakeid=user_info['msg_item'][0]['fakeid'])