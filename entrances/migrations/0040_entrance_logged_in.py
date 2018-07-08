# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entrances', '0039_auto_20170521_1512'),
    ]

    operations = [
        migrations.AddField(
            model_name='entrance',
            name='logged_in',
            field=models.BooleanField(default=False, verbose_name='logged_in'),
            preserve_default=True,
        ),
    ]
