# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Context',
            fields=[
                ('openid', models.CharField(max_length=50, serialize=False, verbose_name='\u7528\u6237OpenID', primary_key=True)),
                ('context_data', models.TextField(verbose_name='\u4e0a\u4e0b\u6587\u5bf9\u8bdd\u6570\u636e')),
                ('expire_date', models.DateTimeField(verbose_name='\u8fc7\u671f\u65e5\u671f', db_index=True)),
            ],
            options={
                'db_table': 'wechat_context',
                'verbose_name': '\u5fae\u4fe1\u4e0a\u4e0b\u6587\u5bf9\u8bdd',
                'verbose_name_plural': '\u5fae\u4fe1\u4e0a\u4e0b\u6587\u5bf9\u8bdd',
            },
            bases=(models.Model,),
        ),
    ]
