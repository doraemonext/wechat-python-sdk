==========================
 FAQ 汇总
==========================

1. 当使用 == 操作符比较两边内容时出现警告：

::

   UnicodeWarning: Unicode equal comparison failed to convert both arguments to Unicode - interpreting them as being unequal

**解决方案:**

因为在 ``wechat-python-sdk`` 内部，所有中文字符串均为 ``unicode`` 类型，如果您使用了一个 ``str`` 类型的字符串作比较，就会出现上述问题，解决方案很简单，把您的 ``str`` 类型的字符串转换为 ``unicode`` 类型即可。
