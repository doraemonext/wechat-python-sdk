# -*- coding: utf-8 -*-

import base64
from datetime import datetime, timedelta

from django.conf import settings
from django.utils import timezone
from django.utils.crypto import constant_time_compare
from django.utils.crypto import salted_hmac
from django.utils.encoding import force_bytes

try:
    from django.utils.module_loading import import_string as import_by_string   # For Django 1.7+
except ImportError:
    from django.utils.module_loading import import_by_path as import_by_string  # For Django 1.6

from wechat_sdk.context.framework.django.exceptions import SuspiciousOpenID

DEFAULT_WECHAT_CONTEXT_SERIALIZER = 'wechat_sdk.context.framework.django.serializers.JSONSerializer'  # 默认微信上下文对话序列化类
DEFAULT_WECHAT_CONTEXT_AGE = 7200  # 默认微信上下文对话有效时间 (单位: s)


class CreateError(Exception):
    pass


class ContextBase(object):
    """
    所有上下文对话类的基类
    """

    def __init__(self, openid):
        self._openid = openid
        self.accessed = False
        self.modified = False
        try:
            self.serializer = import_by_string(settings.WECHAT_CONTEXT_SERIALIZER)
        except AttributeError:
            self.serializer = import_by_string(DEFAULT_WECHAT_CONTEXT_SERIALIZER)

    def __contains__(self, openid):
        return openid in self._context

    def __getitem__(self, openid):
        return self._context[openid]

    def __setitem__(self, openid, context_data):
        self._context[openid] = context_data
        self.modified = True

    def __delitem__(self, openid):
        del self._context[openid]
        self.modified = True

    def get(self, openid, default=None):
        return self._context.get(openid, default)

    def pop(self, openid, *args):
        self.modified = self.modified or openid in self._context
        return self._context.pop(openid, *args)

    def setdefault(self, openid, context_data):
        if openid in self._context:
            return self._context[openid]
        else:
            self.modified = True
            self._context[openid] = context_data
            return context_data

    def _hash(self, value):
        return salted_hmac('wechat_sdk.context.framework.django', value).hexdigest()

    def encode(self, context_dict):
        serialized = self.serializer().dumps(context_dict)
        hash = self._hash(serialized)
        return base64.b64encode(hash.encode() + b':' + serialized).decode('ascii')

    def decode(self, context_data):
        encoded_data = base64.b64decode(force_bytes(context_data))
        try:
            hash, serialized = encoded_data.split(b':', 1)
            expected_hash = self._hash(serialized)
            if not constant_time_compare(hash.decode(), expected_hash):
                raise SuspiciousOpenID('Context data corrupted')
            else:
                return self.serializer().loads(serialized)
        except Exception as e:
            # TODO: logger
            return {}

    def update(self, dict_):
        self._context.update(dict_)
        self.modified = True

    def has_key(self, openid):
        return openid in self._context

    def keys(self):
        return self._context.keys()

    def values(self):
        return self._context.values()

    def items(self):
        return self._context.items()

    def iterkeys(self):
        return self._context.iterkeys()

    def itervalues(self):
        return self._context.itervalues()

    def iteritems(self):
        return self._context.iteritems()

    def clear(self):
        self._context_cache = {}
        self.modified = True
        self.accessed = True

    def _get_openid(self):
        return self._openid

    openid = property(_get_openid)

    def _get_context(self, no_load=False):
        self.accessed = True
        try:
            return self._context_cache
        except AttributeError:
            if no_load:
                self._context_cache = {}
            else:
                self._context_cache = self.load()
        return self._context_cache

    _context = property(_get_context)

    def get_expiry_age(self, **kwargs):
        try:
            modification = kwargs['modification']
        except KeyError:
            modification = timezone.now()
        try:
            expiry = kwargs['expiry']
        except KeyError:
            expiry = self.get('_context_expiry')

        if not expiry:  # 检查 0 和 None 的情况
            try:
                return settings.WECHAT_CONTEXT_AGE
            except AttributeError:
                return DEFAULT_WECHAT_CONTEXT_AGE
        if not isinstance(expiry, datetime):
            return expiry
        delta = expiry - modification
        return delta.days * 86400 + delta.seconds

    def get_expiry_date(self, **kwargs):
        try:
            modification = kwargs['modification']
        except KeyError:
            modification = timezone.now()
        try:
            expiry = kwargs['expiry']
        except KeyError:
            expiry = self.get('_context_expiry')

        if isinstance(expiry, datetime):
            return expiry
        if not expiry:
            try:
                expiry = settings.WECHAT_CONTEXT_AGE
            except AttributeError:
                expiry = DEFAULT_WECHAT_CONTEXT_AGE
        return modification + timedelta(seconds=expiry)

    def set_expiry(self, value):
        if value is None:
            try:
                del self['_context_expiry']
            except KeyError:
                pass
            return
        if isinstance(value, timedelta):
            value = timezone.now() + value
        self['_context_expiry'] = value

    def flush(self):
        self.clear()
        self.save()

    def exists(self, openid):
        """
        当 openid 存在时返回 True
        """
        raise NotImplementedError('subclasses of ContextBase must provide an exists() method')

    def create(self, openid):
        """
        根据 openid 新建一个上下文对话存储
        """
        raise NotImplementedError('subclasses of ContextBase must provide an create() method')

    def save(self):
        raise NotImplementedError('subclasses of ContextBase must provide an save() method')

    def delete(self, openid=None):
        raise NotImplementedError('subclasses of ContextBase must provide an delete() method')

    def load(self):
        raise NotImplementedError('subclasses of ContextBase must provide an load() method')

    @staticmethod
    def clear_expired():
        raise NotImplementedError('This backend does not support clear_expired().')