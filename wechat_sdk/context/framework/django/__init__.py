# -*- coding: utf-8 -*-

default_app_config = 'wechat_sdk.context.framework.django.apps.ContextConfig'

try:
    from wechat_sdk.context.framework.django.models import Context as DatabaseContext
    from wechat_sdk.context.framework.django.backends.db import ContextStore as DatabaseContextStore
except ImportError:
    pass