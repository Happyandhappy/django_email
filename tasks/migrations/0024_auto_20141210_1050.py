# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import select2.fields


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0023_auto_20141207_1613'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='task',
            options={'ordering': ('apartment__floor', 'apartment__apartment_integer'), 'verbose_name': 'task', 'verbose_name_plural': 'tasks'},
        ),
        migrations.AlterField(
            model_name='schedule',
            name='assignee',
            field=select2.fields.ForeignKey(verbose_name='User', blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
    ]
