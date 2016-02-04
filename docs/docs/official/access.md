# 官方接口 - 接入指南

## 验证服务器地址有效性

**调用方法：**`.check_signature(signature, timestmap, nonce)`

**参数说明：**

* `signature`: 微信加密签名
* `timestamp`: 时间戳
* `nonce`: 随机数

**调用前检查：**Token

**返回值：**成功返回 `True`，失败返回 `False`

**对应官方文档：**[验证服务器地址的有效性](http://mp.weixin.qq.com/wiki/8/f9a0b8382e0b77d87b3bcc1ce6fbc104.html#.E7.AC.AC.E4.BA.8C.E6.AD.A5.EF.BC.9A.E9.AA.8C.E8.AF.81.E6.9C.8D.E5.8A.A1.E5.99.A8.E5.9C.B0.E5.9D.80.E7.9A.84.E6.9C.89.E6.95.88.E6.80.A7)

## 获取 access_token

**该方法仅为自行维护单机版 access_token 使用。**

获取 access_token 及 access_token 过期日期, 仅供缓存使用。

**调用方法：**`.get_access_token()`

**调用前检查：**App ID / App Secret

**返回值：**dict 对象, key 包括 `access_token` 及 `access_token_expires_at`。

**异常：**当发生失败时抛出 [`exceptions.OfficialAPIError`](/api/exception.md#officialapierror) 异常，该异常包含了错误的代号与原因信息。

```json
{
    "access_token":"Uj6gDn1My01ElQvLXjudqdXlnTYosqWnxPT-1AX_jJEqeYhbqASZXPlnur7k6YV7Erjvd_JDXbQWeZYIMmu958WV4VWe7GKD65q_VLHecTp8nA5DwU_DOdmVBACU2wDkPGBbAHAEVQ",
    "access_token_expires_at":1454476716
}
```

**对应官方文档：**[获取access token](http://mp.weixin.qq.com/wiki/14/9f9c82c1af308e3b14ba9b973f99a8ba.html)


