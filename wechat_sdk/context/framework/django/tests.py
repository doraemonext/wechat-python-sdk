# -*- coding: utf-8 -*-

from datetime import timedelta

from django.conf import settings
from django.test import TestCase
from django.utils import six
from django.utils import timezone

from wechat_sdk.context.framework.django.backends.db import ContextStore as DatabaseContext
from wechat_sdk.context.framework.django.backends.base import DEFAULT_WECHAT_CONTEXT_AGE
from wechat_sdk.context.framework.django.models import Context


class ContextTestsMixin(object):
    backend = None  # 子类必须指定

    def setUp(self):
        self.context = self.backend(openid='openid')

    def tearDown(self):
        self.context.delete()

    def test_new_context(self):
        self.assertFalse(self.context.modified)
        self.assertFalse(self.context.accessed)

    def test_get_empty(self):
        self.assertEqual(self.context.get('cat'), None)

    def test_store(self):
        self.context['cat'] = 'dog'
        self.assertTrue(self.context.modified)
        self.assertEqual(self.context.pop('cat'), 'dog')

    def test_pop(self):
        self.context['some key'] = 'exists'
        self.assertEqual(self.context.pop('some key'), 'exists')
        self.assertTrue(self.context.accessed)
        self.assertTrue(self.context.modified)
        self.assertEqual(self.context.get('some key'), None)

    def test_pop_default(self):
        self.assertEqual(self.context.pop('some key', 'does not exist'), 'does not exist')
        self.assertTrue(self.context.accessed)
        self.assertFalse(self.context.modified)

    def test_setdefault(self):
        self.assertEqual(self.context.setdefault('foo', 'bar'), 'bar')
        self.assertEqual(self.context.setdefault('foo', 'baz'), 'bar')
        self.assertTrue(self.context.accessed)
        self.assertTrue(self.context.modified)

    def test_update(self):
        self.context.update({'update key': 1})
        self.assertTrue(self.context.accessed)
        self.assertTrue(self.context.modified)
        self.assertEqual(self.context.get('update key', None), 1)

    def test_has_key(self):
        self.context['some key'] = 1
        self.context.modified = False
        self.context.accessed = False
        self.assertIn('some key', self.context)
        self.assertTrue(self.context.accessed)
        self.assertFalse(self.context.modified)

    def test_values(self):
        self.assertEqual(list(self.context.values()), [])
        self.assertTrue(self.context.accessed)
        self.context['some key'] = 1
        self.assertEqual(list(self.context.values()), [1])

    def test_iterkeys(self):
        self.context['x'] = 1
        self.context.modified = False
        self.context.accessed = False
        i = six.iterkeys(self.context)
        self.assertTrue(hasattr(i, '__iter__'))
        self.assertTrue(self.context.accessed)
        self.assertFalse(self.context.modified)
        self.assertEqual(list(i), ['x'])

    def test_itervalues(self):
        self.context['x'] = 1
        self.context.modified = False
        self.context.accessed = False
        i = six.itervalues(self.context)
        self.assertTrue(hasattr(i, '__iter__'))
        self.assertTrue(self.context.accessed)
        self.assertFalse(self.context.modified)
        self.assertEqual(list(i), [1])

    def test_iteritems(self):
        self.context['x'] = 1
        self.context.modified = False
        self.context.accessed = False
        i = six.iteritems(self.context)
        self.assertTrue(hasattr(i, '__iter__'))
        self.assertTrue(self.context.accessed)
        self.assertFalse(self.context.modified)
        self.assertEqual(list(i), [('x', 1)])

    def test_clear(self):
        self.context['x'] = 1
        self.context.modified = False
        self.context.accessed = False
        self.assertEqual(list(self.context.items()), [('x', 1)])
        self.context.clear()
        self.assertEqual(list(self.context.items()), [])
        self.assertTrue(self.context.accessed)
        self.assertTrue(self.context.modified)

    def test_save(self):
        self.context.save()
        self.assertTrue(self.context.exists(self.context.openid))

    def test_delete(self):
        self.context.save()
        self.context.delete(self.context.openid)
        self.assertFalse(self.context.exists(self.context.openid))

    def test_default_expiry(self):
        try:
            self.assertEqual(self.context.get_expiry_age(), settings.WECHAT_CONTEXT_AGE)
        except AttributeError:
            self.assertEqual(self.context.get_expiry_age(), DEFAULT_WECHAT_CONTEXT_AGE)

        self.context.set_expiry(0)
        try:
            self.assertEqual(self.context.get_expiry_age(), settings.WECHAT_CONTEXT_AGE)
        except AttributeError:
            self.assertEqual(self.context.get_expiry_age(), DEFAULT_WECHAT_CONTEXT_AGE)

    def test_custom_expiry_seconds(self):
        modification = timezone.now()

        self.context.set_expiry(10)

        date = self.context.get_expiry_date(modification=modification)
        self.assertEqual(date, modification + timedelta(seconds=10))

        age = self.context.get_expiry_age(modification=modification)
        self.assertEqual(age, 10)

    def test_custom_expiry_timedelta(self):
        modification = timezone.now()

        # Mock timezone.now, because set_expiry calls it on this code path.
        original_now = timezone.now
        try:
            timezone.now = lambda: modification
            self.context.set_expiry(timedelta(seconds=10))
        finally:
            timezone.now = original_now

        date = self.context.get_expiry_date(modification=modification)
        self.assertEqual(date, modification + timedelta(seconds=10))

        age = self.context.get_expiry_age(modification=modification)
        self.assertEqual(age, 10)

    def test_custom_expiry_datetime(self):
        modification = timezone.now()

        self.context.set_expiry(modification + timedelta(seconds=10))

        date = self.context.get_expiry_date(modification=modification)
        self.assertEqual(date, modification + timedelta(seconds=10))

        age = self.context.get_expiry_age(modification=modification)
        self.assertEqual(age, 10)

    def test_custom_expiry_reset(self):
        self.context.set_expiry(None)
        self.context.set_expiry(10)
        self.context.set_expiry(None)
        try:
            self.assertEqual(self.context.get_expiry_age(), settings.WECHAT_CONTEXT_AGE)
        except AttributeError:
            self.assertEqual(self.context.get_expiry_age(), DEFAULT_WECHAT_CONTEXT_AGE)

    def test_decode(self):
        data = {'a test key': 'a test value'}
        encoded = self.context.encode(data)
        self.assertEqual(self.context.decode(encoded), data)


class DatabaseContextTests(ContextTestsMixin, TestCase):
    backend = DatabaseContext

    def test_context_get_decoded(self):
        self.context['x'] = 1
        self.context.save()

        s = Context.objects.get(openid=self.context.openid)

        self.assertEqual(s.get_decoded(), {'x': 1})

    def test_contextmanager_save(self):
        self.context['y'] = 1
        self.context.save()

        s = Context.objects.get(openid=self.context.openid)
        Context.objects.save(s.openid, {'y': 2}, s.expire_date)
        del self.context._context_cache
        self.assertEqual(self.context['y'], 2)

    def test_clearcontext(self):
        self.assertEqual(0, Context.objects.count())

        self.context['foo'] = 'bar'
        self.context.set_expiry(3600)
        self.context.save()

        other_context = self.backend(openid='test_open_id')
        other_context['foo'] = 'bar'
        other_context.set_expiry(-3600)
        other_context.save()

        self.assertEqual(2, Context.objects.count())
        DatabaseContext.clear_expired()
        self.assertEqual(1, Context.objects.count())

    def test_flush(self):
        self.assertEqual(0, Context.objects.count())
        self.context['foo'] = 'bar'
        self.context.save()
        self.assertEqual(1, Context.objects.count())
        self.context.flush()
        # 确保新的数据会从数据库中获取
        del self.context._context_cache
        self.assertEqual(list(self.context.items()), [])
        self.assertTrue(self.context.modified)
        self.assertTrue(self.context.accessed)