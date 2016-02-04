# 官方接口 - 微信网页开发

## 网页授权

待开发

## 获取 jsapi ticket

**该方法仅为自行维护单机版 jsapi_ticket 使用。**

获取 jsapi_ticket 及 jsapi_ticket 过期日期, 仅供缓存使用。

**调用方法：**`.get_jsapi_ticket()`

**调用前检查：**App ID / App Secret

**返回值：**dict 对象, key 包括 `jsapi_ticket` 及 `jsapi_ticket_expires_at`。

**异常：**当发生失败时抛出 [`exceptions.OfficialAPIError`](/api/exception.md#officialapierror) 异常，该异常包含了错误的代号与原因信息。

```json
{
    "jsapi_ticket":"bxLdikRXVbTPdHSM05e5u8EoHz_JA7Re-noqE0ZAnxk3XzAntyhT4_k272aJ4LprCM68rVXv6DDydT7JW1Mwsw",
    "jsapi_ticket_expires_at": 1454476720
}
```

**对应官方文档：**[获取jsapi ticket](http://mp.weixin.qq.com/wiki/11/74ad127cc054f6b80759c40f77ec03db.html#.E8.8E.B7.E5.8F.96api_ticket)


