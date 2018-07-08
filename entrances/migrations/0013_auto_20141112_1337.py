# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entrances', '0012_auto_20141112_1336'),
    ]

    operations = [
        migrations.AddField(
            model_name='apartment',
            name='contact_email',
            field=models.CharField(max_length=255, null=True, verbose_name='Email', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='apartment',
            name='contact_phone',
            field=models.CharField(max_length=255, null=True, verbose_name='Phone', blank=True),
            preserve_default=True,
        ),
    ]
