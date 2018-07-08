# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('entrances', '0030_apartment_is_board'),
    ]

    operations = [
        migrations.AddField(
            model_name='apartment',
            name='client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='User', blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='apartment',
            name='is_board',
            field=models.BooleanField(default=False, verbose_name='Is Board'),
            preserve_default=True,
        ),
    ]
