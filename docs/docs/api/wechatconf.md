# WechatConf API

WechatConf 是 **微信配置类**，你需要将在公众平台开发者选项中的 Token/AppID/AppSecret/EncodingAESKey 等信息传入其中，之后该类将会自行维护相关配置信息（access_token/jsapi_ticket）的有效性，支持分布式。

## WechatConf()

**导入方式：**`from wechat_sdk import WechatConf`

**signature:** 

```python
WechatConf(token=None, appid=None, appsecret=None, encrypt_mode='safe', encoding_aes_key=None,
           access_token_getfunc=None, access_token_setfunc=None, access_token_refreshfunc=None, access_token=None, 
           access_token_expires_at=None, jsapi_ticket_getfunc=None, jsapi_ticket_setfunc=None, 
           jsapi_ticket_refreshfunc=None, jsapi_ticket=None, jsapi_ticket_expires_at=None, checkssl=False)
```

|参数名称|参数解释|
|-------|-------|
|`token`|公众平台开发者选项中你设置的 Token|
|`appid`|公众平台开发者选项中的 App ID|
|`appsecret`|公众平台开发者选项中的 App Secret|
|`encrypt_mode`|消息加解密方式。可选项 `normal`（明文模式）、`compatible`（兼容模式）、`safe`（安全模式）|
|`encoding_aes_key`|公众平台开发者选项中的 EncodingAESKey|
|`access_token_getfunc`|access_token 获取函数。如果传入该参数，WechatConf 内部将会在需要使用 access_token 时直接调用该函数，该函数不应接受任何参数，该函数应返回一个 Tuple，里面包含两个元素，分别是 access_token 和 access_token_expires_at。|
|`access_token_setfunc`|access_token 设置函数。如果传入该参数，WechatConf 内部将会在需要更新 access_token 时直接调用该函数，该函数应接受两个参数，为 access_token 的字符串值和 access_token 的过期时间。该函数无返回值。|
|`access_token_refreshfunc`|access_token 刷新函数。如果传入该参数，WechatConf 内部将会在需要更新 access_token 时直接调用该函数而不会请求官方 API，该函数不应接收任何参数，用于分布式环境下的业务逻辑服务器。该函数应返回一个 Tuple，里面包含两个元素,分别是 access_token 和 access_token_expires_at。|
|`access_token`|直接导入的 access token 值, 该值需要在上一次该类实例化之后手动进行缓存并在此处传入, 如果不传入, 将会在需要时自动重新获取 **(传入 access_token_getfunc 和 access_token_setfunc 函数后将会自动忽略此处的传入值)**|
|`access_token_expires_at`|直接导入的 access token 的过期日期, 该值需要在上一次该类实例化之后手动进行缓存并在此处传入, 如果不传入, 将会在需要时自动重新获取 **(传入 access_token_getfunc 和 access_token_setfunc 函数后将会自动忽略此处的传入值)**|
|`jsapi_ticket_getfunc`|jsapi_ticket 获取函数。如果传入该参数，WechatConf 内部将会在需要使用 jsapi_ticket 时直接调用该函数，该函数不应接受任何参数。该函数应返回一个 Tuple，里面包含两个元素，分别是 jsapi_ticket 和 jsapi_ticket_expires_at。|
|`jsapi_ticket_setfunc`|jsapi_ticket 设置函数。如果传入该参数，WechatConf 内部将会在需要更新 jsapi_ticket 时直接调用该函数，该函数应接受两个参数，为 jsapi_ticket 的字符串值和 jsapi_ticket 的过期时间。该函数无返回值。|
|`jsapi_ticket_refreshfunc`|jsapi_ticket 刷新函数。如果传入该参数，WechatConf 内部将会在需要更新 jsapi_ticket 时直接调用该函数而不会请求官方 API，该函数不应接收任何参数，用于分布式环境下的业务逻辑服务器。该函数应返回一个 Tuple，里面包含两个元素,分别是 jsapi_ticket 和 jsapi_ticket_expires_at。|
|`jsapi_ticket`|直接导入的 jsapi ticket 值, 该值需要在上一次该类实例化之后手动进行缓存并在此处传入, 如果不传入, 将会在需要时自动重新获取 **(传入 jsapi_ticket_getfunc 和 jsapi_ticket_setfunc 函数后将会自动忽略此处的传入值)**|
|`jsapi_ticket_expires_at`|直接导入的 jsapi ticket 的过期日期, 该值需要在上一次该类实例化之后手动进行缓存并在此处传入, 如果不传入, 将会在需要时自动重新获取 **(传入 jsapi_ticket_getfunc 和 jsapi_ticket_setfunc 函数后将会自动忽略此处的传入值)**|
|`checkssl`|是否检查 SSL, 默认不检查 (False), 可避免 urllib3 的 InsecurePlatformWarning 警告|

## 属性

### .token

（可直接赋值更改）当前正在使用的 Token 值
### .appid

当前正在使用的 App ID 值

### .appsecret

当前正在使用的 App Secret 值

### .encrypt_mode

（可直接赋值更改）当前正在使用的消息加解密方式。

返回内容为字符串，`normal`为明文模式，`compatible`为兼容模式，`safe`为安全模式

### .encoding_aes_key

（可直接赋值更改）当前正在使用的 EncodingAESKey

### .crypto

当前 Crypto 实例，可直接用于加密解密消息操作

### .access_token

当前的 access_token 值，该值会由 WechatConf 内部动态维护合法性

### .jsapi_ticket

当前的 jsapi_ticket 值，该值会由 WechatConf 内部动态维护合法性

## 方法

### .set_appid_appsecret(appid, appsecret)

设置当前 App ID 和 App Secret

**Return:** None

### .grant_access_token()

获取 access_token 并更新当前配置（默认情况下会自行维护，无需调用此函数，仅为强制刷新时使用）

**Return:** 返回 [官方接口](http://mp.weixin.qq.com/wiki/14/9f9c82c1af308e3b14ba9b973f99a8ba.html) 返回的 JSON 数据，示例：

```json
{
    "access_token": "HoVFaIslbrofqJgkR0Svcx2d4za0RJKa3H6A_NjzhBbm96Wtg_a3ifUYQvOfJmV76QTcCpNubcsnOLmDopu2hjWfFeQSCE4c8QrsxwE_N3w",
    "expires_in": 7200
}
```

### .grant_jsapi_ticket()

获取 jsapi_ticket 并更新当前配置（默认情况下会自行维护，无需调用此函数，仅为强制刷新时使用）

**Return:** 返回 [官方接口](http://mp.weixin.qq.com/wiki/11/74ad127cc054f6b80759c40f77ec03db.html#.E8.8E.B7.E5.8F.96api_ticket) 返回的 JSON 数据，示例：

```json
{
    "errcode":0,
    "errmsg":"ok",
    "ticket":"bxLdikRXVbTPdHSM05e5u5sUoXNKd8-41ZO3MhKoyN5OfkWITDGgnr2fwJ0m9E8NYzWKVZvdVtaUgWvsdshFKA",
    "expires_in":7200
}
```

### .get_access_token()

**该方法仅为自行维护单机版 access_token 使用**

获取 access_token 及 access_token 过期日期, 仅供缓存使用。 如果希望得到原生的 access_token 请求数据请使用 `grant_access_token`。

**Return:** dict 对象, key 包括 `access_token` 及 `access_token_expires_at`，示例：

```json
{
    "access_token":"Uj6gDn1My01ElQvLXjudqdXlnTYosqWnxPT-1AX_jJEqeYhbqASZXPlnur7k6YV7Erjvd_JDXbQWeZYIMmu958WV4VWe7GKD65q_VLHecTp8nA5DwU_DOdmVBACU2wDkPGBbAHAEVQ",
    "access_token_expires_at":1454476716
}
```

### .get_jsapi_ticket()

**该方法仅为自行维护单机版 jsapi_ticket 使用**

获取 jsapi_ticket 及 jsapi_ticket 过期日期, 仅供缓存使用, 如果希望得到原生的 jsapi_ticket 请求数据请使用 `grant_jsapi_ticket`。

**Return:** dict 对象, key 包括 `jsapi_ticket` 及 `jsapi_ticket_expires_at`，示例：

```json
{
    "jsapi_ticket":"bxLdikRXVbTPdHSM05e5u8EoHz_JA7Re-noqE0ZAnxk3XzAntyhT4_k272aJ4LprCM68rVXv6DDydT7JW1Mwsw",
    "jsapi_ticket_expires_at": 1454476720
}
```

## 异常

当提供参数不足时，会抛出 `wechat_sdk.exceptions.NeedParamError` 异常。

示例（仅提供了 `appid` 参数却调用了需要 `appid` 和 `appsecret` 的 `get_access_token()` 方法）：

    >>> from wechat_sdk import WechatConf
    >>> conf = WechatConf(appid='wxa81b377716e65e59')
    >>> conf.get_access_token()
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "wechat_sdk/core/conf.py", line 236, in get_access_token
        self._check_appid_appsecret()
      File "wechat_sdk/core/conf.py", line 270, in _check_appid_appsecret
        raise NeedParamError('Please provide app_id and app_secret parameters in the construction of class.')
    wechat_sdk.exceptions.NeedParamError: Please provide app_id and app_secret parameters in the construction of class.
    


