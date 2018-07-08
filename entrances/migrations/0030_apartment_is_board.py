# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entrances', '0029_auto_20150614_1616'),
    ]

    operations = [
        migrations.AddField(
            model_name='apartment',
            name='is_board',
            field=models.BooleanField(default=False, verbose_name='Active'),
            preserve_default=True,
        ),
    ]
