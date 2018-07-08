# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entrances', '0013_auto_20141112_1337'),
    ]

    operations = [
        migrations.AddField(
            model_name='apartment',
            name='monthly_fee',
            field=models.DecimalField(null=True, verbose_name='Monthly Fee', max_digits=8, decimal_places=2, blank=True),
            preserve_default=True,
        ),
    ]
