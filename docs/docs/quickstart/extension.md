# 快速上手 - 扩展接口



## 基本用法

第一个例子(examples/tutorial_unofficial_1.py)，展示了几个直接获取信息的函数的用法，至于具体的返回值所包含的内容，请查看 ``WechatExt`` 文档

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


