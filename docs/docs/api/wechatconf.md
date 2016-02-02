# WechatConf API

WechatConf 是 微信配置类，你需要将在公众平台开发者选项中的 Token/AppID/AppSecret/EncodingAESKey 等信息传入其中，之后该类将会自行维护相关配置信息（access_token/jsapi_ticket）的有效性，支持分布式。

## WechatConf()

**导入方式：**`from wechat_sdk import WechatConf`

**signature:** 

```python
WechatConf(token=None, appid=None, appsecret=None, encrypt_mode='safe', encoding_aes_key=None,
           access_token_getfunc=None, access_token_setfunc=None, access_token=None, 
           access_token_expires_at=None, jsapi_ticket_getfunc=None, jsapi_ticket_setfunc=None, 
           jsapi_ticket=None, jsapi_ticket_expires_at=None, checkssl=False)
```

|参数名称|参数解释|
|-------|-------|
|`token`|公众平台开发者选项中你设置的 Token|
|`appid`|公众平台开发者选项中的 App ID|
|`appsecret`|公众平台开发者选项中的 App Secret|
|`encrypt_mode`|消息加解密方式。可选项 `normal`（明文模式）、`compatible`（兼容模式）、`safe`（安全模式）|
|`encoding_aes_key`|公众平台开发者选项中的 EncodingAESKey|
|`access_token_getfunc`|access_token 获取函数。如果传入该参数，WechatConf 内部将会在需要使用 access_token 时直接调用该函数，该函数不应接受任何参数。|
|`access_token_setfunc`|access_token 设置函数。如果传入该参数，WechatConf 内部将会在需要更新 access_token 时直接调用该函数，该函数应接受一个参数，为 access_token 的字符串值。|
|`access_token`|直接导入的 access token 值, 该值需要在上一次该类实例化之后手动进行缓存并在此处传入, 如果不传入, 将会在需要时自动重新获取 **(传入 access_token_getfunc 和 access_token_setfunc 函数后将会自动忽略此处的传入值)**|
|`access_token_expires_at`|直接导入的 access token 的过期日期, 该值需要在上一次该类实例化之后手动进行缓存并在此处传入, 如果不传入, 将会在需要时自动重新获取 **(传入 access_token_getfunc 和 access_token_setfunc 函数后将会自动忽略此处的传入值)**|
|`jsapi_ticket_getfunc`|jsapi_ticket 获取函数。如果传入该参数，WechatConf 内部将会在需要使用 jsapi_ticket 时直接调用该函数，该函数不应接受任何参数。|
|`jsapi_ticket_setfunc`|jsapi_ticket 设置函数。如果传入该参数，WechatConf 内部将会在需要更新 jsapi_ticket 时直接调用该函数，该函数应接受一个参数，为 jsapi_ticket 的字符串值。|
|`jsapi_ticket`|直接导入的 jsapi ticket 值, 该值需要在上一次该类实例化之后手动进行缓存并在此处传入, 如果不传入, 将会在需要时自动重新获取 **(传入 jsapi_ticket_getfunc 和 jsapi_ticket_setfunc 函数后将会自动忽略此处的传入值)**|
|`jsapi_ticket_expires_at`|直接导入的 jsapi ticket 的过期日期, 该值需要在上一次该类实例化之后手动进行缓存并在此处传入, 如果不传入, 将会在需要时自动重新获取 **(传入 jsapi_ticket_getfunc 和 jsapi_ticket_setfunc 函数后将会自动忽略此处的传入值)**|
|`checkssl`|是否检查 SSL, 默认不检查 (False), 可避免 urllib3 的 InsecurePlatformWarning 警告|

### 属性

|属性名称|属性解释|
|-------|------|
|`.token`|当前正在使用的 Token 值|
|`.appid`|当前正在使用的 App ID 值|
|`.appsecret`|当前正在使用的 App Secret 值|
|`.encrypt_mode`|当前正在使用的消息加解密方式。返回内容为字符串，`normal`为明文模式，`compatible`为兼容模式，`safe`为安全模式|
|`.encoding_aes_key`|当前正在使用的 EncodingAESKey|
|`.crypto`|当前 Crypto 实例，可直接用于加密解密消息操作|
|`.access_token`|当前的 access_token 值，该值会由 WechatConf 内部动态维护合法性|
|`.jsapi_ticket`|当前的 jsapi_ticket 值，该值会由 WechatConf 内部动态维护合法性|

### 方法

|属性名称|属性解释|
|-------|------|
|`.grant_

