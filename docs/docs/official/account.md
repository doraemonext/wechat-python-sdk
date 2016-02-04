# 官方接口 - 账号管理

## 创建二维码 ticket

**调用方法：**`.create_qrcode(data)`

**参数：**

* `data`: 你要发送的参数 dict

示例1（临时二维码）：

```python
{
    "expire_seconds": 604800, 
    "action_name": "QR_SCENE", 
    "action_info": {
        "scene": {
            "scene_id": 123
        }
    }
}
```

示例2（永久二维码）：

```python
{
    "action_name": "QR_LIMIT_SCENE", 
    "action_info": {
        "scene": {
            "scene_id": 123
        }
    }
}
```

**调用前检查：**App ID / App Secret

**返回值：**正常返回官方接口的 JSON 数据：

```json
{
    "ticket": "gQH47joAAAAAAAAAASxodHRwOi8vd2VpeGluLnFxLmNvbS9xL2taZ2Z3TVRtNzJXV1Brb3ZhYmJJAAIEZ23sUwMEmm3sUw==",
    "expire_seconds": 60,
    "url": "http:\/\/weixin.qq.com\/q\/kZgfwMTm72WWPkovabbI"
}
```

**异常：**当发生失败时抛出 [`exceptions.OfficialAPIError`](/api/exception.md#officialapierror) 异常，该异常包含了错误的代号与原因信息。

**对应官方文档：**[创建二维码ticket](http://mp.weixin.qq.com/wiki/18/167e7d94df85d8389df6c94a7a8f78ba.html)

## 通过 ticket 换取二维码

**调用方法：**`.show_qrcode(ticket)`

**参数：**

* `ticket`: 二维码 ticket

**调用前检查：**无

**返回值：**当请求成功时，返回一个 [`requests.Response`](http://docs.python-requests.org/en/master/api/#requests.Response) 对象，下面示例将该对象存储为本地文件：

```python
response = wechat.show_qrcode('your ticket')
with open('yourfilename', 'wb') as fd:
    for chunk in response.iter_content(1024):
        fd.write(chunk)
```

当 `ticket` 参数非法导致无法获取二维码时，为 HTTP 404 错误。

**对应官方文档：**[通过 ticket 换取二维码](http://mp.weixin.qq.com/wiki/18/167e7d94df85d8389df6c94a7a8f78ba.html)

## 长链接转短链接接口

待开发

## 微信认证事件推送

待开发

