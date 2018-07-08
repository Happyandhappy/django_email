# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='mobile_phone',
            field=models.CharField(max_length=130, null=True, verbose_name='Mobile phone', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='work_phone',
            field=models.CharField(max_length=130, null=True, verbose_name='Work phone', blank=True),
            preserve_default=True,
        ),
    ]
