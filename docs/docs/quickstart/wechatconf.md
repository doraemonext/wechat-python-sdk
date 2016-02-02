# 快速上手 - WechatConf 详解

WechatConf 是 **微信配置类**，你需要将在公众平台开发者选项中的 Token/AppID/AppSecret/EncodingAESKey 等信息传入其中，之后该类将会自行维护相关配置信息（access_token/jsapi_ticket）的有效性，支持分布式。

> Tips: v0.6.0 以前版本的用户请尽快迁移到 WechatConf 方式，原初始化方式将不会继续维护（但会一直保持兼容），也不会提供 EncodingAESKey 加密。

## WechatConf()

**signature:** 

```python
WechatConf(token=None, appid=None, appsecret=None, encrypt_mode='safe', encoding_aes_key=None,
           access_token_getfunc=None, access_token_setfunc=None, access_token=None, 
           access_token_expires_at=None, jsapi_ticket_getfunc=None, jsapi_ticket_setfunc=None, 
           jsapi_ticket=None, jsapi_ticket_expires_at=None, checkssl=False)
```

参数说明：

* `token`: 公众平台开发者选项中你设置的 Token
* `appid`: 公众平台开发者选项中的 App ID
* `appsecret`: 公众平台开发者选项中的 App Secret
* `encrypt_mode`: 消息加解密方式。可选项 `normal`（明文模式）、`compatible`（兼容模式）、`safe`（安全模式）
* `encoding_aes_key`: 公众平台开发者选项中的 EncodingAESKey
* `access_token_getfunc`: access_token 获取函数。如果传入该参数，WechatConf 内部将会在需要使用 access_token 时直接调用该函数，该函数不应接受任何参数。
* `access_token_setfunc`: access_token 设置函数。如果传入该参数，WechatConf 内部将会在需要更新 access_token 时直接调用该函数，该函数应接受一个参数，为 access_token 的字符串值。
* `access_token`: 
* `access_token_expires_at`: access_token 的过期时间
* `jsapi_ticket_getfunc`:
* `jsapi_ticket_setfunc`:
* `jsapi_ticket`: 
* `jsapi_ticket_expires_at`:
* `checkssl`: 

