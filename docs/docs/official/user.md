# 官方接口 - 用户管理

## 用户分组 - 创建分组

**调用方法：**`.create_group(name)`

**参数：**

* `name`: 分组名字（30个字符以内）

**调用前检查：**App ID / App Secret

**返回值：**正常返回官方接口的 JSON 数据：

```json
{
    "group": {
        "id": 107, 
        "name": "test"
    }
}
```

**异常：**当发生失败时抛出 [`exceptions.OfficialAPIError`](/api/exception.md#officialapierror) 异常，该异常包含了错误的代号与原因信息。

**对应官方文档：**[创建分组](http://mp.weixin.qq.com/wiki/8/d6d33cf60bce2a2e4fb10a21be9591b8.html#.E5.88.9B.E5.BB.BA.E5.88.86.E7.BB.84)

## 用户分组 - 查询所有分组

**调用方法：**`.get_groups()`

**调用前检查：**App ID / App Secret

**返回值：**正常返回官方接口的 JSON 数据：

```json
{
    "groups": [
        {
            "id": 0, 
            "name": "未分组", 
            "count": 72596
        }, 
        {
            "id": 1, 
            "name": "黑名单", 
            "count": 36
        }, 
        {
            "id": 2, 
            "name": "星标组", 
            "count": 8
        }, 
        {
            "id": 104, 
            "name": "华东媒", 
            "count": 4
        }, 
        {
            "id": 106, 
            "name": "★不测试组★", 
            "count": 1
        }
    ]
}
```

**异常：**当发生失败时抛出 [`exceptions.OfficialAPIError`](/api/exception.md#officialapierror) 异常，该异常包含了错误的代号与原因信息。

**对应官方文档：**[查询所有分组](http://mp.weixin.qq.com/wiki/8/d6d33cf60bce2a2e4fb10a21be9591b8.html#.E6.9F.A5.E8.AF.A2.E6.89.80.E6.9C.89.E5.88.86.E7.BB.84)

## 用户分组 - 查询用户所在分组

**调用方法：**`.get_group_by_id(openid)`

**参数：**

* `openid`: 用户的 OpenID

**调用前检查：**App ID / App Secret

**返回值：**正常返回官方接口的 JSON 数据：

```json
{
    "groupid": 102
}
```

**异常：**当发生失败时抛出 [`exceptions.OfficialAPIError`](/api/exception.md#officialapierror) 异常，该异常包含了错误的代号与原因信息。

**对应官方文档：**[查询用户所在分组](http://mp.weixin.qq.com/wiki/8/d6d33cf60bce2a2e4fb10a21be9591b8.html#.E6.9F.A5.E8.AF.A2.E7.94.A8.E6.88.B7.E6.89.80.E5.9C.A8.E5.88.86.E7.BB.84)

## 用户分组 - 修改分组名

**调用方法：**`.update_group(group_id, name)`

**参数：**

* `group_id`: 分组 ID，由微信分配
* `name`: 分组名字（30个字符以内）

**调用前检查：**App ID / App Secret

**返回值：**正常返回官方接口的 JSON 数据：

```json
{
    "errcode": 0, 
    "errmsg": "ok"
}
```

**异常：**当发生失败时抛出 [`exceptions.OfficialAPIError`](/api/exception.md#officialapierror) 异常，该异常包含了错误的代号与原因信息。

**对应官方文档：**[修改分组名](http://mp.weixin.qq.com/wiki/8/d6d33cf60bce2a2e4fb10a21be9591b8.html#.E4.BF.AE.E6.94.B9.E5.88.86.E7.BB.84.E5.90.8D)

## 用户分组 - 移动用户分组

**调用方法：**`.update_group(user_id, group_id)`

**参数：**

* `user_id`: 用户的 OpenID
* `group_id`: 分组 ID

**调用前检查：**App ID / App Secret

**返回值：**正常返回官方接口的 JSON 数据：

```json
{
    "errcode": 0, 
    "errmsg": "ok"
}
```

**异常：**当发生失败时抛出 [`exceptions.OfficialAPIError`](/api/exception.md#officialapierror) 异常，该异常包含了错误的代号与原因信息。

**对应官方文档：**[移动用户分组](http://mp.weixin.qq.com/wiki/8/d6d33cf60bce2a2e4fb10a21be9591b8.html#.E7.A7.BB.E5.8A.A8.E7.94.A8.E6.88.B7.E5.88.86.E7.BB.84)

## 用户分组 - 批量移动用户分组

待开发

## 用户分组 - 删除分组

待开发

## 设置用户备注名

待开发

## 获取用户基本信息

**调用方法：**`.get_user_info(user_id, lang='zh_CN')`

**参数：**

* `user_id`: 用户的 OpenID
* `lang`: 返回国家地区语言版本，zh_CN 简体，zh_TW 繁体，en 英语

**调用前检查：**App ID / App Secret

**返回值：**正常返回官方接口的 JSON 数据：

```json
{
    "subscribe": 1, 
    "openid": "o6_bmjrPTlm6_2sgVt7hMZOPfL2M", 
    "nickname": "Band", 
    "sex": 1, 
    "language": "zh_CN", 
    "city": "广州", 
    "province": "广东", 
    "country": "中国", 
    "headimgurl": "http://wx.qlogo.cn/mmopen/g3MonUZtNHkdmzicIlibx6iaFqAc56vxLSUfpb6n5WKSYVY0ChQKkiaJSgQ1dZuTOgvLLrhJbERQQ4eMsv84eavHiaiceqxibJxCfHe/0", 
    "subscribe_time": 1382694957,
    "unionid": "o6_bmasdasdsad6_2sgVt7hMZOPfL",
    "remark": "",
    "groupid": 0
}
```

**异常：**当发生失败时抛出 [`exceptions.OfficialAPIError`](/api/exception.md#officialapierror) 异常，该异常包含了错误的代号与原因信息。

**对应官方文档：**[获取用户基本信息](http://mp.weixin.qq.com/wiki/1/8a5ce6257f1d3b2afb20f83e72b72ce9.html)

## 批量获取用户基本信息

待开发

## 获取用户列表

**调用方法：**`.get_followers(first_user_id=None)`

**参数：**

* `first_user_id`: 可选。第一个拉取的 OpenID，不填默认从头开始拉取

**调用前检查：**App ID / App Secret

**返回值：**正常返回官方接口的 JSON 数据：

```json
{
    "total": 2,
    "count": 2,
    "data":
    {
        "openid":
        [
            "",
            "OPENID1",
            "OPENID2"
        ]
    },
    "next_openid": "NEXT_OPENID"
}
```

**异常：**当发生失败时抛出 [`exceptions.OfficialAPIError`](/api/exception.md#officialapierror) 异常，该异常包含了错误的代号与原因信息。

**对应官方文档：**[获取用户列表](http://mp.weixin.qq.com/wiki/12/54773ff6da7b8bdc95b7d2667d84b1d4.html)

## 获取用户地理位置

待开发

