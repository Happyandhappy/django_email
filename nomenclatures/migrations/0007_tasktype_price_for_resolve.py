# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nomenclatures', '0006_auto_20141112_0944'),
    ]

    operations = [
        migrations.AddField(
            model_name='tasktype',
            name='price_for_resolve',
            field=models.DecimalField(null=True, verbose_name='Price for resolve', max_digits=8, decimal_places=2, blank=True),
            preserve_default=True,
        ),
    ]
