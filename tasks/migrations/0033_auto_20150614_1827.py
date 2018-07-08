# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0032_auto_20150614_1631'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='partial_paid',
            field=models.DecimalField(decimal_places=2, editable=False, max_digits=8, blank=True, null=True, verbose_name='Partial paid'),
            preserve_default=True,
        ),
    ]
