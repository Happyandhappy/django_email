# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import select2.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('documents', '0002_auto_20141107_1425'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='editable_by_users',
            field=select2.fields.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name='Editable by users'),
            preserve_default=True,
        ),
    ]
