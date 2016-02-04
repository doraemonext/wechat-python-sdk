# 官方接口 - 自定义菜单

## 自定义菜单创建

**调用方法：**`.create_menu(menu_data)`

**参数说明：**

* `menu`: dict 对象，描述了菜单的内容，示例如下：

        {
            'button':[
                {
                    'type': 'click',
                    'name': '今日歌曲',
                    'key': 'V1001_TODAY_MUSIC'
                },
                {
                    'type': 'click',
                    'name': '歌手简介',
                    'key': 'V1001_TODAY_SINGER'
                },
                {
                    'name': '菜单',
                    'sub_button': [
                        {
                            'type': 'view',
                            'name': '搜索',
                            'url': 'http://www.soso.com/'
                        },
                        {
                            'type': 'view',
                            'name': '视频',
                            'url': 'http://v.qq.com/'
                        },
                        {
                            'type': 'click',
                            'name': '赞一下我们',
                            'key': 'V1001_GOOD'
                        }
                    ]
                }
            ]
        }

**调用前检查：**App ID / App Secret

**返回值：**正常返回官方接口的 JSON 数据：`{"errcode": 0, "errmsg": "ok"}`，一般无需理会该返回值，创建失败会抛出异常，捕获异常即可。

**异常：**当发生失败时抛出 [`exceptions.OfficialAPIError`](/api/exception.md#officialapierror) 异常，该异常包含了错误的代号与原因信息。

**对应官方文档：**[自定义菜单创建接口](http://mp.weixin.qq.com/wiki/10/0234e39a2025342c17a7d23595c6b40a.html)

## 自定义菜单查询

**调用方法：**`.get_menu()`

**调用前检查：**App ID / App Secret

**返回值：**正常返回官方接口的 JSON 数据，因示例过长，请直接点击 [自定义菜单查询接口](http://mp.weixin.qq.com/wiki/5/f287d1a5b78a35a8884326312ac3e4ed.html) 查看。

**异常：**当发生失败时抛出 [`exceptions.OfficialAPIError`](/api/exception.md#officialapierror) 异常，该异常包含了错误的代号与原因信息。

**对应官方文档：**[自定义菜单查询接口](http://mp.weixin.qq.com/wiki/5/f287d1a5b78a35a8884326312ac3e4ed.html)

## 自定义菜单删除

**调用方法：**`.delete_menu()`

**调用前检查：**App ID / App Secret

**返回值：**正常返回官方接口的 JSON 数据：`{"errcode": 0, "errmsg": "ok"}`，一般无需理会该返回值，删除失败会抛出异常，捕获异常即可。

**异常：**当发生失败时抛出 [`exceptions.OfficialAPIError`](/api/exception.md#officialapierror) 异常，该异常包含了错误的代号与原因信息。

**对应官方文档：**[自定义菜单删除接口](http://mp.weixin.qq.com/wiki/3/de21624f2d0d3dafde085dafaa226743.html)

## 自定义菜单事件推送

当自定义菜单事件推送 XML 到达并经过 [`.parse_data()`](/official/message.md#xml) 方法解析后，你可以通过下面的代码判断该信息属于事件：

```python
from wechat_sdk.messages import EventMessage
if isinstance(wechat.message, EventMessage):
```

然后你可以继续通过 `wechat.message.type` 来继续判断它属于下列哪种事件并获取事件内容。

### 点击菜单拉取消息时的事件推送

判断代码：`wechat.message.type == 'click'`

判断后的信息获取：

* `wechat.message.key` 对应于 XML 信息中的 `EventKey`，与自定义菜单中的 KEY 值相对应

### 点击菜单跳转链接时的事件推送

判断代码：`wechat.message.type == 'view'`

判断后的信息获取：

* `wechat.message.key` 对应于 XML 信息中的 `EventKey`
* `wechat.message.menu_id` 对应于 XML 信息中的 `MenuId`，指菜单 ID，如果是个性化菜单，则可以通过这个字段，知道是哪个规则的菜单被点击了

### scancode_push：扫码推事件的事件推送

判断代码：`wechat.message.type == 'scancode_push'`

判断后的信息获取：

* `wechat.message.key` 对应于 XML 信息中的 `EventKey`
* `wechat.message.ScanCodeInfo` 对应于 XML 信息中的 `ScanCodeInfo`，扫描信息

### scancode_waitmsg：扫码推事件且弹出“消息接收中”提示框的事件推送

判断代码：`wechat.message.type == 'scancode_waitmsg'`

判断后的信息获取：

* `wechat.message.key` 对应于 XML 信息中的 `EventKey`
* `wechat.message.ScanCodeInfo` 对应于 XML 信息中的 `ScanCodeInfo`，扫描信息 

### pic_sysphoto：弹出系统拍照发图的事件推送

判断代码：`wechat.message.type == 'pic_sysphoto'`

判断后的信息获取：

* `wechat.message.key` 对应于 XML 信息中的 `EventKey`
* `wechat.message.SendPicsInfo` 对应于 XML 信息中的 `SendPicsInfo`，发送的图片信息

### pic_photo_or_album：弹出拍照或者相册发图的事件推送

判断代码：`wechat.message.type == 'pic_photo_or_album'`

判断后的信息获取：

* `wechat.message.key` 对应于 XML 信息中的 `EventKey`
* `wechat.message.SendPicsInfo` 对应于 XML 信息中的 `SendPicsInfo`，发送的图片信息

### pic_weixin：弹出微信相册发图器的事件推送

判断代码：`wechat.message.type == 'pic_weixin'`

判断后的信息获取：

* `wechat.message.key` 对应于 XML 信息中的 `EventKey`
* `wechat.message.SendPicsInfo` 对应于 XML 信息中的 `SendPicsInfo`，发送的图片信息

### location_select：弹出地理位置选择器的事件推送

判断代码：`wechat.message.type == 'location_select'`

判断后的信息获取：

* `wechat.message.key` 对应于 XML 信息中的 `EventKey`
* `wechat.message.SendLocationInfo` 对应于 XML 信息中的 `SendLocationInfo`，发送的位置信息

## 个性化菜单接口

待开发

## 获取公众号的菜单配置 

待开发

