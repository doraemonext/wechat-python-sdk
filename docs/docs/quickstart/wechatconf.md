# 快速上手 - WechatConf 详解

WechatConf 是 **微信配置类**，你需要将在公众平台开发者选项中的 Token/AppID/AppSecret/EncodingAESKey 等信息传入其中，之后该类将会自行维护相关配置信息（access_token/jsapi_ticket）的有效性，支持分布式。

> Tips: v0.6.0 以前版本的用户请尽快迁移到 WechatConf 方式，原初始化方式将不会继续维护（但会一直保持兼容），也不会提供 EncodingAESKey 加密。

## 基本信息传入

WechatConf 接受的基本信息包括：

* Token
* App ID
* App Secret
* Encrypt Mode （消息加解密模式，可选项有 `normal`（明文模式）、`compatible`（兼容模式）、`safe`（安全模式）
* EncodingAESKey （当 Encrypt Mode 为 `normal` 时无需传入此项）

使用方式也很简单，示例：

```python
from wechat_sdk import WechatConf
conf = WechatConf(
    token='your_token', 
    appid='your_appid', 
    appsecret='your_appsecret', 
    encrypt_mode='safe',  # 可选项：normal/compatible/safe，分别对应于 明文/兼容/安全 模式
    encoding_aes_key='your_encoding_aes_key'  # 如果传入此值则必须保证同时传入 token, appid
)
```

根据你自己需要传入对应参数即可，所有项均为可选项。

## access_token 维护

如果你在使用 WechatConf 的时候只传入基本信息，则会在每次实例化时请求一次 access_token。每天的 access_token 有着固定的次数限制，而且每次请求新的 access_token 会拖慢代码执行效率，所以，**你需要根据你的代码运行环境及你的个人喜好选择下面任意一种方式缓存 access_token 的值。**

### 方式 1 - 单机环境

单机环境下，可以将 access_token 及过期时间存放在任意位置（磁盘文件/数据库/缓存等）。你需要做的只是在每次 WechatConf 实例化的时候将你存储的 access_token 和 access_token_expires_at 作为参数传入即可，示例如下：

```python
access_token = get_access_token_from_somewhere()
access_token_expires_at = get_access_token_expires_at_from_somewhere()

conf = WechatConf(
    ... ,  # 基本信息传入，此处忽略
    access_token=access_token,
    access_token_expires_at=access_token_expires_at,
)
```

当第一次实例化没有有效的 access_token 时，这两个参数全部传入 `None` 即可。

实例化完成后（首次实例化两个参数均使用 `None`），你需要在该实例有效期内的任意时刻调用 [`.get_access_token()`](/api/wechatconf.md#get_access_token) 方法获得自动维护过的新的 access_token 和 access_token_expires_at 值，然后将他们用你自己的方式（磁盘文件/数据库/缓存）进行保存，方便下次实例化的时候传入。

[`.get_access_token()`](/api/wechatconf.md#get_access_token) 的返回示例如下：

```python
{
    "access_token":"Uj6gDn1My01ElQvLXjudqdXlnTYosqWnxPT-1AX_jJEqeYhbqASZXPlnur7k6YV7Erjvd_JDXbQWeZYIMmu958WV4VWe7GKD65q_VLHecTp8nA5DwU_DOdmVBACU2wDkPGBbAHAEVQ",
    "access_token_expires_at":1454476716
}
```

### 方式 2 - 单机环境

第二种方式将 access_token 及 access_token_expires_at 的获取与设置的权利完全交付与你。你只需要写两个函数，分别去获取 access_token 和设置 access_token 即可。示例如下：

```python
def get_access_token_function():
    """ 注意返回值为一个 Tuple，第一个元素为 access_token 的值，第二个元素为 access_token_expires_at 的值 """
    return get_access_token_from_somewhere()  # 此处通过你自己的方式获取 access_token

def set_access_token_function(access_token, access_token_expires_at):
    set_access_token_to_somewhere(access_token, access_token_expires_at)  # 此处通过你自己的方式设置 access_token
```

接着你需要做的就是在 WechatConf 实例化的时候将这两个函数作为参数传入，如下：

```python
from wechat_sdk import WechatConf
conf = WechatConf(
    ... ,  # 基本信息传入，此处忽略
    access_token_getfunc=get_access_token_function,
    access_token_setfunc=set_access_token_function,
)
```

经过以上步骤，WechatConf 实例内部在维护 access_token 有效性时均会调用你自己的函数去操作。

### 方式 3 - 分布式环境

如果你需要在分布式环境下使用 wechat-python-sdk，那么服务器的类型分两种，一种是中控服务器，另一种是业务逻辑服务器：

* 中控服务器用于 access_token 的获取和刷新，为业务逻辑服务器提供获取接口以及强制刷新接口。仅需一台中控服务器。
* 业务逻辑服务器的 access_token 均是调用中控服务器的接口得来，禁止业务逻辑服务器自行刷新 access_token。

#### 中控服务器

中控服务器的设置参考 [方式 2 - 单机环境](#2-) 设置即可，推荐将 access_token 及 access_token_expires_at 放置于缓存服务器中。对外提供的接口需自行编写。

#### 业务逻辑服务器

业务逻辑服务器的设置同样也参考 [方式 2 - 单机环境](#2-) 设置，唯一不同的一点是：

获取和设置 access_token 均需要调用中控服务器的对外接口。

## jsapi_ticket 维护

**如果你的代码中并未涉及 JSSDK 的相关内容，那么你可以直接跳过本节。**

如果你在使用 WechatConf 的时候只传入基本信息，则会在每次实例化时请求一次 jsapi_ticket。每天的 jsapi_ticket 有着固定的次数限制，而且每次请求新的 jsapi_ticket 会拖慢代码执行效率，所以，**你需要根据你的代码运行环境及你的个人喜好选择下面任意一种方式缓存 jsapi_ticket 的值。**

### 方式 1 - 单机环境

单机环境下，可以将 jsapi_ticket 及过期时间存放在任意位置（磁盘文件/数据库/缓存等）。你需要做的只是在每次 WechatConf 实例化的时候将你存储的 jsapi_ticket 和 jsapi_ticket_expires_at 作为参数传入即可，示例如下：

```python
jsapi_ticket = get_jsapi_ticket_from_somewhere()
jsapi_ticket_expires_at = get_jsapi_ticket_expires_at_from_somewhere()

conf = WechatConf(
    ... ,  # 基本信息传入，此处忽略
    jsapi_ticket=jsapi_ticket,
    jsapi_ticket_expires_at=jsapi_ticket_expires_at,
)
```

当第一次实例化没有有效的 jsapi_ticket 时，这两个参数全部传入 `None` 即可。

实例化完成后（首次实例化两个参数均使用 `None`），你需要在该实例有效期内的任意时刻调用 [`.get_jsapi_ticket()`](/api/wechatconf.md#get_jsapi_ticket) 方法获得自动维护过的新的 jsapi_ticket 和 jsapi_ticket_expires_at 值，然后将他们用你自己的方式（磁盘文件/数据库/缓存）进行保存，方便下次实例化的时候传入。

[`.get_jsapi_ticket()`](/api/wechatconf.md#get_jsapi_ticket) 的返回示例如下：

```python
{
    "jsapi_ticket":"bxLdikRXVbTPdHSM05e5u8EoHz_JA7Re-noqE0ZAnxk3XzAntyhT4_k272aJ4LprCM68rVXv6DDydT7JW1Mwsw",
    "jsapi_ticket_expires_at": 1454476720
}
```

### 方式 2 - 单机环境

第二种方式将 jsapi_ticket 及 jsapi_ticket_expires_at 的获取与设置的权利完全交付与你。你只需要写两个函数，分别去获取 jsapi_ticket 和设置 jsapi_ticket 即可。示例如下：

```python
def get_jsapi_ticket_function():
    """ 注意返回值为一个 Tuple，第一个元素为 jsapi_ticket 的值，第二个元素为 jsapi_ticket_expires_at 的值 """
    return get_jsapi_ticket_from_somewhere()  # 此处通过你自己的方式获取 jsapi_ticket

def set_jsapi_ticket_function(jsapi_ticket, jsapi_ticket_expires_at):
    set_jsapi_ticket_to_somewhere(jsapi_ticket, jsapi_ticket_expires_at)  # 此处通过你自己的方式设置 jsapi_ticket
```

接着你需要做的就是在 WechatConf 实例化的时候将这两个函数作为参数传入，如下：

```python
from wechat_sdk import WechatConf
conf = WechatConf(
    ... ,  # 基本信息传入，此处忽略
    jsapi_ticket_getfunc=get_jsapi_ticket_function,
    jsapi_ticket_setfunc=set_jsapi_ticket_function,
)
```

经过以上步骤，WechatConf 实例内部在维护 jsapi_ticket 有效性时均会调用你自己的函数去操作。

### 方式 3 - 分布式环境

如果你需要在分布式环境下使用 wechat-python-sdk，那么服务器的类型分两种，一种是中控服务器，另一种是业务逻辑服务器：

* 中控服务器用于 jsapi_ticket 的获取和刷新，为业务逻辑服务器提供获取接口以及强制刷新接口。仅需一台中控服务器。
* 业务逻辑服务器的 jsapi_ticket 均是调用中控服务器的接口得来，禁止业务逻辑服务器自行刷新 jsapi_ticket。

#### 中控服务器

中控服务器的设置参考 [方式 2 - 单机环境](#2-_1) 设置即可，推荐将 jsapi_ticket 及 jsapi_ticket_expires_at 放置于缓存服务器中。对外提供的接口需自行编写。

#### 业务逻辑服务器

业务逻辑服务器的设置同样也参考 [方式 2 - 单机环境](#2-_1) 设置，唯一不同的一点是：

获取和设置 jsapi_ticket 均需要调用中控服务器的对外接口。

## 下一步   

现在你已经了解了如何将基本信息传入 WechatConf 并自行维护 access_token 及 jsapi_ticket 的有效性。

接下来，你可以：

* 继续阅读 [WechatConf API](/api/wechatconf.md) 加深对 WechatConf 的印象
* 直接点击导航栏上方的的 **官方接口** 或 **扩展接口**，选择自己需要的章节进行阅读

