# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entrances', '0031_auto_20150918_0028'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apartment',
            name='common_area',
            field=models.DecimalField(null=True, verbose_name='Common area', max_digits=6, decimal_places=3, blank=True),
            preserve_default=True,
        ),
    ]
