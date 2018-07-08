# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0004_auto_20141207_1613'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='editable_by_users',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name='Editable by users'),
            preserve_default=True,
        ),
    ]
