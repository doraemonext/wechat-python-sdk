# -*- coding: utf-8 -*-

from django.db import IntegrityError, transaction, router
from django.utils import timezone

from wechat_sdk.context.framework.django.backends.base import ContextBase, CreateError
from wechat_sdk.context.framework.django.exceptions import SuspiciousOpenID


class ContextStore(ContextBase):
    """
    数据库存储微信上下文对话
    """
    def __init__(self, openid):
        super(ContextStore, self).__init__(openid)

    def load(self):
        try:
            s = Context.objects.get(
                openid=self.openid,
                expire_date__gt=timezone.now()
            )
            return self.decode(s.context_data)
        except (Context.DoesNotExist, SuspiciousOpenID) as e:
            self.create(self.openid)
            return {}

    def exists(self, openid):
        return Context.objects.filter(openid=openid).exists()

    def create(self, openid):
        self.save(must_create=True)
        self.modified = True
        self._session_cache = {}
        return

    def save(self, must_create=False):
        obj = Context(
            openid=self.openid,
            context_data=self.encode(self._get_context(no_load=must_create)),
            expire_date=self.get_expiry_date()
        )
        self.clear_expired()
        using = router.db_for_write(Context, instance=obj)
        try:
            with transaction.atomic(using=using):
                obj.save(force_insert=must_create, using=using)
        except IntegrityError:
            if must_create:
                raise CreateError
            raise

    def delete(self, openid=None):
        if openid is None:
            openid = self.openid
        try:
            Context.objects.get(openid=openid).delete()
        except Context.DoesNotExist:
            pass

    @staticmethod
    def clear_expired():
        Context.objects.filter(expire_date__lt=timezone.now()).delete()


from wechat_sdk.context.framework.django.models import Context