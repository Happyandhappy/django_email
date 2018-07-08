# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tasks', '0029_partialtaskpay'),
    ]

    operations = [
        migrations.AddField(
            model_name='partialtaskpay',
            name='assignee',
            field=models.ForeignKey(default=0, verbose_name='User', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='partialtaskpay',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Created at'),
            preserve_default=True,
        ),
    ]
