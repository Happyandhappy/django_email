# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entrances', '0023_auto_20141207_1550'),
    ]

    operations = [
        migrations.AddField(
            model_name='entrance',
            name='tax_amount',
            field=models.DecimalField(null=True, verbose_name='Tax amount', max_digits=8, decimal_places=2, blank=True),
            preserve_default=True,
        ),
    ]
