微信公众平台 Python 开发包文档
====================================

**当前代码还未完成全部功能，非官方接口功能尚不能使用，请耐心等待代码及文档的完善。**

非官方微信公众平台 Python 开发包，包括官方接口和非官方接口。

* 官方接口依据公众平台开发者文档编写，可以实现公众平台开发者文档中的所有内容；

* 非官方接口采用模拟登陆的方式，可以实现更多高级功能，但也存在相应风险。尤其注意，本开发包不提供群发功能，此功能被微信公众平台明令禁止。

**请注意：本开发包并不打算提供一个独立的完整微信解决方案，我们更希望这个开发包可以非常融洽的在各个框架中进行集成并使用，对于HTTP请求及响应方面并不涉及，该开发包仅仅接受必要参数，提供各种微信操作的方法，并返回相应的可以响应微信服务器的数据(Response)或操作执行结果。**

项目地址：`https://github.com/doraemonext/wechat-python-sdk <https://github.com/doraemonext/wechat-python-sdk>`_

目录：

.. toctree::
   :maxdepth: 2

   install
   tutorial
   basic
   ext
   messages

感谢 `WeRoBot <https://github.com/whtsky/WeRoBot>`_ 项目，本项目中官方接口的许多代码均借鉴于此。

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
