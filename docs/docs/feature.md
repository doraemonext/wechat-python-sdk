本页面会定期同步官方文档的接口与 wechat-python-sdk 的开发进度。

## 消息管理

|接口名称|官方文档地址|本文档地址|完成度|
|-------|----------|--------|-----|
|接收普通消息 - 文本消息|[链接][normal_message_text]| |![image][p100]|
|接收普通消息 - 图片消息|[链接][normal_message_image]| |![image][p100]|
|接收普通消息 - 语音消息|[链接][normal_message_voice]| |![image][p100]|
|接收普通消息 - 视频消息|[链接][normal_message_video]| |![image][p100]|
|接收普通消息 - 小视频消息|[链接][normal_message_small_video]| |![image][p100]|
|接收普通消息 - 地理位置消息|[链接][normal_message_location]| |![image][p100]|
|接收普通消息 - 链接消息|[链接][normal_message_link]| |![image][p100]|
|接收事件推送 - 关注/取消关注事件|[链接][event_subscribe]| |![image][p100]|
|接收事件推送 - 扫描带参数二维码事件|[链接][event_scan_qrcode]| |![image][p100]|
|接收事件推送 - 上报地理位置事件|[链接][event_upload_location]| |![image][p100]|
|接收事件推送 - 自定义菜单事件|[链接][event_custom_menu]| |![image][p100]|
|接收事件推送 - 点击菜单拉取消息时的事件推送|[链接][event_menu_message]| |![image][p100]|
|接收事件推送 - 点击菜单跳转链接时的事件推送|[链接][event_menu_link]| |![image][p100]|
|被动回复 - 文本消息|[链接][response_text]| |![image][p100]|
|被动回复 - 图片消息|[链接][response_image]| |![image][p100]|
|被动回复 - 语音消息|[链接][response_voice]| |![image][p100]|
|被动回复 - 视频消息|[链接][response_video]| |![image][p100]|
|被动回复 - 音乐消息|[链接][response_music]| |![image][p100]|
|被动回复 - 图文消息|[链接][response_news]| |![image][p100]|
|客服接口 - 客服账号管理|[链接][kfaccount_manage]| |![image][p0]|
|客服接口 - 发消息|[链接][kfaccount_send]| |![image][p100]|
|高级群发接口 - 根据分组进行群发|[链接][advance_mass_group]| |![image][p0]|
|高级群发接口 - 根据 OpenID 列表群发|[链接][advance_mass_openid]| |![image][p0]|
|高级群发接口 - 删除群发|[链接][advance_mass_delete]| |![image][p0]|
|高级群发接口 - 预览接口|[链接][advance_mass_preview]| |![image][p0]|
|高级群发接口 - 查询群发消息发送状态|[链接][advance_mass_status]| |![image][p0]|
|高级群发接口 - 事件推送群发结果|[链接][advance_mass_result]| |![image][p0]|
|模板消息接口 - 设置所属行业|[链接][template_set_industry]| |![image][p100]|
|模板消息接口 - 获取设置的行业信息|[链接][template_get_industry]| |![image][p0]|
|模板消息接口 - 获得模板 ID|[链接][template_get_id]| |![image][p100]|
|模板消息接口 - 获取模板列表|[链接][template_get_list]| |![image][p0]|
|模板消息接口 - 删除模板|[链接][template_delete]| |![image][p0]|
|模板消息接口 - 发送模板消息|[链接][template_send]| |![image][p100]|
|模板消息接口 - 事件推送|[链接][template_event]| |![image][p0]|
|获取自动回复规则|[链接][get_current_autoreply_info]| |![image][p0]|

## 自定义菜单

|接口名称|官方文档地址|本文档地址|完成度|
|-------|----------|--------|-----|
|自定义菜单创建接口|[链接][menu_create]| |![image][p100]|
|自定义菜单查询接口|[链接][menu_query]| |![image][p100]|
|自定义菜单删除接口|[链接][menu_delete]| |![image][p100]|
|自定义菜单事件推送|[链接][menu_event]| |![image][p100]|
|个性化菜单接口|[链接][menu_personalization]| |![image][p0]|
|获取公众号的菜单配置|[链接][menu_config]| |![image][p0]|

## 微信网页开发

|接口名称|官方文档地址|本文档地址|完成度|
|-------|----------|--------|-----|
|用户同意授权，获取code|[链接][oauth_authorize]| |![image][p0]|
|通过 code 换取网页授权 access_token|[链接][oauth_access_token]| |![image][p0]|
|刷新 access_token|[链接][oauth_refresh_token]| |![image][p0]|
|拉取用户信息|[链接][oauth_userinfo]| |![image][p0]|
|检验授权凭证是否有效|[链接][oauth_auth]| |![image][p0]|
|JSSDK - 获取 api_ticket|[链接][jssdk_api_ticket]| |![image][p100]|

## 素材管理

|接口名称|官方文档地址|本文档地址|完成度|
|-------|----------|--------|-----|
|新增临时素材|[链接][media_upload_temp]| |![image][p100]|
|获取临时素材|[链接][media_get_temp]| |![image][p100]|
|新增永久素材|[链接][media_upload_forever]| |![image][p0]|
|获取永久素材|[链接][media_get_forever]| |![image][p0]|
|删除永久素材|[链接][media_delete_forever]| |![image][p0]|
|修改永久图文素材|[链接][media_modify_forever]| |![image][p0]|
|获取素材总数|[链接][media_count]| |![image][p0]|
|获取素材列表|[链接][media_list]| |![image][p0]|

## 用户管理

|接口名称|官方文档地址|本文档地址|完成度|
|-------|----------|--------|-----|
|用户分组管理|[链接][user_group]| |![image][p0]|
|设置用户备注名|[链接][user_remark]| |![image][p0]|
|获取用户基本信息(UnionID机制)|[链接][user_info]| |![image][p0]|
|获取用户列表|[链接][user_list]| |![image][p0]|
|获取用户地理位置|[链接][user_location]| |![image][p0]|

## 账号管理

|接口名称|官方文档地址|本文档地址|完成度|
|-------|----------|--------|-----|
|生成带参数的二维码|[链接][account_qrcode]| |![image][p0]|
|长链接转短链接接口|[链接][account_link]| |![image][p0]|
|微信认证事件推送|[链接][account_qualification_verify]| |![image][p0]|

## 数据统计

|接口名称|官方文档地址|本文档地址|完成度|
|-------|----------|--------|-----|
|用户分析数据接口|[链接][datacube_user]| |![image][p0]|
|图文分析数据接口|[链接][datacube_news]| |![image][p0]|
|消息分析数据接口|[链接][datacube_message]| |![image][p0]|
|接口分析数据接口|[链接][datacube_api]| |![image][p0]|

## 微信小店

|接口名称|官方文档地址|本文档地址|完成度|
|-------|----------|--------|-----|
|商品管理接口|[链接][store_good]| |![image][p0]|
|库存管理接口|[链接][store_stock]| |![image][p0]|
|邮费模板管理接口|[链接][store_postage]| |![image][p0]|
|分组管理接口|[链接][store_group]| |![image][p0]|
|货架管理接口|[链接][store_shelf]| |![image][p0]|
|订单管理接口|[链接][store_order]| |![image][p0]|
|功能接口|[链接][store_feature]| |![image][p0]|

## 微信卡券

待开发

## 微信门店

待开发

## 微信智能接口

待开发

## 微信设备功能

待开发

## 微信多客服功能

|接口名称|官方文档地址|本文档地址|完成度|
|-------|----------|--------|-----|
|将消息转发到多客服|[链接][customer_service]| |![image][p100]|
|客服管理|[链接][customer_manage]| |![image][p0]|
|多客服会话控制|[链接][customer_session]| |![image][p0]|
|获取客服聊天记录|[链接][customer_chat]| |![image][p0]|

## 微信摇一摇周边

待开发

## 微信连 Wi-Fi

待开发

## 微信扫一扫

待开发

[p100]: http://progressed.io/bar/100
[p75]: http://progressed.io/bar/75
[p50]: http://progressed.io/bar/50
[p25]: http://progressed.io/bar/25
[p0]: http://progressed.io/bar/0

[menu_create]: http://mp.weixin.qq.com/wiki/10/0234e39a2025342c17a7d23595c6b40a.html
[menu_query]: http://mp.weixin.qq.com/wiki/5/f287d1a5b78a35a8884326312ac3e4ed.html
[menu_delete]: http://mp.weixin.qq.com/wiki/3/de21624f2d0d3dafde085dafaa226743.html
[menu_event]: http://mp.weixin.qq.com/wiki/19/a037750e2df0261ab0a84899d16abd33.html
[menu_personalization]: http://mp.weixin.qq.com/wiki/0/c48ccd12b69ae023159b4bfaa7c39c20.html
[menu_config]: http://mp.weixin.qq.com/wiki/14/293d0cb8de95e916d1216a33fcb81fd6.html

[normal_message_text]: http://mp.weixin.qq.com/wiki/17/f298879f8fb29ab98b2f2971d42552fd.html#.E6.96.87.E6.9C.AC.E6.B6.88.E6.81.AF
[normal_message_image]: http://mp.weixin.qq.com/wiki/17/f298879f8fb29ab98b2f2971d42552fd.html#.E5.9B.BE.E7.89.87.E6.B6.88.E6.81.AF
[normal_message_voice]: http://mp.weixin.qq.com/wiki/17/f298879f8fb29ab98b2f2971d42552fd.html#.E8.AF.AD.E9.9F.B3.E6.B6.88.E6.81.AF
[normal_message_video]: http://mp.weixin.qq.com/wiki/17/f298879f8fb29ab98b2f2971d42552fd.html#.E8.A7.86.E9.A2.91.E6.B6.88.E6.81.AF
[normal_message_small_video]: http://mp.weixin.qq.com/wiki/17/f298879f8fb29ab98b2f2971d42552fd.html#.E5.B0.8F.E8.A7.86.E9.A2.91.E6.B6.88.E6.81.AF
[normal_message_location]: http://mp.weixin.qq.com/wiki/17/f298879f8fb29ab98b2f2971d42552fd.html#.E5.9C.B0.E7.90.86.E4.BD.8D.E7.BD.AE.E6.B6.88.E6.81.AF
[normal_message_link]: http://mp.weixin.qq.com/wiki/17/f298879f8fb29ab98b2f2971d42552fd.html#.E9.93.BE.E6.8E.A5.E6.B6.88.E6.81.AF

[event_subscribe]: http://mp.weixin.qq.com/wiki/7/9f89d962eba4c5924ed95b513ba69d9b.html#.E5.85.B3.E6.B3.A8.2F.E5.8F.96.E6.B6.88.E5.85.B3.E6.B3.A8.E4.BA.8B.E4.BB.B6
[event_scan_qrcode]: http://mp.weixin.qq.com/wiki/7/9f89d962eba4c5924ed95b513ba69d9b.html#.E6.89.AB.E6.8F.8F.E5.B8.A6.E5.8F.82.E6.95.B0.E4.BA.8C.E7.BB.B4.E7.A0.81.E4.BA.8B.E4.BB.B6
[event_upload_location]: http://mp.weixin.qq.com/wiki/7/9f89d962eba4c5924ed95b513ba69d9b.html#.E4.B8.8A.E6.8A.A5.E5.9C.B0.E7.90.86.E4.BD.8D.E7.BD.AE.E4.BA.8B.E4.BB.B6
[event_custom_menu]: http://mp.weixin.qq.com/wiki/7/9f89d962eba4c5924ed95b513ba69d9b.html#.E8.87.AA.E5.AE.9A.E4.B9.89.E8.8F.9C.E5.8D.95.E4.BA.8B.E4.BB.B6
[event_menu_message]: http://mp.weixin.qq.com/wiki/7/9f89d962eba4c5924ed95b513ba69d9b.html#.E7.82.B9.E5.87.BB.E8.8F.9C.E5.8D.95.E6.8B.89.E5.8F.96.E6.B6.88.E6.81.AF.E6.97.B6.E7.9A.84.E4.BA.8B.E4.BB.B6.E6.8E.A8.E9.80.81
[event_menu_link]: http://mp.weixin.qq.com/wiki/7/9f89d962eba4c5924ed95b513ba69d9b.html#.E7.82.B9.E5.87.BB.E8.8F.9C.E5.8D.95.E8.B7.B3.E8.BD.AC.E9.93.BE.E6.8E.A5.E6.97.B6.E7.9A.84.E4.BA.8B.E4.BB.B6.E6.8E.A8.E9.80.81

[response_text]: http://mp.weixin.qq.com/wiki/1/6239b44c206cab9145b1d52c67e6c551.html#.E5.9B.9E.E5.A4.8D.E6.96.87.E6.9C.AC.E6.B6.88.E6.81.AF
[response_image]: http://mp.weixin.qq.com/wiki/1/6239b44c206cab9145b1d52c67e6c551.html#.E5.9B.9E.E5.A4.8D.E5.9B.BE.E7.89.87.E6.B6.88.E6.81.AF
[response_voice]: http://mp.weixin.qq.com/wiki/1/6239b44c206cab9145b1d52c67e6c551.html#.E5.9B.9E.E5.A4.8D.E8.AF.AD.E9.9F.B3.E6.B6.88.E6.81.AF
[response_video]: http://mp.weixin.qq.com/wiki/1/6239b44c206cab9145b1d52c67e6c551.html#.E5.9B.9E.E5.A4.8D.E8.A7.86.E9.A2.91.E6.B6.88.E6.81.AF
[response_music]: http://mp.weixin.qq.com/wiki/1/6239b44c206cab9145b1d52c67e6c551.html#.E5.9B.9E.E5.A4.8D.E9.9F.B3.E4.B9.90.E6.B6.88.E6.81.AF
[response_news]: http://mp.weixin.qq.com/wiki/1/6239b44c206cab9145b1d52c67e6c551.html#.E5.9B.9E.E5.A4.8D.E5.9B.BE.E6.96.87.E6.B6.88.E6.81.AF

[kfaccount_manage]: http://mp.weixin.qq.com/wiki/11/c88c270ae8935291626538f9c64bd123.html#.E5.AE.A2.E6.9C.8D.E5.B8.90.E5.8F.B7.E7.AE.A1.E7.90.86
[kfaccount_send]: http://mp.weixin.qq.com/wiki/11/c88c270ae8935291626538f9c64bd123.html#.E5.AE.A2.E6.9C.8D.E6.8E.A5.E5.8F.A3-.E5.8F.91.E6.B6.88.E6.81.AF

[advance_mass_group]: http://mp.weixin.qq.com/wiki/15/40b6865b893947b764e2de8e4a1fb55f.html#.E6.A0.B9.E6.8D.AE.E5.88.86.E7.BB.84.E8.BF.9B.E8.A1.8C.E7.BE.A4.E5.8F.91.E3.80.90.E8.AE.A2.E9.98.85.E5.8F.B7.E4.B8.8E.E6.9C.8D.E5.8A.A1.E5.8F.B7.E8.AE.A4.E8.AF.81.E5.90.8E.E5.9D.87.E5.8F.AF.E7.94.A8.E3.80.91
[advance_mass_openid]: http://mp.weixin.qq.com/wiki/15/40b6865b893947b764e2de8e4a1fb55f.html#.E6.A0.B9.E6.8D.AEOpenID.E5.88.97.E8.A1.A8.E7.BE.A4.E5.8F.91.E3.80.90.E8.AE.A2.E9.98.85.E5.8F.B7.E4.B8.8D.E5.8F.AF.E7.94.A8.EF.BC.8C.E6.9C.8D.E5.8A.A1.E5.8F.B7.E8.AE.A4.E8.AF.81.E5.90.8E.E5.8F.AF.E7.94.A8.E3.80.91
[advance_mass_delete]: http://mp.weixin.qq.com/wiki/15/40b6865b893947b764e2de8e4a1fb55f.html#.E5.88.A0.E9.99.A4.E7.BE.A4.E5.8F.91.E3.80.90.E8.AE.A2.E9.98.85.E5.8F.B7.E4.B8.8E.E6.9C.8D.E5.8A.A1.E5.8F.B7.E8.AE.A4.E8.AF.81.E5.90.8E.E5.9D.87.E5.8F.AF.E7.94.A8.E3.80.91
[advance_mass_preview]: http://mp.weixin.qq.com/wiki/15/40b6865b893947b764e2de8e4a1fb55f.html#.E9.A2.84.E8.A7.88.E6.8E.A5.E5.8F.A3.E3.80.90.E8.AE.A2.E9.98.85.E5.8F.B7.E4.B8.8E.E6.9C.8D.E5.8A.A1.E5.8F.B7.E8.AE.A4.E8.AF.81.E5.90.8E.E5.9D.87.E5.8F.AF.E7.94.A8.E3.80.91
[advance_mass_status]: http://mp.weixin.qq.com/wiki/15/40b6865b893947b764e2de8e4a1fb55f.html#.E6.9F.A5.E8.AF.A2.E7.BE.A4.E5.8F.91.E6.B6.88.E6.81.AF.E5.8F.91.E9.80.81.E7.8A.B6.E6.80.81.E3.80.90.E8.AE.A2.E9.98.85.E5.8F.B7.E4.B8.8E.E6.9C.8D.E5.8A.A1.E5.8F.B7.E8.AE.A4.E8.AF.81.E5.90.8E.E5.9D.87.E5.8F.AF.E7.94.A8.E3.80.91
[advance_mass_result]: http://mp.weixin.qq.com/wiki/15/40b6865b893947b764e2de8e4a1fb55f.html#.E4.BA.8B.E4.BB.B6.E6.8E.A8.E9.80.81.E7.BE.A4.E5.8F.91.E7.BB.93.E6.9E.9C

[template_set_industry]: http://mp.weixin.qq.com/wiki/5/6dde9eaa909f83354e0094dc3ad99e05.html#.E8.AE.BE.E7.BD.AE.E6.89.80.E5.B1.9E.E8.A1.8C.E4.B8.9A
[template_get_industry]: http://mp.weixin.qq.com/wiki/5/6dde9eaa909f83354e0094dc3ad99e05.html#.E8.8E.B7.E5.8F.96.E8.AE.BE.E7.BD.AE.E7.9A.84.E8.A1.8C.E4.B8.9A.E4.BF.A1.E6.81.AF
[template_get_id]: http://mp.weixin.qq.com/wiki/5/6dde9eaa909f83354e0094dc3ad99e05.html#.E8.8E.B7.E5.BE.97.E6.A8.A1.E6.9D.BFID
[template_get_list]: http://mp.weixin.qq.com/wiki/5/6dde9eaa909f83354e0094dc3ad99e05.html#.E8.8E.B7.E5.8F.96.E6.A8.A1.E6.9D.BF.E5.88.97.E8.A1.A8
[template_delete]: http://mp.weixin.qq.com/wiki/5/6dde9eaa909f83354e0094dc3ad99e05.html#.E5.88.A0.E9.99.A4.E6.A8.A1.E6.9D.BF
[template_send]: http://mp.weixin.qq.com/wiki/5/6dde9eaa909f83354e0094dc3ad99e05.html#.E5.8F.91.E9.80.81.E6.A8.A1.E6.9D.BF.E6.B6.88.E6.81.AF
[template_event]: http://mp.weixin.qq.com/wiki/5/6dde9eaa909f83354e0094dc3ad99e05.html#.E4.BA.8B.E4.BB.B6.E6.8E.A8.E9.80.81

[get_current_autoreply_info]: http://mp.weixin.qq.com/wiki/8/806878e1fc2b9e9aa618ae33896b04c4.html

[oauth_authorize]: http://mp.weixin.qq.com/wiki/4/9ac2e7b1f1d22e9e57260f6553822520.html#.E7.AC.AC.E4.B8.80.E6.AD.A5.EF.BC.9A.E7.94.A8.E6.88.B7.E5.90.8C.E6.84.8F.E6.8E.88.E6.9D.83.EF.BC.8C.E8.8E.B7.E5.8F.96code
[oauth_access_token]: http://mp.weixin.qq.com/wiki/4/9ac2e7b1f1d22e9e57260f6553822520.html#.E7.AC.AC.E4.BA.8C.E6.AD.A5.EF.BC.9A.E9.80.9A.E8.BF.87code.E6.8D.A2.E5.8F.96.E7.BD.91.E9.A1.B5.E6.8E.88.E6.9D.83access_token
[oauth_refresh_token]: http://mp.weixin.qq.com/wiki/4/9ac2e7b1f1d22e9e57260f6553822520.html#.E7.AC.AC.E4.B8.89.E6.AD.A5.EF.BC.9A.E5.88.B7.E6.96.B0access_token.EF.BC.88.E5.A6.82.E6.9E.9C.E9.9C.80.E8.A6.81.EF.BC.89
[oauth_userinfo]: http://mp.weixin.qq.com/wiki/4/9ac2e7b1f1d22e9e57260f6553822520.html#.E7.AC.AC.E5.9B.9B.E6.AD.A5.EF.BC.9A.E6.8B.89.E5.8F.96.E7.94.A8.E6.88.B7.E4.BF.A1.E6.81.AF.28.E9.9C.80scope.E4.B8.BA_snsapi_userinfo.29
[oauth_auth]: http://mp.weixin.qq.com/wiki/4/9ac2e7b1f1d22e9e57260f6553822520.html#.E9.99.84.EF.BC.9A.E6.A3.80.E9.AA.8C.E6.8E.88.E6.9D.83.E5.87.AD.E8.AF.81.EF.BC.88access_token.EF.BC.89.E6.98.AF.E5.90.A6.E6.9C.89.E6.95.88

[jssdk_api_ticket]: http://mp.weixin.qq.com/wiki/11/74ad127cc054f6b80759c40f77ec03db.html#.E8.8E.B7.E5.8F.96api_ticket

[media_upload_temp]: http://mp.weixin.qq.com/wiki/15/2d353966323806a202cd2deaafe8e557.html
[media_get_temp]: http://mp.weixin.qq.com/wiki/9/677a85e3f3849af35de54bb5516c2521.html
[media_upload_forever]: http://mp.weixin.qq.com/wiki/10/10ea5a44870f53d79449290dfd43d006.html
[media_get_forever]: http://mp.weixin.qq.com/wiki/12/3c12fac7c14cb4d0e0d4fe2fbc87b638.html
[media_delete_forever]: http://mp.weixin.qq.com/wiki/7/2212203f4e17253b9aef77dc788f5337.html
[media_modify_forever]: http://mp.weixin.qq.com/wiki/10/c7bad9a463db20ff8ccefeedeef51f9e.html
[media_count]: http://mp.weixin.qq.com/wiki/5/a641fd7b5db7a6a946ebebe2ac166885.html
[media_list]: http://mp.weixin.qq.com/wiki/15/8386c11b7bc4cdd1499c572bfe2e95b3.html

[user_group]: http://mp.weixin.qq.com/wiki/8/d6d33cf60bce2a2e4fb10a21be9591b8.html
[user_remark]: http://mp.weixin.qq.com/wiki/16/528098c4a6a87b05120a7665c8db0460.html
[user_info]: http://mp.weixin.qq.com/wiki/1/8a5ce6257f1d3b2afb20f83e72b72ce9.html
[user_list]: http://mp.weixin.qq.com/wiki/12/54773ff6da7b8bdc95b7d2667d84b1d4.html
[user_location]: http://mp.weixin.qq.com/wiki/4/0bd25e04332eccf83bc2e71df9d3e860.html

[account_qrcode]: http://mp.weixin.qq.com/wiki/18/167e7d94df85d8389df6c94a7a8f78ba.html
[account_link]: http://mp.weixin.qq.com/wiki/6/856aaeb492026466277ea39233dc23ee.html
[account_qualification_verify]: http://mp.weixin.qq.com/wiki/10/2adfb2f10828e87aa1e5c3ef83b17906.html

[datacube_user]: http://mp.weixin.qq.com/wiki/15/88726a421bfc54654a3095821c3ca3bb.html
[datacube_news]: http://mp.weixin.qq.com/wiki/9/d347c6ddb6f86ab11ec3b41c2729c8d9.html
[datacube_message]: http://mp.weixin.qq.com/wiki/10/b29e8ca8bf1b0dce033ccb70273f90fa.html
[datacube_api]: http://mp.weixin.qq.com/wiki/17/252a976f20bd3062af3f03a45f30cff9.html

[store_good]: http://mp.weixin.qq.com/wiki/static/assets/6f10c5d0769bf2d30c17e299736c0385.zip
[store_stock]: http://mp.weixin.qq.com/wiki/static/assets/6f10c5d0769bf2d30c17e299736c0385.zip
[store_postage]: http://mp.weixin.qq.com/wiki/static/assets/6f10c5d0769bf2d30c17e299736c0385.zip
[store_group]: http://mp.weixin.qq.com/wiki/static/assets/6f10c5d0769bf2d30c17e299736c0385.zip
[store_shelf]: http://mp.weixin.qq.com/wiki/static/assets/6f10c5d0769bf2d30c17e299736c0385.zip
[store_order]: http://mp.weixin.qq.com/wiki/static/assets/6f10c5d0769bf2d30c17e299736c0385.zip
[store_feature]: http://mp.weixin.qq.com/wiki/static/assets/6f10c5d0769bf2d30c17e299736c0385.zip

[customer_service]: http://mp.weixin.qq.com/wiki/11/f0e34a15cec66fefb28cf1c0388f68ab.html 
[customer_manage]: http://mp.weixin.qq.com/wiki/18/749901f4e123170fb8a4d447ae6040ba.html
[customer_session]: http://mp.weixin.qq.com/wiki/4/4b256cfb246b22ad020e07cf8a61a738.html
[customer_chat]: http://mp.weixin.qq.com/wiki/3/178d2982bd590adf33fc03cf6cf45b33.html

