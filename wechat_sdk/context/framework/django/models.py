# -*- coding: utf-8 -*-

from django.db import models


class ContextManager(models.Manager):
    def encode(self, openid, context_dict):
        return ContextStore(openid).encode(context_dict)

    def save(self, openid, context_dict, expire_date):
        s = self.model(openid, self.encode(openid, context_dict), expire_date)
        if context_dict:
            s.save()
        else:
            s.delete()  # 清除该 OpenID 下所有的上下文对话数据
        return s


class Context(models.Model):
    openid = models.CharField(u'用户OpenID', max_length=50, primary_key=True)
    context_data = models.TextField(u'上下文对话数据')
    expire_date = models.DateTimeField(u'过期日期', db_index=True)
    objects = ContextManager()

    class Meta:
        db_table = 'wechat_context'
        verbose_name = u'微信上下文对话'
        verbose_name_plural = u'微信上下文对话'

    def get_decoded(self):
        return ContextStore(self.openid).decode(self.context_data)


from wechat_sdk.context.framework.django.backends.db import ContextStore