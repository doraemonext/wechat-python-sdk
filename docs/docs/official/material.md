# 官方接口 - 素材管理

## 新增临时素材

原“上传多媒体文件”接口。

**调用方法：**`.upload_media(media_type, media_file, extension='')`

**参数说明：**

* `media_type`: 媒体文件类型字符串，分别有图片（`image`）、语音（`voice`）、视频（`video`）和缩略图（`thumb`）
* `media_file`: 要上传的文件，一个 File object 或 StringIO object
* `extension`: 如果 media_file 传入的为 StringIO object，那么必须传入 extension 显示指明该媒体文件扩展名，如 `mp3`, `amr`；如果 media_file 传入的为 File object，那么该参数请留空

**调用前检查：**App ID / App Secret

**返回值：**正常返回官方接口的 JSON 数据，示例：

```json
{
    "media_id": "dPlluMsb5R5uw24i-bUKNi7_MMTJ2enonGNkjmbcSlJjzsD2SdAB7DICkU8JIfjK", 
    "created_at": 1454546204, 
    "type": "image"
}
```

**异常：**当发生失败时抛出 [`exceptions.OfficialAPIError`](/api/exception.md#officialapierror) 异常，该异常包含了错误的代号与原因信息。

**对应官方文档：**[新增临时素材](http://mp.weixin.qq.com/wiki/15/2d353966323806a202cd2deaafe8e557.html)

## 获取临时素材

原“下载多媒体文件”接口。

**调用方法：**`.download_media(media_id)`

**参数说明：**

* `media_id`: 需要下载文件的 Media ID

**调用前检查：**App ID / App Secret

**返回值：**当请求成功时，返回一个 [`requests.Response`](http://docs.python-requests.org/en/master/api/#requests.Response) 对象，下面示例将该对象存储为本地文件：

```python
response = wechat.download_media('your media id')
with open('yourfilename', 'wb') as fd:
    for chunk in response.iter_content(1024):
        fd.write(chunk)
```

**异常：**当发生失败时抛出 [`exceptions.OfficialAPIError`](/api/exception.md#officialapierror) 异常，该异常包含了错误的代号与原因信息。

**对应官方文档：**[获取临时素材](http://mp.weixin.qq.com/wiki/9/677a85e3f3849af35de54bb5516c2521.html)

## 新增永久素材

待开发

## 获取永久素材

待开发

## 删除永久素材

待开发

## 修改永久图文素材

待开发

## 获取素材总数

待开发

## 获取素材列表

待开发

